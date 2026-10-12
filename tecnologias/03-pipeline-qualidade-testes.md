# Pipeline de Qualidade, Testes e Automação de CI/CD

> **Objetivo:** Fornecer uma esteira de testes e checagem de qualidade à prova de falhas, cobrindo testes unitários, testes E2E, tipagem estrita, linting e hooks pré-commit com suporte robusto para Windows e Linux/macOS.

---

## 1. Visão Geral da Pilha de Qualidade

| Ferramenta | Pacote | Papel no Projeto |
| :--- | :--- | :--- |
| **Vitest** | `vitest`, `@vitejs/plugin-react` | Runner de testes unitários ultrarrápido compatível com Vite/Next |
| **Testing Library** | `@testing-library/react`, `@testing-library/jest-dom`, `@testing-library/user-event` | Asserções no DOM real simulado (JSDOM) |
| **Playwright** | `@playwright/test` | Testes End-to-End multi-device contra o build real de produção |
| **ESLint 9 (Flat Config)** | `eslint`, `eslint-config-next`, `eslint-config-prettier` | Checagem estática de sintaxe e regras de Core Web Vitals |
| **Prettier** | `prettier` | Padronização e formatação automática de código |
| **Husky & lint-staged** | `husky`, `lint-staged` | Garantia de execução de lint e formatação a cada `git commit` |

---

## 2. Configuração de Testes Unitários (Vitest)

### Arquivo `vitest.config.mts`

```typescript
import react from "@vitejs/plugin-react";
import tsconfigPaths from "vite-tsconfig-paths";
import { defineConfig } from "vitest/config";

export default defineConfig({
  plugins: [tsconfigPaths(), react()],
  test: {
    environment: "jsdom",
    globals: true,
    setupFiles: ["./vitest.setup.ts"],
    include: ["src/**/*.test.{ts,tsx}"],
    // Permite que os testes acessem nomes legíveis de classes CSS Modules
    css: { modules: { classNameStrategy: "non-scoped" } },
  },
});
```

### Arquivo `vitest.setup.ts` (Mocks de Ambiente Web)

O JSDOM do Node.js não possui APIs nativas de áudio, observadores e mídia. O `vitest.setup.ts` provê stubs essenciais:

```typescript
import "@testing-library/jest-dom/vitest";
import { vi } from "vitest";

// 1. Mock de matchMedia (prefers-color-scheme, prefers-reduced-motion)
Object.defineProperty(window, "matchMedia", {
  writable: true,
  value: vi.fn().mockImplementation((query: string) => ({
    matches: false,
    media: query,
    onchange: null,
    addListener: vi.fn(),
    removeListener: vi.fn(),
    addEventListener: vi.fn(),
    removeEventListener: vi.fn(),
    dispatchEvent: vi.fn(),
  })),
});

// 2. Mock de IntersectionObserver
class MockIntersectionObserver {
  observe = vi.fn();
  unobserve = vi.fn();
  disconnect = vi.fn();
}
Object.defineProperty(window, "IntersectionObserver", {
  writable: true,
  value: MockIntersectionObserver,
});

// 3. Mock de ResizeObserver
class MockResizeObserver {
  observe = vi.fn();
  unobserve = vi.fn();
  disconnect = vi.fn();
}
Object.defineProperty(window, "ResizeObserver", {
  writable: true,
  value: MockResizeObserver,
});

// 4. Mock de Web Audio API (AudioContext)
class MockAudioContext {
  createGain = vi.fn().mockReturnValue({
    gain: { setValueAtTime: vi.fn(), linearRampToValueAtTime: vi.fn(), exponentialRampToValueAtTime: vi.fn() },
    connect: vi.fn(),
  });
  createOscillator = vi.fn().mockReturnValue({
    type: "sine",
    frequency: { setValueAtTime: vi.fn(), linearRampToValueAtTime: vi.fn(), exponentialRampToValueAtTime: vi.fn() },
    connect: vi.fn(),
    start: vi.fn(),
    stop: vi.fn(),
  });
  destination = {};
  currentTime = 0;
  close = vi.fn().mockResolvedValue(undefined);
}
Object.defineProperty(window, "AudioContext", {
  writable: true,
  value: MockAudioContext,
});
```

---

## 3. Configuração de Testes E2E (Playwright)

### Arquivo `playwright.config.ts`

Executa os testes contra o servidor de produção compilado (`pnpm build && pnpm start`), garantindo que o comportamento testado seja idêntico ao que o usuário final receberá:

```typescript
import { defineConfig, devices } from "@playwright/test";

const PORT = Number(process.env.PORT ?? 3100);

export default defineConfig({
  testDir: "./e2e",
  fullyParallel: true,
  forbidOnly: !!process.env.CI,
  retries: 1,
  reporter: process.env.CI ? "github" : "list",
  use: {
    baseURL: `http://localhost:${PORT}`,
    trace: "retain-on-failure",
  },
  projects: [
    { name: "desktop", use: { ...devices["Desktop Chrome"], viewport: { width: 1440, height: 900 } } },
    { name: "mobile", use: { ...devices["Pixel 7"] } },
  ],
  webServer: {
    command: `pnpm build && pnpm start --port ${PORT}`,
    url: `http://localhost:${PORT}`,
    reuseExistingServer: !process.env.CI,
    timeout: 300_000,
  },
});
```

---

## 4. Configuração de Lint e Prettier

### Arquivo `eslint.config.mjs` (ESLint 9 Flat Config)

```javascript
import { defineConfig, globalIgnores } from "eslint/config";
import nextVitals from "eslint-config-next/core-web-vitals";
import nextTs from "eslint-config-next/typescript";
import prettier from "eslint-config-prettier/flat";

const eslintConfig = defineConfig([
  ...nextVitals,
  ...nextTs,
  prettier, // Desativa regras de estilo conflitantes com o Prettier
  globalIgnores([
    ".next/**",
    "out/**",
    "build/**",
    "next-env.d.ts",
    "playwright-report/**",
    "test-results/**",
    "tools/**",
    "graphify-out/**",
  ]),
]);

export default eslintConfig;
```

---

## 5. Automação Pré-Commit com Resiliência para Windows

No Windows, comandos de linha muito longos estouram o buffer do `cmd.exe` (~8 KB), fazendo o `lint-staged` falhar quando dezenas de arquivos são commitados juntos.

### Arquivo `lint-staged.config.mjs`

```javascript
/**
 * Proteção contra estouro de linha de comando no Windows (limite de ~8 KB do cmd).
 * Acima de 30 arquivos alterados, executa no projeto inteiro de forma direta.
 */
const MAX = 30;
const quote = (files) => files.map((f) => JSON.stringify(f)).join(" ");

const config = {
  "*.{ts,tsx,mts}": (files) =>
    files.length > MAX
      ? ["eslint --fix --max-warnings=0 .", "prettier --write src e2e"]
      : [`eslint --fix --max-warnings=0 ${quote(files)}`, `prettier --write ${quote(files)}`],
  "*.{css,json,md,mjs}": (files) =>
    files.length > MAX ? "prettier --write ." : `prettier --write ${quote(files)}`,
};

export default config;
```

### Inicialização do Husky

```bash
# Inicializa os hooks do Git
pnpm dlx husky init

# Adiciona o hook de pre-commit
echo "npx lint-staged" > .husky/pre-commit
```
