---
name: creative-libraries-hub
description: Use when discovering, selecting, and integrating modern creative web libraries, shaders, 3D engines, canvas physics, audio synthesis, and animation toolkits from the Libraries.dev catalog (Jakubantalik/Libraries.dev). Provides curated architectural guidance for high-end web experiences.
---

# Creative Libraries Hub — Diretório de Ferramentas Web Criativas

Skill especializada na pesquisa, curadoria e seleção de bibliotecas de ponta para desenvolvimento criativo, baseada no ecossistema **Libraries.dev** (`Jakubantalik/Libraries.dev`).

## Quando Utilizar
- Arquitetura de projetos que requerem capacidades visuais além do padrão corporativo comum (3D, áudio interativo, shaders WebGL/WebGPU, canvas 2D físico, tipografia cinética).
- Necessidade de escolher a melhor biblioteca para um problema específico (ex: física de corpos rígidos vs física de partículas, Three.js vs Babylon.js vs OGL vs PixiJS).
- Auditoria de stacks criativas para garantir performance, compatibilidade móvel e manutenção a longo prazo.

## Taxonomia de Ferramentas & Recomendações por Domínio

| Categoria | Bibliotecas de Referência | Caso de Uso Ideal |
|---|---|---|
| **Motores 3D & WebGL/WebGPU** | Three.js, React Three Fiber (R3F), TresJS, OGL, Babylon.js | Cenas tridimensionais, modelos GLTF, shaders customizados PBR |
| **Animação & Motion Design** | GSAP, Motion (Framer Motion), Anime.js, Theatre.js, AutoAnimate | Transições de layout, orquestração de timeline, microinterações |
| **Rolagem & Cinemática** | Lenis, Locomotive Scroll, Virtual Scroll | Suavização inercial, sincronização com ScrollTrigger e WebGL |
| **Física 2D / 3D** | Matter.js, Rapier.rs, Cannon-es, Planck.js | Colisões em canvas, gravidade de partículas, jogos web, ragdolls |
| **Áudio Interativo & Síntese** | Howler.js, Tone.js, Pizzicato.js, Web Audio API | Trilha sonora reativa, efeitos sonoros táteis de clique/hover, sintetizadores |
| **Shaders & Arte Generativa** | GLSL Canvas, Curtains.js, P5.js, Paper.js, Two.js | Efeitos de distorção de imagem por ruído Perlin, ondulações de água, filtros |
| **UI Primitives & Acessibilidade** | Radix UI, Ariakit, React Aria, Base UI, Headless UI | Fundamentos semânticos desestilizados e acessíveis para compor com design custom |
| **Ícones & Vetores Dinâmicos** | Lucide Icons, Iconify, Phosphor Icons, Heroicons | Iconografia SVG consistente com variantes de peso e estados |

## Critérios de Decisão Técnica
1. **Orçamento de Performance (Performance Budget):**
   - Evite bibliotecas monolíticas pesadas quando uma alternativa micro-modular atender à demanda (ex: OGL em vez de Three.js completo quando só há um shader simples de pós-processamento).
2. **Ciclo de Vida & Destruição de Contexto:**
   - Todo renderizador de canvas (Three.js, Pixi, Matter.js) deve expor método de `dispose()` acionado no desmontar de rotas SPA / Next.js para não esgotar a VRAM da GPU.
3. **Degradação Graciosa:**
   - Se WebGL não for suportado pelo dispositivo ou estiver desativado no navegador, a aplicação DEVE cair suavemente para renderização CSS/SVG estática legível.
