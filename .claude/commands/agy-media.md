---
description: Gera imagem ou vídeo via Antigravity (agy, OAuth) com contexto do projeto e validação visual
argument-hint: <o que gerar, onde será usado>
---
Use a skill `bridging-antigravity-cli`, modo **media**. Siga o Protocolo de Contexto, reescreva o pedido pelas matrizes em `reference/prompt-matrices.md`, rode `scripts/agy-runner.sh media` (use `--transparent` para elementos isolados) e valide o arquivo final com `Read` antes de concluir. Se `.claude/antigravity.json` não existir, execute o setup primeiro.

Pedido: $ARGUMENTS
