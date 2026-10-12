# Invocação no Claude Code

Os subagentes são globais: ficam em `~/.claude/agents/` e valem em qualquer projeto.

## Como são chamados
- Automático: o Claude escolhe o subagente pela `description`, que traz os gatilhos "Use quando" e "Não use para".
- Explícito: peça pelo nome, por exemplo "use o subagente lay-seguranca para auditar este módulo".
- Subagentes não chamam outros subagentes. O roteamento entre domínios é feito pela conversa principal, que segue o índice do bloco LAY no `~/.claude/CLAUDE.md`.
- Se um subagente novo não aparecer, reinicie a sessão do Claude Code: os perfis são carregados no início.

## Ferramentas
Cada perfil declara as ferramentas que pode usar (`tools`). `lay-seguranca` só lê e analisa; não edita arquivos.

## Contrato
Ver `HANDOFF.md`: o subagente devolve RESULT com status, artifacts, summary e open_items.
