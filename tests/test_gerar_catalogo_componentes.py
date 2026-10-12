import importlib.util
import tempfile
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
_spec = importlib.util.spec_from_file_location(
    'gerar_catalogo_componentes', REPO / 'scripts' / 'gerar_catalogo_componentes.py')
g = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(g)


def arquivo(caminho, conteudo):
    return {'path': caminho, 'content': conteudo}


class TierTest(unittest.TestCase):
    def test_css_sem_biblioteca_e_tier_1(self):
        self.assertEqual(g.tier_de([], 'export const x = 1'), 1)

    def test_biblioteca_de_animacao_e_tier_2(self):
        self.assertEqual(g.tier_de(['gsap'], ''), 2)
        self.assertEqual(g.tier_de(['@gsap/react', 'framer-motion'], ''), 2)

    def test_canvas_2d_e_tier_2(self):
        self.assertEqual(g.tier_de([], 'const c = el.getContext("2d")'), 2)

    def test_three_por_dependencia_ou_import_e_tier_3(self):
        self.assertEqual(g.tier_de(['three'], ''), 3)
        self.assertEqual(g.tier_de(['@react-three/fiber'], ''), 3)
        self.assertEqual(g.tier_de([], 'import X from "./image-shader-canvas"'), 3)


class ImportacoesTest(unittest.TestCase):
    def test_import_local_sem_arquivo_aparece_como_faltante(self):
        arquivos = [arquivo('registry/new-york/shaders/img-glitch.tsx',
                            'import ImageShaderCanvas from "./image-shader-canvas";')]
        self.assertEqual(g.importacoes_faltando(arquivos), ['./image-shader-canvas'])

    def test_import_do_proprio_arquivo_nao_e_faltante(self):
        arquivos = [
            arquivo('registry/new-york/x/principal.tsx', 'import A from "./auxiliar";'),
            arquivo('registry/new-york/x/auxiliar.ts', 'export {}'),
        ]
        self.assertEqual(g.importacoes_faltando(arquivos), [])

    def test_utils_do_shadcn_nao_conta_como_faltante(self):
        arquivos = [arquivo('components/x.tsx', 'import { cn } from "@/lib/utils";')]
        self.assertEqual(g.importacoes_faltando(arquivos), [])

    def test_faltante_resolve_para_item_do_mesmo_registro(self):
        self.assertEqual(g.resolver_importacao('./image-shader-canvas', {'image-shader-canvas'}),
                         'instalar `image-shader-canvas`')

    def test_shadcn_padrao_e_manual_quando_nao_existe(self):
        self.assertEqual(g.resolver_importacao('@/components/ui/button', set()), 'shadcn: `button`')
        self.assertEqual(g.resolver_importacao('@/components/ui/message-scroller', set()),
                         'manual: não encontrado no registro')


class ClienteTest(unittest.TestCase):
    def test_diretiva_no_arquivo_principal_e_sim(self):
        arquivos = [arquivo('a.tsx', '"use client";\nexport default function A() { useState(); }')]
        self.assertEqual(g.cliente_de(arquivos), 'sim')

    def test_hook_sem_diretiva_e_verificar(self):
        arquivos = [arquivo('a.tsx', 'export default function A() { const [x] = useState(0); }')]
        self.assertEqual(g.cliente_de(arquivos), 'verificar')

    def test_sem_hook_nao_precisa(self):
        arquivos = [arquivo('a.tsx', 'export const A = () => null;')]
        self.assertEqual(g.cliente_de(arquivos), 'não precisa')


class FlagsTest(unittest.TestCase):
    def test_movimento_reduzido_detectado(self):
        self.assertTrue(g.REDUZIDO.search('matchMedia("(prefers-reduced-motion: reduce)")'))
        self.assertTrue(g.REDUZIDO.search('const r = useReducedMotion();'))
        self.assertFalse(g.REDUZIDO.search('gsap.to(x, { x: 10 })'))

    def test_toque_so_quando_ha_ponteiro(self):
        dados = {'files': [arquivo('a.tsx', 'el.addEventListener("mousemove", f);')],
                 'dependencies': []}
        item = g.montar_item('componentry', 'a', dados, {'a'})
        self.assertEqual(item['toque'], 'não')
        dados['files'][0]['content'] += ' if (matchMedia("(hover: none)").matches) {}'
        self.assertEqual(g.montar_item('componentry', 'a', dados, {'a'})['toque'], 'sim')

    def test_lil_gui_e_marcado_como_depuracao(self):
        dados = {'files': [arquivo('a.ts', 'export {}')], 'dependencies': ['lil-gui', 'three']}
        self.assertEqual(g.montar_item('pixel-perfect', 'a', dados, {'a'})['depuracao'], 'lil-gui')


class DominioTest(unittest.TestCase):
    def test_img_de_filtro_e_efeito_de_imagem(self):
        self.assertEqual(g.dominio_de('pixel-perfect', 'img-glitch', 'shaders'), 'efeitos-de-imagem')

    def test_img_de_transicao_e_revelacao(self):
        self.assertEqual(g.dominio_de('pixel-perfect', 'img-blinds-transition', 'shaders'), 'revelacao-de-imagem')

    def test_auxiliar_e_base_tecnica(self):
        self.assertEqual(g.dominio_de('pixel-perfect', 'shader-canvas', 'shaders'), 'base-tecnica')

    def test_componentry_usa_tabela_explicita(self):
        self.assertEqual(g.dominio_de('componentry', 'magnetic-dock', ''), 'navegacao-e-chat')


class FechamentoTest(unittest.TestCase):
    def test_cadeia_de_importacoes_na_ordem_de_instalacao(self):
        por_nome = {
            'a': {'faltam': [('./b', 'instalar `b`')]},
            'b': {'faltam': [('./c', 'instalar `c`')]},
            'c': {'faltam': []},
        }
        self.assertEqual(g.fechamento('a', por_nome), ['c', 'b'])

    def test_ciclo_nao_repete_nem_inclui_o_proprio_item(self):
        por_nome = {
            'a': {'faltam': [('./b', 'instalar `b`')]},
            'b': {'faltam': [('./a', 'instalar `a`')]},
        }
        self.assertEqual(g.fechamento('a', por_nome), ['b'])

    def test_plano_separa_item_do_registro_de_shadcn_e_manual(self):
        por_nome = {
            'a': {'faltam': [('./b', 'instalar `b`'),
                             ('@/components/ui/button', 'shadcn: `button`'),
                             ('@/x/y', 'manual: não encontrado no registro')]},
            'b': {'faltam': []},
        }
        item = {'nome': 'a', 'instalar': g.fechamento('a', por_nome), 'alcance': set()}
        self.assertEqual(
            g.plano_de(item, por_nome),
            'instalar à mão, nesta ordem: `b`; shadcn: `button` (`@/components/ui/button`); '
            'manual: não encontrado no registro (`@/x/y`)')

    def test_cadeia_que_o_cli_traz_nao_vai_para_instalacao_manual(self):
        por_nome = {
            'a': {'faltam': [('./b', 'instalar `b`')], 'registry_deps': ['b'], 'nome': 'a'},
            'b': {'faltam': [], 'registry_deps': []},
        }
        item = {'nome': 'a', 'instalar': g.fechamento('a', por_nome), 'alcance': g.alcance_do_cli('a', por_nome)}
        self.assertEqual(g.plano_de(item, por_nome), 'o CLI traz a cadeia (registryDependencies)')


class AlcanceTest(unittest.TestCase):
    def test_alcance_segue_registryDependencies_em_cadeia(self):
        por_nome = {
            'a': {'registry_deps': ['b']},
            'b': {'registry_deps': ['c']},
            'c': {'registry_deps': []},
        }
        self.assertEqual(g.alcance_do_cli('a', por_nome), {'b', 'c'})

    def test_dependencia_fora_do_registro_nao_entra(self):
        por_nome = {'a': {'registry_deps': ['externo']}}
        self.assertEqual(g.alcance_do_cli('a', por_nome), set())


class LeituraTest(unittest.TestCase):
    def test_leitura_local_ignora_indice_e_le_so_itens(self):
        with tempfile.TemporaryDirectory() as tmp:
            pasta = Path(tmp) / 'public' / 'r'
            pasta.mkdir(parents=True)
            (pasta / 'registry.json').write_text('{"items": []}', encoding='utf-8')
            (pasta / 'botao.json').write_text('{"name": "botao", "files": []}', encoding='utf-8')
            self.assertEqual(list(g.ler_local('pixel-perfect', tmp)), ['botao'])


class SaidaTest(unittest.TestCase):
    def test_reference_comeca_com_table_of_contents(self):
        """O validador de skills exige que reference.md comece com '## Table of Contents'."""
        dados = {'files': [arquivo('registry/new-york/text/t.tsx', 'export const T = () => null;')],
                 'dependencies': ['gsap'], 'description': 'Texto de teste.'}
        item = g.montar_item('pixel-perfect', 't', dados, {'t'})
        with tempfile.TemporaryDirectory() as tmp:
            saida = Path(tmp) / 'reference.md'
            g.escrever([item], {'pixel-perfect': 'teste', 'componentry': 'teste'}, saida)
            texto = saida.read_text(encoding='utf-8')
        self.assertTrue(texto.startswith('## Table of Contents\n'))
        self.assertIn('`t`', texto)


if __name__ == '__main__':
    unittest.main()
