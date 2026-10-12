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
        (self.root / 'scripts').mkdir()
        shutil.copy2(Path(hub.__file__), self.root / 'scripts/skill_hub.py')
        project = self.base / 'project'
        project.mkdir()
        (project / 'package.json').write_text('{}', encoding='utf-8')
        (project / 'src.tsx').write_text('export const x = 1;', encoding='utf-8')
        self.project = project

    def test_install_reinstall_hooks_and_uninstall(self):
        old = self.home / '.claude/settings.json'
        old.parent.mkdir()
        old.write_text(json.dumps({'theme': 'dark', 'hooks': {'SessionStart': [{'matcher': 'startup', 'hooks': [{'type': 'command', 'command': 'existing'}]}]}}), encoding='utf-8')
        with contextlib.redirect_stdout(io.StringIO()):
            state = hub.install(self.home, list(hub.DESTINATIONS), self.root)
            hub.install(self.home, list(hub.DESTINATIONS), self.root)
        self.assertEqual(len(state['wrappers']), 4)
        self.assertEqual(json.loads(old.read_text())['theme'], 'dark')
        self.assertEqual(len(json.loads(old.read_text())['hooks']['SessionStart']), 2)
        original = next(w['original'] for w in state['wrappers'] if w['id'] == 'lay-design-page')
        self.assertEqual(Path(original).read_text(), (self.root / 'refactored_skills/design/design-page/SKILL.md').read_text())
        moved = self.base / 'repo-moved'
        self.root.rename(moved)
        runtime = self.home / '.lay-skills/runtime/scripts/skill_hub.py'
        command = [__import__('sys').executable, str(runtime)]
        result = subprocess.run(command + ['doctor', '--home', str(self.home)], capture_output=True, text=True, encoding='utf-8')
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        result = subprocess.run(command + ['start', '--home', str(self.home), '--project', str(self.project), '--offline'], capture_output=True, text=True, encoding='utf-8')
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn('P1', result.stdout)
        with contextlib.redirect_stdout(io.StringIO()):
            hub.uninstall(self.home)
        self.assertFalse((self.home / '.agents/skills/lay-design-page').exists())
        self.assertEqual(json.loads(old.read_text())['hooks']['SessionStart'][0]['hooks'][0]['command'], 'existing')
        self.assertEqual(json.loads(old.read_text())['theme'], 'dark')

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
            hub.install(self.home, ['codex'], self.root)
        (src / 'skills/design/SKILL.md').write_text('changed', encoding='utf-8')
        with self.assertRaisesRegex(ValueError, 'Fonte modificada'):
            hub.install(self.home, ['codex'], self.root)

    def test_private_skills_install_locally_but_stay_out_of_public_catalog(self):
        private = self.root / 'skills-privadas-lay/refactored/frontend/private-skill'
        private.mkdir(parents=True)
        (private / 'SKILL.md').write_text('---\nname: private-skill\ndescription: Private test. Use this skill when: x. Do NOT use this skill when: y.\n---\nBody.\n', encoding='utf-8')
        catalog = hub.build_catalog(self.root)
        self.assertNotIn('lay-private-skill', [e['id'] for e in catalog['skills']])
        with contextlib.redirect_stdout(io.StringIO()):
            state = hub.install(self.home, ['codex'], self.root)
        wrapper = next(w for w in state['wrappers'] if w['id'] == 'lay-private-skill')
        self.assertTrue(Path(wrapper['original']).is_file())
        self.assertIn('runtime', wrapper['original'])
        installed = json.loads((self.home / '.lay-skills/runtime/catalog/installed.json').read_text(encoding='utf-8'))
        self.assertIn('lay-private-skill', [e['id'] for e in installed['skills']])

    def test_collision_preserves_existing_skill(self):
        dest = self.home / '.agents/skills/lay-design-page'
        dest.mkdir(parents=True)
        (dest / 'SKILL.md').write_text('personal', encoding='utf-8')
        with self.assertRaisesRegex(ValueError, 'Colisão'):
            hub.install(self.home, ['codex'], self.root)
        self.assertEqual((dest / 'SKILL.md').read_text(), 'personal')

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
