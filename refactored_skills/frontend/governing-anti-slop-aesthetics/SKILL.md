---
name: governing-anti-slop-aesthetics
description: >
  Applies anti-slop design guidelines to interfaces: avoids generic AI-generated visual patterns and enforces deliberate visual tension, typographic voice, solid shadows, texture and information density, with WCAG AA contrast and reduced-motion support. Use this skill when: reviewing or building a landing page, dashboard or component that looks templated, generic or interchangeable. Do NOT use this skill when: the project already has a defined design system that must be followed exactly, or the task is a functional change with no visual impact.
---

# Anti-Slop Aesthetics Guidelines

> **Atribuição:** adaptado e inspirado pelo projeto [taste-skill](https://github.com/leonxlnx/taste-skill) criado por Leon Lin (@Leonxlnx), licença MIT.

Esta skill orienta o desenvolvimento e a revisão de interfaces para evitar código visual genérico ("AI slop") e garantir que cada componente tenha personalidade própria.

---

## 1. O Manifesto Anti-Slop

O "slop" de frontend acontece quando modelos de IA recorrem a padrões genéricos e sem alma:

- Botões cinzas com sombras suaves repetitivas (`box-shadow: 0 4px 6px rgba(0,0,0,0.1)`).
- Bordas arredondadas sem propósito (`border-radius: 8px` em tudo).
- Fontes neutras sem hierarquia expressiva (ex: Arial/Inter em corpo e títulos sem variação).
- Espaçamentos mornos e falta de tensão visual deliberada.

O padrão oposto:

- **Tensão Visual e Densidade:** contrastes arrojados entre uma base clara ou escura, um acento de alta saturação e uma superfície neutra de apoio.
- **Tipografia com Voz:** alternância entre fontes de exibição (`--font-display`), uma fonte de destaque decorativa (`--font-hand`) e blocos monoespaçados (`--font-mono`).
- **Bordas e Chanfros:** sombras sólidas sem desfoque (`box-shadow: 4px 4px 0 #000`, `box-shadow: 6px 8px 0 var(--color-accent)`).
- **Textura e Materialidade:** ruído procedural, padrões binários, retículas halftone ou scanlines, quando couberem ao projeto.

---

## 2. Parâmetros de Taste para Componentes

Ao criar ou revisar interfaces:

### A. Variância Tipográfica

- Nunca use a mesma fonte para cabeçalhos e rótulos de suporte.
- Títulos de impacto usam `--font-display` com `line-height: 0.9` e `text-transform: uppercase`.
- Selos, etiquetas e tags técnicas usam `--font-mono` em negrito com `letter-spacing: 0.08em`.
- Assinaturas e toques humanos usam `--font-hand` com rotação deliberada (`transform: rotate(-6deg)`).

### B. Densidade e Espaçamento

- Em telas compactas, prefira agrupamento denso com divisões sólidas de 2px ou 3px em vez de espaços brancos vazios.
- Use a escala base 8 do projeto (`4px`, `8px`, `16px`, `24px`, `32px`, `48px`, `64px`).

### C. Microinterações

- Hover e foco devem deslocar fisicamente o elemento com contra-sombra (`transform: translate(-3px, -3px); box-shadow: 8px 10px 0 #000`).
- Sons de clique procedurais são opcionais e devem poder ser desligados.

---

## 3. Checklist de Validação

- [ ] A interface parece única ou poderia estar em qualquer template SaaS genérico?
- [ ] Há contraste suficiente entre texto e fundo (mínimo WCAG AA 4.5:1)?
- [ ] As sombras são sólidas e com personalidade, sem blur genérico?
- [ ] Há suporte a `prefers-reduced-motion` e a modo de redução de efeitos?
