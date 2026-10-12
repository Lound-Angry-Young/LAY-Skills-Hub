# Invocação no Claude Code

Há dois escopos com os mesmos nomes:
- Projeto: `.claude/agents/` neste repositório, versionado, com as skills públicas.
- Global: `~/.claude/agents/`, instalado por `scripts/skill_hub.py install`, com as skills privadas locais. Vale em todos os projetos.
Quando os dois existem, o do projeto prevalece.

## Como são chamados
- Automático: o Claude escolhe o subagente pela `description`, com os gatilhos "Use quando" e "Não use para".
- Explícito: peça pelo nome, por exemplo "use o subagente lay-seguranca para auditar este módulo".
- Subagentes não chamam outros subagentes. O roteamento entre domínios é feito pela conversa principal, que segue a seção de orquestração do `CLAUDE.md` do projeto.
- Se um subagente novo não aparecer, reinicie a sessão: os perfis são carregados no início.

## Ferramentas
Cada perfil declara as ferramentas que pode usar (`tools`). `lay-seguranca` só lê e analisa; não edita arquivos.

## Contrato
Ver `HANDOFF.md`: o subagente devolve RESULT com status, artifacts, summary e open_items.
