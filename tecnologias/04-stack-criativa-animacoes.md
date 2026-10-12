# Stack Criativa, Shaders WebGL, Animações e Áudio Procedural

> **Objetivo:** Documentar a integração e os padrões arquiteturais das tecnologias visuais de alta performance utilizadas para criar interfaces imersivas, reativas e contemporâneas sem sacrificar performance.

---

## 1. Visão Geral das Tecnologias Criativas

| Tecnologia | Pacotes | Função no Ecossistema |
| :--- | :--- | :--- |
| **Three.js + R3F** | `three`, `@react-three/fiber`, `@react-three/drei` | Cena 3D, geometria de quads e gerenciamento do contexto WebGL |
| **Pós-Processamento** | `postprocessing`, `@react-three/postprocessing` | Passes de shader em ping-pong (glitch VHS, halftone, retícula CRT) |
| **Orquestração de Scroll** | `gsap`, `@gsap/react` | Linhas do tempo (timelines), ScrollTrigger, scrub e pins de tela |
| **Smooth Scroll Cinético** | `lenis` | Rolagem suave com amortecimento inercial perfeitamente sincronizada ao GSAP |
| **Física de Spring UI** | `motion` (`motion/react`) | Cursor magnético dinâmico, física elástica e modais responsivos |
| **Animações Micro / Stagger** | `animejs` | Efeitos matriciais em texto ASCII, estampas mecânicas e transições rápidas |
| **Áudio Procedural** | Web Audio API nativa | Síntese de áudio 8-bit em tempo real (zero arquivos MP3/WAV pesados) |

---

## 2. Padrão Arquitetural: Single Canvas WebGL

> **Regra Fundamental:** Nunca crie múltiplos elementos `<canvas>` WebGL em diferentes páginas ou componentes. Múltiplos contextos estouram o limite da GPU em navegadores móveis e causam recarga ou travamentos ("WebGL context lost").

### Como Funciona

1. **Montagem Única no Layout Raiz:**
   O canvas é montado uma única vez em `src/app/layout.tsx` (ou componente equivalente) com `position: fixed` cobrindo toda a janela.
2. **Controle Declarativo via Store Reativa:**
   Qualquer página ou componente sincroniza propriedades visuais (opacidade, intensidade de glitch, transição de textura, escala) através de uma store leve (`useSyncExternalStore` ou similar).
3. **Renderização Sob Demanda (`frameloop="demand"`):**
   A cena só renderiza quando há alteração de estado ou durante animações ativas, poupando bateria em repouso.

---

## 3. Sincronização Perfeita: Lenis + GSAP ScrollTrigger

Para evitar o clássico efeito de tremor (*jitter*) entre o scroll suave e os gatilhos de animação do GSAP, o relógio do Lenis deve ser conectado diretamente ao ticker do GSAP:

```typescript
import gsap from "gsap";
import { ScrollTrigger } from "gsap/ScrollTrigger";
import Lenis from "lenis";

gsap.registerPlugin(ScrollTrigger);

export function initSmoothScroll() {
  const lenis = new Lenis({
    duration: 1.2,
    easing: (t) => Math.min(1, 1.001 - Math.pow(2, -10 * t)),
    smoothWheel: true,
  });

  // Atualiza o ScrollTrigger a cada evento do Lenis
  lenis.on("scroll", ScrollTrigger.update);

  // Alimenta o loop do Lenis a partir do RAF do GSAP
  gsap.ticker.add((time) => {
    lenis.raf(time * 1000);
  });

  // Desativa lagSmoothing para manter sincronia estrita de frames
  gsap.ticker.lagSmoothing(0);

  return lenis;
}
```

---

## 4. Síntese de Áudio Procedural (Web Audio API)

Para evitar download de dezenas de arquivos de áudio que aumentam o bundle e dependem de requisições de rede, utilize síntese direta via osciladores matemáticos.

### Exemplo de Gerador de Sons 8-bit

```typescript
let audioCtx: AudioContext | null = null;

function getAudioContext(): AudioContext {
  if (!audioCtx) {
    const AudioContextClass = window.AudioContext || (window as unknown as { webkitAudioContext: typeof AudioContext }).webkitAudioContext;
    audioCtx = new AudioContextClass();
  }
  if (audioCtx.state === "suspended") {
    audioCtx.resume();
  }
  return audioCtx;
}

// Efeito de "Blip" mecânico para cliques em botões
export function blip(freq = 440, duration = 0.04) {
  try {
    const ctx = getAudioContext();
    const osc = ctx.createOscillator();
    const gain = ctx.createGain();

    osc.type = "square"; // Onda quadrada para sonoridade arcade/8-bit
    osc.frequency.setValueAtTime(freq, ctx.currentTime);
    osc.frequency.exponentialRampToValueAtTime(freq * 0.5, ctx.currentTime + duration);

    gain.gain.setValueAtTime(0.12, ctx.currentTime);
    gain.gain.exponentialRampToValueAtTime(0.001, ctx.currentTime + duration);

    osc.connect(gain);
    gain.connect(ctx.destination);

    osc.start();
    osc.stop(ctx.currentTime + duration);
  } catch {
    // Falha silenciosa caso o áudio não tenha sido desbloqueado por interação do usuário
  }
}
```

---

## 5. Diretrizes de Acessibilidade e Performance Gráfica

1. **Fotossensibilidade:** Efeitos de flicker, estroboscópio ou glitch não devem ultrapassar a frequência de **2,5 Hz**.
2. **Respeito a `prefers-reduced-motion`:**
   - Desative rotações contínuas e transições drásticas de câmera.
   - Forneça uma opção de interface para o usuário ativar "Reduzir Efeitos" (`reduce-fx`).
3. **Orçamento de DPR (*Device Pixel Ratio*):**
   - Limite o DPR do canvas WebGL a no máximo `Math.min(window.devicePixelRatio, 2)` (ou 1.5 em telas retina de alta densidade) para evitar quedas drásticas de taxa de quadros (FPS) em monitores 4K.
