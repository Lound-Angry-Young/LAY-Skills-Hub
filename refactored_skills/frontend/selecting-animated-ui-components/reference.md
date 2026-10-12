## Table of Contents
1. Como usar este catálogo
2. Resumo por domínio e custo
3. Flags de decisão
4. Domínios e itens
5. Fontes e licenças
6. Como regenerar

## 1. Como usar este catálogo

Este arquivo foi gerado por `scripts/gerar_catalogo_componentes.py` a partir de 357 registros shadcn (Pixel-Perfect: 300; Componentry: 57). Não edite à mão: regenere.

- Instalar um item: `npx shadcn@latest add <url>`, com a URL da coluna da fonte (seção 5).
- Coluna **Instalar antes**: itens do registro que o item importa e não traz. Se o CLI já traz a cadeia (registryDependencies), a coluna diz isso. Se não, lista o que instalar à mão, na ordem. Sem essa cadeia, o import quebra.
- Coluna **Tier**: custo de renderização estimado pelo código (seção 2). Leia antes de escolher.

## 2. Resumo por domínio e custo

| Domínio | T1 | T2 | T3 | Total |
|---|---|---|---|---|
| Texto animado | 3 | 37 | 0 | 40 |
| Botões e CTAs | 22 | 21 | 0 | 43 |
| Revelação e transição de imagem | 0 | 18 | 19 | 37 |
| Efeitos contínuos sobre imagem | 0 | 2 | 38 | 40 |
| Galerias e carrosséis | 1 | 29 | 5 | 35 |
| Scroll e seções | 1 | 8 | 3 | 12 |
| Cursor e interação | 0 | 15 | 15 | 30 |
| Fundos animados | 1 | 19 | 29 | 49 |
| Cards e widgets | 4 | 18 | 0 | 22 |
| 3D e perspectiva | 0 | 12 | 4 | 16 |
| SVG, logos e bordas | 5 | 16 | 0 | 21 |
| Navegação e chat | 1 | 2 | 0 | 3 |
| Blocos de página | 3 | 0 | 1 | 4 |
| Base técnica | 1 | 1 | 3 | 5 |
| **Total** | 42 | 198 | 117 | 357 |

- T1: CSS e DOM. Sem biblioteca de animação e sem canvas. Menor custo.
- T2: biblioteca de animação (GSAP, Framer Motion ou Motion) ou canvas 2D. Custo moderado, em JavaScript.
- T3: WebGL ou Three.js. Renderiza na GPU a cada quadro. Maior custo.

O tier é uma estimativa pelo código-fonte: dependências declaradas e padrões como `getContext`, `WebGL` ou `three`. Não é medição de desempenho. Meça no navegador antes de decidir por um item T2 ou T3 em página crítica.

## 3. Flags de decisão

- **Use client:** 268 com a diretiva no arquivo principal; 60 com hook num arquivo sem a diretiva (verificar o grafo de importação); 29 sem hooks.
- **Movimento reduzido tratado no código:** 78 sim; 279 não. Quando não tratam, adicione a checagem (skill integrating-external-ui-components).
- **Toque:** 94 itens respondem ao ponteiro; 13 mostram sinal de tratamento para toque. Os demais precisam de fallback antes de publicar.
- **Depuração:** 17 itens importam `lil-gui`, painel de controles para desenvolvimento. Remova antes de publicar.
- **Instalar antes:** 95 itens importam arquivos que não vêm no próprio item. Destes, 4 precisam de instalação à mão, porque o CLI não traz a cadeia.

## 4. Domínios e itens

Colunas: **Tier** (seção 2), **Use client**, **Mov. reduzido**, **Toque** (— quando o item não depende de ponteiro), **Deps** (npm), **Faltam**.

### Texto animado (40)

Títulos, frases e palavras com entrada, loop ou efeito de digitação.

| Item | Fonte | Tier | Use client | Mov. reduzido | Toque | Deps | Instalar antes |
|---|---|---|---|---|---|---|---|
| `annotated-text` | Componentry | T1 | sim | sim | — | — | — |
| `text-gradient` | Pixel-Perfect | T1 | não precisa | não | — | — | — |
| `text-video` | Pixel-Perfect | T1 | não precisa | não | — | — | — |
| `cursor-driven-particle-typography` | Componentry | T2 | sim | não | sim | — | — |
| `custom` | Pixel-Perfect | T2 | sim | não | — | @gsap/react, gsap | instalar à mão, nesta ordem: `engine` |
| `effects` | Pixel-Perfect | T2 | não precisa | não | — | gsap | — |
| `flipping-word-swap` | Componentry | T2 | sim | sim | sim | gsap | — |
| `gooey-text` | Pixel-Perfect | T2 | sim | não | não | @gsap/react, gsap | — |
| `kinetic-text-reveal` | Componentry | T2 | sim | sim | — | framer-motion | — |
| `letter-cascade` | Componentry | T2 | sim | não | não | framer-motion | — |
| `line-hover` | Pixel-Perfect | T2 | sim | não | não | @gsap/react, gsap | — |
| `scroll-based-velocity` | Componentry | T2 | sim | não | — | framer-motion | — |
| `stagger-1` | Pixel-Perfect | T2 | verificar | não | — | @gsap/react, gsap | instalar à mão, nesta ordem: `3d-button` |
| `text-along-path` | Pixel-Perfect | T2 | sim | não | — | gsap | — |
| `text-assemble` | Pixel-Perfect | T2 | sim | não | — | @gsap/react, gsap | — |
| `text-black-hole` | Pixel-Perfect | T2 | sim | não | — | @gsap/react, framer-motion, gsap | — |
| `text-block-transitions` | Pixel-Perfect | T2 | sim | não | — | @gsap/react, gsap | — |
| `text-broken-glass` | Pixel-Perfect | T2 | sim | não | — | @gsap/react, framer-motion, gsap | — |
| `text-burn-neon` | Pixel-Perfect | T2 | sim | não | — | @gsap/react, framer-motion, gsap | — |
| `text-editor-italic` | Pixel-Perfect | T2 | sim | não | não | framer-motion, lucide-react | — |
| `text-fade` | Pixel-Perfect | T2 | sim | não | — | @gsap/react, gsap | — |
| `text-glitch-portal` | Pixel-Perfect | T2 | sim | não | — | @gsap/react, framer-motion, gsap | — |
| `text-highlight-wave` | Pixel-Perfect | T2 | sim | sim | — | @gsap/react, gsap | — |
| `text-inertia` | Pixel-Perfect | T2 | sim | não | não | @gsap/react, gsap | — |
| `text-inline-chip-reveal` | Pixel-Perfect | T2 | sim | sim | — | motion | — |
| `text-matrix-rain` | Pixel-Perfect | T2 | sim | não | — | @gsap/react, framer-motion, gsap | — |
| `text-morph` | Componentry | T2 | sim | sim | — | clsx, tailwind-merge | — |
| `text-reveal` | Pixel-Perfect | T2 | sim | não | — | @gsap/react, framer-motion, gsap | — |
| `text-reveal2` | Pixel-Perfect | T2 | sim | não | — | @gsap/react, framer-motion, gsap | — |
| `text-scatter` | Pixel-Perfect | T2 | sim | não | — | @gsap/react, framer-motion, gsap | — |
| `text-scatter1` | Pixel-Perfect | T2 | sim | não | — | @gsap/react, framer-motion, gsap | — |
| `text-typewriter-glitch` | Pixel-Perfect | T2 | sim | não | — | @gsap/react, framer-motion, gsap | — |
| `text-x-rotate` | Pixel-Perfect | T2 | sim | não | — | @gsap/react, framer-motion, gsap | — |
| `text-x-rotate2` | Pixel-Perfect | T2 | sim | não | — | @gsap/react, gsap | — |
| `text-y-animation` | Pixel-Perfect | T2 | sim | não | — | @gsap/react, framer-motion, gsap | — |
| `text-y-animation2` | Pixel-Perfect | T2 | sim | não | — | @gsap/react, framer-motion, gsap | — |
| `text-y-animation3` | Pixel-Perfect | T2 | sim | não | — | @gsap/react, framer-motion, gsap | — |
| `text-y-animation4` | Pixel-Perfect | T2 | sim | não | — | @gsap/react, framer-motion, gsap | — |
| `text-z-rotate` | Pixel-Perfect | T2 | sim | não | — | @gsap/react, framer-motion, gsap | — |
| `text-z-rotate2` | Pixel-Perfect | T2 | sim | não | — | @gsap/react, framer-motion, gsap | — |

### Botões e CTAs (43)

Botões de ação, toggles e controles com resposta a hover e clique.

| Item | Fonte | Tier | Use client | Mov. reduzido | Toque | Deps | Instalar antes |
|---|---|---|---|---|---|---|---|
| `abhinav-bento-button` | Pixel-Perfect | T1 | sim | não | — | — | — |
| `bevel-button` | Pixel-Perfect | T1 | sim | não | — | — | — |
| `book-demo-button` | Pixel-Perfect | T1 | sim | sim | — | — | — |
| `border-gradient-button` | Pixel-Perfect | T1 | não precisa | não | — | — | shadcn: `button` (`@/components/ui/button`) |
| `framer-cta-button` | Pixel-Perfect | T1 | sim | não | — | react-icons | — |
| `glass-button` | Pixel-Perfect | T1 | não precisa | não | — | — | — |
| `glass-circle-button` | Pixel-Perfect | T1 | sim | não | — | lucide-react | — |
| `glass-icon-button` | Pixel-Perfect | T1 | sim | não | — | lucide-react | — |
| `glass-square-button` | Pixel-Perfect | T1 | não precisa | não | — | — | — |
| `glassy-button` | Pixel-Perfect | T1 | sim | não | sim | lucide-react | — |
| `liquid-button` | Pixel-Perfect | T1 | sim | não | — | — | — |
| `matte-dark-button` | Pixel-Perfect | T1 | não precisa | não | — | — | — |
| `matte-shadow-button` | Pixel-Perfect | T1 | não precisa | não | — | — | — |
| `metal-button` | Pixel-Perfect | T1 | não precisa | não | — | — | — |
| `orange-premium-button` | Pixel-Perfect | T1 | não precisa | não | — | — | — |
| `pixel-credits-button` | Pixel-Perfect | T1 | não precisa | não | — | — | — |
| `premium-button` | Pixel-Perfect | T1 | não precisa | não | — | — | — |
| `rainbow-glowing-button` | Pixel-Perfect | T1 | sim | não | — | — | — |
| `recessed-stepper-button` | Pixel-Perfect | T1 | sim | não | — | — | — |
| `silver-button` | Pixel-Perfect | T1 | sim | não | — | — | — |
| `soft-pill-button` | Pixel-Perfect | T1 | sim | não | — | — | — |
| `stripe-button` | Pixel-Perfect | T1 | não precisa | não | — | — | — |
| `3d-button` | Pixel-Perfect | T2 | sim | não | não | @gsap/react, gsap | — |
| `antinomy-button` | Pixel-Perfect | T2 | sim | sim | — | motion | — |
| `blue-chrome-button` | Pixel-Perfect | T2 | sim | não | — | framer-motion | — |
| `blur-toggle-button` | Pixel-Perfect | T2 | sim | não | — | framer-motion, lucide-react | — |
| `color-flair-button` | Pixel-Perfect | T2 | verificar | não | não | @gsap/react, gsap | — |
| `cyber-button` | Pixel-Perfect | T2 | sim | não | — | framer-motion | — |
| `free-premium-toggle` | Pixel-Perfect | T2 | sim | não | — | framer-motion | — |
| `goe-button` | Pixel-Perfect | T2 | sim | não | — | framer-motion, lucide-react | — |
| `learn-more-button` | Pixel-Perfect | T2 | sim | não | — | framer-motion | — |
| `liquid-gradient-button` | Pixel-Perfect | T2 | sim | não | — | framer-motion, lucide-react | shadcn: `spinner` (`@/components/ui/spinner`) |
| `mitosis-button` | Pixel-Perfect | T2 | sim | sim | — | lucide-react, motion | — |
| `morph-button` | Pixel-Perfect | T2 | sim | não | não | @gsap/react, gsap | — |
| `morph-image-button` | Pixel-Perfect | T2 | sim | não | não | @gsap/react, gsap | shadcn: `button` (`@/components/ui/button`) |
| `mouse-follower-button` | Pixel-Perfect | T2 | sim | não | não | @gsap/react, gsap | shadcn: `button` (`@/components/ui/button`) |
| `pearl-toggle-button` | Pixel-Perfect | T2 | sim | não | — | framer-motion | — |
| `prism-glass-button` | Pixel-Perfect | T2 | sim | não | — | framer-motion | — |
| `radial-gradient-button` | Pixel-Perfect | T2 | sim | não | — | framer-motion, lucide-react | shadcn: `spinner` (`@/components/ui/spinner`) |
| `shiny-button` | Pixel-Perfect | T2 | sim | não | — | @gsap/react, gsap | shadcn: `button` (`@/components/ui/button`) |
| `squircle-counter-button` | Pixel-Perfect | T2 | sim | não | — | framer-motion | — |
| `toggle-button` | Pixel-Perfect | T2 | sim | não | — | framer-motion | — |
| `visit-button` | Pixel-Perfect | T2 | verificar | não | — | framer-motion, lucide-react | — |

### Revelação e transição de imagem (37)

Troca ou abertura de imagem por máscara, corte ou transição, geralmente disparada por scroll ou hover.

| Item | Fonte | Tier | Use client | Mov. reduzido | Toque | Deps | Instalar antes |
|---|---|---|---|---|---|---|---|
| `aperture-mask-reveal` | Pixel-Perfect | T2 | sim | não | — | gsap | — |
| `blinds-mask-reveal` | Pixel-Perfect | T2 | sim | não | — | gsap | — |
| `brush-mask-reveal` | Pixel-Perfect | T2 | sim | não | — | gsap | — |
| `center-split-reveal` | Pixel-Perfect | T2 | sim | não | — | gsap | — |
| `clock-mask-reveal` | Pixel-Perfect | T2 | sim | não | — | gsap | — |
| `directional-mask-reveal` | Pixel-Perfect | T2 | sim | não | — | gsap | — |
| `flip-text-reveal` | Pixel-Perfect | T2 | sim | não | — | framer-motion, gsap | — |
| `ink-blob-mask-reveal` | Pixel-Perfect | T2 | sim | não | — | gsap | — |
| `iris-mask-reveal` | Pixel-Perfect | T2 | sim | não | — | gsap | — |
| `keyhole-mask-reveal` | Pixel-Perfect | T2 | sim | não | — | gsap | — |
| `mosaic-mask-reveal` | Pixel-Perfect | T2 | sim | não | — | gsap | — |
| `pinwheel-mask-reveal` | Pixel-Perfect | T2 | sim | não | — | gsap | — |
| `rect-mask-reveal` | Pixel-Perfect | T2 | sim | não | — | gsap | — |
| `sonar-mask-reveal` | Pixel-Perfect | T2 | sim | não | — | gsap | — |
| `spotlight-mask-reveal` | Pixel-Perfect | T2 | sim | não | não | gsap | — |
| `star-mask-reveal` | Pixel-Perfect | T2 | sim | não | — | gsap | — |
| `text-zoom-mask-reveal` | Pixel-Perfect | T2 | sim | não | — | gsap | — |
| `wave-mask-reveal` | Pixel-Perfect | T2 | sim | não | — | gsap | — |
| `bend-image-reveal` | Pixel-Perfect | T3 | sim | não | — | @react-three/fiber, gsap, three | — |
| `cursor-reveal` | Pixel-Perfect | T3 | sim | não | não | three | o CLI traz a cadeia (registryDependencies) |
| `img-blinds-transition` | Pixel-Perfect | T3 | sim | não | — | — | o CLI traz a cadeia (registryDependencies) |
| `img-burn-dissolve` | Pixel-Perfect | T3 | sim | não | — | — | o CLI traz a cadeia (registryDependencies) |
| `img-checker-flip` | Pixel-Perfect | T3 | sim | não | — | — | o CLI traz a cadeia (registryDependencies) |
| `img-liquid-transition` | Pixel-Perfect | T3 | sim | não | — | — | o CLI traz a cadeia (registryDependencies) |
| `img-pixel-dissolve` | Pixel-Perfect | T3 | sim | não | — | — | o CLI traz a cadeia (registryDependencies) |
| `img-pixel-melt-transition` | Pixel-Perfect | T3 | sim | não | — | — | o CLI traz a cadeia (registryDependencies) |
| `img-pixel-rise-reveal` | Pixel-Perfect | T3 | sim | não | — | — | o CLI traz a cadeia (registryDependencies) |
| `img-ripple-reveal` | Pixel-Perfect | T3 | sim | não | — | — | o CLI traz a cadeia (registryDependencies) |
| `img-spotlight-reveal` | Pixel-Perfect | T3 | sim | não | — | — | o CLI traz a cadeia (registryDependencies) |
| `img-wipe-reveal` | Pixel-Perfect | T3 | sim | não | — | — | o CLI traz a cadeia (registryDependencies) |
| `img-zoom-blur-transition` | Pixel-Perfect | T3 | sim | não | — | — | o CLI traz a cadeia (registryDependencies) |
| `liquid-melt` | Pixel-Perfect | T3 | sim | não | não | three, lil-gui (depuração) | o CLI traz a cadeia (registryDependencies) |
| `noise-dissolve-reveal` | Pixel-Perfect | T3 | sim | não | — | gsap, three | — |
| `noise-mask-reveal` | Pixel-Perfect | T3 | sim | não | — | gsap, three | — |
| `paint-reveal` | Pixel-Perfect | T3 | sim | não | — | gsap, three, lil-gui (depuração) | o CLI traz a cadeia (registryDependencies) |
| `ripple-transition` | Componentry | T3 | sim | não | — | framer-motion | — |
| `seventies-melt` | Pixel-Perfect | T3 | sim | não | — | — | o CLI traz a cadeia (registryDependencies) |

### Efeitos contínuos sobre imagem (40)

Filtros, distorções e estilizações aplicados a uma imagem (shaders).

| Item | Fonte | Tier | Use client | Mov. reduzido | Toque | Deps | Instalar antes |
|---|---|---|---|---|---|---|---|
| `ascii-effect` | Componentry | T2 | sim | sim | não | — | — |
| `dithered-logo` | Componentry | T2 | sim | não | sim | — | — |
| `image-ripple-effect` | Componentry | T3 | verificar | não | não | three, @types/three, @react-three/fiber, @react-three/drei | — |
| `img-anaglyph` | Pixel-Perfect | T3 | sim | não | — | — | o CLI traz a cadeia (registryDependencies) |
| `img-ascii-art` | Pixel-Perfect | T3 | sim | não | — | — | o CLI traz a cadeia (registryDependencies) |
| `img-ballpoint-drawing` | Pixel-Perfect | T3 | sim | não | — | — | o CLI traz a cadeia (registryDependencies) |
| `img-chromatic-aberration` | Pixel-Perfect | T3 | sim | não | — | — | o CLI traz a cadeia (registryDependencies) |
| `img-comic-cel` | Pixel-Perfect | T3 | sim | não | — | — | o CLI traz a cadeia (registryDependencies) |
| `img-crt-scanlines` | Pixel-Perfect | T3 | sim | não | — | — | o CLI traz a cadeia (registryDependencies) |
| `img-crystallize` | Pixel-Perfect | T3 | sim | não | — | — | o CLI traz a cadeia (registryDependencies) |
| `img-depth-parallax` | Pixel-Perfect | T3 | sim | não | — | — | o CLI traz a cadeia (registryDependencies) |
| `img-dot-matrix-scatter` | Pixel-Perfect | T3 | sim | não | — | — | o CLI traz a cadeia (registryDependencies) |
| `img-duotone` | Pixel-Perfect | T3 | sim | não | — | — | o CLI traz a cadeia (registryDependencies) |
| `img-edge-sketch` | Pixel-Perfect | T3 | sim | não | — | — | o CLI traz a cadeia (registryDependencies) |
| `img-engraving` | Pixel-Perfect | T3 | sim | não | — | — | o CLI traz a cadeia (registryDependencies) |
| `img-gameboy` | Pixel-Perfect | T3 | sim | não | — | — | o CLI traz a cadeia (registryDependencies) |
| `img-glass-shatter` | Pixel-Perfect | T3 | sim | não | — | — | o CLI traz a cadeia (registryDependencies) |
| `img-glitch` | Pixel-Perfect | T3 | sim | não | — | — | o CLI traz a cadeia (registryDependencies) |
| `img-halftone` | Pixel-Perfect | T3 | sim | não | — | — | o CLI traz a cadeia (registryDependencies) |
| `img-hex-mosaic` | Pixel-Perfect | T3 | sim | não | — | — | o CLI traz a cadeia (registryDependencies) |
| `img-ink-bleed` | Pixel-Perfect | T3 | sim | não | — | — | o CLI traz a cadeia (registryDependencies) |
| `img-kaleidoscope` | Pixel-Perfect | T3 | sim | não | — | — | o CLI traz a cadeia (registryDependencies) |
| `img-led-dot-matrix` | Pixel-Perfect | T3 | sim | não | — | — | o CLI traz a cadeia (registryDependencies) |
| `img-low-poly` | Pixel-Perfect | T3 | sim | não | — | — | o CLI traz a cadeia (registryDependencies) |
| `img-magnifier-lens` | Pixel-Perfect | T3 | sim | não | — | — | o CLI traz a cadeia (registryDependencies) |
| `img-oil-paint` | Pixel-Perfect | T3 | sim | não | — | — | o CLI traz a cadeia (registryDependencies) |
| `img-ordered-dither` | Pixel-Perfect | T3 | sim | não | — | — | o CLI traz a cadeia (registryDependencies) |
| `img-pixel-distortion` | Pixel-Perfect | T3 | sim | não | — | — | o CLI traz a cadeia (registryDependencies) |
| `img-pixelate` | Pixel-Perfect | T3 | sim | não | — | — | o CLI traz a cadeia (registryDependencies) |
| `img-posterize` | Pixel-Perfect | T3 | sim | não | — | — | o CLI traz a cadeia (registryDependencies) |
| `img-ripple` | Pixel-Perfect | T3 | sim | não | — | — | o CLI traz a cadeia (registryDependencies) |
| `img-shery-cyber-squares` | Pixel-Perfect | T3 | sim | não | — | — | o CLI traz a cadeia (registryDependencies) |
| `img-shery-liquid` | Pixel-Perfect | T3 | sim | não | — | — | o CLI traz a cadeia (registryDependencies) |
| `img-shery-liquid-cursor` | Pixel-Perfect | T3 | sim | não | — | — | o CLI traz a cadeia (registryDependencies) |
| `img-shery-perlin` | Pixel-Perfect | T3 | sim | não | — | — | o CLI traz a cadeia (registryDependencies) |
| `img-shery-wind` | Pixel-Perfect | T3 | sim | não | — | — | o CLI traz a cadeia (registryDependencies) |
| `img-thermal-vision` | Pixel-Perfect | T3 | sim | não | — | — | o CLI traz a cadeia (registryDependencies) |
| `img-twirl` | Pixel-Perfect | T3 | sim | não | — | — | o CLI traz a cadeia (registryDependencies) |
| `img-vhs` | Pixel-Perfect | T3 | sim | não | — | — | o CLI traz a cadeia (registryDependencies) |
| `img-wave` | Pixel-Perfect | T3 | sim | não | — | — | o CLI traz a cadeia (registryDependencies) |

### Galerias e carrosséis (35)

Coleções de imagens ou cards com navegação, órbita ou empilhamento.

| Item | Fonte | Tier | Use client | Mov. reduzido | Toque | Deps | Instalar antes |
|---|---|---|---|---|---|---|---|
| `photo-flip-wall` | Pixel-Perfect | T1 | verificar | sim | não | — | — |
| `accordion-carousel` | Pixel-Perfect | T2 | sim | não | — | framer-motion | — |
| `cards-slider` | Pixel-Perfect | T2 | sim | não | — | framer-motion | — |
| `case-study-flip-stack` | Componentry | T2 | sim | sim | — | framer-motion | — |
| `collection-surfer` | Componentry | T2 | sim | não | não | framer-motion | — |
| `cover-flow-carousel` | Pixel-Perfect | T2 | sim | não | não | — | — |
| `coverflow-marquee` | Pixel-Perfect | T2 | verificar | sim | — | framer-motion | — |
| `cylinder-carousel` | Pixel-Perfect | T2 | sim | sim | sim | framer-motion | — |
| `fanned-deck-carousel` | Pixel-Perfect | T2 | sim | não | não | — | — |
| `ferris-wheel-carousel` | Pixel-Perfect | T2 | sim | não | não | — | — |
| `infinite-carousel` | Pixel-Perfect | T2 | verificar | não | não | @gsap/react, gsap | — |
| `infinite-image-field` | Componentry | T2 | sim | não | não | — | — |
| `layered-stack` | Componentry | T2 | sim | não | não | gsap | — |
| `orbit-card-stack` | Componentry | T2 | sim | sim | não | framer-motion, lucide-react | — |
| `orbit-carousel` | Pixel-Perfect | T2 | sim | não | não | — | — |
| `perspective-deck-carousel` | Pixel-Perfect | T2 | sim | não | não | — | — |
| `photo-coverflow-cycle` | Pixel-Perfect | T2 | verificar | sim | — | @gsap/react, gsap | — |
| `photo-lemniscate-flight` | Pixel-Perfect | T2 | verificar | sim | — | @gsap/react, gsap | — |
| `photo-magnet-grid` | Pixel-Perfect | T2 | verificar | sim | não | — | — |
| `photo-ring-orbit` | Pixel-Perfect | T2 | verificar | sim | — | @gsap/react, gsap | — |
| `photo-sphere-drift` | Pixel-Perfect | T2 | verificar | sim | — | @gsap/react, gsap | — |
| `photo-spiral-vortex` | Pixel-Perfect | T2 | verificar | sim | — | @gsap/react, gsap | — |
| `photo-sweep-conveyor` | Pixel-Perfect | T2 | verificar | sim | — | @gsap/react, gsap | — |
| `radial-carousel` | Pixel-Perfect | T2 | verificar | não | — | @gsap/react, gsap | — |
| `rotating-ring-carousel` | Pixel-Perfect | T2 | verificar | sim | — | framer-motion | — |
| `scroll-direction-carousel` | Pixel-Perfect | T2 | verificar | não | — | @gsap/react, gsap | — |
| `slat-flip-carousel` | Pixel-Perfect | T2 | sim | não | — | framer-motion, lucide-react | — |
| `sliced-reveal-carousel` | Pixel-Perfect | T2 | sim | não | — | framer-motion, lucide-react | — |
| `toss-deck-carousel` | Pixel-Perfect | T2 | sim | não | — | framer-motion | — |
| `wheel-carousel` | Componentry | T2 | sim | sim | não | framer-motion, next-themes | — |
| `creative-space-gallery` | Pixel-Perfect | T3 | verificar | sim | não | three | — |
| `fisheye-infinite-grid` | Componentry | T3 | sim | sim | sim | — | — |
| `liquid-glass-carousel` | Componentry | T3 | sim | sim | sim | gsap, three | — |
| `newsletter-bookshelf` | Componentry | T3 | sim | sim | não | three, @react-three/fiber, lucide-react | — |
| `spiral-3d-slider` | Componentry | T3 | sim | sim | — | @react-three/fiber, clsx, tailwind-merge, three | — |

### Scroll e seções (12)

Efeitos ligados à rolagem: pin, sticky, parallax e revelação de seções.

| Item | Fonte | Tier | Use client | Mov. reduzido | Toque | Deps | Instalar antes |
|---|---|---|---|---|---|---|---|
| `footer-reveal` | Pixel-Perfect | T1 | sim | não | — | — | — |
| `hero-cover-reveal` | Pixel-Perfect | T2 | sim | não | — | @gsap/react, gsap | — |
| `project-slice-scroll` | Pixel-Perfect | T2 | sim | não | — | @gsap/react, gsap | — |
| `scroll-choreography` | Componentry | T2 | sim | não | — | framer-motion | — |
| `scroll-split-card` | Componentry | T2 | sim | não | — | framer-motion | — |
| `scroll-tilted-grid` | Componentry | T2 | sim | sim | — | framer-motion, lenis | — |
| `stacking-cards-parallax` | Pixel-Perfect | T2 | sim | não | — | framer-motion | — |
| `sticky-scroll-cards` | Componentry | T2 | sim | sim | — | framer-motion, lenis | — |
| `text-clip-mask-reveal` | Pixel-Perfect | T2 | sim | não | — | — | — |
| `fluid-cube-scroll` | Pixel-Perfect | T3 | sim | não | não | framer-motion, three | — |
| `glass-scroll-navbar` | Pixel-Perfect | T3 | verificar | não | — | — | — |
| `scroll-warp-gallery` | Pixel-Perfect | T3 | verificar | sim | não | @studio-freight/lenis, gsap, three | — |

### Cursor e interação (30)

Efeitos que respondem ao ponteiro: trails, ímãs, distorções e comparação.

| Item | Fonte | Tier | Use client | Mov. reduzido | Toque | Deps | Instalar antes |
|---|---|---|---|---|---|---|---|
| `bend-button-follower` | Pixel-Perfect | T2 | sim | não | não | — | — |
| `eye-tracking` | Componentry | T2 | sim | não | sim | framer-motion | — |
| `gravity-image-trail` | Pixel-Perfect | T2 | verificar | não | não | gsap | — |
| `image-trail` | Componentry | T2 | sim | não | não | gsap | — |
| `image-trail-effects` | Pixel-Perfect | T2 | verificar | não | não | — | — |
| `magnet-lines` | Componentry | T2 | sim | não | não | framer-motion | — |
| `motion-trail-classic` | Pixel-Perfect | T2 | verificar | não | não | gsap | — |
| `mouse-follower-1` | Pixel-Perfect | T2 | sim | não | não | @gsap/react, gsap | — |
| `mouse-follower-2` | Pixel-Perfect | T2 | sim | não | não | @gsap/react, gsap | shadcn: `button` (`@/components/ui/button`) |
| `pixel-canvas` | Componentry | T2 | sim | não | sim | — | — |
| `pixel-cursor-trail` | Pixel-Perfect | T2 | verificar | não | não | — | — |
| `pixel-displace-field` | Pixel-Perfect | T2 | verificar | sim | sim | — | — |
| `pixel-image-trail` | Componentry | T2 | sim | sim | não | — | — |
| `scale-image-trail` | Pixel-Perfect | T2 | verificar | não | não | gsap | — |
| `text-repel` | Componentry | T2 | sim | não | não | framer-motion | — |
| `before-after` | Pixel-Perfect | T3 | sim | não | não | three | o CLI traz a cadeia (registryDependencies) |
| `bend-mouse-follower` | Pixel-Perfect | T3 | sim | não | não | @react-three/fiber, gsap, three | — |
| `cursor-spotlight` | Pixel-Perfect | T3 | sim | não | — | — | o CLI traz a cadeia (registryDependencies) |
| `cursor-trail-smear` | Pixel-Perfect | T3 | sim | não | não | three, lil-gui (depuração) | o CLI traz a cadeia (registryDependencies) |
| `dither-cursor-trail` | Pixel-Perfect | T3 | verificar | sim | sim | — | — |
| `flow-field` | Pixel-Perfect | T3 | sim | não | não | three, lil-gui (depuração) | o CLI traz a cadeia (registryDependencies) |
| `fluid-image` | Pixel-Perfect | T3 | sim | não | não | three, lil-gui (depuração) | o CLI traz a cadeia (registryDependencies) |
| `image-particles` | Pixel-Perfect | T3 | sim | não | não | three, lil-gui (depuração) | o CLI traz a cadeia (registryDependencies) |
| `inertia-particles` | Pixel-Perfect | T3 | sim | não | não | three, lil-gui (depuração) | o CLI traz a cadeia (registryDependencies) |
| `jelly-bulge` | Pixel-Perfect | T3 | sim | não | não | three, lil-gui (depuração) | o CLI traz a cadeia (registryDependencies) |
| `magnetic-swarm` | Pixel-Perfect | T3 | sim | não | não | three, lil-gui (depuração) | o CLI traz a cadeia (registryDependencies) |
| `magnetic-warp` | Pixel-Perfect | T3 | sim | não | não | three, lil-gui (depuração) | o CLI traz a cadeia (registryDependencies) |
| `pixel-distortion` | Pixel-Perfect | T3 | sim | não | não | three, lil-gui (depuração) | o CLI traz a cadeia (registryDependencies) |
| `ripple-touch` | Pixel-Perfect | T3 | sim | não | não | three, lil-gui (depuração) | o CLI traz a cadeia (registryDependencies) |
| `vortex-pull` | Pixel-Perfect | T3 | sim | não | não | three, lil-gui (depuração) | o CLI traz a cadeia (registryDependencies) |

### Fundos animados (49)

Planos de fundo de hero e seções, em CSS, canvas ou shader.

| Item | Fonte | Tier | Use client | Mov. reduzido | Toque | Deps | Instalar antes |
|---|---|---|---|---|---|---|---|
| `red-fire` | Pixel-Perfect | T1 | sim | não | — | — | — |
| `arrow-letter-background` | Pixel-Perfect | T2 | verificar | sim | não | — | — |
| `bayer-sunset-background` | Pixel-Perfect | T2 | verificar | sim | — | — | — |
| `braille-terrain-background` | Pixel-Perfect | T2 | verificar | sim | — | — | — |
| `brick-blobs-background` | Pixel-Perfect | T2 | verificar | sim | não | — | — |
| `cd` | Pixel-Perfect | T2 | sim | não | — | — | — |
| `checker-blocks-background` | Pixel-Perfect | T2 | verificar | sim | não | — | — |
| `currency-sky-background` | Pixel-Perfect | T2 | verificar | sim | — | — | — |
| `dither-field-background` | Pixel-Perfect | T2 | verificar | sim | — | — | — |
| `dither-gradient` | Componentry | T2 | sim | não | — | — | — |
| `glyph-blocks-background` | Pixel-Perfect | T2 | verificar | sim | — | — | — |
| `halftone-blobs-background` | Pixel-Perfect | T2 | verificar | sim | — | — | — |
| `matrix-rain` | Componentry | T2 | sim | não | — | — | — |
| `misprint-background` | Pixel-Perfect | T2 | verificar | sim | não | — | — |
| `op-art-stripes-background` | Pixel-Perfect | T2 | verificar | sim | não | — | — |
| `particle-shape-morph` | Pixel-Perfect | T2 | sim | sim | — | @gsap/react, gsap | — |
| `pixel-map-background` | Pixel-Perfect | T2 | verificar | sim | — | — | — |
| `sparkle-grid-background` | Pixel-Perfect | T2 | verificar | sim | não | — | — |
| `truchet-weave-background` | Pixel-Perfect | T2 | verificar | sim | — | — | — |
| `vector-field-background` | Pixel-Perfect | T2 | verificar | sim | não | — | — |
| `animated-gradient` | Componentry | T3 | sim | não | — | — | — |
| `aurora-curtain` | Pixel-Perfect | T3 | sim | não | — | — | o CLI traz a cadeia (registryDependencies) |
| `aurora-flow` | Componentry | T3 | sim | sim | não | clsx, tailwind-merge | — |
| `closing-plasma` | Componentry | T3 | sim | não | não | clsx, tailwind-merge | — |
| `contour-map-background` | Pixel-Perfect | T3 | verificar | sim | — | — | — |
| `day-night-sky` | Pixel-Perfect | T3 | sim | não | — | three | — |
| `dither-prism-hero` | Componentry | T3 | sim | não | — | @react-three/fiber, @react-three/drei, three, framer-motion | — |
| `dither-wave-background` | Pixel-Perfect | T3 | verificar | sim | sim | gsap | — |
| `dreamy-clouds` | Pixel-Perfect | T3 | sim | não | — | — | o CLI traz a cadeia (registryDependencies) |
| `drifting-clouds` | Pixel-Perfect | T3 | sim | não | — | — | o CLI traz a cadeia (registryDependencies) |
| `gentle-waves` | Pixel-Perfect | T3 | sim | não | — | — | o CLI traz a cadeia (registryDependencies) |
| `god-rays` | Pixel-Perfect | T3 | sim | não | — | — | o CLI traz a cadeia (registryDependencies) |
| `grain-gradient` | Componentry | T3 | sim | sim | — | — | — |
| `kaleidoscope` | Pixel-Perfect | T3 | sim | não | — | — | o CLI traz a cadeia (registryDependencies) |
| `liquid-caustics` | Pixel-Perfect | T3 | sim | não | — | — | o CLI traz a cadeia (registryDependencies) |
| `liquid-chrome` | Componentry | T3 | sim | não | não | — | — |
| `liquid-metal` | Pixel-Perfect | T3 | sim | não | — | — | o CLI traz a cadeia (registryDependencies) |
| `mesh-gradient` | Pixel-Perfect | T3 | sim | não | — | — | o CLI traz a cadeia (registryDependencies) |
| `metaballs` | Pixel-Perfect | T3 | sim | não | — | — | o CLI traz a cadeia (registryDependencies) |
| `neon-rings` | Pixel-Perfect | T3 | sim | não | — | — | o CLI traz a cadeia (registryDependencies) |
| `neuro-noise` | Pixel-Perfect | T3 | sim | não | — | — | o CLI traz a cadeia (registryDependencies) |
| `plasma-flow` | Pixel-Perfect | T3 | sim | não | — | — | o CLI traz a cadeia (registryDependencies) |
| `prism-gradient` | Componentry | T3 | sim | sim | — | next-themes, clsx, tailwind-merge | — |
| `silk-aurora` | Componentry | T3 | sim | sim | não | — | — |
| `smoke-ring` | Pixel-Perfect | T3 | sim | não | — | — | o CLI traz a cadeia (registryDependencies) |
| `spectral-ribbon` | Componentry | T3 | sim | sim | — | — | — |
| `voronoi-glass` | Pixel-Perfect | T3 | sim | não | — | — | o CLI traz a cadeia (registryDependencies) |
| `wave-lines` | Pixel-Perfect | T3 | sim | não | — | — | o CLI traz a cadeia (registryDependencies) |
| `webgl-liquid` | Componentry | T3 | sim | não | — | clsx, tailwind-merge | — |

### Cards e widgets (22)

Cartões e pequenos painéis de interface com animação própria.

| Item | Fonte | Tier | Use client | Mov. reduzido | Toque | Deps | Instalar antes |
|---|---|---|---|---|---|---|---|
| `dial-knob-motion` | Pixel-Perfect | T1 | sim | não | não | — | — |
| `hover-transition` | Componentry | T1 | sim | sim | sim | clsx, tailwind-merge | — |
| `mac-keyboard` | Componentry | T1 | sim | não | — | lucide-react | — |
| `split-flap-display` | Componentry | T1 | sim | não | — | — | — |
| `car-lock-drive-motion` | Pixel-Perfect | T2 | sim | não | — | framer-motion, lucide-react | — |
| `card-animation` | Pixel-Perfect | T2 | verificar | não | — | framer-motion, lucide-react, motion | instalar à mão, nesta ordem: `text-burn-neon` → `text-matrix-rain`; shadcn: `button` (`@/components/ui/button`) |
| `cd-envelope-player` | Pixel-Perfect | T2 | sim | sim | — | lucide-react, motion | — |
| `circuit-board` | Componentry | T2 | sim | não | — | framer-motion | — |
| `coin-spin-animation` | Pixel-Perfect | T2 | sim | não | — | framer-motion | — |
| `fisheye-faq` | Pixel-Perfect | T2 | verificar | sim | não | motion | — |
| `flight-status-card` | Componentry | T2 | sim | não | — | framer-motion | — |
| `github-calendar` | Componentry | T2 | sim | não | não | framer-motion | — |
| `hover-expand-player` | Pixel-Perfect | T2 | verificar | sim | — | framer-motion, lucide-react | — |
| `image-hover-animation` | Pixel-Perfect | T2 | sim | não | não | framer-motion | — |
| `inertia-arrow-card` | Pixel-Perfect | T2 | verificar | não | não | @gsap/react, gsap, motion | — |
| `lens-clock` | Componentry | T2 | sim | sim | — | framer-motion | — |
| `milestone-odometer` | Pixel-Perfect | T2 | sim | não | — | framer-motion | — |
| `music-player` | Componentry | T2 | sim | não | — | framer-motion | — |
| `orbit-dot-motion` | Pixel-Perfect | T2 | sim | não | — | framer-motion | — |
| `success-ripple-animation` | Pixel-Perfect | T2 | sim | não | — | framer-motion | — |
| `tab-background-animation` | Pixel-Perfect | T2 | sim | não | não | framer-motion | — |
| `yoga-invite-card` | Pixel-Perfect | T2 | sim | não | — | framer-motion | — |

### 3D e perspectiva (16)

Objetos e cards em 3D, em CSS 3D ou Three.js.

| Item | Fonte | Tier | Use client | Mov. reduzido | Toque | Deps | Instalar antes |
|---|---|---|---|---|---|---|---|
| `accordion-fold` | Pixel-Perfect | T2 | verificar | sim | — | framer-motion | — |
| `depth-tunnel` | Pixel-Perfect | T2 | verificar | sim | — | framer-motion | — |
| `exploding-dice-cube` | Pixel-Perfect | T2 | verificar | sim | não | framer-motion | — |
| `flip-clock-counter` | Pixel-Perfect | T2 | verificar | sim | — | framer-motion | — |
| `flip-tile-wave` | Pixel-Perfect | T2 | verificar | sim | — | framer-motion | — |
| `helix-spinner` | Pixel-Perfect | T2 | verificar | sim | — | framer-motion | — |
| `hover-layer-stack` | Pixel-Perfect | T2 | verificar | sim | — | framer-motion | — |
| `perspective-text-crawl` | Pixel-Perfect | T2 | verificar | sim | — | framer-motion | — |
| `spinning-cube-motion` | Pixel-Perfect | T2 | verificar | sim | — | framer-motion | — |
| `swing-door-reveal` | Pixel-Perfect | T2 | verificar | sim | — | framer-motion | — |
| `swinging-sign` | Pixel-Perfect | T2 | verificar | sim | — | framer-motion | — |
| `tilt-card-glare` | Pixel-Perfect | T2 | verificar | sim | não | framer-motion | — |
| `blob-sphere` | Pixel-Perfect | T3 | sim | não | — | @react-three/drei, @react-three/fiber, three, lil-gui (depuração) | — |
| `floating-logo-intro` | Pixel-Perfect | T3 | sim | não | não | @react-three/drei, @react-three/fiber, framer-motion, three | — |
| `raycaster-shapes` | Pixel-Perfect | T3 | sim | não | — | @react-three/drei, @react-three/fiber, three | — |
| `twisted-blob` | Pixel-Perfect | T3 | sim | não | — | @react-three/drei, @react-three/fiber, three, lil-gui (depuração) | — |

### SVG, logos e bordas (21)

Ícones, logos, traçados SVG e molduras decorativas.

| Item | Fonte | Tier | Use client | Mov. reduzido | Toque | Deps | Instalar antes |
|---|---|---|---|---|---|---|---|
| `border-1` | Pixel-Perfect | T1 | não precisa | não | — | — | — |
| `border-2` | Pixel-Perfect | T1 | não precisa | não | — | — | — |
| `intersection-1` | Pixel-Perfect | T1 | não precisa | não | — | — | — |
| `intersection-2` | Pixel-Perfect | T1 | não precisa | não | — | — | — |
| `star-border` | Pixel-Perfect | T1 | não precisa | não | — | — | — |
| `bar-wave-animation` | Pixel-Perfect | T2 | sim | não | — | framer-motion | — |
| `bounce-smiley-animation` | Pixel-Perfect | T2 | sim | não | — | motion | — |
| `glow-card-animation` | Pixel-Perfect | T2 | sim | não | — | motion | — |
| `guitar-svg` | Pixel-Perfect | T2 | sim | não | não | @gsap/react, gsap | — |
| `liquid-pause-animation` | Pixel-Perfect | T2 | sim | não | — | motion | — |
| `logo-animation` | Pixel-Perfect | T2 | sim | não | — | framer-motion | — |
| `orbit-smiley-animation` | Pixel-Perfect | T2 | sim | não | — | motion | — |
| `signature` | Componentry | T2 | sim | não | — | framer-motion, opentype.js | — |
| `smiley-orb-animation` | Pixel-Perfect | T2 | sim | não | — | motion | — |
| `svg-1` | Pixel-Perfect | T2 | não precisa | não | — | @gsap/react, gsap | — |
| `svg-2` | Pixel-Perfect | T2 | não precisa | não | — | @gsap/react, gsap | — |
| `svg-4` | Pixel-Perfect | T2 | não precisa | não | — | @gsap/react, gsap | — |
| `svg-5` | Pixel-Perfect | T2 | não precisa | não | — | @gsap/react, gsap | — |
| `svg-6` | Pixel-Perfect | T2 | não precisa | não | — | @gsap/react, gsap | — |
| `svg-8` | Pixel-Perfect | T2 | não precisa | não | — | @gsap/react, gsap | — |
| `svg-9` | Pixel-Perfect | T2 | não precisa | não | — | @gsap/react, gsap | — |

### Navegação e chat (3)

Menus, docks, sidebars e interfaces de conversa.

| Item | Fonte | Tier | Use client | Mov. reduzido | Toque | Deps | Instalar antes |
|---|---|---|---|---|---|---|---|
| `claude-sidebar` | Pixel-Perfect | T1 | sim | não | — | — | shadcn: `sidebar` (`@/components/ui/sidebar`) |
| `chat-ui` | Pixel-Perfect | T2 | sim | sim | — | lucide-react, motion | manual: não encontrado no registro (`@/components/ui/dotm-square-11`); manual: não encontrado no registro (`@/components/ui/message-scroller`) |
| `magnetic-dock` | Componentry | T2 | sim | sim | não | framer-motion | — |

### Blocos de página (4)

Seções completas prontas (hero, preços). Exigem adaptação de conteúdo.

| Item | Fonte | Tier | Use client | Mov. reduzido | Toque | Deps | Instalar antes |
|---|---|---|---|---|---|---|---|
| `gradient-hero-01` | Componentry | T1 | não precisa | não | — | — | — |
| `pricing-01` | Componentry | T1 | não precisa | não | — | lucide-react | — |
| `pricing-02` | Componentry | T1 | sim | sim | — | lucide-react | — |
| `hero-geometric` | Componentry | T3 | sim | não | — | framer-motion, lucide-react, three, @react-three/fiber, @react-three/drei | — |

### Base técnica (5)

Arquivos auxiliares importados por outros itens. Não são componentes de tela.

| Item | Fonte | Tier | Use client | Mov. reduzido | Toque | Deps | Instalar antes |
|---|---|---|---|---|---|---|---|
| `specs` | Pixel-Perfect | T1 | não precisa | não | — | — | instalar à mão, nesta ordem: `engine` |
| `engine` | Pixel-Perfect | T2 | sim | não | — | @gsap/react, gsap | — |
| `animated-texture` | Pixel-Perfect | T3 | não precisa | não | — | three | — |
| `image-shader-canvas` | Pixel-Perfect | T3 | sim | não | não | three, lil-gui (depuração) | o CLI traz a cadeia (registryDependencies) |
| `shader-canvas` | Pixel-Perfect | T3 | sim | não | não | three, lil-gui (depuração) | — |

## 5. Fontes e licenças

- **Pixel-Perfect** (github.com/vansh-nagar/Pixel-Perfect), lido ao vivo em 2026-10-12 a partir de https://www.pixel-perfect.space/r/registry.json. URL de instalação: `https://www.pixel-perfect.space/r/{nome}.json`. Licença: MIT (Vansh Nagar). Os arquivos copiados devem manter o aviso MIT.
- **Componentry** (github.com/harshjdhv/componentry), lido ao vivo em 2026-10-12 a partir de https://componentry.dev/r/registry.json. URL de instalação: `https://componentry.dev/r/{nome}.json`. Licença: MIT (Harsh Jadhav). Ressalva do próprio README: image-trail e layered-stack exigem atenção à licença do GSAP.
- Estes repositórios não são submódulos do hub. Os clones servem só para gerar esta referência. Em uso, a skill baixa pela URL de cada item, sem clonar.

## 6. Como regenerar

```bash
python scripts/gerar_catalogo_componentes.py
```

Sem argumentos, lê os registros ao vivo. Para gerar offline, passe `--pixel-perfect <clone>` ou `--componentry <clone>`. Depois de regenerar, confira a origem na seção 5 e rode `python scripts/validate_skills.py`.
