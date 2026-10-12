# Agentes LAY

Um subagente por domínio de skills, gerado a partir de `perfis.json`.

- `perfis.json`: fonte única (nome, description com gatilhos, ferramentas).
- `.claude/agents/`: subagentes do projeto (versionados), com as skills públicas.
- `scripts/skill_hub.py install`: subagentes globais em `~/.claude/agents/`, com as skills privadas locais.
- `scripts/build_agents.py`: valida, gera `.claude/agents/` e esta documentação.
- `CLAUDE.md`, seção "Orquestração de subagentes": roteamento domínio → subagente.
- `wiring/`: mapa de domínios, contrato de handoff e invocação.
- `index/INDEX.md`: índice de uma linha por domínio.
