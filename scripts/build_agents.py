#!/usr/bin/env python3
"""Gera a documentação de agents/ a partir de agents/perfis.json.

Os arquivos que o Claude Code carrega são gerados e instalados por scripts/skill_hub.py install
(em ~/.claude/agents). Este script só valida os perfis e escreve a documentação do repositório.
"""
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO))

from scripts.skill_hub import AGENTS_DOMINIOS, load_profiles  # noqa: E402


def contar_skills(dominio):
    return len(list((REPO / 'refactored_skills' / dominio).glob('*/SKILL.md')))


def escrever(caminho, texto):
    caminho.parent.mkdir(parents=True, exist_ok=True)
    caminho.write_text(texto, encoding='utf-8', newline='\n')


def main():
    perfis = load_profiles(REPO)
    total = sum(contar_skills(d) for d in AGENTS_DOMINIOS)

    indice = ['# Índice de subagentes (1 linha por domínio)', '']
    indice += [f'- {p["dominio"]}: {contar_skills(p["dominio"])} skills, subagente `{p["nome"]}`' for p in perfis]
    indice += ['', f'Total: {total} skills públicas em {len(perfis)} domínios.', '']
    escrever(REPO / 'agents/index/INDEX.md', '\n'.join(indice))

    mapa = ['# Mapa de domínios', '', '| Domínio | Skills (repo) | Subagente | Arquivo instalado |', '|---|---|---|---|']
    mapa += [f'| {p["dominio"]} | `refactored_skills/{p["dominio"]}/` | `{p["nome"]}` | `~/.claude/agents/{p["nome"]}.md` |' for p in perfis]
    escrever(REPO / 'agents/wiring/DOMAIN_MAP.md', '\n'.join(mapa) + '\n')

    invocacao = '\n'.join([
        '# Invocação no Claude Code', '',
        'Os subagentes são globais: ficam em `~/.claude/agents/` e valem em qualquer projeto.', '',
        '## Como são chamados',
        '- Automático: o Claude escolhe o subagente pela `description`, que traz os gatilhos "Use quando" e "Não use para".',
        '- Explícito: peça pelo nome, por exemplo "use o subagente lay-seguranca para auditar este módulo".',
        '- Subagentes não chamam outros subagentes. O roteamento entre domínios é feito pela conversa principal, que segue o índice do bloco LAY no `~/.claude/CLAUDE.md`.',
        '- Se um subagente novo não aparecer, reinicie a sessão do Claude Code: os perfis são carregados no início.', '',
        '## Ferramentas',
        'Cada perfil declara as ferramentas que pode usar (`tools`). `lay-seguranca` só lê e analisa; não edita arquivos.', '',
        '## Contrato',
        'Ver `HANDOFF.md`: o subagente devolve RESULT com status, artifacts, summary e open_items.', '',
    ])
    escrever(REPO / 'agents/wiring/INVOCATION.md', invocacao)

    leiame = '\n'.join([
        '# Agentes LAY', '',
        'Um subagente por domínio de skills, gerado a partir de `perfis.json`.',
        '',
        '- `perfis.json`: fonte única (nome, description com gatilhos, ferramentas).',
        '- `scripts/skill_hub.py install`: grava os subagentes em `~/.claude/agents/` e atualiza o índice no CLAUDE.md global.',
        '- `scripts/build_agents.py`: valida os perfis e regenera esta documentação.',
        '- `wiring/`: mapa de domínios, contrato de handoff e invocação.',
        '- `index/INDEX.md`: índice de uma linha por domínio.', '',
    ])
    escrever(REPO / 'agents/README.md', leiame)

    print(f'domínios: {len(perfis)}  subagentes: {len(perfis)}  skills: {total}')
    print('documentação gerada em agents/ (README, index, wiring)')


if __name__ == '__main__':
    main()
