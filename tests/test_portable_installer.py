"""Testes de Portabilidade e Segurança do LAY Skills Hub (Fase C)
Valida instalação portátil, adapters multicliente, junctions Codex (depth=1),
backup, rollback de arquivos novos e existentes, preservação de regras e segurança.
Totalmente independente de credenciais, chaves ou skills privadas da máquina host.
"""
from __future__ import annotations

import io
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
import skill_hub as hub


class PortableInstallerSecurityTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.test_root = Path(self.temp_dir.name).resolve()
        self.mock_home = self.test_root / 'home' / 'rodrigo'
        self.mock_home.mkdir(parents=True, exist_ok=True)
        self.mock_workspace = self.test_root / 'workspace' / 'meu-projeto'
        self.mock_workspace.mkdir(parents=True, exist_ok=True)
        self.fixture_junction = None

    def tearDown(self):
        try:
            if self.fixture_junction and self.fixture_junction.exists():
                if os.name == 'nt':
                    subprocess.run(['cmd', '/c', 'rmdir', str(self.fixture_junction)], capture_output=True)
            self.temp_dir.cleanup()
        except Exception:
            pass

    def test_01_dry_run_zero_side_effects(self):
        """Dry-run não deve criar nenhum arquivo, diretório ou backup no mock_home."""
        result = hub.install(
            home=self.mock_home,
            agents=['claude', 'codex', 'antigravity'],
            root=ROOT,
            skip_tools=True,
            mode='public',
            dry_run=True
        )
        self.assertTrue(result.get('dry_run'))
        created_items = list(self.mock_home.iterdir())
        self.assertEqual(len(created_items), 0, f"Dry-run criou arquivos inesperados: {created_items}")

    def test_02_public_install_count(self):
        """Instalação pública provisiona exatamente 138 skills e remove blocos privados."""
        hub.install(
            home=self.mock_home,
            agents=['claude', 'codex', 'antigravity'],
            root=ROOT,
            skip_tools=True,
            mode='public',
            dry_run=False
        )
        installed_json = self.mock_home / '.lay-skills/runtime/catalog/installed.json'
        self.assertTrue(installed_json.exists())
        data = json.loads(installed_json.read_text(encoding='utf-8'))
        self.assertEqual(len(data['skills']), 138)
        self.assertEqual(data['mode'], 'public')

        claude_agents_dir = self.mock_home / '.claude/agents'
        for agent_file in claude_agents_dir.glob('*.md'):
            content = agent_file.read_text(encoding='utf-8')
            self.assertNotIn('<!-- LAY-PRIVATE-SKILLS:BEGIN -->', content)
            self.assertNotIn('skills-privadas-lay', content)

    def test_03_complete_install_count(self):
        """Instalação completa provisiona skills públicas + privadas usando fixture temporária."""
        fixture_root = self.test_root / 'fixture_repo'
        fixture_root.mkdir(parents=True, exist_ok=True)

        self.fixture_junction = fixture_root / 'refactored_skills'
        if os.name == 'nt':
            subprocess.run(['cmd', '/c', 'mklink', '/J', str(self.fixture_junction), str(ROOT / 'refactored_skills')],
                           check=True, capture_output=True)
        else:
            self.fixture_junction.symlink_to(ROOT / 'refactored_skills', target_is_directory=True)

        mock_private_skill = fixture_root / 'skills-privadas-lay/refactored/frontend/fixture-private-skill'
        mock_private_skill.mkdir(parents=True, exist_ok=True)
        (mock_private_skill / 'SKILL.md').write_text(
            "---\nname: fixture-private-skill\ndescription: Skill privada de teste para validação do modo complete\n---\n# Fixture\n",
            encoding='utf-8'
        )

        hub.install(
            home=self.mock_home,
            agents=['claude', 'codex', 'antigravity'],
            root=fixture_root,
            skip_tools=True,
            mode='complete',
            dry_run=False
        )
        installed_json = self.mock_home / '.lay-skills/runtime/catalog/installed.json'
        self.assertTrue(installed_json.exists())
        data = json.loads(installed_json.read_text(encoding='utf-8'))
        self.assertEqual(len(data['skills']), 139)
        self.assertEqual(data['mode'], 'complete')

        if os.name == 'nt':
            subprocess.run(['cmd', '/c', 'rmdir', str(self.fixture_junction)], capture_output=True)
        self.fixture_junction = None

    def test_04_portable_path_resolution(self):
        """Verifica se todos os templates resolvem caminhos dinamicamente sem marcadores pendentes."""
        hub.install(
            home=self.mock_home,
            agents=['claude', 'codex', 'antigravity'],
            root=ROOT,
            skip_tools=True,
            mode='public',
            dry_run=False
        )
        expected_home_posix = self.mock_home.as_posix()
        expected_runtime_posix = (self.mock_home / '.lay-skills/runtime').as_posix()

        for path_file in [self.mock_home / '.claude/CLAUDE.md',
                          self.mock_home / '.codex/AGENTS.md',
                          self.mock_home / '.gemini/GEMINI.md']:
            content = path_file.read_text(encoding='utf-8')
            self.assertNotIn('{{USER_HOME}}', content)
            self.assertNotIn('{{LAY_RUNTIME_DIR}}', content)
            self.assertNotIn('{{PYTHON_EXE}}', content)
            self.assertIn(expected_runtime_posix, content)
            self.assertIn(expected_home_posix, content)

        for ag_file in (self.mock_home / '.claude/agents').glob('*.md'):
            content = ag_file.read_text(encoding='utf-8')
            self.assertNotIn('{{LAY_RUNTIME_DIR}}', content)
            if ag_file.name != 'lay-arbitro-opus.md':
                self.assertIn(expected_runtime_posix, content)

    def test_05_idempotence(self):
        """Instalações consecutivas produzem hashes idênticos sem efeitos colaterais."""
        state1 = hub.install(
            home=self.mock_home,
            agents=['claude', 'codex', 'antigravity'],
            root=ROOT,
            skip_tools=True,
            mode='public',
            dry_run=False
        )
        claude_files1 = {f.name: hub.sha(f) for f in (self.mock_home / '.claude/agents').glob('*.md')}

        state2 = hub.install(
            home=self.mock_home,
            agents=['claude', 'codex', 'antigravity'],
            root=ROOT,
            skip_tools=True,
            mode='public',
            dry_run=False
        )
        claude_files2 = {f.name: hub.sha(f) for f in (self.mock_home / '.claude/agents').glob('*.md')}
        self.assertEqual(claude_files1, claude_files2)

    def test_06_personal_rules_preservation(self):
        """Instruções pessoais antes e depois do bloco gerenciado são preservadas intactas."""
        claude_dir = self.mock_home / '.claude'
        claude_dir.mkdir(parents=True, exist_ok=True)
        personal_claude = "# Minhas Regras Pessoais Claude\n- Não use emojis.\n- Responda em português.\n"
        (claude_dir / 'CLAUDE.md').write_text(personal_claude, encoding='utf-8')

        hub.install(
            home=self.mock_home,
            agents=['claude'],
            root=ROOT,
            skip_tools=True,
            mode='public',
            dry_run=False
        )
        updated = (claude_dir / 'CLAUDE.md').read_text(encoding='utf-8')
        self.assertIn('# Minhas Regras Pessoais Claude', updated)
        self.assertIn('- Não use emojis.', updated)
        self.assertIn('<!-- LAY-SKILLS:BEGIN -->', updated)
        self.assertIn('<!-- LAY-MANAGED:END -->', updated)

    def test_07_backup_and_rollback_preexisting_and_new(self):
        """Rollback restaura arquivos pré-existentes e remove arquivos novos não modificados."""
        claude_dir = self.mock_home / '.claude'
        claude_dir.mkdir(parents=True, exist_ok=True)
        orig_claude = "# Versão Original do Usuário\n"
        (claude_dir / 'CLAUDE.md').write_text(orig_claude, encoding='utf-8')

        hub.install(
            home=self.mock_home,
            agents=['claude'],
            root=ROOT,
            skip_tools=True,
            mode='public',
            dry_run=False
        )

        new_agent = claude_dir / 'agents/lay-frontend.md'
        self.assertTrue(new_agent.exists())
        self.assertIn('<!-- LAY-SKILLS:BEGIN -->', (claude_dir / 'CLAUDE.md').read_text(encoding='utf-8'))

        hub.rollback(self.mock_home)

        self.assertEqual((claude_dir / 'CLAUDE.md').read_text(encoding='utf-8'), orig_claude)
        self.assertFalse(new_agent.exists())

    def test_08_rollback_preserves_user_modified_new_files(self):
        """Se o usuário editou um arquivo novo criado pelo instalador, o rollback o preserva."""
        hub.install(
            home=self.mock_home,
            agents=['claude'],
            root=ROOT,
            skip_tools=True,
            mode='public',
            dry_run=False
        )
        new_agent = self.mock_home / '.claude/agents/lay-frontend.md'
        self.assertTrue(new_agent.exists())

        new_agent.write_text("CUSTOMIZADO PELO USUARIO", encoding='utf-8')

        hub.rollback(self.mock_home)

        self.assertTrue(new_agent.exists())
        self.assertEqual(new_agent.read_text(encoding='utf-8'), "CUSTOMIZADO PELO USUARIO")

    def test_09_link_junctions_codex_depth_1(self):
        """Junctions individuais devem ser criadas a depth=1 (.agents/skills/<skill>/SKILL.md)."""
        hub.install(
            home=self.mock_home,
            agents=['codex'],
            root=ROOT,
            skip_tools=True,
            mode='public',
            dry_run=False
        )
        hub_dir = self.mock_home / '.lay-skills'
        linked_count = hub.link_junctions(self.mock_workspace, hub_dir, domain='frontend')
        self.assertGreater(linked_count, 0)

        skills_dir = self.mock_workspace / '.agents/skills'
        self.assertTrue(skills_dir.exists())

        sample_skill = skills_dir / 'elevating-frontend-taste'
        self.assertTrue(sample_skill.exists())
        self.assertTrue((sample_skill / 'SKILL.md').exists(), "SKILL.md deve estar diretamente sob a pasta da skill (depth 1)")

    def test_10_confinement_security(self):
        """Confined rejeita caminhos fora do diretório base (path traversal)."""
        base = self.mock_home
        with self.assertRaises(ValueError):
            hub.confined(base, '../hack')
        with self.assertRaises(ValueError):
            hub.confined(base, '..')

    def test_11_doctor_verification(self):
        """Doctor valida com sucesso a instalação em ambiente mock."""
        hub.install(
            home=self.mock_home,
            agents=['claude', 'codex', 'antigravity'],
            root=ROOT,
            skip_tools=True,
            mode='public',
            dry_run=False
        )
        ok = hub.doctor(self.mock_home)
        self.assertTrue(ok)


if __name__ == '__main__':
    unittest.main()
