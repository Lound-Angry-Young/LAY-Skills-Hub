#!/usr/bin/env python3
"""Gera o catálogo de componentes animados usado pela skill selecting-animated-ui-components.

Lê os registros shadcn publicados ao vivo (índice registry.json e um JSON por item) e escreve um
reference.md com: domínio de cada item, custo de renderização (tier), flags de acessibilidade e de client
component, e os itens que cada um importa e não traz. Clones locais são opcionais, para gerar offline.

Uso:
  python scripts/gerar_catalogo_componentes.py [--pixel-perfect <clone>] [--componentry <clone>] [--saida <reference.md>]

Padrão de saída: refactored_skills/frontend/selecting-animated-ui-components/reference.md
Somente biblioteca padrão. A classificação por domínio é uma tabela explícita e revisável aqui.
"""
import argparse
import json
import re
import subprocess
import sys
import time
import urllib.request
from collections import Counter, defaultdict
from concurrent.futures import ThreadPoolExecutor
from datetime import date
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
SAIDA_PADRAO = REPO / 'refactored_skills' / 'frontend' / 'selecting-animated-ui-components' / 'reference.md'

FONTES = {
    'pixel-perfect': {
        'titulo': 'Pixel-Perfect',
        'repo': 'github.com/vansh-nagar/Pixel-Perfect',
        'subdir': Path('public') / 'r',
        'indice': 'https://www.pixel-perfect.space/r/registry.json',
        'url': 'https://www.pixel-perfect.space/r/{nome}.json',
        'licenca': 'MIT (Vansh Nagar). Os arquivos copiados devem manter o aviso MIT.',
    },
    'componentry': {
        'titulo': 'Componentry',
        'repo': 'github.com/harshjdhv/componentry',
        'subdir': Path('apps') / 'web' / 'public' / 'r',
        'indice': 'https://componentry.dev/r/registry.json',
        'url': 'https://componentry.dev/r/{nome}.json',
        'licenca': 'MIT (Harsh Jadhav). Ressalva do próprio README: image-trail e layered-stack exigem atenção à licença do GSAP.',
    },
}

DOMINIOS = {
    'texto': ('Texto animado', 'Títulos, frases e palavras com entrada, loop ou efeito de digitação.'),
    'botoes': ('Botões e CTAs', 'Botões de ação, toggles e controles com resposta a hover e clique.'),
    'revelacao-de-imagem': ('Revelação e transição de imagem', 'Troca ou abertura de imagem por máscara, corte ou transição, geralmente disparada por scroll ou hover.'),
    'efeitos-de-imagem': ('Efeitos contínuos sobre imagem', 'Filtros, distorções e estilizações aplicados a uma imagem (shaders).'),
    'galerias-e-carrosseis': ('Galerias e carrosséis', 'Coleções de imagens ou cards com navegação, órbita ou empilhamento.'),
    'scroll-e-secoes': ('Scroll e seções', 'Efeitos ligados à rolagem: pin, sticky, parallax e revelação de seções.'),
    'cursor-e-interacao': ('Cursor e interação', 'Efeitos que respondem ao ponteiro: trails, ímãs, distorções e comparação.'),
    'fundos-animados': ('Fundos animados', 'Planos de fundo de hero e seções, em CSS, canvas ou shader.'),
    'cards-e-widgets': ('Cards e widgets', 'Cartões e pequenos painéis de interface com animação própria.'),
    '3d-e-perspectiva': ('3D e perspectiva', 'Objetos e cards em 3D, em CSS 3D ou Three.js.'),
    'svg-logos-e-bordas': ('SVG, logos e bordas', 'Ícones, logos, traçados SVG e molduras decorativas.'),
    'navegacao-e-chat': ('Navegação e chat', 'Menus, docks, sidebars e interfaces de conversa.'),
    'blocos-de-pagina': ('Blocos de página', 'Seções completas prontas (hero, preços). Exigem adaptação de conteúdo.'),
    'base-tecnica': ('Base técnica', 'Arquivos auxiliares importados por outros itens. Não são componentes de tela.'),
}

TIERS = {
    1: 'T1: CSS e DOM. Sem biblioteca de animação e sem canvas. Menor custo.',
    2: 'T2: biblioteca de animação (GSAP, Framer Motion ou Motion) ou canvas 2D. Custo moderado, em JavaScript.',
    3: 'T3: WebGL ou Three.js. Renderiza na GPU a cada quadro. Maior custo.',
}

BASE_TECNICA = {'shader-canvas', 'image-shader-canvas', 'animated-texture', 'engine', 'specs', 'index', 'registry'}

PERSPECTIVA_GALERIA = {'rotating-ring-carousel', 'coverflow-marquee', 'perspective-deck-carousel', 'fanned-deck-carousel'}

SHADERS_3D = {'blob-sphere', 'twisted-blob'}
SHADERS_INTERATIVOS = re.compile(r'cursor|magnetic|vortex|inertia|jelly|ripple-touch|liquid-melt|pixel-distortion|fluid-image|before-after|image-particles|flow-field|pixel-displace')
SHADERS_REVELACAO = re.compile(r'reveal|transition|dissolve|flip|blinds|wipe|melt|rise|burn|checker')

COMPONENTRY = {
    'animated-gradient': 'fundos-animados', 'annotated-text': 'texto', 'ascii-effect': 'efeitos-de-imagem',
    'aurora-flow': 'fundos-animados', 'case-study-flip-stack': 'galerias-e-carrosseis', 'circuit-board': 'cards-e-widgets',
    'closing-plasma': 'fundos-animados', 'collection-surfer': 'galerias-e-carrosseis', 'cursor-driven-particle-typography': 'texto',
    'dither-gradient': 'fundos-animados', 'dither-prism-hero': 'fundos-animados', 'dithered-logo': 'efeitos-de-imagem',
    'eye-tracking': 'cursor-e-interacao', 'fisheye-infinite-grid': 'galerias-e-carrosseis', 'flight-status-card': 'cards-e-widgets',
    'flipping-word-swap': 'texto', 'github-calendar': 'cards-e-widgets', 'grain-gradient': 'fundos-animados',
    'gradient-hero-01': 'blocos-de-pagina', 'hero-geometric': 'blocos-de-pagina', 'hover-transition': 'cards-e-widgets',
    'image-ripple-effect': 'efeitos-de-imagem', 'image-trail': 'cursor-e-interacao', 'infinite-image-field': 'galerias-e-carrosseis',
    'kinetic-text-reveal': 'texto', 'layered-stack': 'galerias-e-carrosseis', 'letter-cascade': 'texto',
    'liquid-chrome': 'fundos-animados', 'liquid-glass-carousel': 'galerias-e-carrosseis', 'mac-keyboard': 'cards-e-widgets',
    'magnet-lines': 'cursor-e-interacao', 'magnetic-dock': 'navegacao-e-chat', 'matrix-rain': 'fundos-animados',
    'music-player': 'cards-e-widgets', 'newsletter-bookshelf': 'galerias-e-carrosseis', 'orbit-card-stack': 'galerias-e-carrosseis',
    'pixel-canvas': 'cursor-e-interacao', 'pixel-image-trail': 'cursor-e-interacao', 'pricing-01': 'blocos-de-pagina',
    'pricing-02': 'blocos-de-pagina', 'prism-gradient': 'fundos-animados', 'ripple-transition': 'revelacao-de-imagem',
    'scroll-based-velocity': 'texto', 'scroll-choreography': 'scroll-e-secoes', 'scroll-split-card': 'scroll-e-secoes',
    'scroll-tilted-grid': 'scroll-e-secoes', 'signature': 'svg-logos-e-bordas', 'silk-aurora': 'fundos-animados',
    'spectral-ribbon': 'fundos-animados', 'spiral-3d-slider': 'galerias-e-carrosseis', 'split-flap-display': 'cards-e-widgets',
    'sticky-scroll-cards': 'scroll-e-secoes', 'text-morph': 'texto', 'text-repel': 'cursor-e-interacao',
    'webgl-liquid': 'fundos-animados', 'wheel-carousel': 'galerias-e-carrosseis',
}

SHADCN_PADRAO = {'button', 'spinner', 'sidebar', 'input', 'kbd', 'badge', 'card', 'tooltip', 'dialog',
                 'separator', 'scroll-area', 'skeleton', 'label', 'textarea', 'select', 'switch', 'tabs'}

IMPORTA = re.compile(r'''(?:from|import)\s+["']([^"']+)["']''')
HOOK = re.compile(r'\buse[A-Z]\w*\s*\(')
REDUZIDO = re.compile(r'prefers-reduced-motion|useReducedMotion|reducedMotion')
MOUSE = re.compile(r'mousemove|onMouseMove|pointermove|onPointerMove|mouseenter|onMouseEnter')
TOQUE = re.compile(r'hover:\s*none|pointer:\s*coarse|touchstart|touchmove|touchend|onTouch|maxTouchPoints|pointerType|isTouch|isMobile|useIsMobile')
JS_ANIM = {'gsap', '@gsap/react', 'framer-motion', 'motion', '@studio-freight/lenis'}
WEBGL_IMP = re.compile(r'''from\s+["'](?:three|@react-three/[^"']*)["']|WebGL|webgl|from\s+["']\./(?:image-shader-canvas|shader-canvas|animated-texture)["']''')
CANVAS_2D = re.compile(r'''getContext\(\s*["']2d|<canvas|requestAnimationFrame''')


NAO_SAO_COMPONENTES = ('index', 'registry')


def http_get(url):
    pedido = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (lay-skills-hub gerador)'})
    with urllib.request.urlopen(pedido, timeout=60) as resposta:
        return resposta.read().decode('utf-8')


def ler_ao_vivo(fonte):
    """Lê o índice público da fonte e baixa cada item pela URL. Falha alta: não ignora item com erro."""
    indice = json.loads(http_get(FONTES[fonte]['indice']))
    nomes = [i['name'] for i in indice.get('items', []) if i['name'] not in NAO_SAO_COMPONENTES]

    def baixar(nome):
        ultimo = None
        for tentativa in range(3):
            try:
                return json.loads(http_get(FONTES[fonte]['url'].format(nome=nome)))
            except Exception as erro:
                ultimo = erro
                time.sleep(1 + tentativa)
        raise SystemExit(f'falha ao baixar {nome} de {fonte} após 3 tentativas: {ultimo}')

    with ThreadPoolExecutor(max_workers=8) as pool:
        return dict(zip(nomes, pool.map(baixar, nomes)))


def ler_local(fonte, clone):
    pasta = Path(clone) / FONTES[fonte]['subdir']
    if not pasta.is_dir():
        raise SystemExit(f'pasta de registros não encontrada: {pasta}')
    itens = {}
    for arquivo in sorted(pasta.glob('*.json')):
        if arquivo.stem in NAO_SAO_COMPONENTES:
            continue
        itens[arquivo.stem] = json.loads(arquivo.read_text(encoding='utf-8'))
    return itens


def ler_registro(fonte, clone=None):
    return ler_local(fonte, clone) if clone else ler_ao_vivo(fonte)


def commit_do_clone(clone):
    try:
        r = subprocess.run(['git', '-C', str(clone), 'rev-parse', '--short', 'HEAD'],
                           capture_output=True, text=True, check=True)
        return r.stdout.strip()
    except (OSError, subprocess.CalledProcessError):
        return 'desconhecido'


def categoria_de(arquivos):
    caminho = arquivos[0].get('path', '') if arquivos else ''
    partes = caminho.split('/')
    if len(partes) > 3 and partes[0] == 'registry':
        return partes[2]
    return ''


def dominio_de(fonte, nome, categoria):
    if nome in BASE_TECNICA:
        return 'base-tecnica'
    if fonte == 'componentry':
        return COMPONENTRY.get(nome, 'cards-e-widgets')
    if nome == 'pixel-credits-button':
        return 'botoes'
    mapa = {
        'text': 'texto', 'buttons': 'botoes', 'mask': 'revelacao-de-imagem',
        'image-animations': 'galerias-e-carrosseis', 'carousel': 'galerias-e-carrosseis',
        'scroll': 'scroll-e-secoes', 'mouse-follower': 'cursor-e-interacao', 'backgrounds': 'fundos-animados',
        'ascii': 'fundos-animados', 'svg': 'svg-logos-e-bordas', 'svg-path-effects': 'svg-logos-e-bordas',
        'borders': 'svg-logos-e-bordas', 'chat': 'navegacao-e-chat', 'sidebars': 'navegacao-e-chat',
        'three-js': '3d-e-perspectiva',
    }
    if categoria in mapa:
        return mapa[categoria]
    if categoria == 'gsap':
        if 'reveal' in nome:
            return 'revelacao-de-imagem'
        if 'text' in nome or 'stagger' in nome:
            return 'texto'
        return 'fundos-animados' if 'morph' in nome else 'cards-e-widgets'
    if categoria == 'perspective':
        return 'galerias-e-carrosseis' if nome in PERSPECTIVA_GALERIA else '3d-e-perspectiva'
    if categoria == 'motion-framer':
        if 'toggle' in nome or 'button' in nome:
            return 'botoes'
        if nome == 'logo-animation':
            return 'svg-logos-e-bordas'
        if 'text' in nome:
            return 'texto'
        return 'cards-e-widgets'
    if categoria == 'shaders':
        if nome.startswith('img-'):
            return 'revelacao-de-imagem' if SHADERS_REVELACAO.search(nome) else 'efeitos-de-imagem'
        if nome in SHADERS_3D:
            return '3d-e-perspectiva'
        if SHADERS_REVELACAO.search(nome):
            return 'revelacao-de-imagem'
        if SHADERS_INTERATIVOS.search(nome):
            return 'cursor-e-interacao'
        return 'fundos-animados'
    print(f'aviso: sem domínio para {nome} (categoria {categoria or "?"}); usando cards-e-widgets', file=sys.stderr)
    return 'cards-e-widgets'


def tier_de(deps, conteudo):
    if any(d == 'three' or d.startswith('@react-three/') for d in deps) or WEBGL_IMP.search(conteudo):
        return 3
    if any(d in JS_ANIM for d in deps) or CANVAS_2D.search(conteudo):
        return 2
    return 1


def importacoes_faltando(arquivos):
    nomes = {Path(a.get('path', '')).stem for a in arquivos}
    faltam = set()
    for a in arquivos:
        for esp in IMPORTA.findall(a.get('content', '')):
            if esp.startswith(('.', '@/')):
                base = esp.rstrip('/').split('/')[-1]
                if base not in nomes and base not in ('utils', 'index'):
                    faltam.add(esp)
    return sorted(faltam)


def resolver_importacao(esp, nomes_do_registro):
    base = esp.rstrip('/').split('/')[-1]
    if base in nomes_do_registro:
        return f'instalar `{base}`'
    if esp.startswith('@/components/ui/') and base in SHADCN_PADRAO:
        return f'shadcn: `{base}`'
    return 'manual: não encontrado no registro'


def cliente_de(arquivos):
    """'sim': arquivo principal tem a diretiva. 'verificar': algum arquivo usa hook sem a diretiva,
    o que só é problema se esse arquivo for importado por código de servidor. 'não precisa': sem hooks."""
    principal = arquivos[0].get('content', '') if arquivos else ''
    if principal.lstrip().startswith(('"use client"', "'use client'")):
        return 'sim'
    tem_hook = any(HOOK.search(a.get('content', '')) for a in arquivos)
    return 'verificar' if tem_hook else 'não precisa'


def montar_item(fonte, nome, dados, nomes_do_registro):
    arquivos = dados.get('files') or []
    conteudo = '\n'.join(a.get('content', '') for a in arquivos)
    deps = [x for x in (dados.get('dependencies') or []) if x not in ('react', 'react-dom')]
    categoria = categoria_de(arquivos)
    mouse = bool(MOUSE.search(conteudo))
    if mouse:
        toque = 'sim' if TOQUE.search(conteudo) else 'não'
    else:
        toque = '—'
    return {
        'fonte': fonte,
        'nome': nome,
        'descricao': ' '.join((dados.get('description') or '').split()) or '(sem descrição no registro)',
        'dominio': dominio_de(fonte, nome, categoria),
        'tier': tier_de(deps, conteudo),
        'cliente': cliente_de(arquivos),
        'reduzido': 'sim' if REDUZIDO.search(conteudo) else 'não',
        'toque': toque,
        'depuracao': 'lil-gui' if 'lil-gui' in deps else '',
        'deps': deps,
        'faltam': [(esp, resolver_importacao(esp, nomes_do_registro)) for esp in importacoes_faltando(arquivos)],
        'registry_deps': [u.rstrip('/').split('/')[-1].replace('.json', '') for u in (dados.get('registryDependencies') or [])],
        'instalar': [],
        'alcance': set(),
        'plano': '—',
        'url': FONTES[fonte]['url'].format(nome=nome),
    }


def fechamento(nome, por_nome):
    """Itens do mesmo registro que `nome` importa, direta ou indiretamente, na ordem de instalação.
    Dependências vêm antes de quem as usa. `nome` não entra na lista."""
    ordem, visitados = [], {nome}

    def visita(n):
        for esp, acao in por_nome[n]['faltam']:
            base = esp.rstrip('/').split('/')[-1]
            if acao.startswith('instalar') and base not in visitados:
                visitados.add(base)
                visita(base)
                ordem.append(base)

    visita(nome)
    return ordem


def alcance_do_cli(nome, por_nome):
    """Itens que o CLI do shadcn traz ao instalar `nome`: fechamento transitivo de registryDependencies."""
    vistos, pilha = set(), [nome]
    while pilha:
        n = pilha.pop()
        for b in por_nome[n]['registry_deps']:
            if b in por_nome and b not in vistos:
                vistos.add(b)
                pilha.append(b)
    return vistos


def plano_de(item, por_nome):
    """Texto da coluna 'Instalar antes': o que o CLI traz sozinho e o que precisa ser instalado à mão."""
    partes = []
    if item['instalar']:
        manuais = [n for n in item['instalar'] if n not in item['alcance']]
        if manuais:
            partes.append('instalar à mão, nesta ordem: ' + ' → '.join(f'`{n}`' for n in manuais))
        else:
            partes.append('o CLI traz a cadeia (registryDependencies)')
    extras = []
    for n in [item['nome']] + item['instalar']:
        for esp, acao in por_nome[n]['faltam']:
            if not acao.startswith('instalar') and (esp, acao) not in extras:
                extras.append((esp, acao))
    partes += [f'{acao} (`{esp}`)' for esp, acao in extras]
    return '; '.join(partes) or '—'


def coletar(clones):
    itens = []
    for fonte, clone in clones.items():
        registro = ler_registro(fonte, clone)
        nomes = set(registro)
        por_nome = {nome: montar_item(fonte, nome, dados, nomes) for nome, dados in registro.items()}
        for nome, item in por_nome.items():
            item['instalar'] = fechamento(nome, por_nome)
            item['alcance'] = alcance_do_cli(nome, por_nome)
        for item in por_nome.values():
            item['plano'] = plano_de(item, por_nome)
        itens.extend(por_nome.values())
    return itens


def celula(texto):
    return str(texto).replace('|', '\\|').replace('\n', ' ')


def linha_faltam(item):
    return item['plano']


def escrever(itens, origens, saida):
    L = []
    L.append('## Table of Contents')
    L.append('1. Como usar este catálogo')
    L.append('2. Resumo por domínio e custo')
    L.append('3. Flags de decisão')
    L.append('4. Domínios e itens')
    L.append('5. Fontes e licenças')
    L.append('6. Como regenerar')
    L.append('')
    total = len(itens)
    por_fonte = Counter(i['fonte'] for i in itens)
    L.append('## 1. Como usar este catálogo')
    L.append('')
    L.append(f'Este arquivo foi gerado por `scripts/gerar_catalogo_componentes.py` a partir de {total} registros shadcn '
             f'(Pixel-Perfect: {por_fonte["pixel-perfect"]}; Componentry: {por_fonte["componentry"]}). '
             'Não edite à mão: regenere.')
    L.append('')
    L.append('- Instalar um item: `npx shadcn@latest add <url>`, com a URL da coluna da fonte (seção 5).')
    L.append('- Coluna **Instalar antes**: itens do registro que o item importa e não traz. Se o CLI já traz a cadeia (registryDependencies), a coluna diz isso. Se não, lista o que instalar à mão, na ordem. Sem essa cadeia, o import quebra.')
    L.append('- Coluna **Tier**: custo de renderização estimado pelo código (seção 2). Leia antes de escolher.')
    L.append('')
    L.append('## 2. Resumo por domínio e custo')
    L.append('')
    L.append('| Domínio | T1 | T2 | T3 | Total |')
    L.append('|---|---|---|---|---|')
    por_dom = defaultdict(Counter)
    for i in itens:
        por_dom[i['dominio']][i['tier']] += 1
    for chave, (titulo, _) in DOMINIOS.items():
        c = por_dom.get(chave)
        if not c:
            continue
        L.append(f'| {titulo} | {c[1]} | {c[2]} | {c[3]} | {sum(c.values())} |')
    tot = Counter(i['tier'] for i in itens)
    L.append(f'| **Total** | {tot[1]} | {tot[2]} | {tot[3]} | {total} |')
    L.append('')
    for n in (1, 2, 3):
        L.append(f'- {TIERS[n]}')
    L.append('')
    L.append('O tier é uma estimativa pelo código-fonte: dependências declaradas e padrões como `getContext`, `WebGL` ou `three`. Não é medição de desempenho. Meça no navegador antes de decidir por um item T2 ou T3 em página crítica.')
    L.append('')
    L.append('## 3. Flags de decisão')
    L.append('')
    n_cliente = Counter(i['cliente'] for i in itens)
    n_reduz = Counter(i['reduzido'] for i in itens)
    n_dep = sum(1 for i in itens if i['depuracao'])
    n_falta = sum(1 for i in itens if i['faltam'])
    mouse_total = sum(1 for i in itens if i['toque'] != '—')
    mouse_tocc = sum(1 for i in itens if i['toque'] == 'sim')
    L.append(f'- **Use client:** {n_cliente["sim"]} com a diretiva no arquivo principal; {n_cliente["verificar"]} com hook num arquivo sem a diretiva (verificar o grafo de importação); {n_cliente["não precisa"]} sem hooks.')
    L.append(f'- **Movimento reduzido tratado no código:** {n_reduz["sim"]} sim; {n_reduz["não"]} não. Quando não tratam, adicione a checagem (skill integrating-external-ui-components).')
    L.append(f'- **Toque:** {mouse_total} itens respondem ao ponteiro; {mouse_tocc} mostram sinal de tratamento para toque. Os demais precisam de fallback antes de publicar.')
    L.append(f'- **Depuração:** {n_dep} itens importam `lil-gui`, painel de controles para desenvolvimento. Remova antes de publicar.')
    n_manual = sum(1 for i in itens if any(n not in i['alcance'] for n in i['instalar']))
    L.append(f'- **Instalar antes:** {n_falta} itens importam arquivos que não vêm no próprio item. Destes, {n_manual} precisam de instalação à mão, porque o CLI não traz a cadeia.')
    L.append('')
    L.append('## 4. Domínios e itens')
    L.append('')
    L.append('Colunas: **Tier** (seção 2), **Use client**, **Mov. reduzido**, **Toque** (— quando o item não depende de ponteiro), **Deps** (npm), **Faltam**.')
    L.append('')
    por_chave = defaultdict(list)
    for i in itens:
        por_chave[i['dominio']].append(i)
    for chave, (titulo, descricao) in DOMINIOS.items():
        lista = por_chave.get(chave)
        if not lista:
            continue
        L.append(f'### {titulo} ({len(lista)})')
        L.append('')
        L.append(descricao)
        L.append('')
        L.append('| Item | Fonte | Tier | Use client | Mov. reduzido | Toque | Deps | Instalar antes |')
        L.append('|---|---|---|---|---|---|---|---|')
        for i in sorted(lista, key=lambda x: (x['tier'], x['nome'])):
            deps_lista = [d for d in i['deps'] if d != 'lil-gui']
            if i['depuracao']:
                deps_lista.append('lil-gui (depuração)')
            deps = ', '.join(deps_lista) or '—'
            L.append(f"| `{i['nome']}` | {FONTES[i['fonte']]['titulo']} | T{i['tier']} | {i['cliente']} | {i['reduzido']} | {i['toque']} | {celula(deps)} | {celula(linha_faltam(i))} |")
        L.append('')
    L.append('## 5. Fontes e licenças')
    L.append('')
    for fonte, cfg in FONTES.items():
        L.append(f"- **{cfg['titulo']}** ({cfg['repo']}), {origens[fonte]}. "
                 f"URL de instalação: `{cfg['url']}`. Licença: {cfg['licenca']}")
    L.append('- Estes repositórios não são submódulos do hub. Os clones servem só para gerar esta referência. Em uso, a skill baixa pela URL de cada item, sem clonar.')
    L.append('')
    L.append('## 6. Como regenerar')
    L.append('')
    L.append('```bash')
    L.append('python scripts/gerar_catalogo_componentes.py')
    L.append('```')
    L.append('')
    L.append('Sem argumentos, lê os registros ao vivo. Para gerar offline, passe `--pixel-perfect <clone>` ou `--componentry <clone>`. Depois de regenerar, confira a origem na seção 5 e rode `python scripts/validate_skills.py`.')
    L.append('')
    saida.parent.mkdir(parents=True, exist_ok=True)
    saida.write_text('\n'.join(L), encoding='utf-8', newline='\n')
    return total


def principal(argv=None):
    p = argparse.ArgumentParser(description='Gera o catálogo de componentes animados.')
    p.add_argument('--pixel-perfect', default=None, help='clone local do Pixel-Perfect (offline); sem ele, lê ao vivo')
    p.add_argument('--componentry', default=None, help='clone local do Componentry (offline); sem ele, lê ao vivo')
    p.add_argument('--saida', default=str(SAIDA_PADRAO), help='arquivo reference.md de saída')
    args = p.parse_args(argv)
    clones = {'pixel-perfect': args.pixel_perfect, 'componentry': args.componentry}
    origens = {}
    for fonte, clone in clones.items():
        if clone:
            origens[fonte] = f'commit `{commit_do_clone(clone)}` (clone local)'
        else:
            origens[fonte] = f'lido ao vivo em {date.today().isoformat()} a partir de {FONTES[fonte]["indice"]}'
    itens = coletar(clones)
    total = escrever(itens, origens, Path(args.saida))
    print(f'itens: {total}  saída: {args.saida}')
    for fonte, origem in origens.items():
        print(f'  {fonte}: {origem}')
    return 0


if __name__ == '__main__':
    sys.exit(principal())
