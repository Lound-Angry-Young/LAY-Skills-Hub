---
description: Revisão adversária do diff atual pelo Antigravity (somente leitura, máx. 2 rodadas)
argument-hint: [id-da-tarefa]
---
Use a skill `bridging-antigravity-cli`, modo **review**. Extraia o `git diff`, resuma objetivo e contratos afetados, rode `scripts/agy-runner.sh review --task <id>`, classifique cada apontamento como `[PROCEDENTE]`, `[CONTESTADO]` ou `[DECISÃO HUMANA]` verificando o código real, aplique só os procedentes e respeite o limite de 2 rodadas.

Tarefa: $ARGUMENTS
