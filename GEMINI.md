# Antigravity — LAY Skills Hub

Leia [AGENTS.md](AGENTS.md) e aplique [skills/lay-orchestrator/SKILL.md](skills/lay-orchestrator/SKILL.md) conforme a tarefa. Use [docs/GUIA.md](docs/GUIA.md) para roteamento e [docs/OPERACAO.md](docs/OPERACAO.md) para instalação e início de projeto.

A instalação deste hub cobre o perfil global do Antigravity IDE/2.0 e o diretório global do Antigravity CLI. O hook `PreInvocation` é registrado na configuração da IDE; verifique a descoberta real no cliente, pois presença de arquivos não prova que a skill foi carregada.

Toda nova skill criada ou adicionada deve obedecer estritamente a [docs/PADRAO_DE_SKILLS.md](docs/PADRAO_DE_SKILLS.md) e ao modelo [templates/SKILL.template.md](templates/SKILL.template.md) (frontmatter YAML com nome em gerúndio e limites explícitos, responsabilidade única, assinatura I/O, passos imperativos com graus de liberdade, checklist, seção On Failure e progressive disclosure em reference.md).

