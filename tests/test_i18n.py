"""Testes de internacionalização (i18n) e LanguageSelector do LAY Skills Hub."""
import json
import re
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]


class I18nIntegrationTests(unittest.TestCase):
    def test_hub_i18n_js_exists_and_has_valid_locales(self):
        js_file = REPO / "hub/i18n.js"
        self.assertTrue(js_file.is_file(), "hub/i18n.js deve existir")
        conteudo = js_file.read_text(encoding="utf-8")
        self.assertIn("lay:locale", conteudo, "Deve usar a chave 'lay:locale' compatível com Portifolio-LAY")
        self.assertIn("'pt-BR':", conteudo, "Deve suportar pt-BR")
        self.assertIn("'en':", conteudo, "Deve suportar en")
        self.assertIn("LAY_I18N", conteudo, "Deve expor LAY_I18N globalmente")

    def test_pages_include_i18n_script(self):
        for pagina in ("index.html", "instalacao.html"):
            html = (REPO / pagina).read_text(encoding="utf-8")
            self.assertIn('src="hub/i18n.js"', html, f"{pagina} deve incluir o script hub/i18n.js")

    def test_pages_have_language_selector_markup(self):
        for pagina in ("index.html", "instalacao.html"):
            html = (REPO / pagina).read_text(encoding="utf-8")
            self.assertIn('id="lang-wrap"', html, f"{pagina} deve conter o wrapper do seletor #lang-wrap")
            self.assertIn('id="lang-btn"', html, f"{pagina} deve conter o botão do globo #lang-btn")
            self.assertIn('id="lang-popover"', html, f"{pagina} deve conter o popover #lang-popover")
            self.assertIn('data-lang="pt-BR"', html, f"{pagina} deve conter opção pt-BR com bandeira do Brasil")
            self.assertIn('data-lang="en"', html, f"{pagina} deve conter opção en com bandeira dos EUA")

    def test_flags_svg_present(self):
        # Verifica elementos gráficos específicos das bandeiras (polígono amarelo do Brasil, listras e cantão azul dos EUA)
        html = (REPO / "index.html").read_text(encoding="utf-8")
        self.assertIn('fill="#009739"', html, "Bandeira do Brasil com verde característico")
        self.assertIn('fill="#FFF201"', html, "Bandeira do Brasil com amarelo característico")
        self.assertIn('fill="#002868"', html, "Bandeira dos EUA com azul marinho característico")
        self.assertIn('fill="#C21818"', html, "Bandeira dos EUA com faixas vermelhas características")

    def test_popover_z_index_above_content(self):
        for pagina in ("index.html", "instalacao.html"):
            html = (REPO / pagina).read_text(encoding="utf-8")
            self.assertIn("z-index: 200;", html, f"{pagina} deve ter cabecalho com z-index 200 para ficar acima do principal")
            self.assertIn("z-index: 1000;", html, f"{pagina} deve ter popover-lang com z-index 1000 para sobrepor o conteudo")

    def test_pernambuco_single_line_style(self):
        html = (REPO / "index.html").read_text(encoding="utf-8")
        self.assertIn(".destaque-magenta { color: var(--magenta); white-space: nowrap; display: inline-block; }", html)
        self.assertIn('<span class="destaque-magenta">Pernambuco', html)


if __name__ == "__main__":
    unittest.main()

