# Claude — LAY Skills Hub

Leia [AGENTS.md](AGENTS.md) e siga [skills/lay-orchestrator/SKILL.md](skills/lay-orchestrator/SKILL.md) quando trabalhar com este hub ou aplicar seu repertório.

Use os caminhos e comandos de [docs/OPERACAO.md](docs/OPERACAO.md). O instalador registra `SessionStart` nas configurações globais e preserva hooks existentes; verifique o arquivo carregado pelo cliente antes de declarar execução automática. As instruções globais continuam como fallback.

Skills globais desta máquina não implicam instalação no Claude web, Cowork, contêineres ou máquinas remotas. Preserve regras pessoais existentes durante integração.

## Orquestração de subagentes

Os subagentes deste projeto ficam em `.claude/agents/` e são versionados, com as skills públicas do repositório. Os globais em `~/.claude/agents/` valem em todos os projetos, com as skills privadas locais. Quando os dois existem, o do projeto prevalece.

Roteamento de domínio para subagente. A conversa principal decide e delega; subagentes não chamam outros subagentes:

- routing-and-proxy → `lay-omniroute`
- frontend → `lay-frontend`
- engineering → `lay-engenharia`
- context → `lay-contexto`
- devops → `lay-devops`
- qa → `lay-qa`
- security → `lay-seguranca`
- creative-3d → `lay-3d`
- documentation → `lay-documentacao`
- design → `lay-design`
- database → `lay-banco-de-dados`

Regras:
- Um domínio primário por pedido. Domínios independentes podem rodar em paralelo, em lotes de até 5.
- Pedido ambíguo: no máximo uma pergunta de clarificação.
- Nenhum domínio cobre o pedido: informe e sugira criar uma skill.
- Quem delega envia HANDOFF e recebe RESULT. A resposta final ao usuário é em português direto.
- Ações externas ou irreversíveis (enviar, publicar, apagar) só com confirmação explícita.
- Contrato: `agents/wiring/HANDOFF.md`. Invocação: `agents/wiring/INVOCATION.md`.
