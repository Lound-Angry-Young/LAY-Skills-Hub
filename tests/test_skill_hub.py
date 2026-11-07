"""Exercise installation invariants in an isolated, tiny repository."""
import contextlib
import io
import json
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest
from unittest.mock import patch

from scripts import skill_hub as hub

REPO = Path(hub.__file__).resolve().parents[1]


class HubIntegrationTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.base = Path(self.tmp.name)
        self.root = self.base / 'repo'
        self.home = self.base / 'home'
        self.root.mkdir()
        self.home.mkdir()
        local = self.root / 'skills/core'
        local.mkdir(parents=True)
        (local / 'SKILL.md').write_text('---\nname: core\ndescription: Local sample.\n---\nUse local.\n', encoding='utf-8')
        src = self.root / 'upstream/vendor'
        src.mkdir(parents=True)
        (src / 'skills/design').mkdir(parents=True)
        (src / 'skills/design/SKILL.md').write_text('---\nname: design\ndescription: Design a page.\n---\nUse design.\n', encoding='utf-8')
        subprocess.run(['git', 'init', str(src)], check=True, capture_output=True)
        subprocess.run(['git', '-C', str(src), 'add', '.'], check=True, capture_output=True)
        subprocess.run(['git', '-C', str(src), '-c', 'user.name=Test', '-c', 'user.email=test@example.org', 'commit', '-m', 'init'], check=True, capture_output=True)
        commit = subprocess.check_output(['git', '-C', str(src), 'rev-parse', 'HEAD'], text=True).strip()
        registry = self.root / 'registry/sources.json'
        registry.parent.mkdir()
        registry.write_text(json.dumps({'schema_version': 1, 'sources': [{'id': 'vendor', 'repo': 'test/vendor', 'url': 'https://github.com/test/vendor',
           'path': 'upstream/vendor', 'commit': commit, 'version': 'v1', 'kind': 'skills', 'skill_paths': ['skills/design/SKILL.md'], 'notes': []}]}), encoding='utf-8')
        refactored = self.root / 'refactored_skills/design/design-page'
        refactored.mkdir(parents=True)
        (refactored / 'SKILL.md').write_text('---\nname: design-page\ndescription: Design a page. Use this skill when: a page needs layout. Do NOT use this skill when: backend only.\n---\nUse design.\n', encoding='utf-8')
        (self.root / 'refactored_skills/design/SKILL.md').write_text('---\nname: routing-design-skills\ndescription: Routes design requests.\n---\n', encoding='utf-8')
        (self.root / 'agents').mkdir()
        shutil.copy2(REPO / 'agents/perfis.json', self.root / 'agents/perfis.json')
        (self.root / 'core').mkdir()
        shutil.copy2(REPO / 'core/perfis.json', self.root / 'core/perfis.json')
        shutil.copytree(REPO / 'adapters', self.root / 'adapters')
        (self.root / 'scripts').mkdir()
        shutil.copy2(Path(hub.__file__), self.root / 'scripts/skill_hub.py')
        project = self.base / 'project'
        project.mkdir()
        (project / 'package.json').write_text('{}', encoding='utf-8')
        (project / 'src.tsx').write_text('export const x = 1;', encoding='utf-8')
        self.project = project

    def test_install_reinstall_hooks_and_uninstall(self):
        old = self.home / '.claude/CLAUDE.md'
        old.parent.mkdir(parents=True)
        old.write_text('# Pre-existing Claude instructions\n- Do not delete my files.\n', encoding='utf-8')
        with contextlib.redirect_stdout(io.StringIO()):
            state = hub.install(self.home, list(hub.DESTINATIONS), self.root, mode='public')
            hub.install(self.home, list(hub.DESTINATIONS), self.root, mode='public')
        self.assertEqual(state['mode'], 'public')
        self.assertGreater(state['catalog_count'], 0)
        self.assertEqual(len(state['claude_agents']), 12)

        # Preservação de arquivo preexistente + injeção do bloco LAY
        claude_md = old.read_text(encoding='utf-8')
        self.assertIn('# Pre-existing Claude instructions', claude_md)
        self.assertIn('- Do not delete my files.', claude_md)
        self.assertEqual(claude_md.count(hub.BEGIN), 1)
        self.assertEqual(claude_md.count(hub.END), 1)

        # Artefatos gerados pelo runtime v2
        runtime_installed = self.home / '.lay-skills/runtime/catalog/installed.json'
        self.assertTrue(runtime_installed.is_file())
        installed_data = json.loads(runtime_installed.read_text(encoding='utf-8'))
        self.assertEqual(installed_data['mode'], 'public')
        self.assertTrue((self.home / '.lay-skills/runtime/refactored_skills/design/design-page/SKILL.md').is_file())
        self.assertTrue((self.home / '.codex/AGENTS.md').is_file())
        self.assertTrue((self.home / '.gemini/GEMINI.md').is_file())

        # Backups criados
        backups = list((self.home / '.lay-skills/backups').glob('pre-install-*'))
        self.assertGreaterEqual(len(backups), 1)

        # Autonomia do runtime após mover repositório de origem
        moved = self.base / 'repo-moved'
        self.root.rename(moved)
        runtime = self.home / '.lay-skills/runtime/scripts/skill_hub.py'
        command = [__import__('sys').executable, str(runtime)]
        result = subprocess.run(command + ['doctor', '--home', str(self.home)], capture_output=True, text=True, encoding='utf-8')
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        result = subprocess.run(command + ['start', '--home', str(self.home), '--project', str(self.project), '--offline'], capture_output=True, text=True, encoding='utf-8')
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn('P1', result.stdout)

        # Desinstalação limpa
        with contextlib.redirect_stdout(io.StringIO()):
            hub.uninstall(self.home)
        self.assertEqual(list((self.home / '.claude/agents').glob('lay-*.md')), [])
        claude_md_after = old.read_text(encoding='utf-8')
        self.assertNotIn(hub.BEGIN, claude_md_after)
        self.assertIn('# Pre-existing Claude instructions', claude_md_after)

    def test_rollback_restores_preexisting_files_and_removes_unmodified_new(self):
        old = self.home / '.claude/CLAUDE.md'
        old.parent.mkdir(parents=True)
        old.write_text('# Before Install\n', encoding='utf-8')
        with contextlib.redirect_stdout(io.StringIO()):
            hub.install(self.home, ['claude'], self.root, mode='public')
        self.assertTrue((self.home / '.claude/agents/lay-frontend.md').is_file())
        self.assertIn(hub.BEGIN, old.read_text(encoding='utf-8'))

        with contextlib.redirect_stdout(io.StringIO()):
            hub.rollback(self.home)
        self.assertEqual(old.read_text(encoding='utf-8'), '# Before Install\n')
        self.assertFalse((self.home / '.claude/agents/lay-frontend.md').exists())

    def test_catalog_lists_only_refactored_skills(self):
        catalog = hub.build_catalog(self.root)
        self.assertEqual([e['id'] for e in catalog['skills']], ['lay-design-page'])
        self.assertEqual(catalog['skills'][0]['categories'], ['design'])
        self.assertIn('lay-design-page', (self.root / 'docs/CATALOGO.md').read_text(encoding='utf-8'))

    def test_untracked_files_do_not_block_but_tracked_changes_do(self):
        src = self.root / 'upstream/vendor'
        (src / 'generated').mkdir()
        (src / 'generated/obj.json').write_text('{}', encoding='utf-8')
        with contextlib.redirect_stdout(io.StringIO()):
            hub.install(self.home, ['codex'], self.root, mode='public')
        (src / 'skills/design/SKILL.md').write_text('changed', encoding='utf-8')
        with self.assertRaisesRegex(ValueError, 'Fonte modificada'):
            hub.install(self.home, ['codex'], self.root, mode='public')

    def test_private_skills_install_locally_but_stay_out_of_public_catalog(self):
        private = self.root / 'skills-privadas-lay/refactored/frontend/private-skill'
        private.mkdir(parents=True)
        (private / 'SKILL.md').write_text('---\nname: private-skill\ndescription: Private test. Use this skill when: x. Do NOT use this skill when: y.\n---\nBody.\n', encoding='utf-8')
        catalog = hub.build_catalog(self.root)
        self.assertNotIn('lay-private-skill', [e['id'] for e in catalog['skills']])
        with contextlib.redirect_stdout(io.StringIO()):
            state = hub.install(self.home, ['codex'], self.root, mode='complete')
        self.assertEqual(state['mode'], 'complete')
        installed = json.loads((self.home / '.lay-skills/runtime/catalog/installed.json').read_text(encoding='utf-8'))
        self.assertIn('lay-private-skill', [e['id'] for e in installed['skills']])
        self.assertTrue((self.home / '.lay-skills/runtime/skills-privadas-lay/refactored/frontend/private-skill/SKILL.md').is_file())

    def test_installed_wrapper_keeps_full_trigger_boundaries(self):
        # Descrições acima de 400 caracteres perdiam a cláusula "Do NOT use this skill when:" no wrapper instalado.
        longa = 'Desenha layouts responsivos com tokens consistentes em múltiplas telas. ' * 8
        descricao = longa + 'Use this skill when: a page needs responsive layout. Do NOT use this skill when: backend only.'
        self.assertGreater(len(descricao), 400)
        skill = self.root / 'refactored_skills/design/long-page'
        skill.mkdir(parents=True)
        (skill / 'SKILL.md').write_text(f'---\nname: long-page\ndescription: {descricao}\n---\nUse design.\n', encoding='utf-8')
        with contextlib.redirect_stdout(io.StringIO()):
            state = hub.install(self.home, ['codex'], self.root, mode='public')
        installed = self.home / '.lay-skills/runtime/refactored_skills/design/long-page/SKILL.md'
        self.assertTrue(installed.is_file())
        texto = installed.read_text(encoding='utf-8')
        self.assertIn('Do NOT use this skill when: backend only.', texto)
        catalog = hub.build_catalog(self.root)
        entry = next(e for e in catalog['skills'] if e['id'] == 'lay-long-page')
        self.assertIn('Do NOT use this skill when: backend only.', entry['description'])

    def test_collision_preserves_existing_skill(self):
        dest = self.home / '.claude/agents/lay-design.md'
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text('personal agent', encoding='utf-8')
        with self.assertRaisesRegex(ValueError, 'Colisão'):
            hub.install(self.home, ['claude'], self.root, mode='public')
        self.assertEqual(dest.read_text(encoding='utf-8'), 'personal agent')

    def test_parent_local_commit_is_not_replaced_by_remote(self):
        bare = self.base / 'remote.git'
        checkout = self.base / 'checkout'
        subprocess.run(['git', 'init', '--bare', str(bare)], check=True, capture_output=True)
        subprocess.run(['git', 'clone', str(bare), str(checkout)], check=True, capture_output=True)
        (checkout / 'readme.txt').write_text('local work', encoding='utf-8')
        subprocess.run(['git', '-C', str(checkout), 'add', '.'], check=True, capture_output=True)
        subprocess.run(['git', '-C', str(checkout), '-c', 'user.name=Test', '-c', 'user.email=test@example.org', 'commit', '-m', 'first'], check=True, capture_output=True)
        subprocess.run(['git', '-C', str(checkout), 'push', '-u', 'origin', 'HEAD'], check=True, capture_output=True)
        (checkout / 'readme.txt').write_text('local ahead', encoding='utf-8')
        subprocess.run(['git', '-C', str(checkout), 'add', '.'], check=True, capture_output=True)
        subprocess.run(['git', '-C', str(checkout), '-c', 'user.name=Test', '-c', 'user.email=test@example.org', 'commit', '-m', 'ahead'], check=True, capture_output=True)
        head = subprocess.check_output(['git', '-C', str(checkout), 'rev-parse', 'HEAD'], text=True).strip()
        with patch.object(hub, 'sync_sources', return_value=True), contextlib.redirect_stdout(io.StringIO()) as output:
            self.assertTrue(hub.sync(checkout, apply=True))
        self.assertIn('à frente', output.getvalue())
        self.assertNotIn('atualizado versão', output.getvalue())
        self.assertEqual(subprocess.check_output(['git', '-C', str(checkout), 'rev-parse', 'HEAD'], text=True).strip(), head)


if __name__ == '__main__':
    unittest.main()
