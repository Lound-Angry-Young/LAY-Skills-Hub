---
name: react-bits-animations
description: Use when crafting modern, production-grade animated UI components inspired by DavidHDev/react-bits. Covers text FX (DecryptedText, BlurText, SplitText, ShinyText, TrueFocus), animated backgrounds (Hyperspeed, Waves, Squares, LiquidChrome, Ballpit), and creative interactive components (SpotlightCard, TiltedCard, Stack, ElasticSlider).
---

# React Bits — Coleção de Componentes & Animações Modernas

Skill especializada em componentes de animação e microinterações modulares para React/Next.js baseados na coleção **React Bits** (`DavidHDev/react-bits`).

## Quando Utilizar
- Desenvolvimento de interfaces com apelo estético contemporâneo (dark mode brutalista, cyber, minimalista, editorial).
- Necessidade de efeitos de texto dinâmicos (efeito hacker/descriptografia, blur progressivo, split por caractere, reflexo luminoso, foco óptico).
- Criação de cartões interativos com iluminação radial ao movimento do mouse (`SpotlightCard`), inclinação física 3D (`TiltedCard`), pilhas expansíveis (`Stack`), ou sliders táteis (`ElasticSlider`).
- Fundos animados performáticos com Canvas ou CSS (`Hyperspeed`, `Squares`, `LiquidChrome`).

## Catálogo de Componentes Chave

### 1. Efeitos de Texto (Text Animations)
- **`DecryptedText`**: Revela o texto caractere a caractere substituindo aleatoriamente por glifos cibernéticos/monospaçados até a estabilização.
- **`BlurText`**: Anima palavras ou letras a partir de um desfoque gaussiano suave (`filter: blur(...)`) com opacidade escalonada.
- **`SplitText`**: Divisão de parágrafos em spans com stagger controlado por Framer Motion ou GSAP.
- **`ShinyText`**: Gradiente metálico ou neon deslizando continuamente sobre os caracteres com máscara de texto CSS (`background-clip: text`).
- **`TrueFocus`**: Moldura retangular móvel com cantos realçados que persegue a palavra focada em uma frase.

### 2. Fundos & Efeitos Visuais (Backgrounds)
- **`Hyperspeed`**: Linhas de velocidade de warp tridimensionais inspiradas em tunelamento espacial com Three.js.
- **`Squares`**: Grade vetorial de quadrículas piscantes com efeito hover reativo de proximidade.
- **`LiquidChrome`**: Shader WebGL simulando superfície líquida de mercúrio cromado reativa a reflexos e movimento.
- **`Ballpit`**: Simulação física 2D de esferas com gravidade e colisão em canvas.

### 3. Componentes Interativos (UI Components)
- **`SpotlightCard`**: Card escuro com borda e preenchimento iluminados por um gradiente radial centralizado nas coordenadas do cursor (`clientX`, `clientY`).
- **`TiltedCard`**: Rotação 3D perspectiva calculada pelo vetor de distância em relação ao centro do elemento.
- **`Stack`**: Pilha de cards empilhados que se expandem em leque ou se alternam com swipe gestures.

## Diretrizes de Implementação Técnica

1. **Dependências Mínimas:** Prefira implementações em Framer Motion (`framer-motion`) ou Tailwind CSS puro com CSS Custom Properties (`--mouse-x`, `--mouse-y`) para evitar sobrecarga de bundles.
2. **Performance:** Utilize `will-change: transform` estritamente durante a interação e `transform: translate3d(0, 0, 0)` para aceleração de GPU.
3. **Responsividade:** Em dispositivos touch, desative cálculos de hover contínuos e substitua por transições de toque ativadas por `:active` ou gestos de swipe.
4. **Semântica:** Garanta que componentes de texto como `DecryptedText` e `BlurText` preservem o texto acessível integral no DOM (`aria-label` ou texto real sem quebra de leitura por leitores de tela).
