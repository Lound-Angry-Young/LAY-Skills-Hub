"""Subagentes do Claude Code: perfis, frontmatter, instalação global, colisão e remoção."""
import contextlib
import io
import json
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest

import yaml

from scripts import skill_hub as hub

REPO = Path(hub.__file__).resolve().parents[1]


class AgentProfileTests(unittest.TestCase):
    def test_profiles_cover_every_domain_once(self):
        perfis = hub.load_profiles(REPO)
        self.assertEqual(sorted(p['dominio'] for p in perfis), sorted(hub.AGENTS_DOMINIOS))
        self.assertEqual(len({p['nome'] for p in perfis}), len(perfis))

    def test_each_description_has_triggers_and_fits_limit(self):
        for p in hub.load_profiles(REPO):
            self.assertIn('Use quando:', p['descricao'], p['nome'])
            self.assertIn('Não use para:', p['descricao'], p['nome'])
            self.assertLessEqual(len(p['descricao']), 1024, p['nome'])

    def test_generated_file_has_valid_claude_frontmatter(self):
        perfil = next(p for p in hub.load_profiles(REPO) if p['dominio'] == 'security')
        texto = hub.claude_agent_text(perfil, [('demo', 'C:/x/demo/SKILL.md', 'Demo skill. Use this skill when: x.')])
        meta = yaml.safe_load(texto.split('---\n', 2)[1])
        self.assertEqual(meta['name'], perfil['nome'])
        self.assertEqual(meta['description'], perfil['descricao'])
        self.assertEqual([t.strip() for t in meta['tools'].split(',')], perfil['ferramentas'])
        self.assertIn('`demo`: `C:/x/demo/SKILL.md`', texto)
        self.assertIn('status: success | failure | needs_clarification | escalated', texto)

    def test_security_profile_cannot_edit_files(self):
        perfil = next(p for p in hub.load_profiles(REPO) if p['dominio'] == 'security')
        self.assertNotIn('Edit', perfil['ferramentas'])
        self.assertNotIn('Write', perfil['ferramentas'])

    def test_invalid_profile_is_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / 'agents').mkdir()
            dados = json.loads((REPO / 'agents/perfis.json').read_text(encoding='utf-8'))
            dados['perfis'][0]['descricao'] = 'sem gatilhos'
            (root / 'agents/perfis.json').write_text(json.dumps(dados, ensure_ascii=False), encoding='utf-8')
            with self.assertRaisesRegex(ValueError, 'sem gatilhos'):
                hub.load_profiles(root)


class AgentInstallTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.base = Path(self.tmp.name)
        self.root = self.base / 'repo'
        self.home = self.base / 'home'
        self.root.mkdir()
        self.home.mkdir()
        skill = self.root / 'refactored_skills/frontend/demo-skill'
        skill.mkdir(parents=True)
        (skill / 'SKILL.md').write_text('---\nname: demo-skill\ndescription: Demo. Use this skill when: testar.\n---\nCorpo.\n', encoding='utf-8')
        src = self.root / 'upstream/vendor'
        src.mkdir(parents=True)
        (src / 'README.md').write_text('vendor', encoding='utf-8')
        subprocess.run(['git', 'init', str(src)], check=True, capture_output=True)
        subprocess.run(['git', '-C', str(src), 'add', '.'], check=True, capture_output=True)
        subprocess.run(['git', '-C', str(src), '-c', 'user.name=Test', '-c', 'user.email=test@example.org', 'commit', '-m', 'init'], check=True, capture_output=True)
        commit = subprocess.check_output(['git', '-C', str(src), 'rev-parse', 'HEAD'], text=True).strip()
        registry = self.root / 'registry/sources.json'
        registry.parent.mkdir()
        registry.write_text(json.dumps({'schema_version': 1, 'sources': [{'id': 'vendor', 'repo': 'test/vendor', 'url': 'https://github.com/test/vendor',
                                                                         'path': 'upstream/vendor', 'commit': commit, 'version': 'v1', 'kind': 'skills',
                                                                         'skill_paths': [], 'notes': []}]}), encoding='utf-8')
        (self.root / 'agents').mkdir()
        shutil.copy2(REPO / 'agents/perfis.json', self.root / 'agents/perfis.json')
        (self.root / 'scripts').mkdir()
        shutil.copy2(Path(hub.__file__), self.root / 'scripts/skill_hub.py')

    def agents_dir(self):
        return self.home / '.claude/agents'

    def test_install_writes_global_agents_and_claude_md_index(self):
        with contextlib.redirect_stdout(io.StringIO()):
            state = hub.install(self.home, ['claude'], self.root)
        self.assertEqual(len(list(self.agents_dir().glob('lay-*.md'))), 11)
        texto = (self.agents_dir() / 'lay-frontend.md').read_text(encoding='utf-8')
        self.assertIn('`demo-skill`', texto)
        self.assertIn('demo-skill', texto)
        self.assertEqual(len(state['claude_agents']), 11)
        claude_md = (self.home / '.claude/CLAUDE.md').read_text(encoding='utf-8')
        self.assertIn('`lay-frontend`', claude_md)
        self.assertEqual(claude_md.count(hub.BEGIN), 1)

    def test_reinstall_is_idempotent_and_detects_manual_edit(self):
        with contextlib.redirect_stdout(io.StringIO()):
            hub.install(self.home, ['claude'], self.root)
            hub.install(self.home, ['claude'], self.root)
        self.assertEqual(len(list(self.agents_dir().glob('lay-*.md'))), 11)
        (self.agents_dir() / 'lay-frontend.md').write_text('editado à mão', encoding='utf-8')
        with self.assertRaisesRegex(ValueError, 'modificado'):
            with contextlib.redirect_stdout(io.StringIO()):
                hub.install(self.home, ['claude'], self.root)
        self.assertEqual((self.agents_dir() / 'lay-frontend.md').read_text(encoding='utf-8'), 'editado à mão')

    def test_collision_with_user_agent_is_preserved(self):
        self.agents_dir().mkdir(parents=True)
        (self.agents_dir() / 'lay-qa.md').write_text('meu agente', encoding='utf-8')
        with self.assertRaisesRegex(ValueError, 'Colisão'):
            with contextlib.redirect_stdout(io.StringIO()):
                hub.install(self.home, ['claude'], self.root)
        self.assertEqual((self.agents_dir() / 'lay-qa.md').read_text(encoding='utf-8'), 'meu agente')

    def test_uninstall_removes_only_managed_agents(self):
        with contextlib.redirect_stdout(io.StringIO()):
            hub.install(self.home, ['claude'], self.root)
            (self.agents_dir() / 'meu-agente.md').write_text('meu', encoding='utf-8')
            hub.uninstall(self.home)
        self.assertEqual(list(self.agents_dir().glob('lay-*.md')), [])
        self.assertTrue((self.agents_dir() / 'meu-agente.md').exists())


class ProjectAgentTests(unittest.TestCase):
    def test_project_agents_have_matching_names_and_existing_skill_paths(self):
        from scripts import build_agents
        import re
        textos = build_agents.subagentes_do_projeto()
        perfis = hub.load_profiles(REPO)
        self.assertEqual(sorted(textos), sorted(p['nome'] + '.md' for p in perfis))
        for nome, texto in textos.items():
            partes = texto.split('---' + chr(10), 2)
            meta = yaml.safe_load(partes[1])
            self.assertEqual(meta['name'] + '.md', nome)
            for caminho in re.findall(r'`(refactored_skills/[^`]+)`', texto):
                self.assertTrue((REPO / caminho).is_file(), caminho)
            self.assertNotIn('skills-privadas', texto)

    def test_project_claude_md_routing_matches_profiles(self):
        claude_md = (REPO / 'CLAUDE.md').read_text(encoding='utf-8')
        for p in hub.load_profiles(REPO):
            self.assertIn(p['dominio'] + ' → `' + p['nome'] + '`', claude_md, p['nome'])

    def test_install_page_lists_every_subagent_and_is_linked_from_catalog(self):
        pagina = (REPO / 'instalacao.html').read_text(encoding='utf-8')
        for p in hub.load_profiles(REPO):
            self.assertIn('<td>' + p['nome'] + '</td>', pagina, p['nome'])
            self.assertIn(p['dominio'], pagina, p['dominio'])
        self.assertIn('install --agents claude', pagina)
        self.assertIn('href="instalacao.html"', (REPO / 'index.html').read_text(encoding='utf-8'))

    def test_readme_and_catalog_page_reference_every_subagent(self):
        for arquivo in ['README.md', 'index.html']:
            texto = (REPO / arquivo).read_text(encoding='utf-8')
            for p in hub.load_profiles(REPO):
                self.assertIn(p['nome'], texto, arquivo + ' ' + p['nome'])
        readme = (REPO / 'README.md').read_text(encoding='utf-8')
        self.assertIn('LAY-Skills-Hub.git', readme)
        self.assertIn('instalacao.html', readme)
        self.assertIn('install --agents claude', readme)


if __name__ == '__main__':
    unittest.main()
