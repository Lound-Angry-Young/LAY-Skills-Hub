#!/usr/bin/env python3
"""Builds the comprehensive, self-contained visual LAY Skills Hub web application."""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CATALOG_PATH = ROOT / "catalog/skills.json"
SOURCES_PATH = ROOT / "registry/sources.json"
HUB_DIR = ROOT / "hub"
DATA_JS_PATH = HUB_DIR / "data.js"

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

def clean_markdown_body(raw: str) -> str:
    # Remove frontmatter
    text = re.sub(r'^---\s*[\r\n]+.*?[\r\n]+---\s*[\r\n]+', '', raw, flags=re.DOTALL)
    return text.strip()

def build_data():
    HUB_DIR.mkdir(parents=True, exist_ok=True)
    catalog = json.loads(CATALOG_PATH.read_text(encoding="utf-8"))
    skills_list = []

    LOCAL_ATTRIBUTIONS = {
        "vanta-backgrounds": "tengbao--vanta",
        "react-bits-animations": "DavidHDev--react-bits",
        "lenis-smooth-scroll": "darkroomengineering--lenis",
        "creative-libraries-hub": "Jakubantalik--Libraries.dev",
        "generative-ai-reference": "anil-matcha--open-generative-ai",
        "design-reference": "voltagent--awesome-design-md",
        "lay-core-vanta-backgrounds": "tengbao--vanta",
        "lay-core-react-bits-animations": "DavidHDev--react-bits",
        "lay-core-lenis-smooth-scroll": "darkroomengineering--lenis",
        "lay-core-creative-libraries-hub": "Jakubantalik--Libraries.dev",
        "lay-core-generative-ai-reference": "anil-matcha--open-generative-ai",
        "lay-core-design-reference": "voltagent--awesome-design-md",
    }

    for item in catalog["skills"]:
        source_key = item["source"]
        effective_source = LOCAL_ATTRIBUTIONS.get(item["name"], LOCAL_ATTRIBUTIONS.get(item["id"], source_key))
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

    # Sort skills logically: local first, then by category and name
    skills_list.sort(key=lambda s: (0 if s["source"] == "local" else 1, s["categories"][0], s["name"]))

    # Fontes de referência do registro (upstream). Não é a contagem de origens dos cards, que só lista as presentes.
    sources_count = len(json.loads(SOURCES_PATH.read_text(encoding="utf-8"))["sources"])
    output_js = f"// LAY SKILLS HUB - GENERATED DATASET ({len(skills_list)} SKILLS)\nwindow.LAY_SKILLS = {json.dumps(skills_list, ensure_ascii=False, indent=2)};\nwindow.LAY_SOURCES = {json.dumps(SOURCE_METADATA, ensure_ascii=False, indent=2)};\nwindow.LAY_SOURCES_COUNT = {sources_count};\n"
    DATA_JS_PATH.write_text(output_js, encoding="utf-8")
    print(f"[OK] Generated {DATA_JS_PATH} with {len(skills_list)} skills.")

if __name__ == "__main__":
    build_data()
