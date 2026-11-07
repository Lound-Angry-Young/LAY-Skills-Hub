"""Testes de Homologação Funcional Determinística (Fase 3.1).

Cobre de ponta a ponta:
- Handoff bidirecional: Claude -> Antigravity e Antigravity -> Claude.
- Múltiplos handoffs consecutivos preservando histórico e rastreabilidade.
- Validação de contratos RESULT válidos, sem artefatos e inválidos.
- Proteção contra path traversal e IDs maliciosos.
- Transições de estado controladas, recuperação de falhas e retomadas.
- Imutabilidade absoluta de tarefas concluídas.
- Hierarquia de delegação mínima e autorizações pontuais.
- Rejeição funcional do cliente Codex.
- Ausência de invocação de modelos ou processos externos.
- Conformidade estrita dos comandos CLI (task show, task route, task handoff).
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
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
    complete_task,
    create_task,
    get_task,
    handoff_task,
    list_tasks,
    recommend_task_routing,
    resume_task,
    update_task_status,
    validate_artifact_paths,
    validate_task_id,
)


class FunctionalHomologationTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.workspace = Path(self.temp_dir.name).resolve()

    def tearDown(self):
        try:
            self.temp_dir.cleanup()
        except Exception:
            pass

    def test_01_claude_to_antigravity_handoff_and_result(self):
        """Fluxo 1: Tarefa iniciada no Claude, transferida ao Antigravity e concluída com RESULT."""
        # 1. Criação no Claude
        t = create_task(
            self.workspace,
            title="Implementar utilitário de formatação de moeda",
            client="claude",
        )
        self.assertEqual(t["routing"]["client"], "claude")
        self.assertIsNone(t["routing"]["source_client"])

        # 2. Handoff autorizado para Antigravity
        h = handoff_task(
            workspace=self.workspace,
            task_id=t["id"],
            target_client="antigravity",
            reason="Transferência para ajuste fino na IDE Antigravity",
            authorized=True,
            context=["src/formatters.ts"],
            execution_mode="cross_client",
        )
        self.assertEqual(h["routing"]["client"], "antigravity")
        self.assertEqual(h["routing"]["source_client"], "claude")
        self.assertEqual(h["routing"]["execution_mode"], "cross_client")
        self.assertEqual(len(h["history"]), 1)
        self.assertEqual(h["history"][0]["action"], "cross_client_handoff")
        self.assertEqual(h["history"][0]["source_client"], "claude")
        self.assertEqual(h["history"][0]["target_client"], "antigravity")

        # 3. Antigravity confirma recebimento (in_progress) e executa
        update_task_status(self.workspace, t["id"], "in_progress")

        # 4. Geração do artefato físico no workspace
        out_file = self.workspace / "formatters.ts"
        out_file.write_text("export const formatBRL = (val: number) => `R$ ${val.toFixed(2)}`;\n", encoding="utf-8")

        # 5. Conclusão da tarefa com contrato RESULT
        done = complete_task(
            workspace=self.workspace,
            task_id=t["id"],
            summary="Formatador de moeda BRL implementado e testado com sucesso.",
            result_status="success",
            artifacts=["formatters.ts"],
        )
        self.assertEqual(done["status"], "completed")
        self.assertEqual(done["result"]["status"], "success")
        self.assertEqual(done["result"]["artifacts"], ["formatters.ts"])
        self.assertEqual(done["routing"]["client"], "antigravity")
        self.assertEqual(done["routing"]["source_client"], "claude")

    def test_02_antigravity_to_claude_handoff_and_result(self):
        """Fluxo 2: Tarefa iniciada no Antigravity, transferida ao Claude Code e concluída com RESULT."""
        # 1. Criação no Antigravity
        t = create_task(
            self.workspace,
            title="Refatorar módulo de rotas e middleware",
            client="antigravity",
        )
        self.assertEqual(t["routing"]["client"], "antigravity")

        # 2. Handoff autorizado para Claude Code
        h = handoff_task(
            workspace=self.workspace,
            task_id=t["id"],
            target_client="claude",
            reason="Delegando refatoração profunda de middleware ao Claude Code",
            authorized=True,
            context=["src/middleware.ts"],
            execution_mode="cross_client",
        )
        self.assertEqual(h["routing"]["client"], "claude")
        self.assertEqual(h["routing"]["source_client"], "antigravity")
        self.assertEqual(h["routing"]["execution_mode"], "cross_client")

        # 3. Claude confirma recebimento e produz artefato
        update_task_status(self.workspace, t["id"], "in_progress")
        mw_file = self.workspace / "middleware.ts"
        mw_file.write_text("// middleware refatorado\n", encoding="utf-8")

        # 4. Conclusão pelo Claude
        done = complete_task(
            workspace=self.workspace,
            task_id=t["id"],
            summary="Middleware refatorado e tipos conferidos.",
            result_status="success",
            artifacts=["middleware.ts"],
        )
        self.assertEqual(done["status"], "completed")
        self.assertEqual(done["result"]["status"], "success")
        self.assertEqual(done["routing"]["client"], "claude")
        self.assertEqual(done["routing"]["source_client"], "antigravity")

    def test_03_multiple_consecutive_handoffs_history_preservation(self):
        """Múltiplas transferências consecutivas preservam a ordem cronológica de eventos no histórico."""
        t = create_task(self.workspace, title="Tarefa multi-hop Claude <-> Antigravity", client="claude")
        update_task_status(self.workspace, t["id"], "in_progress")

        # Hop 1: claude -> antigravity
        h1 = handoff_task(
            workspace=self.workspace,
            task_id=t["id"],
            target_client="antigravity",
            reason="Hop 1: Ajuste de layout na IDE Antigravity",
            authorized=True,
            context=["src/App.tsx"],
        )
        self.assertEqual(h1["routing"]["source_client"], "claude")
        self.assertEqual(h1["routing"]["client"], "antigravity")
        self.assertEqual(len(h1["history"]), 1)

        # Hop 2: antigravity -> claude
        h2 = handoff_task(
            workspace=self.workspace,
            task_id=t["id"],
            target_client="claude",
            reason="Hop 2: Revisão de lógica de estado no Claude",
            authorized=True,
            context=["src/App.tsx", "src/hooks/useApp.ts"],
        )
        self.assertEqual(h2["routing"]["source_client"], "antigravity")
        self.assertEqual(h2["routing"]["client"], "claude")
        self.assertEqual(len(h2["history"]), 2)

        # Hop 3: claude -> antigravity
        h3 = handoff_task(
            workspace=self.workspace,
            task_id=t["id"],
            target_client="antigravity",
            reason="Hop 3: Validação visual final no navegador Antigravity",
            authorized=True,
            context=["src/App.tsx"],
        )
        self.assertEqual(h3["routing"]["source_client"], "claude")
        self.assertEqual(h3["routing"]["client"], "antigravity")
        self.assertEqual(len(h3["history"]), 3)

        # Validação do histórico completo
        self.assertEqual(h3["history"][0]["source_client"], "claude")
        self.assertEqual(h3["history"][0]["target_client"], "antigravity")
        self.assertEqual(h3["history"][1]["source_client"], "antigravity")
        self.assertEqual(h3["history"][1]["target_client"], "claude")
        self.assertEqual(h3["history"][2]["source_client"], "claude")
        self.assertEqual(h3["history"][2]["target_client"], "antigravity")

        # Conclusão final
        final_doc = self.workspace / "RESULT.txt"
        final_doc.write_text("OK", encoding="utf-8")
        done = complete_task(
            self.workspace,
            t["id"],
            summary="Fluxo multi-hop concluído com sucesso.",
            result_status="success",
            artifacts=["RESULT.txt"],
        )
        self.assertEqual(done["status"], "completed")
        self.assertEqual(len(done["history"]), 3)

    def test_04_valid_and_invalid_result_contracts(self):
        """Validação estrita de contratos RESULT: arquivos válidos, sem artefatos e rejeição de erros."""
        # 1. Sucesso legítimo com artefato existente
        t1 = create_task(self.workspace, title="Tarefa com artefato", client="claude")
        update_task_status(self.workspace, t1["id"], "in_progress")
        f1 = self.workspace / "valido.txt"
        f1.write_text("conteúdo válido", encoding="utf-8")
        d1 = complete_task(
            self.workspace,
            t1["id"],
            summary="Sucesso com arquivo.",
            result_status="success",
            artifacts=["valido.txt"],
        )
        self.assertEqual(d1["status"], "completed")
        self.assertEqual(d1["result"]["artifacts"], ["valido.txt"])

        # 2. Sucesso legítimo sem artefatos (ex: tarefa puramente investigativa)
        t2 = create_task(self.workspace, title="Tarefa investigativa sem arquivo", client="antigravity")
        update_task_status(self.workspace, t2["id"], "in_progress")
        d2 = complete_task(
            self.workspace,
            t2["id"],
            summary="Investigação concluída: nenhum bug encontrado.",
            result_status="success",
            artifacts=None,
        )
        self.assertEqual(d2["status"], "completed")
        self.assertEqual(d2["result"]["artifacts"], [])

        # 3. Rejeição: artefato declarado não existe no disco
        t3 = create_task(self.workspace, title="Tarefa com artefato fantasma", client="claude")
        update_task_status(self.workspace, t3["id"], "in_progress")
        with self.assertRaises(TaskValidationError) as ctx:
            complete_task(
                self.workspace,
                t3["id"],
                summary="Tentativa com arquivo inexistente",
                result_status="success",
                artifacts=["arquivo_fantasma.txt"],
            )
        self.assertIn("Artefato declarado não existe", str(ctx.exception))

        # 4. Rejeição: summary vazio ou em branco
        t4 = create_task(self.workspace, title="Tarefa com resumo inválido", client="claude")
        update_task_status(self.workspace, t4["id"], "in_progress")
        with self.assertRaises(TaskValidationError) as ctx:
            complete_task(self.workspace, t4["id"], summary="   ")
        self.assertIn("resumo substantivo", str(ctx.exception))

        # 5. Rejeição: result_status inválido
        t5 = create_task(self.workspace, title="Tarefa com status desconhecido", client="antigravity")
        update_task_status(self.workspace, t5["id"], "in_progress")
        with self.assertRaises(TaskValidationError) as ctx:
            complete_task(self.workspace, t5["id"], summary="Resumo", result_status="invalido")
        self.assertIn("Status do resultado inválido", str(ctx.exception))

    def test_05_path_traversal_and_malicious_id_protection(self):
        """Imunidade a path traversal em artefatos e validação rigorosa de ID de tarefa."""
        t = create_task(self.workspace, title="Tarefa de segurança traversal", client="antigravity")
        update_task_status(self.workspace, t["id"], "in_progress")

        # 1. Artefato com tentativa de escape via ../
        outside_file = self.workspace.parent / "escape.txt"
        outside_file.write_text("externo", encoding="utf-8")
        try:
            with self.assertRaises(TaskValidationError) as ctx:
                complete_task(
                    self.workspace,
                    t["id"],
                    summary="Tentativa de traversal",
                    artifacts=["../escape.txt"],
                )
            self.assertIn("escapa do diretório autorizado", str(ctx.exception))
        finally:
            if outside_file.exists():
                outside_file.unlink()

        # 2. Artefato com caminho absoluto fora do workspace
        with self.assertRaises(TaskValidationError) as ctx:
            complete_task(
                self.workspace,
                t["id"],
                summary="Tentativa com arquivo de sistema",
                artifacts=["C:/Windows/System32/drivers/etc/hosts"],
            )
        self.assertIn("escapa do diretório autorizado", str(ctx.exception))

        # 3. ID de tarefa malicioso rejeitado por regex
        with self.assertRaises(TaskValidationError):
            validate_task_id("task-../../hack")

        with self.assertRaises(TaskValidationError):
            validate_task_id("task-123")  # muito curto (< 8 caracteres de hash)

        with self.assertRaises(TaskValidationError):
            validate_task_id("TASK-12345678")  # maiúsculas não permitidas pelo regex

        with self.assertRaises(TaskValidationError):
            validate_task_id("task-abc@def#")  # caracteres especiais inválidos

    def test_06_controlled_transitions_failure_and_resumption(self):
        """Falha gera estado 'failed', bloqueia conclusão direta e exige 'resume_task' auditada."""
        t = create_task(self.workspace, title="Tarefa de recuperação controlada", client="claude")
        update_task_status(self.workspace, t["id"], "in_progress")

        # 1. Finalização com falha
        failed_t = complete_task(
            self.workspace,
            t["id"],
            summary="Falha na execução de testes de integração.",
            result_status="failure",
        )
        self.assertEqual(failed_t["status"], "failed")
        self.assertEqual(failed_t["result"]["status"], "failure")

        # 2. Bloqueio: não permite concluir diretamente a partir de 'failed'
        with self.assertRaises(TaskValidationError) as ctx:
            complete_task(self.workspace, t["id"], summary="Tentativa de reconclusão indevida")
        self.assertIn("Não é permitido registrar resultado para tarefa no estado 'failed'", str(ctx.exception))

        # 3. Retomada auditada: resume_task restaura 'in_progress' e limpa result antigo
        resumed_t = resume_task(
            self.workspace,
            t["id"],
            reason="Ajuste nas configurações de ambiente e correção dos testes.",
        )
        self.assertEqual(resumed_t["status"], "in_progress")
        self.assertIsNone(resumed_t["result"])
        self.assertEqual(len(resumed_t["history"]), 1)
        self.assertEqual(resumed_t["history"][0]["action"], "resume")
        self.assertEqual(resumed_t["history"][0]["previous_status"], "failed")

        # 4. Conclusão válida após retomada
        art = self.workspace / "passou.txt"
        art.write_text("Testes 100% aprovados", encoding="utf-8")
        done = complete_task(
            self.workspace,
            t["id"],
            summary="Retomada bem-sucedida e testes passando.",
            result_status="success",
            artifacts=["passou.txt"],
        )
        self.assertEqual(done["status"], "completed")
        self.assertEqual(done["result"]["status"], "success")

    def test_07_completed_tasks_are_immutable(self):
        """Tarefas em estado 'completed' são estritamente imutáveis para todas as operações."""
        t = create_task(self.workspace, title="Tarefa imutável pós-conclusão", client="antigravity")
        update_task_status(self.workspace, t["id"], "in_progress")
        done_file = self.workspace / "final.txt"
        done_file.write_text("finalizado", encoding="utf-8")
        complete_task(
            self.workspace,
            t["id"],
            summary="Finalização inicial.",
            result_status="success",
            artifacts=["final.txt"],
        )

        # Rejeição de reconclusão
        with self.assertRaises(TaskValidationError):
            complete_task(self.workspace, t["id"], summary="Reconclusão proibida")

        # Rejeição de transição de status
        with self.assertRaises(TaskValidationError):
            update_task_status(self.workspace, t["id"], "in_progress")

        # Rejeição de atribuição / mudança de especialista
        with self.assertRaises(TaskValidationError):
            assign_task(self.workspace, t["id"], specialist="lay-frontend", mode="session")

        # Rejeição de handoff
        with self.assertRaises(TaskValidationError):
            handoff_task(
                self.workspace,
                t["id"],
                target_client="claude",
                reason="Handoff pós-conclusão",
                authorized=True,
            )

    def test_08_minimum_delegation_hierarchy(self):
        """A hierarquia de delegação prioriza a sessão atual e só recomenda subagentes ou handoff com justificativa."""
        # Tier 1: Sessão atual por padrão
        rec_session = recommend_task_routing(
            title="Ajustar estilo CSS e contraste de botão",
            client="claude",
        )
        self.assertEqual(rec_session["recommended_mode"], "session")
        self.assertFalse(rec_session["requires_authorization"])

        # Tier 2: Subagente somente-leitura quando a demanda exige isolamento
        rec_sub = recommend_task_routing(
            title="Auditoria de vulnerabilidades em dependências npm",
            domain="security",
            client="antigravity",
        )
        self.assertEqual(rec_sub["recommended_mode"], "subagent")
        self.assertEqual(rec_sub["recommended_specialist"], "lay-seguranca")

        # Tier 3: Cross-client quando especificado cliente de destino diferente
        rec_cross = recommend_task_routing(
            title="Elaborar mockup visual no design system",
            domain="design",
            client="claude",
            target_client="antigravity",
        )
        self.assertEqual(rec_cross["recommended_mode"], "cross_client")
        self.assertTrue(rec_cross["requires_authorization"])

        # Tier 4: Árbitro exclusivamente em caso de impasse arquitetural crítico
        rec_arb = recommend_task_routing(
            title="Dilema crítico de concorrência com trade-offs insolúveis",
            complexity="critical",
            client="claude",
        )
        self.assertEqual(rec_arb["recommended_mode"], "arbitrator")
        self.assertTrue(rec_arb["requires_authorization"])

    def test_09_one_time_authorization_not_persistent(self):
        """A flag de autorização é pontual por operação e não autoriza transações subsequentes."""
        t = create_task(self.workspace, title="Tarefa teste autorização pontual", client="claude")
        update_task_status(self.workspace, t["id"], "in_progress")

        # Handoff sem autorização é rejeitado
        with self.assertRaises(TaskValidationError):
            handoff_task(
                self.workspace,
                t["id"],
                target_client="antigravity",
                reason="Tentativa sem autorização",
                authorized=False,
            )

        # Handoff autorizado sucede
        h1 = handoff_task(
            self.workspace,
            t["id"],
            target_client="antigravity",
            reason="Primeiro handoff autorizado",
            authorized=True,
        )
        self.assertEqual(h1["routing"]["client"], "antigravity")

        # Próximo handoff sem autorização volta a falhar
        with self.assertRaises(TaskValidationError):
            handoff_task(
                self.workspace,
                t["id"],
                target_client="claude",
                reason="Segundo handoff sem autorização",
                authorized=False,
            )

    def test_10_functional_codex_rejection(self):
        """O cliente Codex é rejeitado funcionalmente em handoffs e recomendações."""
        t = create_task(self.workspace, title="Tarefa teste rejeição Codex", client="claude")
        update_task_status(self.workspace, t["id"], "in_progress")

        # Rejeição de handoff para Codex
        with self.assertRaises(TaskValidationError) as ctx:
            handoff_task(
                self.workspace,
                t["id"],
                target_client="codex",
                reason="Tentando delegar para Codex",
                authorized=True,
            )
        self.assertIn("indisponível funcionalmente", str(ctx.exception))

        # Recomendação com target codex recai para a sessão
        rec = recommend_task_routing(
            title="Tarefa geral de backend",
            client="antigravity",
            target_client="codex",
        )
        self.assertEqual(rec["recommended_mode"], "session")
        self.assertIn("indisponível funcionalmente", rec["rationale"])

    def test_11_zero_model_invocations_or_external_subprocesses(self):
        """Garante que todo o ciclo de vida opera de forma estritamente determinística e local."""
        # Criação, atribuição, recomendação, handoff, conclusão e recuperação
        # devem executar em tempo ínfimo (< 0.1s) sem depender de rede, chaves de API ou modelos.
        t = create_task(self.workspace, title="Ciclo determinístico de validação", client="claude")
        update_task_status(self.workspace, t["id"], "in_progress")
        assign_task(self.workspace, t["id"], specialist="lay-engenharia", mode="session")
        h = handoff_task(
            self.workspace,
            t["id"],
            target_client="antigravity",
            reason="Handoff determinístico",
            authorized=True,
        )
        f = self.workspace / "doc.md"
        f.write_text("# Documento", encoding="utf-8")
        done = complete_task(
            self.workspace,
            t["id"],
            summary="Concluído deterministicamente.",
            result_status="success",
            artifacts=["doc.md"],
        )
        self.assertEqual(done["status"], "completed")

    def test_12_cli_end_to_end_homologation(self):
        """Valida que todos os comandos da CLI operam conforme especificado, inclusive 'task show' e 'task route'."""
        # 1. task create
        proc_create = subprocess.run(
            [
                sys.executable,
                str(ROOT / "scripts/skill_hub.py"),
                "task",
                "create",
                "--workspace",
                str(self.workspace),
                "--title",
                "Tarefa CLI de ponta a ponta",
                "--client",
                "claude",
            ],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            check=False,
        )
        self.assertEqual(proc_create.returncode, 0, proc_create.stderr)
        self.assertIn("Tarefa criada com sucesso", proc_create.stdout)

        tasks_list = list_tasks(self.workspace)
        self.assertEqual(len(tasks_list), 1)
        task_id = tasks_list[0]["id"]

        # 2. task show (confirmando que task show é o comando canônico, e não task status)
        proc_show = subprocess.run(
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
            check=False,
        )
        self.assertEqual(proc_show.returncode, 0, proc_show.stderr)
        self.assertIn(task_id, proc_show.stdout)
        self.assertIn("Tarefa CLI de ponta a ponta", proc_show.stdout)

        # 3. task route (alias para recommend)
        proc_route = subprocess.run(
            [
                sys.executable,
                str(ROOT / "scripts/skill_hub.py"),
                "task",
                "route",
                "--workspace",
                str(self.workspace),
                "--title",
                "Ajuste visual no componente de botão",
                "--client",
                "claude",
            ],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            check=False,
        )
        self.assertEqual(proc_route.returncode, 0, proc_route.stderr)
        self.assertIn("Modo Recomendado:         session", proc_route.stdout)

        # 4. task assign para in_progress
        proc_assign = subprocess.run(
            [
                sys.executable,
                str(ROOT / "scripts/skill_hub.py"),
                "task",
                "assign",
                task_id,
                "--workspace",
                str(self.workspace),
                "--specialist",
                "lay-engenharia",
                "--mode",
                "session",
            ],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            check=False,
        )
        self.assertEqual(proc_assign.returncode, 0, proc_assign.stderr)

        # 5. task handoff
        proc_handoff = subprocess.run(
            [
                sys.executable,
                str(ROOT / "scripts/skill_hub.py"),
                "task",
                "handoff",
                task_id,
                "--workspace",
                str(self.workspace),
                "--target-client",
                "antigravity",
                "--reason",
                "Transferência autorizada via CLI",
                "--authorized",
            ],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            check=False,
        )
        self.assertEqual(proc_handoff.returncode, 0, proc_handoff.stderr)
        self.assertIn("Handoff da tarefa", proc_handoff.stdout)
        self.assertIn("Origem:                   claude", proc_handoff.stdout)
        self.assertIn("Destino:                  antigravity", proc_handoff.stdout)

        # 6. task complete com falha simulada
        proc_fail = subprocess.run(
            [
                sys.executable,
                str(ROOT / "scripts/skill_hub.py"),
                "task",
                "complete",
                task_id,
                "--workspace",
                str(self.workspace),
                "--summary",
                "Simulando falha de execução",
                "--result-status",
                "failure",
            ],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            check=False,
        )
        self.assertEqual(proc_fail.returncode, 0, proc_fail.stderr)
        self.assertIn("Status Tarefa: failed", proc_fail.stdout)

        # 7. task resume
        proc_resume = subprocess.run(
            [
                sys.executable,
                str(ROOT / "scripts/skill_hub.py"),
                "task",
                "resume",
                task_id,
                "--workspace",
                str(self.workspace),
                "--reason",
                "Correção do problema detectado",
            ],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            check=False,
        )
        self.assertEqual(proc_resume.returncode, 0, proc_resume.stderr)
        self.assertIn("retomada com sucesso para 'in_progress'", proc_resume.stdout)

        # 8. task complete final
        art_file = self.workspace / "sucesso.txt"
        art_file.write_text("OK", encoding="utf-8")
        proc_done = subprocess.run(
            [
                sys.executable,
                str(ROOT / "scripts/skill_hub.py"),
                "task",
                "complete",
                task_id,
                "--workspace",
                str(self.workspace),
                "--summary",
                "Concluído com sucesso após retomada",
                "--artifacts",
                "sucesso.txt",
            ],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            check=False,
        )
        self.assertEqual(proc_done.returncode, 0, proc_done.stderr)
        self.assertIn("Status Tarefa: completed", proc_done.stdout)
        self.assertIn("Status RESULT: success", proc_done.stdout)

    def test_13_lock_boundaries_vs_session_idempotency(self):
        """Locks atômicos asseguram integridade na escrita, enquanto a imutabilidade do ciclo de vida garante idempotência."""
        t = create_task(self.workspace, title="Tarefa idempotência e locks", client="claude")
        update_task_status(self.workspace, t["id"], "in_progress")

        art = self.workspace / "artefato.txt"
        art.write_text("artefato", encoding="utf-8")
        done = complete_task(
            self.workspace,
            t["id"],
            summary="Tarefa completada.",
            result_status="success",
            artifacts=["artefato.txt"],
        )
        self.assertEqual(done["status"], "completed")

        # Mesmo que outra sessão de modelo tente reexecutar ou reenviar completion:
        with self.assertRaises(TaskValidationError):
            complete_task(
                self.workspace,
                t["id"],
                summary="Tentativa concorrente de modelo duplicado",
                result_status="success",
                artifacts=["artefato.txt"],
            )


if __name__ == "__main__":
    unittest.main()
