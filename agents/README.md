# Agentes LAY

Um subagente por domínio de skills, gerado a partir de `perfis.json`.

- `perfis.json`: fonte única (nome, description com gatilhos, ferramentas).
- `scripts/skill_hub.py install`: grava os subagentes em `~/.claude/agents/` e atualiza o índice no CLAUDE.md global.
- `scripts/build_agents.py`: valida os perfis e regenera esta documentação.
- `wiring/`: mapa de domínios, contrato de handoff e invocação.
- `index/INDEX.md`: índice de uma linha por domínio.
