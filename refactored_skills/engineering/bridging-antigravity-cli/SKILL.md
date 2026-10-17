---
name: bridging-antigravity-cli
description: >
  Integra o Google Antigravity CLI (`agy`, OAuth da conta Google AI Pro) ao Claude Code como motor multimodal (imagem Nano Banana, vídeo Omni Flash e Veo 3.1) e como auditor adversário somente leitura de diffs, com o Claude como único escritor de código. Use this skill when: o usuário pedir imagem, ícone, vídeo ou asset visual gerado pelo Antigravity, uma revisão adversária de código por outro modelo (/agy-review), ou configurar o Antigravity no projeto (/antigravity-setup). Do NOT use this skill when: for revisão de código sem o Antigravity (use reviewing-multi-axis-code-quality), compor vídeo em código (use as skills de vídeo do hub) ou quando o pedido exigir chave de API paga, Vertex AI ou servidor MCP cobrado por token.
---

# Ponte Claude Code ↔ Antigravity

Nome do pedido original: `antigravity-bridge`. O validador do hub exige gerúndio no `name`, por isso a pasta é `bridging-antigravity-cli`.

## Regras invioláveis

1. **Custo extra zero.** Só o binário `agy` autenticado por OAuth (Google AI Pro). Nunca pedir `GEMINI_API_KEY`, nunca configurar Vertex AI ou AI Studio pay-as-you-go, nunca instalar MCP pago por token. O `agy-runner.sh` remove essas variáveis do ambiente de toda chamada.
2. **Single Writer.** Só o Claude altera código-fonte do projeto. O Antigravity gera mídia e revisa em `--mode=plan` (somente leitura). Nunca passe `--dangerously-skip-permissions`.
3. **Diversidade cognitiva.** `review_config.model` nunca pode ser `claude-*`, `sonnet`, `opus` ou `haiku`. O runner recusa (código 11).
4. **Nada de prompt genérico.** Todo pedido passa pelo Protocolo de Contexto e pelas matrizes de `reference/prompt-matrices.md` antes do `agy`.

## Input/Output Signature

Input:
- modo: `setup` | `media` | `review`
- pedido: texto do usuário (o quê e para quê)
- projeto: raiz do repositório (para ler contexto e `.claude/antigravity.json`)
- saída (media): caminho do asset; `transparent`: boolean
Output:
- success: boolean
- artifacts: asset gerado e validado, ou tabela de apontamentos classificados
- executionLog: stderr do `agy-runner.sh` (rodada usada, modelo, fallback do `brain`)

## Router and Selection Matrix

| Cenário | Ação | Grau de liberdade |
|---|---|---|
| Primeiro uso no repo ou `/antigravity-setup` | Setup interativo, grava `.claude/antigravity.json` | [FLEXÍVEL] |
| Imagem, ícone, logo, sticker | Contexto → prompt de 6 blocos → `agy-runner.sh media` | [FRÁGIL] runner e flags exatos |
| 2+ assets na mesma tela | Prompt JSON com blocos travados | [FRÁGIL] |
| Ajuste de imagem existente | Identity & Geometry Lock | [FRÁGIL] |
| Vídeo com produto específico | Keyframe no Nano Banana → validar → animar | [FRÁGIL] |
| Vídeo de UI/dados/texto | `remotion` (sem `agy`) | [FLEXÍVEL] |
| Revisão adversária | `git diff` → `agy-runner.sh review` → juízo crítico | [FRÁGIL] |

## Protocolo de Contexto (obrigatório antes de qualquer `agy`)

1. **Leia sem perguntar.** `README.md`, `CLAUDE.md`, `package.json`, `tailwind.config.*` ou variáveis CSS (paleta em HEX, tipografia, tema dark/light) e o componente onde o asset ou o código entra.
2. **Entenda o propósito.**
   - Mídia: *qual* elemento é (ícone, hero, textura, mock, componente isolado), *por que* existe (CTA, estado vazio, fundo decorativo, demo) e *onde* renderiza (dimensões do container, contraste com o fundo, transparência).
   - Review: *qual* problema de negócio o `git diff` resolve, quais contratos e camadas toca, quais restrições do projeto não podem quebrar.
3. **Pergunte só o que falta.** No máximo 2 ou 3 perguntas curtas, apenas se restar ambiguidade material, antes de gastar cota.

## Setup por projeto: `.claude/antigravity.json`

Se o arquivo não existir (ou no `/antigravity-setup`): leia o projeto, proponha valores detectados, mostre o JSON e peça confirmação antes de gravar. Esquema:

```json
{
  "project_context": {
    "domain": "detectado do projeto",
    "color_palette_hex": ["#0A0A0A", "#FFFFFF", "#00FF66"],
    "theme_mode": "dark",
    "style_anchor": "ex.: Minimalist SaaS",
    "default_transparent_assets": true
  },
  "review_config": { "model": "gemini-3.8-flash", "effort": "medium", "max_adversarial_rounds": 2 },
  "media_config": {
    "image_profile": "nano-banana-pro",
    "video_profile": "gemini-omni-flash",
    "default_output_dir": "public/assets"
  }
}
```

**Padrão inicial fixo:** `review_config.model` = `gemini-3.8-flash` e `effort` = `medium`, sempre. No setup, proponha esse par; só use outro se o usuário pedir. Antes de sugerir, rode `agy models` e use só os que ele lista (modelos `gemini-*` ou `gpt-oss-*`). Esforço: `low|medium|high|xhigh|max`. Recuse modelo Claude.

## Imperative Execution Workflow

### Mídia
1. [FRÁGIL] Rode `bash <skill>/scripts/agy-runner.sh check`. Falhou: pare e oriente o login OAuth (On Failure).
2. [FLEXÍVEL] Execute o Protocolo de Contexto.
3. [FRÁGIL] Reescreva o pedido pelas matrizes (`reference/prompt-matrices.md`): 6 blocos, ou JSON se houver 2+ assets, ou Identity & Geometry Lock se for edição. Elemento isolado: use o bloco de isolamento; nunca escreva "transparent" nem "checkerboard".
4. [FRÁGIL] Grave o prompt em arquivo temporário e rode:
   `bash <skill>/scripts/agy-runner.sh media --prompt-file P.txt --out <caminho> [--transparent]`
   Uma chamada por asset, sem retry em loop.
5. [FRÁGIL] Use a ferramenta `Read` no arquivo final e confira contra o contexto da UI (cores, recorte, margem, contraste). Só então declare concluído. Reprovou: ajuste o prompt uma vez; não insista.
6. [FLEXÍVEL] Se o Claude vai usar o asset no código, é o Claude quem edita o componente.

### Review adversário
1. [FRÁGIL] `check`, depois `git diff` (staged + unstaged) e Protocolo de Contexto.
2. [FLEXÍVEL] Monte o prompt pelo template da seção 9 das matrizes.
3. [FRÁGIL] `bash <skill>/scripts/agy-runner.sh review --prompt-file P.txt --task <id>` (usa modelo e esforço do JSON; força `--mode plan`).
4. [FRÁGIL] Não aceite passivamente. Verifique cada apontamento no código real e classifique em tabela:

| # | Apontamento | Classe | Ação |
|---|---|---|---|
| 1 | … | `[PROCEDENTE]` | bug real ou melhoria limpa: o Claude aplica o fix agora |
| 2 | … | `[CONTESTADO]` | alucinação, desconhecimento da arquitetura ou overengineering: rejeitar com contra-argumento técnico em 1 linha |
| 3 | … | `[DECISÃO HUMANA]` | altera regra de negócio ou contrato público: apresentar os dois lados e perguntar |

5. [FRÁGIL] **Circuit breaker:** no máximo 2 rodadas por tarefa (`max_adversarial_rounds`). O runner conta por `--task` e recusa a terceira (código 12). A rodada 2 reenvia só o diff dos fixes aplicados.

## Execution Checklist
- [ ] `agy-runner.sh check` passou (OAuth, sem chave de API)
- [ ] Contexto do projeto lido antes de perguntar
- [ ] Pedido reescrito pelas matrizes (nada de tag soup)
- [ ] Mídia: asset aberto com `Read` e validado
- [ ] Review: todos os apontamentos classificados; máximo 2 rodadas
- [ ] Nenhum arquivo de código editado pelo Antigravity

## On Failure
- **`agy` ausente ou não autenticado (10):** informe; oriente instalar e fazer login OAuth na conta Google AI Pro. Não peça chave de API nem proponha Vertex.
- **Modelo Claude escolhido (11):** troque por um modelo `gemini-*` ou `gpt-oss-*` de `agy models`.
- **Circuit breaker (12):** pare; apresente o estado e peça decisão humana.
- **Mídia não encontrada (13):** o runner já procurou em `~/.gemini/antigravity-cli/brain/` (2 min). Não repita em loop; revise o prompt ou aguarde a cota.
- **Alpha falhou (14):** instale `pillow numpy` (ou `rembg`), ou entregue com fundo sólido e avise.
- **Rollback:** o Antigravity não edita o projeto; basta descartar o asset gerado. Fixes do review são do Claude e seguem o fluxo normal de git.

## Reference Documentation

Matrizes de prompt, fontes e templates: `reference/prompt-matrices.md`. Runner: `scripts/agy-runner.sh`.
