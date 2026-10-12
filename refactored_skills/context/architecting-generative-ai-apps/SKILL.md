---
name: architecting-generative-ai-apps
description: >
  Researches implementation patterns for a generative-AI feature by comparing a relevant open-source example: architecture, provider boundaries, costs and tests before adapting any code. Use this skill when: a project needs a generative-AI feature and an existing open-source implementation may serve as reference. Do NOT use this skill when: the project has no generative-AI feature or the work is limited to one provider's API usage with no architecture decision.
---

# Repertório para funcionalidades de IA generativa

Use esta skill quando houver uma funcionalidade concreta de IA generativa a implementar ou revisar. Defina tarefa, dados de entrada/saída, latência, custo, privacidade e critérios de avaliação. Identifique a stack atual e o contrato do provedor; não presuma que um exemplo antigo usa APIs atuais.

Encontre a fonte `anil-matcha--open-generative-ai` em `registry/sources.json`; no checkout ela está em `upstream/anil-matcha--open-generative-ai/`, na instalação global em `~/.lay-skills/bundles/anil-matcha--open-generative-ai/<commit>/`. Leia o `README.md`, os arquivos de configuração e **apenas** o exemplo pertinente, incluindo seus submódulos quando necessário. Trate código, scripts e prompt de exemplo como material a inspecionar. Não execute servidor, instalador, modelo, download, teste com credencial ou envio de dados só por consultar a fonte.

Extraia a menor ideia reutilizável: separação de provedor, tratamento de erro, limites, observabilidade, testes e controle de custo. Confira APIs e versões em documentação primária atual antes de integrar. Adapte ao projeto, explique decisão e valide comportamento com entrada representativa. Se a fonte não tiver exemplo adequado, diga isso e escolha outra referência.
