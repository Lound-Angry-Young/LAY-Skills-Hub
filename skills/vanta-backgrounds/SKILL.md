---
name: vanta-backgrounds
description: Use when integrating interactive 3D WebGL backgrounds (Waves, Net, Halo, Rings, Birds, Cells, Clouds, Globe) powered by Three.js or p5.js from tengbao/vanta. Covers React/Next.js dynamic loading, canvas lifecycle, responsive resizing, color palette calibration, and performance optimization.
---

# Vanta.js — 3D WebGL Backgrounds & Shader FX

Skill especializada na integração de fundos 3D animados, imersivos e interativos com WebGL baseados na biblioteca **Vanta.js** (`tengbao/vanta`).

## Quando Utilizar
- Criação de heros de alto impacto visual, seções com profundidade tridimensional e backgrounds dinâmicos reativos ao mouse/toque.
- Projetos que exigem efeitos como redes de nós (`NET`), ondas fluídas (`WAVES`), anéis orbitais (`RINGS`), halos etéreos (`HALO`), partículas celulares (`CELLS`), pássaros volumétricos (`BIRDS`), ou nuvens volumétricas (`CLOUDS`).
- Quando é necessário transformar páginas estáticas em experiências interativas com Three.js sem sobrecarregar a pipeline de 3D manual.

## Efeitos Disponíveis
1. **`NET`** (Nós conectados, teia geométrica de partículas com física de aproximação ao ponteiro).
2. **`WAVES`** (Ondas tridimensionais suaves e de alta fidelidade com sombreamento Phong).
3. **`RINGS`** (Anéis concêntricos girando em eixos múltiplos com refração de luz).
4. **`HALO`** (Efeito de halo etéreo pulsante com gradiente de luz dinâmico).
5. **`BIRDS`** (Simulação de boids/flocking de pássaros tridimensionais no espaço).
6. **`CELLS`** (Padrão Voronoi orgânico vivo e responsivo a gradientes).
7. **`GLOBE`** (Globo esférico de partículas interativo em rotação).
8. **`DOTS`** / **`FOG`** / **`CLOUDS`** (Partículas pontuais e neblina volumétrica).

## Diretrizes de Implementação Técnica

### 1. React / Next.js (App Router / Pages)
- **Dynamic Import sem SSR:** Como Vanta depende de `window` e `document`, SEMPRE carregue dinamicamente com `ssr: false` ou utilize `useEffect`.
- **Three.js Peer Dependency:** Vanta requer Three.js (`three` na versão compatível `^0.121.0` a `^0.134.0` ou scripts globais).
- **Cleanup no Desmonte:** SEMPRE destrua a instância com `vantaEffect.destroy()` no retorno do `useEffect` para evitar vazamento de memória de WebGL contexts.

```tsx
'use client';
import React, { useEffect, useRef, useState } from 'react';
import * as THREE from 'three';
import NET from 'vanta/dist/vanta.net.min';

export function VantaHero() {
  const [vantaEffect, setVantaEffect] = useState<any>(null);
  const vantaRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (!vantaEffect && vantaRef.current) {
      setVantaEffect(
        NET({
          el: vantaRef.current,
          THREE: THREE,
          mouseControls: true,
          touchControls: true,
          gyroControls: false,
          minHeight: 200.0,
          minWidth: 200.0,
          scale: 1.0,
          scaleMobile: 1.0,
          color: 0x00f0ff,
          backgroundColor: 0x0a0a0c,
          points: 10.0,
          maxDistance: 22.0,
          spacing: 16.0
        })
      );
    }
    return () => {
      if (vantaEffect) vantaEffect.destroy();
    };
  }, [vantaEffect]);

  return (
    <div ref={vantaRef} className="relative w-full min-h-screen flex items-center justify-center">
      <div className="relative z-10 text-white font-mono pointer-events-auto">
        <h1 className="text-5xl font-black tracking-tight">INTERACTIVE HERO</h1>
      </div>
    </div>
  );
}
```

## Performance & Acessibilidade
- **Prevenção de Queda de FPS:** Em telas móveis (`window.innerWidth < 768`), ajuste `scaleMobile` para `0.75` ou diminua a contagem de pontos/malhas.
- **`prefers-reduced-motion`:** Se o usuário possui preferência por redução de movimento, desligue a velocidade (`speed: 0`) ou substitua o WebGL por um gradiente estático de alta resolução.
- **Camadas & Contraste:** Mantenha um overlay semitransparente (ex: `bg-black/40` ou backdrop-blur leve) entre o canvas de fundo e o texto legível para assegurar proporção de contraste WCAG AA (mínimo 4.5:1).
