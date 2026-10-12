# Invocação

Papéis tool-agnósticos. Cada plataforma só muda como o perfil é carregado.

## Paralelização
- Domínios independentes podem rodar em paralelo.
- Limite de concorrência: plataformas podem recusar execuções acima de um teto de sub-agentes ativos. No DeepSeek Harness observou-se teto de 5 simultâneos; use lotes de até 5 quando a plataforma tiver o mesmo limite.

## Sequenciamento
- Quando o RESULT de um domínio é entrada de outro, rode em sequência.

## Escalonamento
- `escalated` e `needs_clarification` voltam ao diretor (`agents/director/SYSTEM.md`).

## Amarração por plataforma
- Claude Code: cada `SYSTEM.md` vira `.claude/agents/<domínio>.md` com frontmatter `name` e `description`. Invoca-se pela ferramenta de subagente.
- Antigravity: a definição de agente recebe o conteúdo do `SYSTEM.md` como instrução.
- DeepSeek Harness: a delegação de sub-agente usa o `SYSTEM.md` como instrução de papel.

## Verificação
- Diretor: 11 domínios, 132 skills no índice, zero leitura de `SKILL.md`.
