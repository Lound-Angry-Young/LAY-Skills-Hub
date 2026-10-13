#!/usr/bin/env python3
"""Builds the comprehensive, self-contained visual LAY Skills Hub web application."""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from scripts.skill_hub import DESTINATIONS, load_profiles  # noqa: E402

CATALOG_PATH = ROOT / "catalog/skills.json"
SOURCES_PATH = ROOT / "registry/sources.json"
HUB_DIR = ROOT / "hub"
DATA_JS_PATH = HUB_DIR / "data.js"
CONTEUDO_JS_PATH = HUB_DIR / "conteudo.js"
AGENTES_JS_PATH = HUB_DIR / "agentes.js"
TOTAIS_JS_PATH = HUB_DIR / "totais.js"

SOURCE_METADATA = {
    "local": {
        "author": "LAY® Core Ecosystem",
        "title": "LAY Core Skills",
        "url": "https://github.com/Lound-Angry-Young/LAY-Skills-Hub",
        "avatar": "data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><rect width='100' height='100' rx='20' fill='%2307080b' stroke='%2300f0ff' stroke-width='4'/><path d='M55 15 L25 55 L48 55 L42 85 L75 45 L52 45 Z' fill='%2300f0ff'/></svg>",
        "icon": "⚡",
        "badge": "LAY® Native",
        "desc": "Habilidades centrais para orquestração de IA, diagnóstico técnico, automação 3D e comunicação sintética Caveman."
    },
    "addyosmani--agent-skills": {
        "author": "Addy Osmani",
        "title": "Agent Skills",
        "url": "https://github.com/addyosmani/agent-skills",
        "avatar": "https://avatars.githubusercontent.com/u/110953?v=4",
        "icon": "💎",
        "badge": "Google Engineering",
        "desc": "Coleção rigorosa de engenharia de software de elite, TDD, arquitetura de interfaces, depuração de raiz e padrões de dúvida sistemática."
    },
    "vercel-labs--agent-skills": {
        "author": "Vercel Labs",
        "title": "Agent Skills",
        "url": "https://github.com/vercel-labs/agent-skills",
        "avatar": "https://avatars.githubusercontent.com/u/14985020?v=4",
        "icon": "▲",
        "badge": "Vercel Official",
        "desc": "Melhores práticas oficiais de React 19, Next.js, padrões de composição modular, diretrizes de web design e otimização de performance."
    },
    "leonxlnx--taste-skill": {
        "author": "Leonxlnx",
        "title": "Taste Skill & Brandkit",
        "url": "https://github.com/Leonxlnx/taste-skill",
        "avatar": "https://avatars.githubusercontent.com/u/7895642?v=4",
        "icon": "🎨",
        "badge": "Design Studio",
        "desc": "Especialista em anti-slop, direção visual de luxo, dark-tech, brutalismo industrial, sistemas de identidade visual e imagens para código."
    },
    "semgrep--skills": {
        "author": "Semgrep Team",
        "title": "Security Skills",
        "url": "https://github.com/semgrep/skills",
        "avatar": "https://avatars.githubusercontent.com/u/15082531?v=4",
        "icon": "🛡️",
        "badge": "AppSec Standard",
        "desc": "Análise estática de código (SAST), diretrizes de segurança de código OWASP Top 10 e blindagem contra vulnerabilidades em LLMs (OWASP Top 10 for LLM 2025)."
    },
    "microsoft--playwright-cli": {
        "author": "Microsoft",
        "title": "Playwright CLI",
        "url": "https://github.com/microsoft/playwright-cli",
        "avatar": "https://avatars.githubusercontent.com/u/6154722?v=4",
        "icon": "🎭",
        "badge": "Microsoft QA",
        "desc": "Automação avançada de navegador via CLI, testes E2E, inspeção visual de interfaces renderizadas e gravação de fluxos interativos."
    },
    "ray0907--security-scan": {
        "author": "Ray0907",
        "title": "Security Scan",
        "url": "https://github.com/Ray0907/security-scan",
        "avatar": "https://avatars.githubusercontent.com/u/38729571?v=4",
        "icon": "🔍",
        "badge": "Vulnerability Scan",
        "desc": "Varredura contínua de vulnerabilidades em dependências, verificação de licenças e auditoria estática de riscos CVE."
    },
    "dietrichgebert--ponytail": {
        "author": "Dietrich Gebert",
        "title": "Ponytail Minimalist Dev",
        "url": "https://github.com/DietrichGebert/ponytail",
        "avatar": "https://avatars.githubusercontent.com/u/14828108?v=4",
        "icon": "✂️",
        "badge": "Anti-Overengineering",
        "desc": "Filosofia radical anti-complexidade: prefira stdlib a dependências pesadas, elimine abstrações especulativas e audite débitos técnicos."
    },
    "safishamsi--graphify": {
        "author": "Safi Shamsi",
        "title": "Graphify Engine",
        "url": "https://github.com/safishamsi/graphify",
        "avatar": "https://avatars.githubusercontent.com/u/23114972?v=4",
        "icon": "🕸️",
        "badge": "AST & Knowledge Graph",
        "desc": "Transforma repositórios em grafos de conhecimento persistentes, detecta comunidades de código e identifica 'god nodes' para refatoração segura."
    },
    "guillaumemeyer--watermarks-remover": {
        "author": "Guillaume Meyer",
        "title": "Watermarks Remover",
        "url": "https://github.com/guillaumemeyer/watermarks-remover",
        "avatar": "https://avatars.githubusercontent.com/u/6504533?v=4",
        "icon": "✨",
        "badge": "Text & Media Polish",
        "desc": "Higienização de texto, remoção de caracteres invisíveis e metadados C2PA em mídias autorizadas para publicação limpa e legível."
    },
    "diegosouzapw--omniroute": {
        "author": "Diego Souza",
        "title": "OmniRoute Infrastructure",
        "url": "https://github.com/diegosouzapw/OmniRoute",
        "avatar": "https://avatars.githubusercontent.com/u/59239841?v=4",
        "icon": "🔀",
        "badge": "LLM Router & Gateway",
        "desc": "Gateway resiliente de roteamento de modelos de IA, caching semântico, compressão RTK de contexto, limites de orçamento e comunicação Agent-to-Agent (A2A)."
    },
    "anil-matcha--open-generative-ai": {
        "author": "Anil Matcha",
        "title": "Open Generative AI",
        "url": "https://github.com/Anil-matcha/open-generative-ai",
        "avatar": "https://avatars.githubusercontent.com/u/20261623?v=4",
        "icon": "🤖",
        "badge": "GenAI Patterns",
        "desc": "Coleção de arquiteturas abertas para produtos baseados em IA generativa, fluxos de design visual e agentes de automação."
    },
    "voltagent--awesome-design-md": {
        "author": "VoltAgent",
        "title": "Awesome Design MD",
        "url": "https://github.com/voltagent/awesome-design-md",
        "avatar": "https://avatars.githubusercontent.com/u/159492150?v=4",
        "icon": "📐",
        "badge": "Design System Specs",
        "desc": "Repositório curado de especificações de design systems modernos (DESIGN.md) de produtos globais de referência."
    },
    "latent-spaces--brag": {
        "author": "Latent Spaces",
        "title": "Brag Showcase",
        "url": "https://github.com/latent-spaces/brag",
        "avatar": "https://avatars.githubusercontent.com/u/118317765?v=4",
        "icon": "🚀",
        "badge": "Project Portfolio",
        "desc": "Padrões de apresentação de engenharia e destaque de portfólio de alta densidade técnica."
    },
    "tengbao--vanta": {
        "author": "Tengbao",
        "title": "Vanta.js 3D WebGL Backgrounds",
        "url": "https://github.com/tengbao/vanta",
        "avatar": "https://avatars.githubusercontent.com/u/618215?v=4",
        "icon": "🌌",
        "badge": "3D WebGL Shader",
        "desc": "Efeitos 3D animados interativos para fundos de página (Waves, Net, Rings, Halo, Birds, Cells, Globe) desenvolvidos com Three.js e WebGL."
    },
    "DavidHDev--react-bits": {
        "author": "David H. Dev",
        "title": "React Bits UI FX",
        "url": "https://github.com/DavidHDev/react-bits",
        "avatar": "https://avatars.githubusercontent.com/u/70211756?v=4",
        "icon": "✨",
        "badge": "React Animation Kit",
        "desc": "60+ componentes de animação e microinterações modulares para React (DecryptedText, BlurText, ShinyText, SpotlightCard, Hyperspeed, LiquidChrome)."
    },
    "darkroomengineering--lenis": {
        "author": "Darkroom Engineering",
        "title": "Lenis Smooth Scroll",
        "url": "https://github.com/darkroomengineering/lenis",
        "avatar": "https://avatars.githubusercontent.com/u/74619356?v=4",
        "icon": "🌊",
        "badge": "Smooth Motion",
        "desc": "Motor de rolagem ultra-suave com física delta-time independente de FPS, sincronização perfeita com GSAP ScrollTrigger e suporte touch natural."
    },
    "Jakubantalik--Libraries.dev": {
        "author": "Jakub Antalik",
        "title": "Libraries.dev Creative Hub",
        "url": "https://github.com/Jakubantalik/Libraries.dev",
        "avatar": "https://avatars.githubusercontent.com/u/1283838?v=4",
        "icon": "📚",
        "badge": "Creative Directory",
        "desc": "Diretório supremo de 1.000+ bibliotecas modernas para desenvolvimento web criativo, shaders GLSL, física de canvas, 3D, áudio e UI."
    }
}

# Campos pesados: saem de data.js e vão para conteudo.js, carregado sob demanda.
CAMPOS_PESADOS = ("content", "prompt")

# Chaves de versões antigas das skills. Nenhuma confere com o catálogo atual,
# então nenhuma skill sai atribuída a fonte upstream (ver fontes_upstream).
# Skills LAY inspiradas e citadas em fontes upstream: a fonte exibida é a upstream.
# Só entram pares confirmados pela própria SKILL.md. architecting-generative-ai-apps
# (anil-matcha--open-generative-ai) fica de fora até confirmação.
LOCAL_ATTRIBUTIONS = {
    "rendering-vanta-backgrounds": "tengbao--vanta",
    "animating-react-bits-components": "DavidHDev--react-bits",
    "orchestrating-smooth-scroll": "darkroomengineering--lenis",
    "selecting-creative-libraries": "Jakubantalik--Libraries.dev",
    "consulting-design-references": "voltagent--awesome-design-md",
    # ponytail (DietrichGebert, MIT)
    "auditing-codebase-bloat": "dietrichgebert--ponytail",
    "measuring-code-savings": "dietrichgebert--ponytail",
    "tracking-technical-debt-ledgers": "dietrichgebert--ponytail",
    "reviewing-code-minimalism": "dietrichgebert--ponytail",
    "minimizing-code-overengineering": "dietrichgebert--ponytail",
    "guiding-ponytail-minimalism": "dietrichgebert--ponytail",
    # taste-skill (Leonxlnx, MIT)
    "applying-legacy-design-taste": "leonxlnx--taste-skill",
    "elevating-frontend-taste": "leonxlnx--taste-skill",
    "governing-anti-slop-aesthetics": "leonxlnx--taste-skill",
    "crafting-high-end-visuals": "leonxlnx--taste-skill",
    "designing-minimalist-interfaces": "leonxlnx--taste-skill",
    "redesigning-legacy-interfaces": "leonxlnx--taste-skill",
    "authoring-stitch-design-systems": "leonxlnx--taste-skill",
    "converting-images-to-code": "leonxlnx--taste-skill",
    "generating-web-ui-references": "leonxlnx--taste-skill",
    "generating-mobile-ui-mockups": "leonxlnx--taste-skill",
    "generating-brandkit-identities": "leonxlnx--taste-skill",
    "enforcing-full-code-output": "leonxlnx--taste-skill",
    "engineering-gsap-motion-uis": "leonxlnx--taste-skill",
    "designing-industrial-brutalist-interfaces": "leonxlnx--taste-skill",
    # playwright-cli (Microsoft, Apache-2.0)
    "automating-browser-tests": "microsoft--playwright-cli",
    # security-scan (Ray Tien, MIT)
    "scanning-dependency-vulnerabilities": "ray0907--security-scan",
    # watermarks-remover (Guillaume Meyer e colaboradores, MIT)
    "polishing-user-facing-prose": "guillaumemeyer--watermarks-remover",
    "stripping-ai-provenance-marks": "guillaumemeyer--watermarks-remover",
}

# Id do filtro de categoria de index.html para cada domínio.
CATEGORIA_FILTRO = {
    "frontend": "design",
    "creative-3d": "design",
    "design": "design",
    "routing-and-proxy": "operacoes",
    "devops": "operacoes",
    "database": "operacoes",
    "engineering": "engenharia",
    "context": "contexto",
    "qa": "testes",
    "security": "seguranca",
    "documentation": "documentacao",
}

# Rótulos exatos do campo label no array de categorias de index.html.
# tests/test_build_hub.py confere cada um com o arquivo: se o site mudar, o teste avisa.
ROTULOS_CATEGORIA = {
    "design": "DESIGN & UI/UX",
    "contexto": "CONTEXTO & AGENTES",
    "engenharia": "ENGENHARIA",
    "testes": "TESTES & QUALIDADE",
    "seguranca": "SEGURANÇA & SCAN",
    "operacoes": "OPERAÇÕES & CI/CD",
    "documentacao": "DOCUMENTAÇÃO",
}

# Marcas da description do perfil (agents/perfis.json) e limites dos textos curtos dos cards.
MARCA_USE_QUANDO = "Use quando:"
MARCA_NAO_USE_PARA = "Não use para:"
LIMITE_RESUMO = 100
LIMITE_NAO_USE_PARA = 140

# Clientes que recebem as skills, em ordem de exibição. Os ids devem existir em DESTINATIONS (skill_hub.py).
CLIENTES_COM_SKILLS = [("claude", "Claude Code"), ("codex", "Codex"), ("antigravity", "Antigravity")]

# Os subagentes do projeto são arquivos do Claude Code em .claude/agents/.
SUBAGENTE_EM = "Claude Code"


def clean_markdown_body(raw: str) -> str:
    # Remove frontmatter
    text = re.sub(r'^---\s*[\r\n]+.*?[\r\n]+---\s*[\r\n]+', '', raw, flags=re.DOTALL)
    return text.strip()

def fonte_efetiva(item, atribuicoes=None):
    """Fonte da skill no hub: a atribuição upstream, se existir; senão a fonte do catálogo."""
    atribuicoes = LOCAL_ATTRIBUTIONS if atribuicoes is None else atribuicoes
    return atribuicoes.get(item["name"], atribuicoes.get(item["id"], item["source"]))


def dominio_da_skill(item):
    """Domínio público da skill: refactored_skills/<dominio>/<nome>/SKILL.md."""
    partes = item["path"].split("/")
    if len(partes) < 3 or partes[0] != "refactored_skills":
        raise ValueError(f"skill fora de refactored_skills/: {item['path']}")
    return partes[1]


def dividir_conteudo(skills):
    """Separa content e prompt do restante de cada skill. Devolve (skills leves, {id: campos pesados}) sem alterar a entrada."""
    leves, conteudo = [], {}
    for skill in skills:
        if skill["id"] in conteudo:
            raise ValueError(f"id duplicado: {skill['id']}")
        conteudo[skill["id"]] = {campo: skill[campo] for campo in CAMPOS_PESADOS}
        leves.append({chave: valor for chave, valor in skill.items() if chave not in CAMPOS_PESADOS})
    return leves, conteudo


def formatar_data_js(skills, metadados, total_fontes):
    """data.js: skills sem content e prompt, metadados das fontes e contagem de fontes."""
    return (f"// LAY SKILLS HUB - GENERATED DATASET ({len(skills)} SKILLS)\n"
            f"window.LAY_SKILLS = {json.dumps(skills, ensure_ascii=False, indent=2)};\n"
            f"window.LAY_SOURCES = {json.dumps(metadados, ensure_ascii=False, indent=2)};\n"
            f"window.LAY_SOURCES_COUNT = {total_fontes};\n")


def linhas_do_conteudo(texto):
    """Linhas do markdown de uma skill, sem espaço no fim e sem linhas vazias nas bordas."""
    linhas = [linha.rstrip() for linha in str(texto or "").replace("\r\n", "\n").replace("\r", "\n").split("\n")]
    while linhas and not linhas[-1]:
        linhas.pop()
    while linhas and not linhas[0]:
        linhas.pop(0)
    return linhas


def formatar_conteudo_js(conteudo):
    """conteudo.js: cada linha do markdown ocupa uma linha do arquivo, para leitura direta no editor e em
    iterações futuras. O site junta as linhas ao exibir a skill; o prompt segue como uma string."""
    linhas = [f"// LAY SKILLS HUB - CONTEUDO GERADO ({len(conteudo)} SKILLS)", "window.LAY_CONTEUDO = {"]
    itens = list(conteudo.items())
    for posicao, (skill_id, campos) in enumerate(itens):
        virgula = "," if posicao < len(itens) - 1 else ""
        trechos = linhas_do_conteudo(campos.get("content"))
        linhas.append(f"  {json.dumps(skill_id, ensure_ascii=False)}: {{")
        linhas.append('    "content": [')
        for indice, trecho in enumerate(trechos):
            fim = "," if indice < len(trechos) - 1 else ""
            linhas.append(f"      {json.dumps(trecho, ensure_ascii=False)}{fim}")
        linhas.append("    ],")
        linhas.append(f'    "prompt": {json.dumps(campos.get("prompt", ""), ensure_ascii=False)}')
        linhas.append(f"  }}{virgula}")
    linhas.append("};")
    return "\n".join(linhas) + "\n"


def fontes_upstream(skills, registro, metadados, atribuicoes=None):
    """Fontes upstream que contribuem às skills (fonte efetiva diferente de 'local').
    id e url vêm do registro, sem o sufixo .git; título e autor, de SOURCE_METADATA."""
    ids = []
    for skill in skills:
        fonte = fonte_efetiva(skill, atribuicoes)
        if fonte != "local" and fonte not in ids:
            ids.append(fonte)
    por_id = {fonte["id"]: fonte for fonte in registro}
    saida = []
    for fonte_id in ids:
        if fonte_id not in por_id or fonte_id not in metadados:
            raise ValueError(f"fonte upstream sem registro ou sem metadados: {fonte_id}")
        url = por_id[fonte_id]["url"]
        saida.append({"id": fonte_id,
                      "titulo": metadados[fonte_id]["title"],
                      "autor": metadados[fonte_id]["author"],
                      "url": url[:-len(".git")] if url.endswith(".git") else url})
    return saida


def gatilhos_do_perfil(descricao):
    """Separa a description do perfil em (use_quando, nao_use_para_completo).

    use_quando: o que vem depois de 'Use quando:' até 'Não use para:', sem o ponto final.
    nao_use_para_completo: o que vem depois de 'Não use para:', sem corte.
    Sem 'Use quando:', vale a descrição inteira; sem 'Não use para:', o segundo valor fica vazio.
    """
    texto = " ".join(descricao.split())
    resto = texto.split(MARCA_USE_QUANDO, 1)[1] if MARCA_USE_QUANDO in texto else texto
    if MARCA_NAO_USE_PARA in resto:
        quando, nao_use = resto.split(MARCA_NAO_USE_PARA, 1)
    else:
        quando, nao_use = resto, ""
    quando = quando.strip()
    if quando.endswith("."):
        quando = quando[:-1].rstrip()
    return quando, nao_use.strip()


# Palavras de ligação e artigos que não encerram um resumo cortado (comparação sem diferenciar maiúsculas).
LIGACOES_DO_FIM = frozenset({
    "de", "da", "do", "das", "dos", "em", "no", "na", "nos", "nas", "para", "por", "com", "sem", "ou", "e",
    "a", "o", "as", "os", "que", "ao", "aos", "à", "às", "sobre", "entre",
})


def tirar_ligacoes_do_fim(texto):
    """Retira do fim do texto as palavras de LIGACOES_DO_FIM e a pontuação solta que sobrar."""
    palavras = texto.split(" ")
    while palavras and palavras[-1].rstrip(",;:.!?").lower() in LIGACOES_DO_FIM:
        palavras.pop()
    return " ".join(palavras).rstrip(",;: ")


def cortar_palavras(texto, limite):
    """Corta no último espaço que cabe em `limite` caracteres, sem reticências e sem partir palavra.

    Texto que já cabe volta igual. Quando há corte, retira pontuação solta no fim e as palavras de ligação
    que ficarem no fim (tirar_ligacoes_do_fim). Se o corte ficar vazio, vale o corte sem essa retirada.
    """
    texto = " ".join(texto.split())
    if len(texto) <= limite:
        return texto
    cortado = ""
    for palavra in texto.split(" "):
        candidato = palavra if not cortado else cortado + " " + palavra
        if len(candidato) > limite:
            break
        cortado = candidato
    if not cortado:
        raise ValueError(f"primeira palavra com mais de {limite} caracteres: {texto.split(' ')[0]!r}")
    cortado = cortado.rstrip(",;: ")
    return tirar_ligacoes_do_fim(cortado) or cortado


def rotulo_acesso(ferramentas):
    """Rótulo de acesso pelas ferramentas do perfil: escrita (Edit ou Write) e Bash."""
    edita = bool({"Edit", "Write"} & set(ferramentas))
    comandos = "Bash" in ferramentas
    if edita and comandos:
        return "Edita e roda comandos"
    if edita:
        return "Edita, sem comandos"
    if comandos:
        return "Não edita · tem Bash"
    return "Só leitura"


def categoria_do_dominio(dominio):
    """Rótulo do filtro de categoria de index.html para o domínio do perfil."""
    return ROTULOS_CATEGORIA[CATEGORIA_FILTRO[dominio]]


def construir_agentes(perfis, catalogo, registro, metadados, tem_subagente, atribuicoes=None):
    """Um objeto por Especialista, em ordem alfabética pelo nome. Entra só o que o build verifica: perfis,
    catálogo, registro de fontes, metadados e a existência do subagente em .claude/agents/ no momento do build."""
    ids_clientes = {cliente for cliente, _ in CLIENTES_COM_SKILLS}
    if ids_clientes != set(DESTINATIONS):
        raise ValueError(f"clientes do hub divergem do instalador: {sorted(ids_clientes ^ set(DESTINATIONS))}")
    por_dominio = {}
    for item in catalogo:
        if item["source"] == "local" and item.get("kind", "skill") == "skill":
            por_dominio.setdefault(dominio_da_skill(item), []).append(item)
    agentes = []
    for perfil in sorted(perfis, key=lambda p: p["nome"]):
        nome, dominio = perfil["nome"], perfil["dominio"]
        if dominio not in CATEGORIA_FILTRO:
            raise ValueError(f"domínio sem categoria no hub: {dominio}")
        ativas = sorted(por_dominio.get(dominio, []), key=lambda item: item["name"])
        use_quando, nao_use_completo = gatilhos_do_perfil(perfil["descricao"])
        agentes.append({
            "nome": nome,
            "dominio": dominio,
            "categoria": categoria_do_dominio(dominio),
            "descricao": perfil["descricao"],
            "ferramentas": list(perfil["ferramentas"]),
            "use_quando": use_quando,
            "nao_use_para": cortar_palavras(nao_use_completo, LIMITE_NAO_USE_PARA),
            "nao_use_para_completo": nao_use_completo,
            "resumo": cortar_palavras(use_quando, LIMITE_RESUMO),
            "acesso": rotulo_acesso(perfil["ferramentas"]),
            "skills_ativas": len(ativas),
            "skills": [item["name"] for item in ativas],
            "fontes_upstream": fontes_upstream(ativas, registro, metadados, atribuicoes),
            "subagente_em": SUBAGENTE_EM,
            "clientes_com_skills": [cliente_nome for _, cliente_nome in CLIENTES_COM_SKILLS],
            "configurado": {
                "projeto": bool(tem_subagente(nome)),
                "projeto_caminho": f".claude/agents/{nome}.md",
                "global_caminho": f"~/.claude/agents/{nome}.md",
            },
        })
    return agentes


def formatar_agentes_js(agentes):
    """agentes.js: window.LAY_AGENTES, um objeto por Especialista."""
    return (f"// LAY SKILLS HUB - AGENTES GERADOS ({len(agentes)} ESPECIALISTAS)\n"
            f"window.LAY_AGENTES = {json.dumps(agentes, ensure_ascii=False, indent=2)};\n")


def formatar_totais_js(skills, fontes, subagentes, dominios):
    """totais.js: contagens pequenas para páginas que não carregam data.js (ex.: instalacao.html)."""
    totais = {"skills": skills, "fontes": fontes, "subagentes": subagentes, "dominios": dominios}
    return f"// LAY SKILLS HUB - TOTAIS GERADOS\nwindow.LAY_TOTAIS = {json.dumps(totais, ensure_ascii=False)};\n"


def chave_de_ordem(skill, origem):
    """Ordem de data.js: skills de origem local primeiro; depois categoria e nome.

    `origem` é o source do catálogo, não a fonte efetiva: uma atribuição upstream não tira a skill do bloco LAY.
    """
    return (0 if origem == "local" else 1, skill["categories"][0], skill["name"])


def build_data():
    HUB_DIR.mkdir(parents=True, exist_ok=True)
    catalog = json.loads(CATALOG_PATH.read_text(encoding="utf-8"))
    skills_list = []

    for item in catalog["skills"]:
        source_key = item["source"]
        effective_source = fonte_efetiva(item)
        meta = SOURCE_METADATA.get(effective_source, {
            "author": source_key,
            "title": source_key,
            "url": f"https://github.com/{source_key.replace('--', '/')}",
            "avatar": "https://github.githubassets.com/images/modules/logos_page/GitHub-Mark.png",
            "icon": "📦",
            "badge": "Community",
            "desc": ""
        })

        # Resolve skill file content
        if source_key == "local":
            skill_file = ROOT / item["path"]
        else:
            skill_file = ROOT / "upstream" / source_key / item["path"]

        content = ""
        if skill_file.exists():
            content = skill_file.read_text(encoding="utf-8", errors="replace")

        clean_body = clean_markdown_body(content) if content else item.get("description", "")

        # Formulate tailored prompt for this specific skill
        prompt_sample = (
            f"Ative e aplique a skill `{item['id']}` para este escopo. "
            f"Siga rigorosamente as instruções da fonte `{meta['author']}` mantendo "
            f"comunicação concisa (Caveman) e validação baseada em evidências."
        )

        categories = item.get("categories", [])
        if not categories:
            categories = ["geral"]

        skills_list.append({
            "id": item["id"],
            "name": item["name"],
            "source": effective_source,
            "author": meta["author"],
            "sourceTitle": meta["title"],
            "sourceUrl": meta["url"],
            "sourceAvatar": meta["avatar"],
            "sourceIcon": meta["icon"],
            "sourceBadge": meta["badge"],
            "sourceDesc": meta["desc"],
            "categories": categories,
            "version": item.get("version", "1.0.0"),
            "commit": item.get("commit", "")[:8],
            "description": item.get("description", "").strip(),
            "prompt": prompt_sample,
            "content": clean_body,
            "kind": item.get("kind", "skill")
        })

    # Ordem de data.js: origem do catálogo (LAY primeiro), depois categoria e nome. A fonte efetiva não entra,
    # para que uma atribuição upstream não tire a skill do bloco LAY.
    origem_por_id = {item["id"]: item["source"] for item in catalog["skills"]}
    skills_list.sort(key=lambda s: chave_de_ordem(s, origem_por_id[s["id"]]))

    # Fontes de referência do registro (upstream). Não é a contagem de origens dos cards, que só lista as presentes.
    registro = json.loads(SOURCES_PATH.read_text(encoding="utf-8"))["sources"]
    sources_count = len(registro)

    leves, conteudo = dividir_conteudo(skills_list)
    DATA_JS_PATH.write_text(formatar_data_js(leves, SOURCE_METADATA, sources_count), encoding="utf-8")
    CONTEUDO_JS_PATH.write_text(formatar_conteudo_js(conteudo), encoding="utf-8")

    perfis = load_profiles(ROOT)
    agentes = construir_agentes(perfis, catalog["skills"], registro, SOURCE_METADATA,
                                lambda nome: (ROOT / ".claude/agents" / f"{nome}.md").is_file())
    AGENTES_JS_PATH.write_text(formatar_agentes_js(agentes), encoding="utf-8")

    dominios = len({dominio_da_skill(item) for item in catalog["skills"]})
    TOTAIS_JS_PATH.write_text(formatar_totais_js(len(skills_list), sources_count, len(perfis), dominios),
                              encoding="utf-8")
    print(f"[OK] Generated {DATA_JS_PATH}, {CONTEUDO_JS_PATH}, {AGENTES_JS_PATH} and {TOTAIS_JS_PATH} with {len(skills_list)} skills.")

if __name__ == "__main__":
    build_data()
