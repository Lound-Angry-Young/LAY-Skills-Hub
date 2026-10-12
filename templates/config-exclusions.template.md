# Template de Isolamento de Ferramentas Externas

> **Objetivo:** Impedir que ferramentas auxiliares ou externas (como submódulos em `tools/` ou saídas do `graphify-out/`) sejam analisadas pelo compilador TypeScript, pelo ESLint ou pelo Prettier.

---

## 1. Em `tsconfig.json`

Adicione as pastas ao array `exclude`:

```json
{
  "compilerOptions": {
    "target": "ES2017",
    "lib": ["dom", "dom.iterable", "esnext"],
    "allowJs": true,
    "skipLibCheck": true,
    "strict": true,
    "noEmit": true,
    "esModuleInterop": true,
    "module": "esnext",
    "moduleResolution": "bundler",
    "resolveJsonModule": true,
    "isolatedModules": true,
    "jsx": "react-jsx",
    "incremental": true,
    "paths": {
      "@/*": ["./src/*"]
    }
  },
  "include": [
    "next-env.d.ts",
    "**/*.ts",
    "**/*.tsx",
    ".next/types/**/*.ts",
    ".next/dev/types/**/*.ts",
    "**/*.mts"
  ],
  "exclude": [
    "node_modules",
    "tools",
    "graphify-out"
  ]
}
```

---

## 2. Em `eslint.config.mjs`

Adicione as pastas ao `globalIgnores`:

```javascript
import { defineConfig, globalIgnores } from "eslint/config";
import nextVitals from "eslint-config-next/core-web-vitals";
import nextTs from "eslint-config-next/typescript";
import prettier from "eslint-config-prettier/flat";

const eslintConfig = defineConfig([
  ...nextVitals,
  ...nextTs,
  prettier,
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

## 3. Em `.prettierignore`

```
.next
node_modules
pnpm-lock.yaml
package-lock.json
playwright-report
test-results
next-env.d.ts
tools
graphify-out
```
