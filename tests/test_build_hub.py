"""Hub gerado: divisão de conteúdo, agentes (gatilhos, cortes, acesso, categoria, configurado), totais e contratos com o site."""
import gzip
import json
import re
import unittest
from pathlib import Path
from unittest import mock

from scripts import build_hub as bh
from scripts import skill_hub

REPO = Path(bh.ROOT)
# Orçamento da carga inicial (data.js, gzip nível 9). Medido após a divisão: 25.237 bytes; antes: 104.881.
ORCAMENTO_DATA_JS_GZIP = 40_000
CAMPOS_AGENTE = {'nome', 'dominio', 'categoria', 'descricao', 'ferramentas', 'use_quando', 'nao_use_para',
                 'nao_use_para_completo', 'resumo', 'acesso', 'skills_ativas', 'skills', 'fontes_upstream',
                 'subagente_em', 'clientes_com_skills', 'configurado'}
ACESSOS = {'Edita e roda comandos', 'Edita, sem comandos', 'Não edita · tem Bash', 'Só leitura'}


def ficha(skill_id, nome, **extra):
    """Skill no formato de data.js, com content e prompt."""
    base = {
        'id': skill_id, 'name': nome, 'source': 'local', 'author': 'LAY® Core Ecosystem',
        'sourceTitle': 'LAY Core Skills', 'sourceUrl': 'https://github.com/x/y', 'sourceAvatar': 'data:x',
        'sourceIcon': '⚡', 'sourceBadge': 'LAY® Native', 'sourceDesc': 'desc', 'categories': ['engenharia'],
        'version': 'refactored', 'commit': 'content-abc', 'description': 'Descrição curta.',
        'prompt': f'Prompt de {nome}', 'content': f'# {nome}\n\nCorpo de {nome}.', 'kind': 'skill',
    }
    base.update(extra)
    return base


def entrada_catalogo(nome, dominio='engineering', **extra):
    """Entrada de catalog/skills.json, como build_catalog grava."""
    base = {'id': 'lay-' + nome, 'name': nome, 'description': 'Descrição.', 'source': 'local',
            'path': f'refactored_skills/{dominio}/{nome}/SKILL.md', 'kind': 'skill',
            'categories': ['engenharia'], 'version': 'refactored', 'commit': 'content-abc',
            'sha256': 'abc', 'url': ''}
    base.update(extra)
    return base


def perfil(nome, dominio, ferramentas=('Read',), descricao=None):
    return {'nome': nome, 'dominio': dominio,
            'descricao': descricao or 'Especialista. Use quando: teste. Não use para: outro.',
            'ferramentas': list(ferramentas)}


def ler_global(texto, nome):
    """Valor JSON de `window.<nome> = ...;` em um arquivo gerado."""
    casa = re.search(rf'^window\.{nome} = (.*?);\r?\n(?=window\.|\Z)', texto, re.S | re.M)
    if casa is None:
        raise AssertionError(f'window.{nome} ausente')
    return json.loads(casa.group(1))


class DividirConteudoTests(unittest.TestCase):
    def test_separa_so_content_e_prompt(self):
        leves, conteudo = bh.dividir_conteudo([ficha('lay-a', 'a')])
        self.assertNotIn('content', leves[0])
        self.assertNotIn('prompt', leves[0])
        self.assertEqual(leves[0]['description'], 'Descrição curta.')
        self.assertEqual(conteudo, {'lay-a': {'content': '# a\n\nCorpo de a.', 'prompt': 'Prompt de a'}})

    def test_mantem_os_campos_que_o_site_usa(self):
        leves, _ = bh.dividir_conteudo([ficha('lay-a', 'a', url='', sha256='x')])
        for campo in ('id', 'name', 'description', 'categories', 'source', 'url', 'version', 'commit', 'sha256', 'kind'):
            self.assertIn(campo, leves[0], campo)

    def test_nao_altera_a_lista_de_origem(self):
        skills = [ficha('lay-a', 'a')]
        copia = json.loads(json.dumps(skills))
        bh.dividir_conteudo(skills)
        self.assertEqual(skills, copia)

    def test_recusa_id_repetido(self):
        with self.assertRaises(ValueError):
            bh.dividir_conteudo([ficha('lay-a', 'a'), ficha('lay-a', 'b')])


class ArquivosDoSiteTests(unittest.TestCase):
    def test_data_js_guarda_campos_leves_e_metadados(self):
        leves, _ = bh.dividir_conteudo([ficha('lay-a', 'a')])
        texto = bh.formatar_data_js(leves, {'local': {'title': 'T'}}, 17)
        self.assertEqual(ler_global(texto, 'LAY_SKILLS'), leves)
        self.assertEqual(ler_global(texto, 'LAY_SOURCES'), {'local': {'title': 'T'}})
        self.assertEqual(ler_global(texto, 'LAY_SOURCES_COUNT'), 17)
        self.assertNotIn('"content"', texto)
        self.assertNotIn('"prompt"', texto)

    def test_conteudo_js_tem_uma_entrada_por_id_e_e_parseavel(self):
        _, conteudo = bh.dividir_conteudo([ficha('lay-a', 'a'), ficha('lay-b', 'b')])
        lido = ler_global(bh.formatar_conteudo_js(conteudo), 'LAY_CONTEUDO')
        self.assertEqual(set(lido), set(conteudo))
        for skill_id, campos in conteudo.items():
            self.assertEqual(lido[skill_id]['content'], bh.linhas_do_conteudo(campos['content']))
            self.assertEqual(lido[skill_id]['prompt'], campos['prompt'])

    def test_conteudo_js_grava_uma_linha_de_markdown_por_linha(self):
        texto = bh.formatar_conteudo_js({'lay-x': {'content': '# Título\n\n```\ncódigo\n```\n', 'prompt': 'p'}})
        linhas = texto.splitlines()
        self.assertIn('      "# Título",', linhas)
        self.assertIn('      "código",', linhas)
        self.assertIn('      "```"', linhas)
        self.assertEqual(ler_global(texto, 'LAY_CONTEUDO')['lay-x']['content'], ['# Título', '', '```', 'código', '```'])

    def test_conteudo_js_vazio_continua_valido(self):
        self.assertEqual(ler_global(bh.formatar_conteudo_js({}), 'LAY_CONTEUDO'), {})

    def test_totais_incluem_subagentes_e_dominios_na_ordem(self):
        valor = ler_global(bh.formatar_totais_js(136, 17, 11, 11), 'LAY_TOTAIS')
        self.assertEqual(valor, {'skills': 136, 'fontes': 17, 'subagentes': 11, 'dominios': 11})
        self.assertEqual(list(valor), ['skills', 'fontes', 'subagentes', 'dominios'])


class FonteEDominioTests(unittest.TestCase):
    def test_fonte_efetiva_prefere_atribuicao_por_nome_e_depois_por_id(self):
        atribuicoes = {'vanta': 'tengbao--vanta', 'lay-b': 'x--y'}
        self.assertEqual(bh.fonte_efetiva({'id': 'lay-a', 'name': 'vanta', 'source': 'local'}, atribuicoes),
                         'tengbao--vanta')
        self.assertEqual(bh.fonte_efetiva({'id': 'lay-b', 'name': 'outra', 'source': 'local'}, atribuicoes), 'x--y')
        self.assertEqual(bh.fonte_efetiva({'id': 'lay-c', 'name': 'outra', 'source': 'local'}, atribuicoes), 'local')

    def test_dominio_vem_do_caminho_publico(self):
        self.assertEqual(bh.dominio_da_skill(entrada_catalogo('a', 'qa')), 'qa')
        with self.assertRaises(ValueError):
            bh.dominio_da_skill({'path': 'upstream/x/SKILL.md'})


class FontesUpstreamTests(unittest.TestCase):
    REGISTRO = [{'id': 'tengbao--vanta', 'url': 'https://github.com/tengbao/vanta.git'}]

    def test_atribuicao_leva_titulo_autor_e_url_sem_git(self):
        saida = bh.fontes_upstream([entrada_catalogo('vanta-x', 'creative-3d')], self.REGISTRO,
                                   bh.SOURCE_METADATA, {'vanta-x': 'tengbao--vanta'})
        self.assertEqual(saida, [{'id': 'tengbao--vanta', 'titulo': 'Vanta.js 3D WebGL Backgrounds',
                                  'autor': 'Tengbao', 'url': 'https://github.com/tengbao/vanta'}])

    def test_sem_atribuicao_a_lista_fica_vazia(self):
        self.assertEqual(bh.fontes_upstream([entrada_catalogo('a')], self.REGISTRO, bh.SOURCE_METADATA, {}), [])

    def test_fonte_fora_do_registro_e_recusada(self):
        with self.assertRaises(ValueError):
            bh.fontes_upstream([entrada_catalogo('vanta-x', 'creative-3d')], [], bh.SOURCE_METADATA,
                               {'vanta-x': 'tengbao--vanta'})

    def test_agente_recebe_so_as_fontes_do_proprio_dominio(self):
        perfis = [perfil('lay-3d', 'creative-3d'), perfil('lay-eng', 'engineering')]
        catalogo = [entrada_catalogo('vanta-x', 'creative-3d'), entrada_catalogo('outra', 'engineering')]
        agentes = bh.construir_agentes(perfis, catalogo, self.REGISTRO, bh.SOURCE_METADATA,
                                       lambda nome: True, {'vanta-x': 'tengbao--vanta'})
        por_nome = {a['nome']: a for a in agentes}
        self.assertEqual([f['id'] for f in por_nome['lay-3d']['fontes_upstream']], ['tengbao--vanta'])
        self.assertEqual(por_nome['lay-eng']['fontes_upstream'], [])


class GatilhosTests(unittest.TestCase):
    def test_separa_use_quando_e_nao_use_para(self):
        self.assertEqual(bh.gatilhos_do_perfil('Especialista. Use quando: revisar código, testes. Não use para: deploy.'),
                         ('revisar código, testes', 'deploy.'))

    def test_use_quando_perde_o_ponto_final_e_nao_use_para_completo_o_mantem(self):
        quando, nao_use = bh.gatilhos_do_perfil('X. Use quando: alfa beta. Não use para: gama delta epsilon.')
        self.assertEqual(quando, 'alfa beta')
        self.assertEqual(nao_use, 'gama delta epsilon.')

    def test_sem_use_quando_vale_a_descricao_inteira(self):
        self.assertEqual(bh.gatilhos_do_perfil('Descrição geral. Não use para: outra coisa.'),
                         ('Descrição geral', 'outra coisa.'))

    def test_sem_nao_use_para_o_segundo_valor_fica_vazio(self):
        self.assertEqual(bh.gatilhos_do_perfil('Use quando: alfa.'), ('alfa', ''))

    def test_espacos_e_quebras_sao_normalizados(self):
        self.assertEqual(bh.gatilhos_do_perfil('Use quando:\n  alfa   beta \n Não use para:  gama'), ('alfa beta', 'gama'))


class CortarPalavrasTests(unittest.TestCase):
    TEXTO_LONGO = ('o pedido envolver revisão de arquitetura depuração de causa raiz migrações de banco de dados '
                   'deprecações de interfaces performance full stack observabilidade restrições de qualidade '
                   'de código entre equipes distintas')
    TEXTO_SEM_LIGACOES = ('revisão arquitetura depuração causa raiz migrações banco dados deprecações interfaces '
                          'performance full stack observabilidade restrições qualidade código equipes distintas')

    def test_texto_que_cabe_volta_igual(self):
        self.assertEqual(bh.cortar_palavras('curto', 100), 'curto')
        exato = 'a' * 50 + ' ' + 'b' * 49  # exatamente 100 caracteres
        self.assertEqual(bh.cortar_palavras(exato, 100), exato)

    def test_corta_na_ultima_palavra_inteira_que_cabe_em_100_e_140(self):
        for limite in (100, 140):
            with self.subTest(limite=limite):
                cortado = bh.cortar_palavras(self.TEXTO_SEM_LIGACOES, limite)
                self.assertLessEqual(len(cortado), limite)
                self.assertTrue(self.TEXTO_SEM_LIGACOES.startswith(cortado + ' '))
                proxima = self.TEXTO_SEM_LIGACOES[len(cortado) + 1:].split(' ')[0]
                self.assertGreater(len(cortado + ' ' + proxima), limite)

    def test_com_ligacoes_no_texto_o_corte_respeita_o_limite_e_nao_termina_em_ligacao(self):
        for limite in (100, 140):
            with self.subTest(limite=limite):
                cortado = bh.cortar_palavras(self.TEXTO_LONGO, limite)
                self.assertLessEqual(len(cortado), limite)
                self.assertTrue(self.TEXTO_LONGO.startswith(cortado + ' '))
                self.assertNotIn(cortado.split(' ')[-1].lower(), bh.LIGACOES_DO_FIM)

    def test_nao_acrescenta_reticencias(self):
        cortado = bh.cortar_palavras(self.TEXTO_LONGO, 100)
        self.assertFalse(cortado.endswith(('…', '...')))

    def test_palavra_que_passa_do_limite_nao_entra(self):
        self.assertEqual(bh.cortar_palavras('abc defghijklmnop q', 10), 'abc')

    def test_pontuacao_que_sobra_no_fim_e_retirada(self):
        self.assertEqual(bh.cortar_palavras('alfa, beta gama', 6), 'alfa')

    def test_espacos_internos_sao_normalizados(self):
        self.assertEqual(bh.cortar_palavras('a   b\n c', 100), 'a b c')

    def test_primeira_palavra_maior_que_o_limite_e_recusada(self):
        with self.assertRaises(ValueError):
            bh.cortar_palavras('x' * 150 + ' fim', 140)

    def test_limites_do_hub(self):
        self.assertEqual((bh.LIMITE_RESUMO, bh.LIMITE_NAO_USE_PARA), (100, 140))

    def test_remove_ligacao_do_fim_depois_do_corte(self):
        self.assertEqual(bh.cortar_palavras('alfa beta de gama', 12), 'alfa beta')

    def test_remove_varias_ligacoes_seguidas_sem_diferenciar_maiusculas_ou_acento(self):
        self.assertEqual(bh.cortar_palavras('alfa beta de O gama', 14), 'alfa beta')
        self.assertEqual(bh.cortar_palavras('alfa beta À gama', 12), 'alfa beta')

    def test_ligacao_no_meio_do_corte_fica(self):
        self.assertEqual(bh.cortar_palavras('alfa de beta gama', 12), 'alfa de beta')

    def test_se_o_corte_ficar_vazio_vale_o_corte_original(self):
        self.assertEqual(bh.cortar_palavras('de a e o xyz', 7), 'de a e')

    def test_texto_que_cabe_nao_perde_ligacao(self):
        self.assertEqual(bh.cortar_palavras('alfa de', 100), 'alfa de')

    def test_tirar_ligacoes_do_fim(self):
        self.assertEqual(bh.tirar_ligacoes_do_fim('varredura de'), 'varredura')
        self.assertEqual(bh.tirar_ligacoes_do_fim('alfa, de'), 'alfa')
        self.assertEqual(bh.tirar_ligacoes_do_fim('alfa de beta'), 'alfa de beta')
        self.assertEqual(bh.tirar_ligacoes_do_fim('de'), '')

    def test_lista_de_ligacoes_do_fim(self):
        esperado = {'de', 'da', 'do', 'das', 'dos', 'em', 'no', 'na', 'nos', 'nas', 'para', 'por', 'com', 'sem',
                    'ou', 'e', 'a', 'o', 'as', 'os', 'que', 'ao', 'aos', 'à', 'às', 'sobre', 'entre'}
        self.assertEqual(set(bh.LIGACOES_DO_FIM), esperado)


class RotuloAcessoTests(unittest.TestCase):
    def test_escrita_com_bash_edita_e_roda_comandos(self):
        for ferramentas in (['Read', 'Edit', 'Bash'], ['Read', 'Write', 'Bash']):
            with self.subTest(ferramentas=ferramentas):
                self.assertEqual(bh.rotulo_acesso(ferramentas), 'Edita e roda comandos')

    def test_escrita_sem_bash_edita_sem_comandos(self):
        for ferramentas in (['Read', 'Edit'], ['Read', 'Write']):
            with self.subTest(ferramentas=ferramentas):
                self.assertEqual(bh.rotulo_acesso(ferramentas), 'Edita, sem comandos')

    def test_bash_sem_escrita_nao_edita(self):
        self.assertEqual(bh.rotulo_acesso(['Read', 'Grep', 'Bash']), 'Não edita · tem Bash')

    def test_sem_escrita_nem_bash_so_leitura(self):
        self.assertEqual(bh.rotulo_acesso(['Read', 'Grep', 'Glob']), 'Só leitura')


class CategoriaTests(unittest.TestCase):
    ESPERADO = {
        'routing-and-proxy': 'OPERAÇÕES & CI/CD', 'devops': 'OPERAÇÕES & CI/CD', 'database': 'OPERAÇÕES & CI/CD',
        'frontend': 'DESIGN & UI/UX', 'creative-3d': 'DESIGN & UI/UX', 'design': 'DESIGN & UI/UX',
        'engineering': 'ENGENHARIA', 'context': 'CONTEXTO & AGENTES', 'qa': 'TESTES & QUALIDADE',
        'security': 'SEGURANÇA & SCAN', 'documentation': 'DOCUMENTAÇÃO',
    }

    def test_categoria_vem_do_filtro_do_site_para_cada_dominio(self):
        for dominio, rotulo in self.ESPERADO.items():
            with self.subTest(dominio):
                self.assertEqual(bh.categoria_do_dominio(dominio), rotulo)

    def test_todo_dominio_de_perfil_tem_categoria(self):
        self.assertEqual(set(bh.CATEGORIA_FILTRO), set(skill_hub.AGENTS_DOMINIOS))
        self.assertEqual(set(bh.ROTULOS_CATEGORIA), set(bh.CATEGORIA_FILTRO.values()))

    def test_rotulos_conferem_com_o_array_de_categorias_de_index_html(self):
        html = (REPO / 'index.html').read_text(encoding='utf-8')
        do_site = dict(re.findall(r"\{ id: '([a-z]+)', label: '([^']+)' \}", html))
        for categoria_id, rotulo in bh.ROTULOS_CATEGORIA.items():
            with self.subTest(categoria_id):
                self.assertEqual(do_site.get(categoria_id), rotulo)

    def test_dominio_sem_categoria_e_recusado(self):
        with self.assertRaises(ValueError):
            bh.construir_agentes([perfil('lay-x', 'dominio-inexistente')], [], [], bh.SOURCE_METADATA, lambda n: True)


class AgentesTests(unittest.TestCase):
    def construir(self, perfis, catalogo, tem=lambda nome: True):
        return bh.construir_agentes(perfis, catalogo, [], bh.SOURCE_METADATA, tem)

    def test_um_objeto_por_perfil_com_os_campos_do_contrato(self):
        perfis = [perfil('lay-engenharia', 'engineering'), perfil('lay-seguranca', 'security', ['Read', 'Grep'])]
        catalogo = [entrada_catalogo('a', 'engineering'), entrada_catalogo('b', 'security')]
        agentes = self.construir(perfis, catalogo)
        self.assertEqual(len(agentes), 2)
        for agente in agentes:
            self.assertEqual(set(agente), CAMPOS_AGENTE)
        self.assertEqual(agentes[0]['nome'], 'lay-engenharia')
        self.assertEqual(agentes[0]['categoria'], 'ENGENHARIA')
        self.assertEqual(agentes[1]['categoria'], 'SEGURANÇA & SCAN')
        self.assertEqual(agentes[1]['ferramentas'], ['Read', 'Grep'])
        self.assertEqual(agentes[1]['acesso'], 'Só leitura')
        self.assertEqual(agentes[0]['subagente_em'], 'Claude Code')

    def test_objetos_em_ordem_alfabetica_pelo_nome(self):
        perfis = [perfil('lay-seguranca', 'security'), perfil('lay-3d', 'creative-3d'), perfil('lay-design', 'design')]
        self.assertEqual([a['nome'] for a in self.construir(perfis, [])], ['lay-3d', 'lay-design', 'lay-seguranca'])

    def test_gatilhos_resumo_e_acesso_vem_do_perfil(self):
        p = perfil('lay-x', 'engineering', ['Read', 'Edit', 'Bash'],
                   descricao='Especialista. Use quando: alfa beta. Não use para: gama delta.')
        agente = self.construir([p], [])[0]
        self.assertEqual(agente['use_quando'], 'alfa beta')
        self.assertEqual(agente['nao_use_para'], 'gama delta.')
        self.assertEqual(agente['nao_use_para_completo'], 'gama delta.')
        self.assertEqual(agente['resumo'], 'alfa beta')
        self.assertEqual(agente['acesso'], 'Edita e roda comandos')

    def test_resumo_e_nao_use_para_cortados_nos_limites(self):
        longo = ' '.join(['palavra'] * 40)
        p = perfil('lay-x', 'engineering', descricao=f'Especialista. Use quando: {longo}. Não use para: {longo}.')
        agente = self.construir([p], [])[0]
        self.assertEqual(agente['resumo'], ' '.join(['palavra'] * 12))  # 95 caracteres
        self.assertEqual(agente['nao_use_para'], ' '.join(['palavra'] * 17))  # 135 caracteres
        self.assertEqual(agente['nao_use_para_completo'], longo + '.')

    def test_nao_use_para_completo_nao_perde_a_ligacao_final(self):
        longo = ' '.join(['palavra'] * 40)
        p = perfil('lay-x', 'engineering', descricao=f'Especialista. Use quando: alfa. Não use para: {longo} de.')
        agente = self.construir([p], [])[0]
        self.assertEqual(agente['nao_use_para'], ' '.join(['palavra'] * 17))  # 135 caracteres, corte sem ligação
        self.assertEqual(agente['nao_use_para_completo'], longo + ' de.')

    def test_resumo_sem_ligacao_final_quando_o_corte_acontece(self):
        quando = ' '.join(['palavra'] * 11) + ' de ' + 'x' * 15
        p = perfil('lay-x', 'engineering', descricao=f'Especialista. Use quando: {quando}. Não use para: y.')
        agente = self.construir([p], [])[0]
        self.assertEqual(agente['resumo'], ' '.join(['palavra'] * 11))

    def test_skills_ativas_contam_so_local_kind_skill_do_dominio(self):
        catalogo = [entrada_catalogo('a', 'engineering'),
                    entrada_catalogo('b', 'engineering', source='private'),
                    entrada_catalogo('c', 'engineering', kind='componente'),
                    entrada_catalogo('d', 'qa')]
        agente = self.construir([perfil('lay-engenharia', 'engineering')], catalogo)[0]
        self.assertEqual(agente['skills_ativas'], 1)
        self.assertEqual(agente['skills'], ['a'])

    def test_skills_em_ordem_alfabetica(self):
        catalogo = [entrada_catalogo('zeta', 'engineering'), entrada_catalogo('alfa', 'engineering')]
        self.assertEqual(self.construir([perfil('lay-engenharia', 'engineering')], catalogo)[0]['skills'],
                         ['alfa', 'zeta'])

    def test_configurado_traz_caminhos_e_so_o_que_o_build_verifica(self):
        perfis = [perfil('lay-a', 'engineering'), perfil('lay-b', 'qa')]
        agentes = self.construir(perfis, [], tem=lambda nome: nome == 'lay-a')
        self.assertEqual([a['configurado'] for a in agentes], [
            {'projeto': True, 'projeto_caminho': '.claude/agents/lay-a.md', 'global_caminho': '~/.claude/agents/lay-a.md'},
            {'projeto': False, 'projeto_caminho': '.claude/agents/lay-b.md', 'global_caminho': '~/.claude/agents/lay-b.md'},
        ])

    def test_clientes_com_skills_vem_do_instalador(self):
        agente = self.construir([perfil('lay-a', 'engineering')], [])[0]
        self.assertEqual(agente['clientes_com_skills'], ['Claude Code', 'Codex', 'Antigravity'])
        self.assertEqual({cliente for cliente, _ in bh.CLIENTES_COM_SKILLS}, set(skill_hub.DESTINATIONS))

    def test_cliente_fora_do_instalador_e_recusado(self):
        with mock.patch.object(bh, 'CLIENTES_COM_SKILLS', [('claude', 'Claude Code')]):
            with self.assertRaises(ValueError):
                self.construir([perfil('lay-a', 'engineering')], [])

    def test_formatar_agentes_js_e_lista_parseavel(self):
        agentes = self.construir([perfil('lay-a', 'engineering')], [entrada_catalogo('a', 'engineering')])
        texto = bh.formatar_agentes_js(agentes)
        self.assertEqual(ler_global(texto, 'LAY_AGENTES'), agentes)


class PerfisTests(unittest.TestCase):
    """Confere os perfis reais do repositório com os gatilhos e o acesso que o hub publica."""
    ACESSO_ESPERADO = {
        'lay-omniroute': 'Edita e roda comandos', 'lay-frontend': 'Edita e roda comandos',
        'lay-engenharia': 'Edita e roda comandos', 'lay-contexto': 'Edita e roda comandos',
        'lay-devops': 'Edita e roda comandos', 'lay-qa': 'Edita e roda comandos',
        'lay-seguranca': 'Não edita · tem Bash', 'lay-3d': 'Edita e roda comandos',
        'lay-documentacao': 'Edita, sem comandos', 'lay-design': 'Edita, sem comandos',
        'lay-banco-de-dados': 'Edita e roda comandos',
    }

    def test_todos_os_perfis_tem_use_quando_e_nao_use_para(self):
        perfis = skill_hub.load_profiles(REPO)
        self.assertEqual(len(perfis), 11)
        for p in perfis:
            with self.subTest(p['nome']):
                self.assertIn(bh.MARCA_USE_QUANDO, p['descricao'])
                self.assertIn(bh.MARCA_NAO_USE_PARA, p['descricao'])
                quando, nao_use = bh.gatilhos_do_perfil(p['descricao'])
                self.assertTrue(quando)
                self.assertTrue(nao_use)

    def test_acesso_de_cada_perfil_real(self):
        for p in skill_hub.load_profiles(REPO):
            with self.subTest(p['nome']):
                self.assertEqual(bh.rotulo_acesso(p['ferramentas']), self.ACESSO_ESPERADO[p['nome']])


class RegistroTests(unittest.TestCase):
    def test_registro_e_metadados_descrevem_as_mesmas_fontes(self):
        registro = json.loads((REPO / 'registry/sources.json').read_text(encoding='utf-8'))['sources']
        self.assertEqual({fonte['id'] for fonte in registro}, set(bh.SOURCE_METADATA) - {'local'})
        for fonte in registro:
            url = fonte['url'].removesuffix('.git')
            # GitHub não diferencia maiúsculas no nome do repositório
            self.assertEqual(url.lower(), bh.SOURCE_METADATA[fonte['id']]['url'].lower(), fonte['id'])


class ChaveDeOrdemTests(unittest.TestCase):
    def test_origem_local_vem_antes_de_origem_externa(self):
        self.assertLess(bh.chave_de_ordem({'categories': ['zzz'], 'name': 'a'}, 'local'),
                        bh.chave_de_ordem({'categories': ['aaa'], 'name': 'a'}, 'externa'))

    def test_depois_vem_categoria_e_nome(self):
        self.assertLess(bh.chave_de_ordem({'categories': ['contexto'], 'name': 'z'}, 'local'),
                        bh.chave_de_ordem({'categories': ['design'], 'name': 'a'}, 'local'))
        self.assertLess(bh.chave_de_ordem({'categories': ['design'], 'name': 'a'}, 'local'),
                        bh.chave_de_ordem({'categories': ['design'], 'name': 'b'}, 'local'))

    def test_fonte_efetiva_nao_tira_a_skill_do_bloco_lay(self):
        skills = [
            {'id': 'lay-x', 'name': 'x', 'categories': ['contexto'], 'source': 'tengbao--vanta'},
            {'id': 'lay-a', 'name': 'a', 'categories': ['design'], 'source': 'local'},
        ]
        origem = {'lay-x': 'local', 'lay-a': 'local'}
        ordenadas = sorted(skills, key=lambda s: bh.chave_de_ordem(s, origem[s['id']]))
        self.assertEqual([s['name'] for s in ordenadas], ['x', 'a'])


class HubPublicadoTests(unittest.TestCase):
    """Arquivos gerados em hub/ batem com o catálogo, os perfis e o site."""

    @classmethod
    def setUpClass(cls):
        cls.catalogo = json.loads((REPO / 'catalog/skills.json').read_text(encoding='utf-8'))['skills']
        cls.registro = json.loads((REPO / 'registry/sources.json').read_text(encoding='utf-8'))['sources']
        cls.perfis = skill_hub.load_profiles(REPO)
        cls.data = (REPO / 'hub/data.js').read_text(encoding='utf-8')
        cls.conteudo = (REPO / 'hub/conteudo.js').read_text(encoding='utf-8')
        cls.agentes = (REPO / 'hub/agentes.js').read_text(encoding='utf-8')
        cls.totais = (REPO / 'hub/totais.js').read_text(encoding='utf-8')
        cls.descricoes = {p['nome']: p['descricao'] for p in cls.perfis}

    def test_data_js_tem_todas_as_skills_sem_conteudo_pesado(self):
        skills = ler_global(self.data, 'LAY_SKILLS')
        self.assertEqual(len(skills), len(self.catalogo))
        self.assertFalse(any('content' in skill or 'prompt' in skill for skill in skills))

    def test_conteudo_js_tem_content_e_prompt_para_cada_skill(self):
        ids = {skill['id'] for skill in ler_global(self.data, 'LAY_SKILLS')}
        conteudo = ler_global(self.conteudo, 'LAY_CONTEUDO')
        self.assertEqual(set(conteudo), ids)
        for skill_id, campos in conteudo.items():
            self.assertTrue('\n'.join(campos['content']).strip(), skill_id)
            self.assertTrue(campos['prompt'].strip(), skill_id)

    def test_agentes_js_tem_um_objeto_por_especialista(self):
        agentes = ler_global(self.agentes, 'LAY_AGENTES')
        self.assertEqual(len(agentes), len(self.perfis))
        self.assertEqual(sum(agente['skills_ativas'] for agente in agentes), len(self.catalogo))

    def test_agentes_js_em_ordem_com_os_campos_do_site(self):
        agentes = ler_global(self.agentes, 'LAY_AGENTES')
        nomes = [a['nome'] for a in agentes]
        self.assertEqual(nomes, sorted(nomes))
        for a in agentes:
            with self.subTest(a['nome']):
                self.assertEqual(set(a), CAMPOS_AGENTE)
                self.assertLessEqual(len(a['resumo']), bh.LIMITE_RESUMO)
                self.assertLessEqual(len(a['nao_use_para']), bh.LIMITE_NAO_USE_PARA)
                self.assertIn(a['acesso'], ACESSOS)
                quando, _ = bh.gatilhos_do_perfil(self.descricoes[a['nome']])
                if len(quando) > bh.LIMITE_RESUMO:
                    ultima = a['resumo'].split(' ')[-1].rstrip(',;:.!?').lower()
                    self.assertNotIn(ultima, bh.LIGACOES_DO_FIM)
                self.assertEqual(a['categoria'], bh.categoria_do_dominio(a['dominio']))
                self.assertEqual(a['skills'], sorted(a['skills']))
                self.assertEqual(set(a['configurado']), {'projeto', 'projeto_caminho', 'global_caminho'})
                self.assertEqual(a['configurado']['projeto_caminho'], f".claude/agents/{a['nome']}.md")
                self.assertEqual(a['configurado']['global_caminho'], f"~/.claude/agents/{a['nome']}.md")

    def test_atribuicoes_upstream_apontam_para_skills_e_fontes_existentes(self):
        # Guarda contra tabela obsoleta: cada skill atribuída precisa existir no catálogo.
        nomes = {item['name'] for item in self.catalogo}
        self.assertEqual(set(bh.LOCAL_ATTRIBUTIONS) - nomes, set())
        self.assertLessEqual(set(bh.LOCAL_ATTRIBUTIONS.values()), set(bh.SOURCE_METADATA))

    def test_data_js_segue_a_ordem_do_hub(self):
        origem_por_id = {item['id']: item['source'] for item in self.catalogo}
        skills = ler_global(self.data, 'LAY_SKILLS')
        chaves = [bh.chave_de_ordem(skill, origem_por_id[skill['id']]) for skill in skills]
        self.assertEqual(chaves, sorted(chaves))

    def test_atribuicoes_upstream_continuam_com_origem_local_no_catalogo(self):
        origem_por_nome = {item['name']: item['source'] for item in self.catalogo}
        for nome in bh.LOCAL_ATTRIBUTIONS:
            with self.subTest(nome):
                self.assertEqual(origem_por_nome[nome], 'local')

    def test_totais_js_publica_as_contagens_reais(self):
        self.assertEqual(ler_global(self.totais, 'LAY_TOTAIS'), {
            'skills': len(self.catalogo),
            'fontes': len(self.registro),
            'subagentes': len(self.perfis),
            'dominios': len({bh.dominio_da_skill(item) for item in self.catalogo}),
        })

    def test_carga_inicial_do_hub_fica_no_orcamento(self):
        bruto = (REPO / 'hub/data.js').read_bytes()
        self.assertLessEqual(len(gzip.compress(bruto, compresslevel=9)), ORCAMENTO_DATA_JS_GZIP)


if __name__ == '__main__':
    unittest.main()
