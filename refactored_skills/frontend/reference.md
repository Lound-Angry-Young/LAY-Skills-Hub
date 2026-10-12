# Referência Arquitetural do Domínio: FRONTEND

## Table of Contents
1. [Visão Geral do Domínio](#visão-geral-do-domínio)
2. [Catálogo de Habilidades e Responsabilidades](#catálogo-de-habilidades-e-responsabilidades)
3. [Padrões de Integração e Roteamento](#padrões-de-integração-e-roteamento)
4. [Diretrizes de Qualidade e Segurança](#diretrizes-de-qualidade-e-segurança)

## Visão Geral do Domínio
O domínio `frontend` reúne um conjunto de habilidades altamente especializadas e desacopladas, projetadas segundo os padrões estritos de Agent Skills da Anthropic.
Finalidade: Engenharia de Frontend e Interfaces de Usuário.

## Catálogo de Habilidades e Responsabilidades
| [architecting-react-composition](./architecting-react-composition/SKILL.md) | Provides React composition patterns that scale: compound components, render props, context providers and React 19 API changes, replacing boolean prop proliferation with flexible, reusable component APIs | `[./architecting-react-composition/SKILL.md](./architecting-react-composition/SKILL.md)` |
| [engineering-frontend-interfaces](./engineering-frontend-interfaces/SKILL.md) | Builds production-quality, accessible and responsive user-facing UIs: components, layouts, state management and WCAG accessibility, so the output looks and works production-ready rather than AI-generated | `[./engineering-frontend-interfaces/SKILL.md](./engineering-frontend-interfaces/SKILL.md)` |
| [engineering-gsap-motion-uis](./engineering-gsap-motion-uis/SKILL.md) | Engineers high-end UX/UI with advanced GSAP motion: Python-driven randomization for layout variance, AIDA page structure, wide editorial typography, gapless bento grids and strict GSAP ScrollTrigger use (pinning, stacking, scrubbing) | `[./engineering-gsap-motion-uis/SKILL.md](./engineering-gsap-motion-uis/SKILL.md)` |
| [converting-images-to-code](./converting-images-to-code/SKILL.md) | Converts a visually important website into code by first generating section-specific design images, analyzing them in depth and implementing the site to match them as closely as possible, with a clean, readable hero | `[./converting-images-to-code/SKILL.md](./converting-images-to-code/SKILL.md)` |
| [orchestrating-smooth-scroll](./orchestrating-smooth-scroll/SKILL.md) | Implements butter-smooth scrolling and scroll orchestration with Lenis, including React wrappers, virtual scroll, touch momentum, anchor navigation and GSAP ScrollTrigger synchronization | `[./orchestrating-smooth-scroll/SKILL.md](./orchestrating-smooth-scroll/SKILL.md)` |
| [designing-minimalist-interfaces](./designing-minimalist-interfaces/SKILL.md) | Designs clean editorial-style interfaces with a warm monochrome palette, typographic contrast, flat bento grids and muted pastels, without gradients or heavy shadows | `[./designing-minimalist-interfaces/SKILL.md](./designing-minimalist-interfaces/SKILL.md)` |
| [enforcing-full-code-output](./enforcing-full-code-output/SKILL.md) | Overrides default LLM truncation behavior to enforce complete, unabridged code generation: bans placeholder patterns and handles token-limit splits cleanly | `[./enforcing-full-code-output/SKILL.md](./enforcing-full-code-output/SKILL.md)` |
| [optimizing-react-performance](./optimizing-react-performance/SKILL.md) | Applies React and Next.js performance guidelines from Vercel Engineering when writing, reviewing or refactoring components, pages, data fetching or bundles | `[./optimizing-react-performance/SKILL.md](./optimizing-react-performance/SKILL.md)` |
| [animating-react-bits-components](./animating-react-bits-components/SKILL.md) | Builds modern, production-grade animated UI components inspired by react-bits: text effects (DecryptedText, BlurText, SplitText, ShinyText, TrueFocus), animated backgrounds (Hyperspeed, Waves, Squares, LiquidChrome, Ballpit) and interactive components (SpotlightCard, TiltedCard, Stack, ElasticSlider) | `[./animating-react-bits-components/SKILL.md](./animating-react-bits-components/SKILL.md)` |
| [building-react-native-interfaces](./building-react-native-interfaces/SKILL.md) | Applies React Native and Expo best practices for performant mobile apps: component structure, list performance, animations and native module usage | `[./building-react-native-interfaces/SKILL.md](./building-react-native-interfaces/SKILL.md)` |
| [animating-react-view-transitions](./animating-react-view-transitions/SKILL.md) | Implements native-feeling animations with React's View Transition API (ViewTransition component, addTransitionType and CSS view-transition pseudo-elements), covering page and route transitions, shared elements, enter and exit animations, list reorder and directional navigation in Next.js | `[./animating-react-view-transitions/SKILL.md](./animating-react-view-transitions/SKILL.md)` |
| [redesigning-legacy-interfaces](./redesigning-legacy-interfaces/SKILL.md) | Upgrades existing websites and apps to premium quality: audits the current design, identifies generic AI patterns and applies high-end standards without breaking functionality, with any CSS framework or vanilla CSS | `[./redesigning-legacy-interfaces/SKILL.md](./redesigning-legacy-interfaces/SKILL.md)` |
| [crafting-high-end-visuals](./crafting-high-end-visuals/SKILL.md) | Teaches the agent to design like a high-end agency, defining the fonts, spacing, shadows, card structures and animations that make a website feel premium, and blocking common defaults that look cheap or generic | `[./crafting-high-end-visuals/SKILL.md](./crafting-high-end-visuals/SKILL.md)` |
| [authoring-stitch-design-systems](./authoring-stitch-design-systems/SKILL.md) | Generates semantic DESIGN.md files for Google Stitch that enforce premium, anti-generic UI standards: strict typography, calibrated color, asymmetric layouts, perpetual micro-motion and hardware-accelerated performance | `[./authoring-stitch-design-systems/SKILL.md](./authoring-stitch-design-systems/SKILL.md)` |
| [governing-anti-slop-aesthetics](./governing-anti-slop-aesthetics/SKILL.md) | Applies anti-slop design guidelines to interfaces: avoids generic AI-generated visual patterns and enforces deliberate visual tension, typographic voice, solid shadows, texture and information density, with WCAG AA contrast and reduced-motion support | `[./governing-anti-slop-aesthetics/SKILL.md](./governing-anti-slop-aesthetics/SKILL.md)` |
| [elevating-frontend-taste](./elevating-frontend-taste/SKILL.md) | Anti-slop frontend guidance for landing pages, portfolios and redesigns: reads the brief, infers the right design direction and ships interfaces that do not look templated, using real design systems where applicable and an audit-first approach to redesigns | `[./elevating-frontend-taste/SKILL.md](./elevating-frontend-taste/SKILL.md)` |
| [applying-legacy-design-taste](./applying-legacy-design-taste/SKILL.md) | Applies the original v1 taste guidance (design-taste-frontend-v1), kept for projects that depend on its exact behavior | `[./applying-legacy-design-taste/SKILL.md](./applying-legacy-design-taste/SKILL.md)` |
| [auditing-web-design-guidelines](./auditing-web-design-guidelines/SKILL.md) | Reviews UI code for Web Interface Guidelines compliance, checking accessibility, design and UX against best practices | `[./auditing-web-design-guidelines/SKILL.md](./auditing-web-design-guidelines/SKILL.md)` |

## Padrões de Integração e Roteamento
- Cada habilidade opera com assinatura estrita de Input/Output.
- O roteador de domínio (`SKILL.md`) atua como camada de orquestração de 1 nível de profundidade.
- Habilidades com rotinas extensas ou especificações técnicas possuem seus próprios arquivos `reference.md` auxiliares.

## Diretrizes de Qualidade e Segurança
- Todas as execuções devem validar pré-condições antes de realizar qualquer alteração estrutural.
- Em caso de falha, acione a seção `## On Failure` com rollback imediato e logs diagnósticos.
