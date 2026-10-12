#!/usr/bin/env python3
"""Gera a configuração de subagentes do projeto e a documentação de agents/.

- .claude/agents/<nome>.md: subagentes do Claude Code deste repositório, com caminhos relativos
  às skills públicas (refactored_skills/). Versionados com o projeto.
- agents/: documentação (índice, mapa de domínios, invocação).

A instalação global (~/.claude/agents, com as skills privadas locais) é feita por
scripts/skill_hub.py install. Os perfis vêm de agents/perfis.json, a fonte única.
"""
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO))

from scripts.skill_hub import (AGENTS_DOMINIOS, REFACTORED, claude_agent_text,  # noqa: E402
                               load_profiles, skill_entries)


def skills_publicas():
    """Skills públicas por domínio, com caminho relativo ao repositório."""
    por_dominio = {}
    for e in skill_entries(REPO, REFACTORED, 'local', 'refactored'):
        dominio = e['path'].split('/')[1]
        por_dominio.setdefault(dominio, []).append((e['name'], e['path'], e['description']))
    return por_dominio


def subagentes_do_projeto():
    """Nome do arquivo -> texto do subagente, prontos para .claude/agents/."""
    perfis = load_profiles(REPO)
    por_dominio = skills_publicas()
    return {p['nome'] + '.md': claude_agent_text(p, por_dominio.get(p['dominio'], [])) for p in perfis}


def escrever(caminho, texto):
    caminho.parent.mkdir(parents=True, exist_ok=True)
    caminho.write_text(texto, encoding='utf-8', newline='\n')


def main():
    perfis = load_profiles(REPO)
    total = sum(len(v) for v in skills_publicas().values())

    for nome, texto in subagentes_do_projeto().items():
        escrever(REPO / '.claude/agents' / nome, texto)

    indice = ['# Índice de subagentes (1 linha por domínio)', '']
    indice += [f'- {p["dominio"]}: {len(skills_publicas().get(p["dominio"], []))} skills públicas, subagente `{p["nome"]}`' for p in perfis]
    indice += ['', f'Total: {total} skills públicas em {len(perfis)} domínios.', '']
    escrever(REPO / 'agents/index/INDEX.md', '\n'.join(indice))

    mapa = ['# Mapa de domínios', '',
            '| Domínio | Skills públicas (repo) | Subagente do projeto | Subagente global |',
            '|---|---|---|---|']
    mapa += [f'| {p["dominio"]} | `refactored_skills/{p["dominio"]}/` | `.claude/agents/{p["nome"]}.md` | `~/.claude/agents/{p["nome"]}.md` |' for p in perfis]
    escrever(REPO / 'agents/wiring/DOMAIN_MAP.md', '\n'.join(mapa) + '\n')

    invocacao = '\n'.join([
        '# Invocação no Claude Code', '',
        'Há dois escopos com os mesmos nomes:',
        '- Projeto: `.claude/agents/` neste repositório, versionado, com as skills públicas.',
        '- Global: `~/.claude/agents/`, instalado por `scripts/skill_hub.py install`, com as skills privadas locais. Vale em todos os projetos.',
        'Quando os dois existem, o do projeto prevalece.', '',
        '## Como são chamados',
        '- Automático: o Claude escolhe o subagente pela `description`, com os gatilhos "Use quando" e "Não use para".',
        '- Explícito: peça pelo nome, por exemplo "use o subagente lay-seguranca para auditar este módulo".',
        '- Subagentes não chamam outros subagentes. O roteamento entre domínios é feito pela conversa principal, que segue a seção de orquestração do `CLAUDE.md` do projeto.',
        '- Se um subagente novo não aparecer, reinicie a sessão: os perfis são carregados no início.', '',
        '## Ferramentas',
        'Cada perfil declara as ferramentas que pode usar (`tools`). `lay-seguranca` só lê e analisa; não edita arquivos.', '',
        '## Contrato',
        'Ver `HANDOFF.md`: o subagente devolve RESULT com status, artifacts, summary e open_items.', '',
    ])
    escrever(REPO / 'agents/wiring/INVOCATION.md', invocacao)

    leiame = '\n'.join([
        '# Agentes LAY', '',
        'Um subagente por domínio de skills, gerado a partir de `perfis.json`.', '',
        '- `perfis.json`: fonte única (nome, description com gatilhos, ferramentas).',
        '- `.claude/agents/`: subagentes do projeto (versionados), com as skills públicas.',
        '- `scripts/skill_hub.py install`: subagentes globais em `~/.claude/agents/`, com as skills privadas locais.',
        '- `scripts/build_agents.py`: valida, gera `.claude/agents/` e esta documentação.',
        '- `CLAUDE.md`, seção "Orquestração de subagentes": roteamento domínio → subagente.',
        '- `wiring/`: mapa de domínios, contrato de handoff e invocação.',
        '- `index/INDEX.md`: índice de uma linha por domínio.', '',
    ])
    escrever(REPO / 'agents/README.md', leiame)

    print(f'domínios: {len(perfis)}  subagentes do projeto: {len(perfis)}  skills públicas: {total}')
    print('gerado: .claude/agents/ e documentação em agents/')


if __name__ == '__main__':
    main()
