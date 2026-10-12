---
name: verifying-animated-component-compliance
description: >
  Verifies a copied or generated animated UI component against the project rules: local imports resolved, use client where hooks are used, reduced-motion handling present, at most one WebGL component per route, touch fallback for pointer-only effects, debug controls removed, license notice kept, and the project type-checks and builds. Use this skill when: an animated component was just added or generated and needs a compliance check before delivery. Do NOT use this skill when: choosing a component (use selecting-animated-ui-components), installing it (use integrating-external-ui-components) or running end-to-end browser tests (use automating-browser-tests).
---

# Verificando conformidade de componente animado

Confere um componente novo ou alterado contra as regras do hub. Esta skill só lê e relata: não altera arquivos.

## Input/Output Signature

Input:
- targetPaths: array # arquivos novos ou alterados
- routePath: string # pasta da rota que usa o componente, para contar WebGL
- projectPath: string # raiz do projeto
- packageManager: string # npm, pnpm, yarn ou bun, pelo lockfile
- dryRun: boolean # sempre verdadeiro nesta skill, por ser só leitura (default: true)

Output:
- success: boolean # verdadeiro só se nenhuma verificação obrigatória falhou
- status: string # completed ou failed
- artifacts: array # um item por verificação, com resultado e arquivos
- executionLog: string # comandos executados e saída de cada um

## Imperative Execution Workflow

1. [FRÁGIL] Imports locais. Para cada arquivo alvo, liste os imports que começam com `./`, `../` ou `@/`. Cada um deve resolver para um arquivo existente. Comando: `grep -n "from ['\"]\(\.\|@/\)" <arquivo>`. Import faltante = falha.
2. [FRÁGIL] Client boundary. Arquivos com hook (`useState`, `useEffect`, `useRef` ou outro) e sem `"use client"` na primeira linha. Se o arquivo for importado só por componente cliente, registre aviso. Se for importado por arquivo de servidor no App Router, falha. Comando: `grep -L "use client" <arquivos com hook>`.
3. [FRÁGIL] Movimento reduzido. O arquivo com animação deve conter `prefers-reduced-motion`, `useReducedMotion`, `matchMedia` ou `gsap.matchMedia`. Ausência em componente animado = falha. Comando: `grep -l "prefers-reduced-motion\|useReducedMotion\|matchMedia" <arquivos>`.
4. [FRÁGIL] WebGL por rota. Conte os componentes T3 que a rota importa, direta ou indiretamente. T3 é identificado por `three`, `@react-three/*`, `WebGL` ou pelos auxiliares de shader. Mais de um por rota = falha. Use o tier do item no catálogo da skill [selecting-animated-ui-components](../../frontend/selecting-animated-ui-components/SKILL.md). Comando: `grep -rl "from ['\"]three\|@react-three\|WebGL" <routePath>`.
5. [FLEXÍVEL] Toque. Efeito que escuta `mousemove`, `pointermove` ou `mouseenter` deve ter caminho para toque: `(hover: none)`, `pointer: coarse`, `touchstart` ou equivalente. Ausência = aviso. Vira falha se o efeito for o único meio de interação.
6. [FRÁGIL] Depuração. Comando: `grep -rn "lil-gui\|dat.gui\|leva" <arquivos>`. Qualquer ocorrência = falha.
7. [FRÁGIL] Licença. O arquivo mantém o aviso MIT do original, ou o item está registrado em `THIRD_PARTY_NOTICES` ou no README com a nota. Ausência = falha.
8. [FRÁGIL] Tipos e build. Rode `npx tsc --noEmit` (ou `pnpm exec tsc --noEmit`) e o build do projeto. Erro = falha, com a saída completa no executionLog. Os erros mais comuns, `TS7016` no `three`, `TS2307` em `class-variance-authority` e em `@/lib/utils`, têm correção no passo de tipos da skill [integrating-external-ui-components](../../frontend/integrating-external-ui-components/SKILL.md). Não corrija aqui: esta skill só relata.
9. [FLEXÍVEL] Navegador. Se o projeto tiver servidor de desenvolvimento, confira o console da página com [testing-in-browser-with-devtools](../testing-in-browser-with-devtools/SKILL.md). Erro de console relacionado ao componente = falha.

## Checklist

- [ ] Imports locais resolvem
- [ ] "Use client" presente onde há hook e importação de servidor
- [ ] Movimento reduzido tratado
- [ ] No máximo um componente WebGL por rota
- [ ] Caminho de toque para efeitos de ponteiro
- [ ] Nenhuma ferramenta de depuração no código
- [ ] Aviso de licença presente
- [ ] Tipos e build passam
- [ ] Console sem erro do componente

## On Failure

- **Gatilho de Erro**: qualquer verificação obrigatória falha, ou um comando sai com código diferente de zero.
- **Ação Imediata**: parar a verificação do item e não corrigir código por conta própria, porque esta skill só lê.
- **Rollback**: não há. Nenhuma alteração foi feita.
- **Fallback**: devolver o relatório ao agente que gerou o código, com as falhas em ordem de gravidade, para correção.
- **Logs**: registrar cada comando, sua saída e o código de saída.
