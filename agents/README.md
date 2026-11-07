# Agentes LAY

Um subagente por domínio de skills, gerado a partir de `core/perfis.json`.

- `core/perfis.json`: fonte autoritativa de perfis (nome, description com gatilhos, ferramentas).
- `agents/perfis.json`: espelho sincronizado para compatibilidade legada.
- `.claude/agents/`: subagentes do projeto (versionados), com as skills públicas.
- `adapters/`: templates canônicos dos adaptadores de clientes (Claude, Codex, Antigravity).
- `scripts/skill_hub.py install`: subagentes e adaptadores globais em `~/.claude`, `~/.codex` e `~/.gemini`.
- `scripts/build_agents.py`: valida, gera `.claude/agents/`, documentação e atualiza adaptadores.
- `CLAUDE.md`, seção "Orquestração de subagentes": roteamento domínio → subagente.
- `wiring/`: mapa de domínios, contrato de handoff e invocação.
- `index/INDEX.md`: índice de uma linha por domínio.
