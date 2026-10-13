"""Renderizador de markdown do modal de skill (index.html). Roda o código do próprio site no Node."""
import json
import re
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
NODE = shutil.which('node')


def funcoes_do_modal():
    """Código de escape e de markdown copiado de index.html, sem alteração."""
    html = (REPO / 'index.html').read_text(encoding='utf-8')
    escape = re.search(r"    function esc\(valor\) \{.*?\n    \}\n", html, re.S).group(0)
    inicio = html.index('    // Markdown do modal, por blocos')
    fim = html.index('    // =========================================================================\n    // MODAIS')
    return escape + '\n' + html[inicio:fim]


@unittest.skipUnless(NODE, 'node não está instalado')
class MarkdownDoModalTests(unittest.TestCase):
    def renderizar(self, md):
        script = funcoes_do_modal() + '\nconsole.log(JSON.stringify(markdownParaHtml(' + json.dumps(md) + ')));\n'
        with tempfile.TemporaryDirectory() as pasta:
            caminho = Path(pasta) / 'markdown.js'
            caminho.write_text(script, encoding='utf-8')
            saida = subprocess.run([NODE, str(caminho)], capture_output=True, text=True, check=True)
        return json.loads(saida.stdout)

    def test_titulos_viram_h3_h4_e_h5(self):
        html = self.renderizar('# A\n\n## B\n\n### C\n\n#### D')
        self.assertIn('<h3>A</h3>', html)
        self.assertIn('<h3>B</h3>', html)
        self.assertIn('<h4>C</h4>', html)
        self.assertIn('<h5>D</h5>', html)

    def test_lista_aninhada_fica_dentro_do_item(self):
        html = self.renderizar('- um\n  - dois\n- tres')
        self.assertEqual(html, '<ul><li>um<ul><li>dois</li></ul></li><li>tres</li></ul>')

    def test_lista_numerada_vira_ol(self):
        self.assertEqual(self.renderizar('1. primeiro\n2. segundo'), '<ol><li>primeiro</li><li>segundo</li></ol>')

    def test_codigo_nao_recebe_marcacao_e_e_escapado(self):
        html = self.renderizar('```\n# comentario\n**nao** <b>x</b>\n```')
        self.assertEqual(html, '<pre><code># comentario\n**nao** &lt;b&gt;x&lt;/b&gt;</code></pre>')

    def test_tabela_com_cabecalho_e_linhas(self):
        html = self.renderizar('| Nome | Valor |\n| --- | --- |\n| a | `b` |')
        self.assertIn('<thead><tr><th>Nome</th><th>Valor</th></tr></thead>', html)
        self.assertIn('<tbody><tr><td>a</td><td><code>b</code></td></tr></tbody>', html)

    def test_links_so_aceitam_http_e_https(self):
        html = self.renderizar('[ok](https://exemplo.com) e [nao](javascript:alert(1))')
        self.assertIn('<a href="https://exemplo.com" target="_blank" rel="noopener noreferrer">ok</a>', html)
        self.assertNotIn('<a href="javascript', html)
        self.assertIn('[nao](javascript:alert(1))', html)

    def test_html_cru_do_texto_e_escapado(self):
        html = self.renderizar('<script>x</script>')
        self.assertIn('&lt;script&gt;x&lt;/script&gt;', html)
        self.assertNotIn('<script>', html)

    def test_negrito_e_italico_no_paragrafo(self):
        self.assertEqual(self.renderizar('Um **forte** e *leve* texto.'),
                         '<p>Um <strong>forte</strong> e <em>leve</em> texto.</p>')

    def test_conteudo_em_lista_de_linhas_e_aceito(self):
        html = self.renderizar(['# T', '', 'corpo'])
        self.assertIn('<h3>T</h3>', html)
        self.assertIn('<p>corpo</p>', html)


if __name__ == '__main__':
    unittest.main()
