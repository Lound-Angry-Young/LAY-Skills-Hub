## Table of Contents
1. Fontes canônicas
2. Regras do Nano Banana
3. Template dos 6 blocos
4. JSON prompting (2+ assets)
5. Elemento isolado e alpha real
6. Tipografia
7. Edição Identity & Geometry Lock
8. Pipeline de vídeo (7 camadas)
9. Template do prompt de revisão adversária
10. Contexto de projeto → prompt (tabela)

# Matrizes de prompt do Antigravity Bridge

O Claude reescreve todo pedido do usuário por estas matrizes antes de chamar `agy-runner.sh`. Pedido cru nunca vai direto ao `agy`.

## 1. Fontes canônicas

Consulte-as (WebFetch) quando uma regra abaixo parecer desatualizada. Não copie trechos longos delas.

| Fonte | URL |
|---|---|
| Gemini Image (Nano Banana) | https://ai.google.dev/gemini-api/docs/image-generation |
| Vertex AI, guia de prompt de imagem | https://cloud.google.com/vertex-ai/generative-ai/docs/image/img-gen-prompt-guide |
| Veo, guia de prompt de vídeo | https://cloud.google.com/vertex-ai/generative-ai/docs/video/video-gen-prompt-guide |
| LMArena (benchmarks Image/Edit) | https://lmarena.ai/ |
| PromptHero | https://prompthero.com/ |
| PromptBase | https://promptbase.com/ |
| Comunidades | r/GeminiAI, r/PromptEngineering, r/ClaudeCode |

As URLs de API acima servem só como documentação de prompt. Nunca configure chave de API, Vertex ou AI Studio: o acesso é somente pelo `agy` via OAuth.

## 2. Regras do Nano Banana (obrigatórias)

1. **Sem tag soup.** Proibido `8k, masterpiece, octane, trending`. Use frases completas e relacionais sobre material, geometria e espaço: o encoder é um LLM Gemini.
2. **Hierarquia front-loaded em 6 blocos** (seção 3). O que importa mais vem primeiro.
3. **JSON prompting** quando houver 2 ou mais assets para a mesma tela ou produto (seção 4).
4. **Tipografia precisa** com a string exata entre aspas duplas (seção 6).
5. **Edição sem máscara** só com Identity & Geometry Lock (seção 7). Proibido reescrever do zero ou pedir "fix".
6. **Uma imagem, um asset.** O prompt descreve exatamente um sujeito (um ícone, um elemento ou uma cena completa). Proibido pedir sheet, grid, set, coleção, "variations", "icons in different sizes" ou vários ícones no mesmo quadro. Para N assets, N prompts em sequência (seção 4 mantém a consistência). Cena: descreva a cena inteira numa só imagem, com todos os elementos, composição e profundidade que o usuário descreveu.
7. **Contexto do projeto obrigatório.** O bloco 2 e o bloco 5 carregam o motivo da marca (o que o projeto já mostra: mascote, logo, motivo), a paleta HEX e o estilo reais, lidos de assets abertos com `Read`. Ex.: projeto com caveira halftone → o favicon é a caveira, não um símbolo genérico.
8. **Nunca** escrever "transparent background", "checkerboard" ou "PNG with alpha". Peça fundo sólido liso e use `--transparent` no runner (seção 5).

## 3. Template dos 6 blocos

Escreva em inglês, em parágrafo corrido, nesta ordem:

```text
[1 ENQUADRAMENTO] Shot type, physical lens and aspect ratio (e.g. "Straight-on product shot, 85mm lens at f/8 for edge-to-edge sharpness, 1:1 square").
[2 SUJEITO] The subject with exact geometry, materials and the project's HEX colors (e.g. "a rounded-square app icon, 3 mm beveled edge, matte anodized aluminum in #0A0A0A with a single inlaid #00FF66 glyph").
[3 CONTEXTO/ISOLAMENTO] Spatial context, or the isolation clause from section 5 when the asset must be cut out.
[4 ILUMINAÇÃO] Direction, color temperature in Kelvin, rim light and shadow (e.g. "key light from upper left at 5600K, cool rim light at 7500K from behind, soft contact shadow only under the object").
[5 STYLE ANCHOR] The project's style_anchor from .claude/antigravity.json, in a full sentence.
[6 RESTRIÇÕES] Negative constraints as a sentence: "No text, no watermarks, no plastic gloss, no cropped borders."
```

## 4. JSON prompting para consistência de design system

Para 2 ou mais assets da mesma tela, envie um objeto por asset. Os blocos `camera`, `lighting`, `color_palette` e `style_anchor` ficam **idênticos** (travados); só `subject` muda.

```json
{
  "camera": "Straight-on, 85mm lens at f/8, 1:1",
  "lighting": "Key light upper left 5600K, cool rim light 7500K, soft contact shadow only",
  "color_palette": ["#0A0A0A", "#FFFFFF", "#00FF66"],
  "style_anchor": "Brutalist cyberpunk UI, matte materials, hard edges",
  "isolation": "Isolated die-cut element on flat uniform background, 15% padding",
  "subject": "A rounded-square shield icon with a single inlaid glyph",
  "constraints": "No text, no watermarks, no plastic gloss, no cropped borders"
}
```

O primeiro asset aprovado vira referência visual dos seguintes: cite o caminho absoluto dele e use a seção 7 para variações.

## 5. Elemento isolado e fundo transparente (alpha real)

Vale para ícone, logo, sticker, personagem, objeto isolado e componente de UI. Não vale para banner ou cenário completo.

Injete este bloco no prompt (substitui o bloco 3):

```text
Isolated UI asset / die-cut element centered with generous padding (15% margin on all sides), no cropped edges, rendered on a completely flat, solid, uniform studio background (<COR>), zero drop shadow on the background floor, crisp well-defined outer silhouette edges for clean alpha extraction.
```

Escolha `<COR>` pelo sujeito, sempre uma cor que **não aparece dentro do sujeito**:

| Sujeito | `<COR>` |
|---|---|
| Escuro | `pure matte white #FFFFFF` |
| Claro | `pure matte black #000000` |
| Claro e com preto, ou contém branco e preto | `chroma green #00FF00` |
| Contém verde | `chroma magenta #FF00FF` |

Depois rode o runner com `--transparent`. O script amostra a cor de fundo nas bordas, remove-a (rembg, se instalado; senão PIL/numpy) e confirma que o PNG/WebP final tem alpha real. Vidro, fumaça e sombras suaves não recortam bem: avise o usuário.

## 6. Tipografia

- String exata entre aspas duplas: `the text "LAUNCH WEEK"`.
- Descreva família e superfície: `set in a heavy geometric sans-serif, engraved into the brushed-steel plate`.
- Texto longo (mais de 5 palavras) é frágil: prefira compor o texto em HTML/CSS no produto.

## 7. Edição Identity & Geometry Lock

Modelo fixo (substitua os campos entre `<>`):

```text
Use <CAMINHO_ABSOLUTO_IMAGEM_BASE> as primary reference. Identity & Geometry Lock: Preserve 100% of the subject's exact geometry, proportions, material textures, and color palette. Modify ONLY <ELEMENTO> to <NOVO_ESTADO>, maintaining original perspective and lighting direction.
```

Uma alteração por chamada. Se a saída mudar mais do que `<ELEMENTO>`, descarte e reduza o pedido; não encadeie correções.

## 8. Pipeline de vídeo

**Ordem obrigatória de 7 camadas:**

```text
[1 Câmera/Movimento/Lente] + [2 Sujeito] + [3 Ação e Física] + [4 Ambiente] + [5 Iluminação/Kelvin] + [6 Estilo/Textura] + [7 Áudio nativo/SFX]
```

Perfis (`media_config.video_profile`):

| Perfil | Quando | Regra |
|---|---|---|
| `veo-3.1` com produto específico | produto, mock ou marca precisa ficar fiel | 1) gerar o **keyframe estático** no Nano Banana; 2) o Claude o abre com `Read` e valida; 3) só então animar a partir dele, citando o caminho absoluto |
| `gemini-omni-flash` | clipe curto, exploração rápida | 7 camadas; um movimento de câmera por clipe |
| `remotion` | motion de UI, dados ou texto | não usa o `agy`: compõe em código (Claude escreve; veja a skill de vídeo do hub) |

Um movimento de câmera e uma ação principal por clipe. Descreva física concreta ("the lid hinges open 40 degrees and settles"), não adjetivos.

## 9. Template do prompt de revisão adversária

Montado pelo Claude a partir do `git diff`. Envie com `--mode plan` (somente leitura, aplicado pelo runner).

```text
ROLE: You are a skeptical senior engineer reviewing a change you did not write. You are READ-ONLY: do not edit files, do not propose to run commands.

BUSINESS GOAL: <qual problema de negócio o diff resolve, em 1-2 frases>
CONTRACTS/LAYERS TOUCHED: <APIs, tipos, tabelas, eventos afetados>
PROJECT CONSTRAINTS (must not be violated): <regras de CLAUDE.md/README/ADRs>

DIFF:
<git diff>

HUNT FOR, in this priority: broken contracts between layers; race conditions and ordering bugs; incomplete transactions and partial failure; type mismatches across layers; hidden side effects; unnecessary abstractions or overengineering.

OUTPUT FORMAT: a numbered list. For each item: file:line, severity (high|medium|low), the concrete failing scenario (inputs -> wrong result), and the smallest fix. If you find nothing material, say "no material findings". Do not pad. Do not suggest style changes.
```

## 10. Contexto de projeto → prompt

O motivo da marca vem primeiro; HEX e estilo vêm depois. Lição de campo: um favicon gerado só com paleta e um raio genérico não comunicava o projeto; refeito com a caveira halftone, a sombra dura amarela e a borda grafite da própria marca, passou.


| Dado lido do projeto | Onde aparece no prompt |
|---|---|
| Motivo da marca (mascote, logo, ilustração central) | bloco 2, como sujeito |
| Regras visuais do UI (bordas, sombras duras, cantos, texturas) | blocos 2 e 5 |
| Paleta (tailwind/CSS vars) em HEX | bloco 2 e `color_palette` |
| Tema dark/light | bloco 4 (luz) e escolha da cor de fundo de isolamento |
| `style_anchor` | bloco 5 |
| Dimensões do container | bloco 1 (proporção) |
| Contraste com o fundo da UI | cor de fundo de isolamento e margens |
| Necessidade de transparência | `--transparent` e seção 5 |
