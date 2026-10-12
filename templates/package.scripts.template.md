# Template de Scripts e Dependências (`package.json`)

> **Instruções:** Adicione estes blocos ao `package.json` do seu novo projeto para garantir suporte completo aos scripts de qualidade, automação e pipeline do Graphify.

---

## 1. Bloco de `scripts`

```json
{
  "scripts": {
    "dev": "next dev",
    "build": "next build",
    "start": "next start",
    "lint": "eslint .",
    "typecheck": "next typegen && tsc --noEmit",
    "format": "prettier --write .",
    "format:check": "prettier --check .",
    "test": "vitest run",
    "test:watch": "vitest",
    "test:e2e": "playwright test",
    "prepare": "husky",
    "graphify": "python -m graphify extract . --code-only && python -m graphify cluster-only . && python -m graphify export html"
  }
}
```

---

## 2. Comandos de Instalação de Dependências

### Dependências de Produção (Stack Criativa e UI)

```bash
pnpm add next@16 react@19 react-dom@19 three @react-three/fiber @react-three/drei @react-three/postprocessing postprocessing gsap @gsap/react lenis motion animejs
```

### Dependências de Desenvolvimento (Qualidade, Tipos, Testes e Lint)

```bash
pnpm add -D typescript @types/node @types/react @types/react-dom @types/three eslint eslint-config-next eslint-config-prettier prettier vitest @vitejs/plugin-react vite-tsconfig-paths jsdom @testing-library/react @testing-library/jest-dom @testing-library/user-event @playwright/test husky lint-staged
```

---

## 3. Instalação do Graphify no Ambiente Python

```bash
pip install graphifyy
# ou
uv tool install graphifyy
```
