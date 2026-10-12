---
name: orchestrating-smooth-scroll
description: >
  Implements butter-smooth scrolling and scroll orchestration with Lenis, including React wrappers, virtual scroll, touch momentum, anchor navigation and GSAP ScrollTrigger synchronization. Use this skill when: adding Lenis smooth scrolling or syncing it with ScrollTrigger. Do NOT use this skill when: the page needs only GSAP ScrollTrigger motion without Lenis (use engineering-gsap-motion-uis).
---

# Lenis — Motor de Rolagem Suave & Orquestração de Scroll

Skill especializada na implementação de rolagem suave e controle preciso de rolagem utilizando o motor **Lenis** da Darkroom Engineering (`darkroomengineering/lenis`).

## Quando Utilizar
- Interfaces com microinterações sofisticadas, pinning de seções, paralaxe e efeitos orientados a scroll.
- Quando o scroll padrão do navegador é excessivamente brusco ou dessincronizado de animações GSAP ScrollTrigger / Framer Motion.
- Criação de landing pages editoriais, websites premiados (Awwwards/FWA style) e experiências ricas em conteúdo narrativo.

## Vantagens Chave do Lenis
1. **Física Independente de Taxa de Quadros:** O cálculo inercial opera com base em delta-time, comportando-se identicamente em telas de 60Hz, 120Hz ou 240Hz ProMotion.
2. **Compatibilidade Nativa:** Não sequestra o scroll removendo a barra de rolagem padrão nem quebrando a acessibilidade de teclado (`Page Down`, `Page Up`, `Space`, setas).
3. **Sincronização Perfeita com GSAP ScrollTrigger:** Evita trepidação (*jitter*) entre o scroll virtual e os cálculos de gatilho do GSAP.
4. **Leveza:** Zero dependências externas e peso inferior a 4KB minificado/gzipado.

## Padrões de Implementação

### 1. React / Next.js (com `lenis/react`)

```tsx
'use client';
import { ReactLenis, useLenis } from 'lenis/react';
import { ReactNode } from 'react';

interface SmoothScrollProps {
  children: ReactNode;
}

export function SmoothScroll({ children }: SmoothScrollProps) {
  return (
    <ReactLenis
      root
      options={{
        lerp: 0.1,             // Inércia linear (0.05 mais suave, 0.1 padrão equilibrado)
        duration: 1.2,         // Duração do amortecimento em segundos
        smoothWheel: true,     // Suavizar rolagem do mouse wheel
        syncTouch: false,      // Manter touch nativo no mobile para maior naturalidade
      }}
    >
      {children}
    </ReactLenis>
  );
}
```

### 2. Sincronização com GSAP ScrollTrigger

```ts
import Lenis from 'lenis';
import gsap from 'gsap';
import { ScrollTrigger } from 'gsap/ScrollTrigger';

gsap.registerPlugin(ScrollTrigger);

const lenis = new Lenis({
  lerp: 0.08,
  duration: 1.2,
});

// Vincula o ticker do GSAP ao Lenis raf
lenis.on('scroll', ScrollTrigger.update);

gsap.ticker.add((time) => {
  lenis.raf(time * 1000);
});

gsap.ticker.lagSmoothing(0);
```

## Boas Práticas & Acessibilidade
- **Respeito ao `prefers-reduced-motion`:**
  ```ts
  const prefersReduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  if (prefersReduced) {
    lenis.destroy(); // Retorna imediatamente ao scroll padrão do sistema operacional
  }
  ```
- **Navegação por Âncora:** Ao clicar em links de âncora (`#section`), utilize `lenis.scrollTo('#section', { offset: -80, duration: 1.5 })` para transição suave que compensa cabeçalhos fixos.
- **Modais e Menus de Tela Cheia:** Pause o Lenis com `lenis.stop()` ao abrir um modal com scroll interno e retome com `lenis.start()` ao fechar.
