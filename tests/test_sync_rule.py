"""Regra de atualização: o início de sessão só consulta; aplicar é explícito."""
import contextlib
import io
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

from scripts import skill_hub as hub


class SyncRuleTests(unittest.TestCase):
    def test_session_start_checks_and_never_applies_or_reinstalls(self):
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            home = base / 'home'
            (home / '.lay-skills').mkdir(parents=True)
            repo = base / 'repo'
            (repo / '.git').mkdir(parents=True)
            (home / '.lay-skills/installation.json').write_text(json.dumps({
                'source_root': str(repo), 'agents': ['claude'], 'python': sys.executable, 'wrappers': []}), encoding='utf-8')
            project = base / 'projeto'
            project.mkdir()
            chamadas = []

            def fake_run(args, **kwargs):
                chamadas.append(list(args))
                return subprocess.CompletedProcess(args, 0, stdout='', stderr='')

            with patch.object(hub, 'run', side_effect=fake_run), \
                    patch.object(hub, 'install') as reinstalar, \
                    contextlib.redirect_stdout(io.StringIO()):
                hub.start(home, project)

            sync = [a for a in chamadas if 'sync' in a]
            self.assertEqual(len(sync), 1)
            self.assertIn('--check', sync[0])
            self.assertNotIn('--apply', sync[0])
            reinstalar.assert_not_called()

    def test_check_flag_does_not_touch_revisions(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            with patch.object(hub, 'sync_sources', return_value=True) as fontes, \
                    patch.object(hub, 'git', return_value='abc') as git, \
                    contextlib.redirect_stdout(io.StringIO()):
                hub.sync(repo, apply=False)
            self.assertFalse(any(c.args[:2] == (repo, 'merge') for c in git.call_args_list))
            self.assertGreaterEqual(len(fontes.call_args_list), 1)
            for call in fontes.call_args_list:
                self.assertFalse(call.args[1])


if __name__ == '__main__':
    unittest.main()
