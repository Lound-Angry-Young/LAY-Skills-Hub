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
    ALL_CANONICAL_DOMAINS,
    ALL_CANONICAL_SPECIALISTS,
    READONLY_SPECIALISTS,
    MAX_ARBITRATION_TOKENS,
    ConcurrencyError,
    TaskNotFoundError,
    TaskValidationError,
    assign_task,
    classify_task,
    complete_task,
    create_task,
    get_task,
    list_tasks,
    normalize_text,
    prepare_arbitration_package,
    recommend_task_routing,
    resume_task,
    task_lock,
    atomic_write_task,
    update_task_status,
    validate_artifact_paths,
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
        (self.workspace / "src").mkdir(parents=True, exist_ok=True)
        (self.workspace / "src" / "output.ts").write_text("// test", encoding="utf-8")
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
        t2 = create_task(self.workspace, title="Varredura de segurança", client="antigravity")
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
        t = create_task(self.workspace, title="Verificar ausência de execução automática", client="antigravity")
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
        (self.workspace / "src").mkdir(parents=True, exist_ok=True)
        (self.workspace / "src" / "Button.tsx").write_text("// button", encoding="utf-8")
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

    def test_15_active_process_never_loses_lock_by_time(self):
        """Teste de regressão: processo proprietário ativo NUNCA perde o lock apenas por tempo decorrido."""
        from unittest.mock import patch

        t = create_task(self.workspace, title="Teste de Lock com PID Ativo")
        task_id = t["id"]
        tasks_dir = self.workspace / ".lay" / "tasks"
        lock_file = tasks_dir / f"{task_id}.lock"

        # Simula processo ativo que iniciou há 200s e criou o lock há 100s (> 60s)
        lock_time = (datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(seconds=100)).isoformat()
        lock_payload = {
            "pid": os.getpid(),
            "token": "active-owner-token",
            "created_at": lock_time,
            "task_id": task_id,
        }
        lock_file.write_text(json.dumps(lock_payload), encoding="utf-8")

        # Mocka get_process_start_time para confirmar que o processo iniciou antes do lock (sem PID reuse)
        with patch("tasks.get_process_start_time", return_value=time.time() - 200.0):
            # Tentativa de obter o lock com timeout curto deve respeitar o processo ativo
            # e levantar ConcurrencyError sem roubar nem desvincular o lock por tempo
            with self.assertRaises(ConcurrencyError):
                with task_lock(self.workspace, task_id, timeout_seconds=0.1):
                    pass

        # O lock deve permanecer intacto pertencente ao processo ativo
        self.assertTrue(lock_file.exists())
        data = json.loads(lock_file.read_text(encoding="utf-8"))
        self.assertEqual(data.get("token"), "active-owner-token")

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
        # Status da tarefa é blocked (aguardando esclarecimento)
        self.assertEqual(t_completed["status"], "blocked")
        # Status do resultado é needs_clarification (contrato RESULT preservado)
        self.assertEqual(t_completed["result"]["status"], "needs_clarification")
        self.assertEqual(t_completed["result"]["open_items"], ["Definir política de rate limiting"])
        self.assertEqual(t_completed["result"]["artifacts"], [])



    def test_18_simple_task_resolved_in_session(self):
        """Tarefa simples pontual deve recomendar resolução na sessão atual sem subagentes."""
        rec = recommend_task_routing(
            title="Ajustar padding do card",
            description="Alterar espaçamento de p-4 para p-6",
            client="antigravity"
        )
        self.assertEqual(rec["complexity"], "low")
        self.assertEqual(rec["recommended_domain"], "frontend")
        self.assertEqual(rec["recommended_mode"], "session")
        self.assertEqual(rec["recommended_specialist"], "lay-frontend")
        self.assertFalse(rec["requires_authorization"])
        self.assertTrue(rec["delegation_allowed"])
        self.assertIn("sem subagentes", rec["rationale"].lower())
        # Não preenche artificialmente com skills de animação para ajuste simples de padding
        self.assertEqual(rec["relevant_skills"], [])

    def test_19_moderate_task_with_skills_no_subagent(self):
        """Tarefa moderada deve mapear skills do domínio sem delegar a subagente."""
        rec = recommend_task_routing(
            title="Implementar componente de formulário com animacao react-bits",
            description="Criar input com feedback visual",
            client="claude"
        )
        self.assertEqual(rec["complexity"], "medium")
        self.assertEqual(rec["recommended_domain"], "frontend")
        self.assertEqual(rec["recommended_mode"], "session")
        self.assertTrue(len(rec["relevant_skills"]) > 0)
        self.assertFalse(rec["requires_authorization"])

    def test_20_complex_task_continues_in_session(self):
        """Tarefa complexa decompõe etapas na sessão e NÃO impõe delegação a subagente."""
        rec = recommend_task_routing(
            title="Refatoração transversal da camada de serviços",
            description="Melhorar concorrência e tipagem de 10 rotas de API",
            client="antigravity"
        )
        self.assertEqual(rec["complexity"], "high")
        self.assertEqual(rec["recommended_domain"], "engineering")
        # Complexidade alta não implica delegação obrigatória: padrão continua session
        self.assertEqual(rec["recommended_mode"], "session")
        self.assertEqual(rec["recommended_specialist"], "lay-engenharia")
        self.assertFalse(rec["requires_authorization"])

    def test_21_specialized_task_with_justified_delegation(self):
        """Tarefa com justificativa concreta de isolamento de segurança recomenda subagente."""
        # 1. Isolamento estrito read-only para segurança
        rec_sec = recommend_task_routing(
            title="Auditoria de segurança estrita e varredura semgrep",
            description="Analisar vulnerabilidades no código",
            client="antigravity"
        )
        self.assertEqual(rec_sec["recommended_domain"], "security")
        self.assertEqual(rec_sec["recommended_mode"], "subagent")
        self.assertEqual(rec_sec["recommended_specialist"], "lay-seguranca")
        self.assertIn("isolamento operacional estrito", rec_sec["rationale"].lower())

        # 2. Especialização de runtime 3D
        rec_3d = recommend_task_routing(
            title="Modelagem 3D e renderização de shaders no blender",
            description="Efeitos visuais WebGL",
            client="claude"
        )
        self.assertEqual(rec_3d["recommended_domain"], "creative-3d")
        self.assertEqual(rec_3d["recommended_mode"], "subagent")
        self.assertEqual(rec_3d["recommended_specialist"], "lay-3d")

    def test_22_critical_task_without_automatic_arbitration(self):
        """Tarefa crítica não equivale a convocar árbitro; sessão é padrão exceto em impasse real."""
        # 1. Impasse arquitetural real -> orienta arbitragem (requer autorização prévia)
        rec_impasse = recommend_task_routing(
            title="Impasse e trade-off de arquitetura sobre persistência relacional vs documento",
            description="Dilema de design estrutural",
            client="antigravity"
        )
        self.assertEqual(rec_impasse["complexity"], "critical")
        self.assertEqual(rec_impasse["recommended_mode"], "arbitrator")
        self.assertEqual(rec_impasse["recommended_specialist"], "lay-arbitro")
        self.assertTrue(rec_impasse["requires_authorization"])
        self.assertIn("autorizacao humana explicita", normalize_text(rec_impasse["rationale"]))

        # Em Claude, recomenda lay-arbitro-opus para impasse
        rec_claude = recommend_task_routing(
            title="Impasse e trade-off de arquitetura sobre persistência relacional vs documento",
            client="claude"
        )
        self.assertEqual(rec_claude["recommended_specialist"], "lay-arbitro-opus")

        # 2. Tarefa crítica SEM impasse arquitetural -> EXECUÇÃO PADRÃO NA SESSÃO
        rec_sem_impasse = recommend_task_routing(
            title="Executar migração crítica de esquema de banco com risco de quebra de contrato",
            domain="database",
            client="antigravity"
        )
        self.assertEqual(rec_sem_impasse["complexity"], "critical")
        self.assertEqual(rec_sem_impasse["recommended_mode"], "session")
        self.assertTrue(rec_sem_impasse["requires_authorization"])
        self.assertIn("execucao padrao mantida na sessao atual", normalize_text(rec_sem_impasse["rationale"]))

    def test_23_invalid_domain_or_specialist_rejected(self):
        """Domínio ou especialista fora dos perfis canônicos deve ser rejeitado."""
        with self.assertRaises(TaskValidationError):
            recommend_task_routing(title="Teste", domain="dominio-inexistente")

        with self.assertRaises(TaskValidationError):
            recommend_task_routing(title="Teste", explicit_specialist="lay-robo-fantasma")

        # Em assign_task também deve rejeitar especialista inválido
        t = create_task(self.workspace, title="Teste assign especialista invalido")
        with self.assertRaises(TaskValidationError):
            assign_task(self.workspace, t["id"], specialist="lay-robo-fantasma")

    def test_24_client_without_delegation_capability(self):
        """Cliente local sem capacidade de delegação reverte para sessão e bloqueia subagent."""
        rec = recommend_task_routing(
            title="Auditoria de segurança estrita e varredura semgrep",
            client="local"
        )
        self.assertFalse(rec["delegation_allowed"])
        self.assertEqual(rec["recommended_mode"], "session")

        t = create_task(self.workspace, title="Tarefa em cliente local", client="local")
        with self.assertRaises(TaskValidationError):
            assign_task(
                self.workspace,
                t["id"],
                specialist="lay-seguranca",
                mode="subagent",
                reason="Tentando delegar em cliente local",
            )

    def test_25_codex_functionally_unavailable(self):
        """Codex deve ser mantido funcionalmente indisponível para delegação."""
        rec = recommend_task_routing(
            title="Auditoria de segurança estrita e varredura semgrep",
            client="codex"
        )
        self.assertFalse(rec["delegation_allowed"])
        self.assertEqual(rec["recommended_mode"], "session")
        self.assertIn("indisponivel funcionalmente", normalize_text(rec["rationale"]))

        t = create_task(self.workspace, title="Tarefa em cliente codex", client="codex")
        with self.assertRaises(TaskValidationError):
            assign_task(
                self.workspace,
                t["id"],
                specialist="lay-seguranca",
                mode="subagent",
                reason="Tentando delegar em codex",
            )

    def test_26_readonly_permissions_and_risk_authorization(self):
        """Preserva salvaguardas de especialistas somente-leitura e sinaliza risco em devops/db."""
        self.assertIn("lay-seguranca", READONLY_SPECIALISTS)
        self.assertIn("lay-contexto", READONLY_SPECIALISTS)
        self.assertIn("lay-banco-de-dados", READONLY_SPECIALISTS)
        self.assertIn("lay-arbitro", READONLY_SPECIALISTS)

        # Operações destrutivas em devops exigem autorização
        rec_devops = recommend_task_routing(
            title="Executar deploy e reset da branch principal",
            domain="devops",
            client="antigravity"
        )
        self.assertTrue(rec_devops["requires_authorization"])

        # Operações destrutivas em database exigem autorização
        rec_db = recommend_task_routing(
            title="Executar drop table e migracao de esquema",
            domain="database",
            client="antigravity"
        )
        self.assertTrue(rec_db["requires_authorization"])

    def test_27_absence_of_model_invocations_and_state_integrity(self):
        """Garante ausência total de chamadas a modelos e integridade dos dados da tarefa."""
        t = create_task(
            self.workspace,
            title="Implementar rota de produtos",
            client="antigravity"
        )
        self.assertEqual(t["status"], "pending")
        self.assertIsNone(t["result"])
        self.assertEqual(t["handoff"]["domain"], "engineering")
        self.assertEqual(t["routing"]["execution_mode"], "session")
        self.assertIsNone(t["routing"]["target_specialist"])

    def test_28_cli_recommend_command(self):
        """Valida comando CLI task recommend via subprocess tanto com --title quanto com --task-id."""
        # 1. recommend com --title
        res = subprocess.run(
            [
                sys.executable,
                str(ROOT / "scripts/skill_hub.py"),
                "task",
                "recommend",
                "--title",
                "Criar componente Badge acessivel com animacao",
                "--client",
                "antigravity",
            ],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            check=True,
        )
        self.assertIn("Decisão de Roteamento (Recomendação)", res.stdout)
        self.assertIn("Domínio Recomendado:      frontend", res.stdout)
        self.assertIn("Modo Recomendado:         session", res.stdout)

        # 2. recommend com --task-id
        t = create_task(self.workspace, title="Auditar dependencias CVE", client="antigravity")
        res_id = subprocess.run(
            [
                sys.executable,
                str(ROOT / "scripts/skill_hub.py"),
                "task",
                "recommend",
                "--workspace",
                str(self.workspace),
                "--task-id",
                t["id"],
            ],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            check=True,
        )
        self.assertIn("Decisão de Roteamento (Recomendação)", res_id.stdout)
        self.assertIn("Domínio Recomendado:      security", res_id.stdout)
        self.assertIn("Especialista Recomendado: lay-seguranca", res_id.stdout)


    def test_29_skill_relevance_and_zero_artificial_fill(self):
        """A seleção de skills não deve preencher artificialmente com skills irrelevantes."""
        # Decisão de persistência em database não deve sugerir backup OmniRoute
        rec_db = recommend_task_routing(
            title="Decisão de arquitetura sobre persistência e quebra de contratos de banco",
            domain="database",
            client="antigravity"
        )
        self.assertEqual(rec_db["relevant_skills"], [])

        # Tarefa com finalidade concreta de animação deve encontrar skills pertinentes
        rec_anim = recommend_task_routing(
            title="Criar componente modal com animacao react-bits e acessibilidade wcag",
            domain="frontend",
            client="antigravity"
        )
        self.assertTrue(len(rec_anim["relevant_skills"]) > 0)
        self.assertTrue(any("animat" in s for s in rec_anim["relevant_skills"]))

    def test_30_specialist_tool_limitations_and_terminal_differentiation(self):
        """Roteador diferencia análise estática por leitura de execução de ferramentas no terminal."""
        # 1. Execução no terminal: lay-seguranca não possui Bash, execução fica na sessão
        rec_cli = recommend_task_routing(
            title="Executar varredura semgrep no terminal",
            domain="security",
            client="antigravity"
        )
        self.assertEqual(rec_cli["recommended_mode"], "session")
        self.assertIn("sem acesso a terminal", rec_cli["rationale"].lower())

        # 2. Análise estática por leitura: pode delegar para sandbox read-only
        rec_audit = recommend_task_routing(
            title="Auditoria estática de vulnerabilidades e inspeção de código",
            domain="security",
            client="antigravity"
        )
        self.assertEqual(rec_audit["recommended_mode"], "subagent")
        self.assertEqual(rec_audit["recommended_specialist"], "lay-seguranca")


    def test_31_result_validation_success_with_existing_artifacts(self):
        """Validação de RESULT com sucesso exige arquivos existentes fisicamente no workspace."""
        t = create_task(self.workspace, title="Gerar artefatos válidos")
        update_task_status(self.workspace, t["id"], "in_progress")

        # Cria artefato físico válido
        art_path = self.workspace / "dist" / "bundle.js"
        art_path.parent.mkdir(parents=True, exist_ok=True)
        art_path.write_text("console.log('ok');", encoding="utf-8")

        res = complete_task(
            workspace=self.workspace,
            task_id=t["id"],
            summary="Build gerado com sucesso.",
            result_status="success",
            artifacts=["dist/bundle.js"],
        )
        self.assertEqual(res["status"], "completed")
        self.assertEqual(res["result"]["status"], "success")
        self.assertEqual(res["result"]["artifacts"], ["dist/bundle.js"])
        self.assertIsNotNone(res["timestamps"]["completed_at"])

    def test_32_result_validation_success_without_artifacts(self):
        """Permite conclusão sem artefatos quando nenhum arquivo for produzido."""
        t = create_task(self.workspace, title="Tarefa puramente analítica")
        update_task_status(self.workspace, t["id"], "in_progress")

        res = complete_task(
            workspace=self.workspace,
            task_id=t["id"],
            summary="Análise conceitual concluída sem produção de arquivos.",
            result_status="success",
            artifacts=[],
        )
        self.assertEqual(res["status"], "completed")
        self.assertEqual(res["result"]["artifacts"], [])

    def test_33_result_validation_fails_when_artifact_does_not_exist(self):
        """Falha ao declarar status success se artefato declarado não existir no disco."""
        t = create_task(self.workspace, title="Tarefa com artefato fantasma")
        update_task_status(self.workspace, t["id"], "in_progress")

        with self.assertRaises(TaskValidationError) as ctx:
            complete_task(
                workspace=self.workspace,
                task_id=t["id"],
                summary="Tentativa de concluir com arquivo inexistente.",
                result_status="success",
                artifacts=["dist/fantasma.js"],
            )
        self.assertIn("Artefato declarado não existe no disco", str(ctx.exception))

    def test_34_result_validation_fails_on_path_traversal_or_workspace_escape(self):
        """Rejeita artefatos com path traversal, escapes de workspace ou caminhos inválidos."""
        t = create_task(self.workspace, title="Tarefa com artefato malicioso")
        update_task_status(self.workspace, t["id"], "in_progress")

        # 1. Path traversal relativo
        with self.assertRaises(TaskValidationError) as ctx:
            complete_task(
                workspace=self.workspace,
                task_id=t["id"],
                summary="Tentativa de escape com path traversal.",
                artifacts=["../../etc/passwd"],
            )
        self.assertIn("escapa do diretório autorizado", str(ctx.exception))

        # 2. String vazia
        with self.assertRaises(TaskValidationError):
            complete_task(
                workspace=self.workspace,
                task_id=t["id"],
                summary="Tentativa com artefato vazio.",
                artifacts=["   "],
            )

        # 3. Diretório ao invés de arquivo regular
        dir_path = self.workspace / "subfolder"
        dir_path.mkdir(exist_ok=True)
        with self.assertRaises(TaskValidationError) as ctx:
            complete_task(
                workspace=self.workspace,
                task_id=t["id"],
                summary="Tentativa com diretório como artefato.",
                result_status="success",
                artifacts=["subfolder"],
            )
        self.assertIn("deve ser um arquivo regular", str(ctx.exception))

    def test_35_consistent_state_transitions_for_result_statuses(self):
        """RESULT mapeia consistentemente para a máquina de estados: success->completed, failure->failed, needs_clarification->blocked, escalated->escalated."""
        # 1. failure -> failed
        t1 = create_task(self.workspace, title="Tarefa que falhou")
        update_task_status(self.workspace, t1["id"], "in_progress")
        r1 = complete_task(
            workspace=self.workspace,
            task_id=t1["id"],
            summary="Falha na compilação por erro de sintaxe.",
            result_status="failure",
        )
        self.assertEqual(r1["status"], "failed")
        self.assertEqual(r1["result"]["status"], "failure")
        self.assertIsNone(r1["timestamps"]["completed_at"])

        # 2. needs_clarification -> blocked
        t2 = create_task(self.workspace, title="Tarefa bloqueada por dúvida")
        update_task_status(self.workspace, t2["id"], "in_progress")
        r2 = complete_task(
            workspace=self.workspace,
            task_id=t2["id"],
            summary="Necessário definir limites de taxa.",
            result_status="needs_clarification",
            open_items=["Definir RPS"],
        )
        self.assertEqual(r2["status"], "blocked")
        self.assertEqual(r2["result"]["status"], "needs_clarification")

        # 3. escalated -> escalated
        t3 = create_task(self.workspace, title="Tarefa escalonada")
        update_task_status(self.workspace, t3["id"], "in_progress")
        r3 = complete_task(
            workspace=self.workspace,
            task_id=t3["id"],
            summary="Impasse técnico identificado.",
            result_status="escalated",
        )
        self.assertEqual(r3["status"], "escalated")
        self.assertEqual(r3["result"]["status"], "escalated")

    def test_36_terminal_completed_state_is_immutable(self):
        """Estado 'completed' é terminal e estritamente imutável para todas as operações."""
        t = create_task(self.workspace, title="Tarefa para terminalidade")
        update_task_status(self.workspace, t["id"], "in_progress")
        complete_task(
            workspace=self.workspace,
            task_id=t["id"],
            summary="Conclusão regular sem artefatos.",
            result_status="success",
        )

        with self.assertRaises(TaskValidationError):
            complete_task(self.workspace, t["id"], summary="Reconclusão bloqueada")

        with self.assertRaises(TaskValidationError):
            resume_task(self.workspace, t["id"])

        with self.assertRaises(TaskValidationError):
            assign_task(self.workspace, t["id"], specialist="lay-engenharia")

        with self.assertRaises(TaskValidationError):
            update_task_status(self.workspace, t["id"], "in_progress")

        with self.assertRaises(TaskValidationError):
            prepare_arbitration_package(
                self.workspace,
                t["id"],
                problem="Problema pós-fechamento",
                alternatives=["Alt 1", "Alt 2"]
            )

    def test_37_controlled_recovery_from_blocked_failed_escalated(self):
        """Recuperação controlada permite retomar tarefas em blocked, failed ou escalated preservando histórico."""
        # 1. Retomada a partir de blocked com esclarecimento
        t = create_task(self.workspace, title="Tarefa para recuperação")
        update_task_status(self.workspace, t["id"], "in_progress")
        complete_task(
            self.workspace,
            t["id"],
            summary="Aguardando especificação do schema.",
            result_status="needs_clarification",
        )
        self.assertEqual(get_task(self.workspace, t["id"])["status"], "blocked")

        resumed = resume_task(
            self.workspace,
            t["id"],
            clarification="Utilizar JSON Schema Draft 7 com IDs canônicos.",
            reason="Esclarecimento de requisitos fornecido",
        )
        self.assertEqual(resumed["status"], "in_progress")
        self.assertIsNone(resumed["result"])
        self.assertIn("[Esclarecimento]: Utilizar JSON Schema Draft 7 com IDs canônicos.", resumed["handoff"]["context"])
        self.assertEqual(len(resumed["history"]), 1)
        self.assertEqual(resumed["history"][0]["previous_status"], "blocked")
        self.assertEqual(resumed["history"][0]["action"], "resume")
        self.assertEqual(resumed["history"][0]["previous_result"]["status"], "needs_clarification")

        # 2. Retomada a partir de failed
        complete_task(self.workspace, t["id"], summary="Falha técnica", result_status="failure")
        resumed_failed = resume_task(self.workspace, t["id"], reason="Tentativa com correção de bug")
        self.assertEqual(resumed_failed["status"], "in_progress")
        self.assertEqual(len(resumed_failed["history"]), 2)

        # 3. Retomada a partir de escalated
        complete_task(self.workspace, t["id"], summary="Escalado", result_status="escalated")
        resumed_esc = resume_task(self.workspace, t["id"], reason="Acordo consensual atingido")
        self.assertEqual(resumed_esc["status"], "in_progress")
        self.assertEqual(len(resumed_esc["history"]), 3)

        # 4. Não permite retomar se já estiver em in_progress ou pending
        with self.assertRaises(TaskValidationError):
            resume_task(self.workspace, t["id"])

        t_pending = create_task(self.workspace, title="Tarefa pendente")
        with self.assertRaises(TaskValidationError):
            resume_task(self.workspace, t_pending["id"])

    def test_38_prepare_arbitration_package_structure_and_limits(self):
        """Preparação de arbitragem estrutura pacote, exige autorização e transita para escalated sem invocar LLM."""
        t = create_task(self.workspace, title="Decisão sobre arquitetura de cache")
        update_task_status(self.workspace, t["id"], "in_progress")

        res = prepare_arbitration_package(
            workspace=self.workspace,
            task_id=t["id"],
            problem="Qual estratégia de cache utilizar para endpoints com alta concorrência?",
            alternatives=[
                "Opção 1: Redis compartilhado com TTL curto",
                "Opção 2: Cache em memória local com invalidação pub/sub"
            ],
            evidences=["Carga observada: 5.000 req/s", "Latência alvo: < 10ms"],
            constraints=["Infraestrutura não possui Redis gerenciado atualmente"],
            criteria=["Custo de operação", "Consistência de dados", "Simplicidade"]
        )

        self.assertEqual(res["status"], "escalated")
        self.assertIsNotNone(res.get("arbitration"))
        arb = res["arbitration"]
        self.assertEqual(arb["rounds_count"], 0)  # Preparação não consome rodada real
        self.assertEqual(len(arb["packages"]), 1)

        pkg = arb["packages"][0]
        self.assertEqual(pkg["round"], 1)
        self.assertEqual(len(pkg["alternatives"]), 2)
        self.assertTrue(pkg["requires_authorization"])
        self.assertGreater(pkg["estimated_tokens"], 0)
        self.assertLess(pkg["estimated_tokens"], 15000)

        # Rejeita menos de 2 alternativas
        with self.assertRaises(TaskValidationError) as ctx:
            prepare_arbitration_package(
                self.workspace,
                t["id"],
                problem="Problema",
                alternatives=["Apenas uma opção"]
            )
        self.assertIn("ao menos 2 alternativas", str(ctx.exception))

    def test_39_arbitration_anti_loop_max_three_rounds(self):
        """Proteção anti-loop preserva limite de 3 rodadas executadas sem consumir limite na preparação."""
        t = create_task(self.workspace, title="Tarefa com dilema persistente")
        update_task_status(self.workspace, t["id"], "in_progress")

        # Preparação do primeiro pacote: não consome rounds_count
        p1 = prepare_arbitration_package(
            self.workspace, t["id"],
            problem="Impasse 1", alternatives=["Alt A", "Alt B"]
        )
        self.assertEqual(p1["arbitration"]["rounds_count"], 0)
        self.assertEqual(p1["arbitration"]["packages"][0]["round"], 1)

        # Atualização/refinamento de pacote: continua sem consumir rounds_count
        p2 = prepare_arbitration_package(
            self.workspace, t["id"],
            problem="Impasse 1 refinado", alternatives=["Alt A", "Alt B refinada"]
        )
        self.assertEqual(p2["arbitration"]["rounds_count"], 0)
        self.assertEqual(len(p2["arbitration"]["packages"]), 2)

        # Simulação de tarefa que atingiu o limite de 3 rodadas reais executadas
        with task_lock(self.workspace, t["id"]):
            task_obj = get_task(self.workspace, t["id"])
            task_obj["arbitration"]["rounds_count"] = 3
            atomic_write_task(self.workspace, task_obj)

        # Tentativa de nova arbitragem com 3 rodadas já executadas: bloqueada
        with self.assertRaises(TaskValidationError) as ctx:
            prepare_arbitration_package(
                self.workspace, t["id"],
                problem="Impasse pós-limite", alternatives=["Alt G", "Alt H"]
            )
        self.assertIn("Limite máximo de 3 rodadas de arbitragem", str(ctx.exception))

    def test_40_arbitration_token_ceiling_heuristic(self):
        """Pacote de arbitragem com volume que exceda o teto heurístico de 15.000 tokens é rejeitado."""
        t = create_task(self.workspace, title="Tarefa com volume excessivo")
        update_task_status(self.workspace, t["id"], "in_progress")

        huge_evidence = "x" * 65000  # ~16.250 tokens estimados
        with self.assertRaises(TaskValidationError) as ctx:
            prepare_arbitration_package(
                self.workspace,
                t["id"],
                problem="Decisão complexa",
                alternatives=["Alt 1", "Alt 2"],
                evidences=[huge_evidence]
            )
        self.assertIn("teto heurístico estimado de 15000 tokens", str(ctx.exception))

    def test_41_cli_task_complete_resume_arbitrate(self):
        """Interface CLI suporta os novos comandos 'complete', 'resume' e 'arbitrate'."""
        t = create_task(self.workspace, title="Tarefa teste CLI completa")
        update_task_status(self.workspace, t["id"], "in_progress")

        # 1. complete -> blocked via needs_clarification
        proc_comp = subprocess.run(
            [
                sys.executable,
                str(ROOT / "scripts/skill_hub.py"),
                "task",
                "complete",
                t["id"],
                "--workspace",
                str(self.workspace),
                "--summary",
                "Aguardando decisão do time sobre autenticação.",
                "--result-status",
                "needs_clarification",
                "--open-items",
                "Decidir entre OAuth e SAML",
            ],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            check=False,
        )
        self.assertEqual(proc_comp.returncode, 0, proc_comp.stderr)
        self.assertIn("Status Tarefa: blocked", proc_comp.stdout)
        self.assertIn("Status RESULT: needs_clarification", proc_comp.stdout)

        # 2. resume com esclarecimento
        proc_res = subprocess.run(
            [
                sys.executable,
                str(ROOT / "scripts/skill_hub.py"),
                "task",
                "resume",
                t["id"],
                "--workspace",
                str(self.workspace),
                "--clarification",
                "Adotado OAuth 2.0 com PKCE.",
            ],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            check=False,
        )
        self.assertEqual(proc_res.returncode, 0, proc_res.stderr)
        self.assertIn("retomada com sucesso para 'in_progress'", proc_res.stdout)
        self.assertIn("Adotado OAuth 2.0 com PKCE", proc_res.stdout)

        # 3. arbitrate preparando pacote de escalonamento
        proc_arb = subprocess.run(
            [
                sys.executable,
                str(ROOT / "scripts/skill_hub.py"),
                "task",
                "arbitrate",
                t["id"],
                "--workspace",
                str(self.workspace),
                "--problem",
                "Dilema entre JWT local e sessão remota",
                "--alternatives",
                "JWT auto-contido",
                "Sessão no Redis",
                "--evidences",
                "Volume esperado: 10k req/min",
                "--criteria",
                "Segurança e revocabilidade",
            ],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            check=False,
        )
        self.assertEqual(proc_arb.returncode, 0, proc_arb.stderr)
        self.assertIn("Pacote de arbitragem preparado com sucesso", proc_arb.stdout)
        self.assertIn("Rodada Alvo:              1 de 3", proc_arb.stdout)
        self.assertIn("Autorização Obrigatória:  Sim", proc_arb.stdout)

if __name__ == "__main__":
    unittest.main()
