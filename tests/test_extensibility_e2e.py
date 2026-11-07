import json
import os
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO))

from scripts import build_agents, nova_skill, skill_hub
from scripts.validate_skills import Validador


class TestExtensibilityE2E(unittest.TestCase):
    """Suíte de testes de ponta a ponta para a extensibilidade contínua de skills e agentes."""

    def setUp(self):
        self.tmp_dir = tempfile.TemporaryDirectory()
        self.test_root = Path(self.tmp_dir.name)
        self.mock_repo = self.test_root / 'repo'
        self.mock_home = self.test_root / 'home' / 'developer'
        self.mock_repo.mkdir(parents=True, exist_ok=True)
        self.mock_home.mkdir(parents=True, exist_ok=True)

        # Copia árvore essencial para isolamento hermético
        for d in ['refactored_skills', 'adapters', 'core', 'agents', 'catalog', 'docs']:
            src = REPO / d
            if src.exists():
                shutil.copytree(src, self.mock_repo / d)
        for f in ['AGENTS.md', 'GEMINI.md']:
            src = REPO / f
            if src.exists():
                shutil.copy2(src, self.mock_repo / f)

        # Cria pasta scripts mínima no mock_repo
        (self.mock_repo / 'scripts').mkdir(parents=True, exist_ok=True)
        for s in ['skill_hub.py', 'build_agents.py', 'nova_skill.py', 'validate_skills.py', 'build_hub.py']:
            shutil.copy2(REPO / 'scripts' / s, self.mock_repo / 'scripts' / s)

    def tearDown(self):
        try:
            self.tmp_dir.cleanup()
        except Exception:
            pass

    def test_01_add_skill_and_validate_strict_pattern(self):
        """Etapas 1-6: Adiciona mock skill no padrão estrito e valida roteadores."""
        skill_name = 'mocking-extensibility-workflow'
        domain = 'qa'
        description = (
            "Executa testes sintéticos ponta a ponta para validar a extensibilidade contínua "
            "de skills e subagentes nos adaptadores multicliente. "
            "Use this skill when: validar a adição de novas capacidades ou testar a pipeline de adaptadores. "
            "Do NOT use this skill when: executar em ambiente de produção sem isolamento temporário."
        )
        corpo = """# mocking-extensibility-workflow

Executa testes sintéticos ponta a ponta para validar a extensibilidade contínua de skills.

## Input/Output Signature
- Input: `target_domain` (string), `mock_skill_payload` (dict)
- Output: `validation_status` (success|failure), `test_report` (markdown)

## Imperative Execution Workflow
1. [FRÁGIL] Verificar se o diretório alvo pertence a um dos 11 domínios canônicos.
2. [FLEXÍVEL] Criar fixture temporária e validar metadados e frontmatter.
3. [FRÁGIL] Executar o validador estrito contra a árvore de skills.

## Checklist
- [ ] Nome em gerúndio verificado
- [ ] Fronteiras explícitas presentes
- [ ] Seção On Failure configurada

## On Failure
- **Gatilho de Erro**: Falha de sintaxe YAML ou ausência de gatilhos na descrição.
- **Ação Imediata**: Abortar gravação no repositório.
- **Rollback**: Reverter diretório criado e restaurar roteador do domínio.
- **Fallback**: Notificar operador com mensagem concisa.
- **Logs**: Gravar log do erro em stdout com detalhes da violação.
"""
        texto_skill = nova_skill.montar_skill_md(skill_name, description, corpo)
        pacotes = [(domain, skill_name, texto_skill, None)]

        # Aplica a skill na árvore do mock_repo
        erros, avisos, alterados = nova_skill.aplicar(self.mock_repo / 'refactored_skills', pacotes, privado=False)
        self.assertEqual(erros, [], f"Erros ao adicionar skill: {erros}")
        self.assertTrue(any(f'{domain}/{skill_name}' in a for a in alterados))

        # Validação estrita
        validador = Validador(self.mock_repo / 'refactored_skills', privado=False)
        validador.skills()
        validador.roteadores()
        validador.estrutura()
        self.assertEqual(validador.erros, [], f"Validação estrita falhou: {validador.erros}")

        # Roteador do domínio qa atualizado
        qa_router = self.mock_repo / 'refactored_skills' / domain / 'SKILL.md'
        self.assertIn(f'[{skill_name}](./{skill_name}/SKILL.md)', qa_router.read_text(encoding='utf-8'))

    def test_02_adapter_regeneration_preserves_contracts(self):
        """Etapas 7-8: Regeneração sincroniza adaptadores Claude e Antigravity preservando contratos."""
        skill_name = 'mocking-extensibility-workflow'
        domain = 'qa'
        description = (
            "Executa testes sintéticos ponta a ponta para validar a extensibilidade. "
            "Use this skill when: validar testes sintéticos. "
            "Do NOT use this skill when: rodar em produção."
        )
        corpo = (
            "# mocking-extensibility-workflow\n\nTeste.\n\n"
            "## Imperative Execution Workflow\n1. [FRÁGIL] Passo 1.\n\n"
            "## Checklist\n- [ ] Passo 1\n\n"
            "## On Failure\n- **Gatilho de Erro**: Falha.\n- **Ação Imediata**: Parar.\n"
            "- **Rollback**: Limpar.\n- **Fallback**: Nenhum.\n- **Logs**: Stdout.\n"
        )
        texto_skill = nova_skill.montar_skill_md(skill_name, description, corpo)
        nova_skill.aplicar(self.mock_repo / 'refactored_skills', [(domain, skill_name, texto_skill, None)], privado=False)

        # Executa atualização de adaptadores
        build_agents.update_adapters(root=self.mock_repo)

        # 1. Claude Adapter: lay-qa.md deve conter a nova skill
        qa_agent_path = self.mock_repo / 'adapters/claude/agents/lay-qa.md'
        qa_txt = qa_agent_path.read_text(encoding='utf-8')
        self.assertIn(f'- `{skill_name}`: `{{{{LAY_RUNTIME_DIR}}}}/refactored_skills/{domain}/{skill_name}/SKILL.md`', qa_txt)
        # Contratos inegociáveis preservados:
        self.assertIn('model: sonnet', qa_txt)
        self.assertIn('tools: Read, Grep, Glob, Bash, Edit, Write', qa_txt)
        self.assertIn('## Regras de atuação', qa_txt)
        self.assertIn('## Contrato de Resposta (RESULT)', qa_txt)

        # 2. Outros especialistas Claude NÃO devem ser contaminados
        sec_agent_path = self.mock_repo / 'adapters/claude/agents/lay-seguranca.md'
        sec_txt = sec_agent_path.read_text(encoding='utf-8')
        self.assertNotIn(skill_name, sec_txt)
        self.assertIn('tools: Read, Grep, Glob', sec_txt)

        # 3. Antigravity Manifests: skills-full.json contém a nova skill
        full_manifest_path = self.mock_repo / 'adapters/antigravity/manifests/skills-full.json'
        full_manifest = json.loads(full_manifest_path.read_text(encoding='utf-8'))
        qa_entry = next((e for e in full_manifest['entries'] if e['path'].endswith('/qa')), None)
        self.assertIsNotNone(qa_entry)
        self.assertIn(skill_name, qa_entry['include_only'])

        # 4. Antigravity Subagents Template: SystemPrompt de lay-qa atualizado
        subagents_path = self.mock_repo / 'adapters/antigravity/agents/subagents-definition-template.json'
        subagents_data = json.loads(subagents_path.read_text(encoding='utf-8'))
        qa_sub = next(s for s in subagents_data['subagents'] if s['Name'] == 'lay-qa')
        self.assertIn(f"- {skill_name}:", qa_sub['SystemPrompt'])

    def test_03_installer_dynamic_count_and_e2e_provisioning(self):
        """Etapas 9-10: Instalador calcula catálogo dinamicamente (139 skills) e provisiona no target."""
        skill_name = 'mocking-extensibility-workflow'
        domain = 'qa'
        description = (
            "Executa testes sintéticos ponta a ponta para validar a extensibilidade. "
            "Use this skill when: validar testes sintéticos. "
            "Do NOT use this skill when: rodar em produção."
        )
        corpo = (
            "# mocking-extensibility-workflow\n\nTeste.\n\n"
            "## Imperative Execution Workflow\n1. [FRÁGIL] Passo 1.\n\n"
            "## Checklist\n- [ ] Passo 1\n\n"
            "## On Failure\n- **Gatilho de Erro**: Falha.\n- **Ação Imediata**: Parar.\n"
            "- **Rollback**: Limpar.\n- **Fallback**: Nenhum.\n- **Logs**: Stdout.\n"
        )
        texto_skill = nova_skill.montar_skill_md(skill_name, description, corpo)
        nova_skill.aplicar(self.mock_repo / 'refactored_skills', [(domain, skill_name, texto_skill, None)], privado=False)
        build_agents.update_adapters(root=self.mock_repo)

        # Instalação pública em mock_home
        skill_hub.install(
            home=self.mock_home,
            agents=['claude', 'codex', 'antigravity'],
            root=self.mock_repo,
            skip_tools=True,
            mode='public',
            dry_run=False
        )

        installed_json = self.mock_home / '.lay-skills/runtime/catalog/installed.json'
        self.assertTrue(installed_json.exists())
        data = json.loads(installed_json.read_text(encoding='utf-8'))
        # Catálogo derivado dinamicamente: 138 + 1 = 139 skills
        self.assertEqual(len(data['skills']), 139)
        self.assertTrue(any(s['name'] == skill_name for s in data['skills']))

        # Subagente Claude instalado no cliente possui o novo skill path resolvido
        installed_claude_qa = self.mock_home / '.claude/agents/lay-qa.md'
        qa_installed_txt = installed_claude_qa.read_text(encoding='utf-8')
        expected_resolved_path = (self.mock_home / '.lay-skills/runtime/refactored_skills/qa' / skill_name / 'SKILL.md').as_posix()
        self.assertIn(skill_name, qa_installed_txt)
        self.assertIn(expected_resolved_path, qa_installed_txt.replace('\\', '/'))

        # Ausência de vazamento de referências privadas na distribuição pública
        for agent_file in (self.mock_home / '.claude/agents').glob('*.md'):
            agent_content = agent_file.read_text(encoding='utf-8')
            self.assertNotIn('<!-- LAY-PRIVATE-SKILLS:BEGIN -->', agent_content)
            self.assertNotIn('skills-privadas-lay', agent_content)

        ag_manifest = self.mock_home / '.gemini/config/skills.json'
        if ag_manifest.exists():
            self.assertNotIn('skills-privadas-lay', ag_manifest.read_text(encoding='utf-8'))

        # Descoberta Codex: link-junctions cria junction para a nova skill
        mock_workspace = self.test_root / 'workspace' / 'test-project'
        mock_workspace.mkdir(parents=True, exist_ok=True)
        if os.name == 'nt':
            skill_hub.link_junctions(mock_workspace, self.mock_home / '.lay-skills', domain=domain)
            junction_path = mock_workspace / '.agents/skills' / skill_name
            self.assertTrue(junction_path.exists())
            self.assertTrue((junction_path / 'SKILL.md').is_file())


if __name__ == '__main__':
    unittest.main()
