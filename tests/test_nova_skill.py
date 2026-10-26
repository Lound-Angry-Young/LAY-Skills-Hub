"""Adição de skills: padrão, tudo ou nada, roteadores e preservação de quebra de linha."""
import json
import tempfile
import unittest
from pathlib import Path

from scripts import nova_skill as ns

ROUTER = (
    '---\n'
    'name: routing-frontend-skills\n'
    'description: >\n'
    '  Routes frontend requests. Use this skill when: choosing a frontend skill. Do NOT use this skill when: backend work.\n'
    '---\n\n'
    '## Domain Skills Catalog\n'
    '| Skill | Finalidade Primária | Link Direto |\n'
    '|---|---|---|\n'
    '| [auditing-existing-layouts](./auditing-existing-layouts/SKILL.md) | Audits layouts | `./auditing-existing-layouts/SKILL.md` |\n'
)
REFERENCE = (
    '# Referência\n\n'
    '## Table of Contents\n1. [Catálogo](#catálogo)\n\n'
    '## Catálogo\n'
    '| [auditing-existing-layouts](./auditing-existing-layouts/SKILL.md) | Audits layouts | `[./auditing-existing-layouts/SKILL.md](./auditing-existing-layouts/SKILL.md)` |\n'
)
EXISTENTE = (
    '---\n'
    'name: auditing-existing-layouts\n'
    'description: >\n'
    '  Audits existing layouts. Use this skill when: reviewing a layout. Do NOT use this skill when: writing new code.\n'
    '---\n\n'
    'Corpo real da skill existente.\n'
)
CORPO = '# Criando layouts\n\n## Imperative Execution Workflow\n1. Lê o briefing.\n2. Monta a grade.\n'
DESCRICAO = 'Creates responsive layouts. Use this skill when: building a new page grid. Do NOT use this skill when: auditing existing code.'


class NovaSkillTests(unittest.TestCase):
    def setUp(self):
        tmp = tempfile.TemporaryDirectory(ignore_cleanup_errors=True)
        self.addCleanup(tmp.cleanup)
        self.raiz = Path(tmp.name) / 'refactored'
        pasta = self.raiz / 'frontend' / 'auditing-existing-layouts'
        pasta.mkdir(parents=True)
        (pasta / 'SKILL.md').write_text(EXISTENTE, encoding='utf-8', newline='\n')
        (self.raiz / 'frontend' / 'SKILL.md').write_text(ROUTER, encoding='utf-8', newline='\n')
        (self.raiz / 'frontend' / 'reference.md').write_text(REFERENCE, encoding='utf-8', newline='\n')
        self.origem = Path(tmp.name) / 'lote'

    def test_nova_skill_entra_no_padrao_e_nos_roteadores(self):
        texto = ns.montar_skill_md('creating-responsive-layouts', DESCRICAO, CORPO)
        erros, _, alterados = ns.aplicar(self.raiz, [('frontend', 'creating-responsive-layouts', texto, None)], privado=True)
        self.assertEqual(erros, [])
        self.assertTrue((self.raiz / 'frontend/creating-responsive-layouts/SKILL.md').exists())
        self.assertIn('frontend/SKILL.md', alterados)
        self.assertIn('[creating-responsive-layouts](./creating-responsive-layouts/SKILL.md)', (self.raiz / 'frontend/SKILL.md').read_text(encoding='utf-8'))
        self.assertIn('[creating-responsive-layouts](./creating-responsive-layouts/SKILL.md)', (self.raiz / 'frontend/reference.md').read_text(encoding='utf-8'))

    def test_rascunho_com_marcador_nao_e_gravado(self):
        texto = ns.montar_skill_md('creating-responsive-layouts', DESCRICAO, ns.corpo_rascunho('creating-responsive-layouts'))
        erros, _, _ = ns.aplicar(self.raiz, [('frontend', 'creating-responsive-layouts', texto, None)], privado=True)
        self.assertTrue(any('PREENCHER' in e for e in erros), erros)
        self.assertFalse((self.raiz / 'frontend/creating-responsive-layouts').exists())
        self.assertNotIn('creating-responsive-layouts', (self.raiz / 'frontend/SKILL.md').read_text(encoding='utf-8'))

    def test_nome_sem_gerundio_ou_fora_do_padrao_e_recusado(self):
        self.assertTrue(ns.erros_de_nome('layout-audit'))
        self.assertTrue(ns.erros_de_nome('../escapar'))
        self.assertTrue(ns.erros_de_nome('-auditing-layout'))
        self.assertEqual(ns.erros_de_nome('auditing-layout'), [])
        self.assertEqual(ns.erros_de_nome('engineering-frontend-interfaces'), [])

    def test_descricao_sem_gatilhos_e_recusada(self):
        erros = ns.erros_de_descricao('Faz algo qualquer.')
        self.assertEqual(len(erros), 2)
        self.assertEqual(ns.erros_de_descricao(DESCRICAO), [])

    def test_lote_com_um_erro_nao_grava_nada(self):
        bom = self.origem / 'frontend' / 'creating-responsive-layouts'
        ruim = self.origem / 'frontend' / 'auditing-broken-layouts'
        bom.mkdir(parents=True)
        ruim.mkdir(parents=True)
        (bom / 'SKILL.md').write_text(ns.montar_skill_md('creating-responsive-layouts', DESCRICAO, CORPO), encoding='utf-8')
        (ruim / 'SKILL.md').write_text('---\nname: auditing-broken-layouts\ndescription: >\n  Sem gatilhos.\n---\nCorpo.\n', encoding='utf-8')
        erros, _, _ = ns.aplicar(self.raiz, ns.pacotes_do_lote(self.origem), privado=True)
        self.assertTrue(erros)
        self.assertFalse((self.raiz / 'frontend/creating-responsive-layouts').exists())
        self.assertFalse((self.raiz / 'frontend/auditing-broken-layouts').exists())

    def test_lote_valido_grava_todas_e_copia_reference(self):
        bom = self.origem / 'frontend' / 'creating-responsive-layouts'
        bom.mkdir(parents=True)
        (bom / 'SKILL.md').write_text(ns.montar_skill_md('creating-responsive-layouts', DESCRICAO, CORPO + '\nVeja [referência](reference.md).\n'), encoding='utf-8')
        (bom / 'reference.md').write_text('## Table of Contents\n\nTemplate longo.\n', encoding='utf-8')
        # reference.md no lote precisa ser apontado pelo SKILL.md (regra do validador)
        erros, _, alterados = ns.aplicar(self.raiz, ns.pacotes_do_lote(self.origem), privado=True)
        self.assertEqual(erros, [])
        self.assertTrue((self.raiz / 'frontend/creating-responsive-layouts/reference.md').exists())
        self.assertIn('frontend/creating-responsive-layouts', alterados)

    def test_dominio_inexistente_e_recusado(self):
        texto = ns.montar_skill_md('creating-responsive-layouts', DESCRICAO, CORPO)
        erros, _, _ = ns.aplicar(self.raiz, [('backend', 'creating-responsive-layouts', texto, None)], privado=True)
        self.assertTrue(any("'backend'" in e for e in erros))

    def test_skill_existente_nao_e_sobrescrita(self):
        texto = ns.montar_skill_md('auditing-existing-layouts', DESCRICAO, CORPO)
        erros, _, _ = ns.aplicar(self.raiz, [('frontend', 'auditing-existing-layouts', texto, None)], privado=True)
        self.assertTrue(any('já existe' in e for e in erros))
        self.assertIn('Corpo real da skill existente.', (self.raiz / 'frontend/auditing-existing-layouts/SKILL.md').read_text(encoding='utf-8'))

    def test_roteador_com_crlf_mantem_quebras_de_linha(self):
        (self.raiz / 'frontend' / 'SKILL.md').write_bytes(ROUTER.replace('\n', '\r\n').encode('utf-8'))
        texto = ns.montar_skill_md('creating-responsive-layouts', DESCRICAO, CORPO)
        erros, _, _ = ns.aplicar(self.raiz, [('frontend', 'creating-responsive-layouts', texto, None)], privado=True)
        self.assertEqual(erros, [])
        bruto = (self.raiz / 'frontend/SKILL.md').read_bytes()
        self.assertEqual(bruto.count(b'\n'), bruto.count(b'\r\n'))


class IntegracaoSiteTests(unittest.TestCase):
    """Guia, README e páginas do site apontam para o fluxo e para a contagem de estrelas."""

    def test_guia_e_comandos_estao_documentados(self):
        repo = Path(ns.REPO)
        guia = (repo / 'docs/ADICIONAR_SKILLS.md').read_text(encoding='utf-8')
        for trecho in ('nova_skill.py nova', 'nova_skill.py lote', 'nova_skill.py regenerar', 'Criar um domínio novo'):
            self.assertIn(trecho, guia, trecho)
        self.assertIn('docs/ADICIONAR_SKILLS.md', (repo / 'README.md').read_text(encoding='utf-8'))
        self.assertIn('ADICIONAR_SKILLS.md', (repo / 'AGENTS.md').read_text(encoding='utf-8'))

    def test_paginas_consultam_estrelas_do_repositorio(self):
        repo = Path(ns.REPO)
        api = 'https://api.github.com/repos/Lound-Angry-Young/LAY-Skills-Hub'
        for pagina in ('index.html', 'instalacao.html'):
            texto = (repo / pagina).read_text(encoding='utf-8')
            self.assertIn(api, texto, pagina)
            self.assertIn('data-gh-stars', texto, pagina)

    def test_build_hub_publica_contagem_de_fontes(self):
        dados = (Path(ns.REPO) / 'hub/data.js').read_text(encoding='utf-8')
        registro = json.loads((Path(ns.REPO) / 'registry/sources.json').read_text(encoding='utf-8'))['sources']
        self.assertIn(f'window.LAY_SOURCES_COUNT = {len(registro)};', dados)


if __name__ == '__main__':
    unittest.main()
