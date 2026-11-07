"""Testes do Sistema de Tarefas do LAY Orchestrator (Fase 1.1 e 1.2).

Cobre persistência atômica, controle de concorrência, recuperação de locks órfãos,
máquina de estados finita, classificação heurística, interface CLI, isolamento
entre workspaces e proteção contra path traversal.
"""
from __future__ import annotations

import datetime
import json
import os
import subprocess
import sys
import tempfile
import time
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import tasks
from tasks import (
    ConcurrencyError,
    TaskNotFoundError,
    TaskValidationError,
    assign_task,
    classify_task,
    complete_task,
    create_task,
    get_task,
    list_tasks,
    task_lock,
    update_task_status,
)


class OrchestratorTasksTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.workspace = Path(self.temp_dir.name).resolve()

    def tearDown(self):
        try:
            self.temp_dir.cleanup()
        except Exception:
            pass

    def test_01_creation_retrieval_and_listing(self):
        """Valida ciclo básico de criação, recuperação e listagem de tarefas."""
        t1 = create_task(
            workspace=self.workspace,
            title="Adicionar componente Badge",
            domain="frontend",
            context=["src/components/Badge.tsx"],
            constraints=["WCAG AA compliance"],
            acceptance_criteria=["Suportar variantes default e outline"],
        )
        self.assertTrue(t1["id"].startswith("task-"))
        self.assertEqual(t1["title"], "Adicionar componente Badge")
        self.assertEqual(t1["status"], "pending")
        self.assertEqual(t1["handoff"]["domain"], "frontend")
        self.assertIsNone(t1["result"])

        # Recuperação por ID
        retrieved = get_task(self.workspace, t1["id"])
        self.assertEqual(retrieved["id"], t1["id"])
        self.assertEqual(retrieved["title"], t1["title"])

        # Criação de segunda tarefa
        t2 = create_task(
            workspace=self.workspace,
            title="Refatorar rota de autenticação",
            domain="security",
        )

        # Listagem total
        all_tasks = list_tasks(self.workspace)
        self.assertEqual(len(all_tasks), 2)
        task_ids = {t["id"] for t in all_tasks}
        self.assertIn(t1["id"], task_ids)
        self.assertIn(t2["id"], task_ids)

        # Listagem com filtro
        pending_tasks = list_tasks(self.workspace, status_filter="pending")
        self.assertEqual(len(pending_tasks), 2)

        completed_tasks = list_tasks(self.workspace, status_filter="completed")
        self.assertEqual(len(completed_tasks), 0)

    def test_02_states_and_valid_transitions(self):
        """Valida transições de estado permitidas e bloqueio de transições inválidas."""
        t = create_task(self.workspace, title="Validar máquina de estados")
        task_id = t["id"]
        self.assertEqual(t["status"], "pending")

        # pending -> in_progress
        t = update_task_status(self.workspace, task_id, "in_progress")
        self.assertEqual(t["status"], "in_progress")

        # in_progress -> blocked (ex: needs_clarification)
        t = update_task_status(self.workspace, task_id, "blocked")
        self.assertEqual(t["status"], "blocked")

        # blocked -> in_progress (usuário esclareceu)
        t = update_task_status(self.workspace, task_id, "in_progress")
        self.assertEqual(t["status"], "in_progress")

        # in_progress -> escalated (escalonado ao árbitro)
        t = update_task_status(self.workspace, task_id, "escalated")
        self.assertEqual(t["status"], "escalated")

        # escalated -> in_progress (parecer emitido)
        t = update_task_status(self.workspace, task_id, "in_progress")
        self.assertEqual(t["status"], "in_progress")

        # in_progress -> completed
        t = complete_task(
            workspace=self.workspace,
            task_id=task_id,
            summary="Tarefa concluída com sucesso.",
            result_status="success",
            artifacts=["src/output.ts"],
        )
        self.assertEqual(t["status"], "completed")
        self.assertEqual(t["result"]["status"], "success")
        self.assertEqual(t["result"]["summary"], "Tarefa concluída com sucesso.")
        self.assertIsNotNone(t["timestamps"]["completed_at"])

        # Transição inválida: a partir de completed (estado terminal)
        with self.assertRaises(TaskValidationError):
            update_task_status(self.workspace, task_id, "in_progress")

        with self.assertRaises(TaskValidationError):
            assign_task(self.workspace, task_id, specialist="lay-frontend")

        with self.assertRaises(TaskValidationError):
            complete_task(self.workspace, task_id, summary="Tentando reconcluir")

    def test_03_simple_classification_without_delegation(self):
        """Classificação de tarefa simples deve sugerir resolução na sessão sem subagentes."""
        clf = classify_task(title="Ajustar padding do card", description="Mudar p-4 para p-6 no componente")
        self.assertEqual(clf["complexity"], "low")
        self.assertEqual(clf["recommended_mode"], "session")
        self.assertFalse(clf["suggests_persistence"])

    def test_04_complex_classification_without_mandatory_delegation(self):
        """Classificação complexa decompõe etapas sem impor delegação obrigatória a subagente."""
        clf = classify_task(
            title="Refatoração transversal da camada de serviços",
            description="Melhorar concorrência e tipagem de 10 rotas"
        )
        self.assertEqual(clf["complexity"], "high")
        # Modo padrão continua sendo resolução na sessão, priorizando etapas locais
        self.assertEqual(clf["recommended_mode"], "session")
        self.assertTrue(clf["suggests_persistence"])

    def test_05_critical_classification_suggests_arbitrator(self):
        """Classificação crítica com trade-off arquitetural orienta escalonamento ao árbitro."""
        clf = classify_task(
            title="Decisão de arquitetura e trade-off de persistência",
            description="Migração de esquema com potencial quebra de contratos"
        )
        self.assertEqual(clf["complexity"], "critical")
        self.assertEqual(clf["recommended_mode"], "arbitrator")
        self.assertTrue(clf["suggests_persistence"])

    def test_06_justified_assignment(self):
        """Atribuição para subagente ou árbitro exige justificativa objetiva (--reason)."""
        t = create_task(self.workspace, title="Auditar dependências")

        # Modo session não exige reason
        t_assigned = assign_task(
            workspace=self.workspace,
            task_id=t["id"],
            specialist="lay-engenharia",
            mode="session",
        )
        self.assertEqual(t_assigned["routing"]["target_specialist"], "lay-engenharia")
        self.assertEqual(t_assigned["routing"]["execution_mode"], "session")
        self.assertEqual(t_assigned["status"], "in_progress")

        # Modo subagent sem reason deve falhar
        t2 = create_task(self.workspace, title="Varredura de segurança")
        with self.assertRaises(TaskValidationError):
            assign_task(
                workspace=self.workspace,
                task_id=t2["id"],
                specialist="lay-seguranca",
                mode="subagent",
                reason=None,
            )

        # Modo subagent com reason deve ser aceito
        t2_assigned = assign_task(
            workspace=self.workspace,
            task_id=t2["id"],
            specialist="lay-seguranca",
            mode="subagent",
            reason="Isolamento read-only estrito para varredura semgrep",
        )
        self.assertEqual(t2_assigned["routing"]["execution_mode"], "subagent")
        self.assertEqual(t2_assigned["routing"]["delegation_reason"], "Isolamento read-only estrito para varredura semgrep")

    def test_07_atomic_write_integrity(self):
        """Escrita atômica não deixa arquivos temporários nem corrompe dados em disco."""
        t = create_task(self.workspace, title="Teste de escrita atômica")
        tasks_dir = self.workspace / ".lay" / "tasks"
        task_file = tasks_dir / f"{t['id']}.json"

        self.assertTrue(task_file.exists())
        # Confirma ausência de arquivos .tmp pendentes
        tmp_files = list(tasks_dir.glob("*.tmp.*"))
        self.assertEqual(len(tmp_files), 0)

        # Validação do JSON
        data = json.loads(task_file.read_text(encoding="utf-8"))
        self.assertEqual(data["id"], t["id"])

    def test_08_concurrency_lock_and_protection(self):
        """Dois processos concorrentes não podem modificar simultaneamente a mesma tarefa."""
        t = create_task(self.workspace, title="Teste de Concorrência")
        task_id = t["id"]

        # Adquire o lock manualmente simulando um processo ativo
        with task_lock(self.workspace, task_id, timeout_seconds=0.5):
            # Tentativa concorrente com timeout curto deve levantar ConcurrencyError
            with self.assertRaises(ConcurrencyError):
                with task_lock(self.workspace, task_id, timeout_seconds=0.2):
                    pass

    def test_09_failure_recovery_from_dead_process_lock(self):
        """Lock órfão deixado por processo comprovadamente morto deve ser recuperado com segurança."""
        t = create_task(self.workspace, title="Teste de Stale Lock")
        task_id = t["id"]
        tasks_dir = self.workspace / ".lay" / "tasks"
        lock_file = tasks_dir / f"{task_id}.lock"

        # Simula lock órfão criado por um PID falso/morto (ex: 99999999)
        lock_payload = {
            "pid": 99999999,
            "created_at": "2026-11-01T00:00:00Z",
            "task_id": task_id,
        }
        lock_file.write_text(json.dumps(lock_payload), encoding="utf-8")

        # update_task_status obtém o task_lock internamente: deve identificar o PID morto,
        # remover o lock órfão com segurança e concluir a transição
        t_updated = update_task_status(self.workspace, task_id, "in_progress")
        self.assertEqual(t_updated["status"], "in_progress")
        self.assertFalse(lock_file.exists())

    def test_10_invalid_ids_and_path_traversal_protection(self):
        """IDs maliciosos ou fora do padrão devem ser rejeitados imediatamente."""
        malicious_ids = [
            "../hack",
            "../../etc/passwd",
            "task-1234",  # Menos de 8 caracteres
            "task-12345678901234567",  # Mais de 16 caracteres
            "task-ABCDEF12",  # Maiúsculas não permitidas
            "task-test;rm -rf",
            "",
        ]
        for bad_id in malicious_ids:
            with self.assertRaises(TaskValidationError):
                tasks.validate_task_id(bad_id)

            with self.assertRaises(TaskValidationError):
                get_task(self.workspace, bad_id)

    def test_11_workspace_isolation(self):
        """Tarefas em workspaces distintos são totalmente isoladas."""
        with tempfile.TemporaryDirectory() as tmp2:
            workspace2 = Path(tmp2).resolve()

            t_ws1 = create_task(self.workspace, title="Tarefa Workspace 1")
            t_ws2 = create_task(workspace2, title="Tarefa Workspace 2")

            # Workspace 1 só enxerga sua tarefa
            tasks1 = list_tasks(self.workspace)
            self.assertEqual(len(tasks1), 1)
            self.assertEqual(tasks1[0]["id"], t_ws1["id"])

            # Workspace 2 só enxerga sua tarefa
            tasks2 = list_tasks(workspace2)
            self.assertEqual(len(tasks2), 1)
            self.assertEqual(tasks2[0]["id"], t_ws2["id"])

            # Workspace 1 não consegue recuperar tarefa de Workspace 2
            with self.assertRaises(TaskNotFoundError):
                get_task(self.workspace, t_ws2["id"])

    def test_12_absence_of_automatic_execution(self):
        """Criação e atribuição apenas persistem dados e nunca despacham modelos ou processos."""
        t = create_task(self.workspace, title="Verificar ausência de execução automática")
        # Sem arquivos executáveis gerados
        self.assertEqual(t["status"], "pending")

        t_assign = assign_task(
            workspace=self.workspace,
            task_id=t["id"],
            specialist="lay-arbitro",
            mode="arbitrator",
            reason="Validação de ausência de chamadas automáticas a LLM",
        )
        self.assertEqual(t_assign["status"], "in_progress")
        # O resultado permanece None até preenchimento explícito
        self.assertIsNone(t_assign["result"])

    def test_13_cli_interface_lifecycle(self):
        """Valida comandos CLI via subprocess (create, list, show, assign, complete)."""
        # 1. task create
        res = subprocess.run(
            [
                sys.executable,
                str(ROOT / "scripts/skill_hub.py"),
                "task",
                "create",
                "--workspace",
                str(self.workspace),
                "--title",
                "CLI Lifecycle Task",
                "--domain",
                "frontend",
            ],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            check=True,
        )
        self.assertIn("Tarefa criada com sucesso:", res.stdout)
        task_id = [l for l in res.stdout.splitlines() if "task-" in l][0].split(": ")[1].strip()

        # 2. task list
        res = subprocess.run(
            [
                sys.executable,
                str(ROOT / "scripts/skill_hub.py"),
                "task",
                "list",
                "--workspace",
                str(self.workspace),
            ],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            check=True,
        )
        self.assertIn(task_id, res.stdout)
        self.assertIn("CLI Lifecycle Task", res.stdout)

        # 3. task assign
        res = subprocess.run(
            [
                sys.executable,
                str(ROOT / "scripts/skill_hub.py"),
                "task",
                "assign",
                task_id,
                "--workspace",
                str(self.workspace),
                "--specialist",
                "lay-frontend",
                "--mode",
                "session",
            ],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            check=True,
        )
        self.assertIn(f"Tarefa {task_id} atribuída:", res.stdout)

        # 4. task show
        res = subprocess.run(
            [
                sys.executable,
                str(ROOT / "scripts/skill_hub.py"),
                "task",
                "show",
                task_id,
                "--workspace",
                str(self.workspace),
            ],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            check=True,
        )
        show_data = json.loads(res.stdout)
        self.assertEqual(show_data["id"], task_id)
        self.assertEqual(show_data["status"], "in_progress")
        self.assertEqual(show_data["routing"]["target_specialist"], "lay-frontend")

        # 5. task complete
        res = subprocess.run(
            [
                sys.executable,
                str(ROOT / "scripts/skill_hub.py"),
                "task",
                "complete",
                task_id,
                "--workspace",
                str(self.workspace),
                "--summary",
                "Componente implementado com sucesso via CLI",
                "--artifacts",
                "src/Button.tsx",
            ],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            check=True,
        )
        self.assertIn(f"Tarefa {task_id} concluída com sucesso:", res.stdout)

        # 6. Conferência final via show
        res = subprocess.run(
            [
                sys.executable,
                str(ROOT / "scripts/skill_hub.py"),
                "task",
                "show",
                task_id,
                "--workspace",
                str(self.workspace),
            ],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            check=True,
        )
        final_data = json.loads(res.stdout)
        self.assertEqual(final_data["status"], "completed")
        self.assertEqual(final_data["result"]["status"], "success")
        self.assertEqual(final_data["result"]["summary"], "Componente implementado com sucesso via CLI")
        self.assertEqual(final_data["result"]["artifacts"], ["src/Button.tsx"])

    def test_14_process_lock_protection_no_accidental_unlink(self):
        """Garante que uma operação nunca remova o lock pertencente a outro processo."""
        t = create_task(self.workspace, title="Teste de Protecao de Lock")
        task_id = t["id"]
        tasks_dir = self.workspace / ".lay" / "tasks"
        lock_file = tasks_dir / f"{task_id}.lock"

        # Simula processo B que possui um token diferente
        foreign_payload = {
            "pid": os.getpid(),
            "token": "foreign-process-token-12345",
            "created_at": "2026-11-07T18:00:00Z",
            "task_id": task_id,
        }

        # Quando o context manager task_lock é forçado a liberar, se o lock foi substituído
        # por outro processo (token diferente), ele NÃO deve deletar o arquivo
        try:
            with task_lock(self.workspace, task_id):
                # Sobrescreve simulando colisão ou novo lock
                lock_file.write_text(json.dumps(foreign_payload), encoding="utf-8")
        except Exception:
            pass

        # O lock do outro processo deve permanecer intacto
        self.assertTrue(lock_file.exists())
        current_data = json.loads(lock_file.read_text(encoding="utf-8"))
        self.assertEqual(current_data.get("token"), "foreign-process-token-12345")

    def test_15_pid_reuse_and_stale_lock_recovery(self):
        """Valida que stale locks (> 60s) são recuperados com segurança mesmo se o PID estiver ativo."""
        t = create_task(self.workspace, title="Teste de Stale Lock com PID Ativo")
        task_id = t["id"]
        tasks_dir = self.workspace / ".lay" / "tasks"
        lock_file = tasks_dir / f"{task_id}.lock"

        # Simula lock criado há 10 minutos com o PID do processo atual (que está comprovadamente vivo)
        stale_time = (datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(minutes=10)).isoformat()
        lock_payload = {
            "pid": os.getpid(),
            "token": "stale-token-abc",
            "created_at": stale_time,
            "task_id": task_id,
        }
        lock_file.write_text(json.dumps(lock_payload), encoding="utf-8")

        # Ao atualizar status, deve identificar que a retenção excede o limite atômico (> 60s),
        # recuperando o lock órfão e completando a operação
        t_updated = update_task_status(self.workspace, task_id, "in_progress")
        self.assertEqual(t_updated["status"], "in_progress")
        self.assertFalse(lock_file.exists())

    def test_16_external_workspace_isolation_and_gitignore(self):
        """Valida proteção do workspace externo: .lay/.gitignore criado sem tocar raiz."""
        with tempfile.TemporaryDirectory() as ext_dir:
            ext_ws = Path(ext_dir).resolve()
            # Workspace externo tem seus próprios arquivos
            (ext_ws / "package.json").write_text("{}", encoding="utf-8")

            # Cria tarefa no workspace externo
            t = create_task(ext_ws, title="Tarefa em Projeto Externo")
            self.assertTrue(t["id"].startswith("task-"))

            # Confirma que .lay/.gitignore foi criado para isolar tarefas
            lay_gi = ext_ws / ".lay" / ".gitignore"
            self.assertTrue(lay_gi.exists())
            self.assertIn("*", lay_gi.read_text(encoding="utf-8"))

            # Confirma que a raiz do projeto externo NÃO teve .gitignore criado/modificado
            root_gi = ext_ws / ".gitignore"
            self.assertFalse(root_gi.exists())

    def test_17_contract_compatibility_handoff_and_result(self):
        """Confirma estrita compatibilidade com contratos HANDOFF.md e RESULT.md."""
        # 1. Handoff não inventa campos ausentes
        t = create_task(self.workspace, title="Tarefa Contrato Limpo", domain="engineering")
        handoff = t["handoff"]
        self.assertEqual(handoff["task"], "Tarefa Contrato Limpo")
        self.assertEqual(handoff["domain"], "engineering")
        self.assertEqual(handoff["context"], [])
        self.assertEqual(handoff["constraints"], [])
        self.assertEqual(handoff["acceptance_criteria"], [])

        # 2. task assign não altera resultado nem executa modelo
        update_task_status(self.workspace, t["id"], "in_progress")
        t_assigned = assign_task(
            workspace=self.workspace,
            task_id=t["id"],
            specialist="lay-engenharia",
            mode="session",
        )
        self.assertEqual(t_assigned["status"], "in_progress")
        self.assertIsNone(t_assigned["result"])

        # 3. Contrato RESULT separa status de execução de status da tarefa
        t_completed = complete_task(
            workspace=self.workspace,
            task_id=t["id"],
            summary="Sub-agente solicitou esclarecimento",
            result_status="needs_clarification",
            artifacts=[],
            open_items=["Definir política de rate limiting"],
        )
        # Status da tarefa é completed (ciclo de orquestração fechado)
        self.assertEqual(t_completed["status"], "completed")
        # Status do resultado é needs_clarification (contrato RESULT preservado)
        self.assertEqual(t_completed["result"]["status"], "needs_clarification")
        self.assertEqual(t_completed["result"]["open_items"], ["Definir política de rate limiting"])
        self.assertEqual(t_completed["result"]["artifacts"], [])


if __name__ == "__main__":
    unittest.main()
