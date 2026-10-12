---
name: integrating-external-ui-components
description: >
  Installs and adapts one Pixel-Perfect or Componentry component in a React or Next.js project: fetches only the chosen item and the registry files it needs through the shadcn CLI at the moment of use, prepares the utils helper and TypeScript types, keeps the MIT notice, adds the use client directive and reduced-motion handling, adds touch fallback for pointer-only effects and removes debug controls. Use this skill when: copying an item from those registries into a project after the item was chosen. Do NOT use this skill when: choosing the component (use selecting-animated-ui-components), writing a component from scratch (use engineering-frontend-interfaces) or checking a finished component (use verifying-animated-component-compliance).
---

# Integrando componentes externos

Instala um item já escolhido e prepara o projeto para ele funcionar. Esta é a única skill que baixa código. Ela baixa só quando é usada, só o item escolhido e o que ele precisa. A linha do item (tier, "Use client", "Mov. reduzido", "Toque", "Instalar antes") está no catálogo da skill [selecting-animated-ui-components](../selecting-animated-ui-components/SKILL.md), na seção de domínios.

## Input/Output Signature

Input:
- itemName: string # nome do item no registro, ex.: img-glitch
- source: string # pixel-perfect ou componentry
- projectPath: string # raiz do projeto alvo
- packageManager: string # npm, pnpm, yarn ou bun, pelo lockfile
- dryRun: boolean # se verdadeiro, só lista comandos e arquivos afetados (default: true)

Output:
- success: boolean # indica se o item foi instalado e adaptado
- status: string # completed, failed, skipped ou awaiting-confirmation
- artifacts: array # arquivos criados ou alterados
- executionLog: string # comandos executados, URLs e saídas

## O que baixar, e quando

Baixe só na execução desta skill, para um item escolhido. Nunca baixe na seleção, nem ao carregar a skill. Nunca clone repositório e nunca baixe o catálogo inteiro. Baixe apenas:
1. O item escolhido, pela URL da fonte.
2. A cadeia de dependências do registro. O CLI traz a maior parte sozinho, pelo campo `registryDependencies`. Só os itens marcados como "instalar à mão" na coluna "Instalar antes" precisam de comando separado.
3. `lib/utils.ts` (função `cn`), quando o código importa `@/lib/utils` e o projeto não tem o arquivo. O CLI não traz esse arquivo sozinho.
4. Componentes padrão do shadcn citados como "shadcn: `nome`", como `button`.
5. Pacotes npm que o código importa e o CLI não declarou (ver o passo de tipos).

Se o arquivo de destino já existir, não baixe de novo. Pare com `status: awaiting-confirmation`.

## Como baixar

Use os comandos abaixo, sempre com `-y` para não abrir pergunta interativa. Troque `npx` pelo gerenciador do lockfile (`pnpm dlx`, `yarn dlx`, `bunx --bun`) quando for o caso.

- Utilitário `cn`: `npx shadcn@latest add utils -y`
- Item pela URL da fonte: `npx shadcn@latest add <url> -y`
  - Pixel-Perfect: `https://www.pixel-perfect.space/r/<nome>.json`
  - Componentry: `https://componentry.dev/r/<nome>.json`
- Componente padrão do shadcn: `npx shadcn@latest add <nome> -y`
- Pacote npm faltando: `npm install <pacote>` (ou o gerenciador do projeto)
- Para ler o código antes de adaptar, sem gravar nada no projeto: `curl -sL "<url>" -o <pasta-temporaria>/<nome>.json` e leia o campo `files[].content`.

## Procedimento

1. [FRÁGIL] Confirme o alvo. Leia `components.json` na raiz. Se não existir, pare com `status: awaiting-confirmation`. Não rode `shadcn init` sem confirmação do usuário.
2. [FRÁGIL] Leia a linha do item no catálogo: tier, "Use client", "Mov. reduzido", "Toque" e "Instalar antes".
3. [FRÁGIL] Instale `utils` se o item importa `@/lib/utils` e `lib/utils.ts` não existe. Quase todos os itens do Componentry importam esse arquivo. Confirme lendo o código com `curl`, ou procure `@/lib/utils` no arquivo depois da instalação.
4. [FRÁGIL] Instale o item: `npx shadcn@latest add <url> -y`. O CLI baixa a cadeia de `registryDependencies`. Se ele relatar conflito com arquivo existente, pare com `status: awaiting-confirmation`. Não sobrescreva arquivo do usuário.
5. [FRÁGIL] Instale à mão o que o CLI não trouxe. Para cada item em "instalar à mão", na ordem indicada, rode `npx shadcn@latest add <url-do-item> -y`. Para "shadcn: `nome`", rode `npx shadcn@latest add <nome> -y`. Para "manual", pare e pergunte: o registro não tem esse arquivo.
6. [FLEXÍVEL] Localize os arquivos. A pasta não é sempre a mesma. Num projeto com `src/`, itens do Pixel-Perfect foram para `src/components/pixel-perfect/`, e o item do Componentry para `components/ui/`. Encontre com `find . -name "<nome>.tsx" -not -path "*/node_modules/*"` e ajuste os imports ao caminho real.
7. [FRÁGIL] Tipos, em projeto TypeScript. Rode `npx tsc --noEmit`. Três erros apareceram nos testes, com a correção confirmada:
   - `TS7016: Could not find a declaration file for module 'three'`: instale `npm install -D @types/three@~<minor>.0`, com o minor do `three` instalado. Exemplo: `three` 0.186.x pede `@types/three@~0.186.0`.
   - `TS2307: Cannot find module 'class-variance-authority'`: o componente `button` do shadcn importa esse pacote e não o declara. Instale com `npm install class-variance-authority`.
   - `TS2307: Cannot find module '@/lib/utils'`: volte ao passo 3.
8. [FRÁGIL] Client boundary. Se o item usa hook ou evento e o arquivo principal não começa com `"use client"`, acrescente a diretiva na primeira linha. Se um arquivo de servidor (App Router) importar esse componente, mova o uso para um componente cliente. Fora do App Router, a diretiva não tem efeito e não atrapalha.
9. [FRÁGIL] Movimento reduzido. Se "Mov. reduzido" for "não", envolva o efeito com a checagem do padrão abaixo.
10. [FRÁGIL] Toque. Se "Toque" for "não" e o efeito depender de ponteiro, desative a animação em `(hover: none)` e mostre o estado final.
11. [FRÁGIL] Depuração. Se o item importa `lil-gui`, remova a importação e os controles, e mantenha os valores padrão como constantes. Depois rode `npm uninstall lil-gui`. A adaptação de controles é manual e não foi testada: confirme no navegador que o efeito continua funcionando.
12. [FRÁGIL] Licença. Mantenha o aviso MIT do arquivo copiado quando o original tiver cabeçalho. Registre a nota de cada biblioteca usada (GSAP, Three.js, Framer Motion, Motion) num `THIRD_PARTY_NOTICES` ou no README do projeto. Não afirme termos de licença que você não verificou na fonte.
13. [FLEXÍVEL] Verifique. Rode `verifying-animated-component-compliance` sobre os arquivos criados.

## Padrão de movimento reduzido

Com Framer Motion, use o hook do próprio pacote:

```tsx
import { useReducedMotion } from "framer-motion";

const reduzir = useReducedMotion();
// Com reduzir === true: renderize o estado final, sem transição.
```

Com GSAP, use `gsap.matchMedia()` e registre a animação apenas na condição `(prefers-reduced-motion: no-preference)`. Sem biblioteca, use `window.matchMedia("(prefers-reduced-motion: reduce)")` e pule a animação.

## Checklist

- [ ] `components.json` existe
- [ ] `lib/utils.ts` existe, quando o código importa `@/lib/utils`
- [ ] Item instalado pelo CLI, sem sobrescrever arquivos
- [ ] Itens "instalar à mão" instalados, na ordem
- [ ] Arquivos localizados e imports ajustados ao caminho real
- [ ] `tsc --noEmit` sem erro (`three`, `class-variance-authority`, `@/lib/utils`)
- [ ] "Use client" conferido no arquivo que o Next.js importa
- [ ] Movimento reduzido tratado
- [ ] Fallback de toque tratado, quando o efeito depende de ponteiro
- [ ] `lil-gui` removido
- [ ] Aviso de licença registrado

## On Failure

- **Gatilho de Erro**: `components.json` ausente, URL com 404, conflito de arquivo, `tsc` com erro que não está na lista do passo 7, ou entrada "manual" em "Instalar antes".
- **Ação Imediata**: interromper a instalação. Não sobrescrever nenhum arquivo existente.
- **Rollback**: remover apenas os arquivos listados como criados nesta execução (o CLI informa "Created N file(s)"). O CLI não desfaz nada sozinho. Não reverter alterações anteriores do usuário.
- **Fallback**: copiar manualmente o campo `content` dos arquivos do JSON do item, e confirmar com o usuário o caminho de destino.
- **Logs**: registrar o comando exato, a URL, o código de saída e a lista de arquivos criados.
