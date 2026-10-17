---
description: Configura o Antigravity no projeto (.claude/antigravity.json) a partir do contexto do repositório
---
Use a skill `bridging-antigravity-cli` (`refactored_skills/design/bridging-antigravity-cli/SKILL.md`), modo **setup**.

1. Rode `bash refactored_skills/design/bridging-antigravity-cli/scripts/agy-runner.sh check` e `agy models` (só modelos listados; nunca `claude-*`).
2. Leia README.md, CLAUDE.md, package.json, tailwind.config.* / variáveis CSS (paleta HEX, tema, tipografia).
3. O padrão do modelo é sempre `gemini-3.8-flash` com esforço `medium`.
4. Proponha o conteúdo de `.claude/antigravity.json`, mostre ao usuário e grave só após confirmação.

Argumentos do usuário: $ARGUMENTS
