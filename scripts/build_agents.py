#!/usr/bin/env python3
"""Gera agents/ a partir de refactored_skills/.

Perfis apontam para os SKILL.md; não copiam o corpo das skills. Só nome e
description entram nos perfis, lidos do frontmatter de cada SKILL.md.
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
REF = ROOT / 'refactored_skills'
OUT = ROOT / 'agents'

DOMAINS = [
    'routing-and-proxy', 'frontend', 'engineering', 'context', 'devops', 'qa',
    'security', 'creative-3d', 'documentation', 'design', 'database',
]

SUMMARY = {
    'routing-and-proxy': 'CLI e API do OmniRoute: inferência, providers, combos, proxies, custos, MCP, A2A, webhooks e túneis.',
    'frontend': 'UI de produção, React, animações (GSAP, Lenis, view transitions), direção visual e redesign.',
    'engineering': 'Arquitetura, APIs, especificações, code review, debug, performance, migrações e minimalismo.',
    'context': 'Contexto de sessão, compressão de prompt e mensagens, grafos de conhecimento, requisitos e planejamento.',
    'devops': 'Git, CI/CD, deploy na Vercel, releases, rollouts graduais e prontidão de lançamento.',
    'qa': 'Testes (TDD, browser, DevTools), benchmarks de modelos, qualidade de código e gates de CI e PR.',
    'security': 'Auditoria de código, Semgrep, dependências, segurança de LLM, chaves e sessões de API.',
    'creative-3d': 'Renderização 3D, Blender, calibração de hardware, fundos WebGL e bibliotecas criativas.',
    'documentation': 'Revisão de escrita, ADRs, limpeza de prosa e remoção de marcas de proveniência de IA.',
    'design': 'Geração de brandkit, mockups de mobile e web e consulta de referências visuais.',
    'database': 'Backup, restauração e cache de banco de dados do OmniRoute e da CLI.',
}


def read_skill(path):
    text = path.read_text(encoding='utf-8').replace('\r\n', '\n')
    m = re.match(r'---\n(.*?)\n---\n', text, re.S)
    if not m:
        raise SystemExit(f'sem frontmatter: {path}')
    fm = m.group(1) + '\n'
    name = re.search(r'^name:\s*(.+)$', fm, re.M).group(1).strip()
    block = re.search(r'^description:\s*>\n((?:  .*\n)+)', fm, re.M)
    if block:
        desc = ' '.join(line.strip() for line in block.group(1).splitlines())
    else:
        desc = re.search(r'^description:\s*(.+)$', fm, re.M).group(1).strip().strip('"')
    return name, desc


def load_domain(domain):
    skills = []
    for folder in sorted(p for p in (REF / domain).iterdir() if p.is_dir()):
        skill_md = folder / 'SKILL.md'
        if skill_md.exists():
            name, desc = read_skill(skill_md)
            if name != folder.name:
                raise SystemExit(f'name {name!r} difere da pasta {folder.name!r}')
            skills.append((folder.name, desc))
    return skills


def write(rel, text):
    path = OUT / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding='utf-8', newline='\n')
    return path


def build():
    data = {d: load_domain(d) for d in DOMAINS}
    total = sum(len(s) for s in data.values())
    index_lines = [f'- {d}: {len(data[d])} skills — {SUMMARY[d]}' for d in DOMAINS]

    director = f"""# Agente Diretor (Roteador)

Você é o roteador do ecossistema LAY Skills Hub. Você NÃO executa tarefas de domínio e NÃO lê nenhum `SKILL.md`. Conhece apenas o índice abaixo.

## Índice Global (1 linha por domínio)
{chr(10).join(index_lines)}

## Regras de roteamento
1. Classifique a intenção em exatamente um domínio primário.
2. Se a tarefa tiver partes independentes, acione os domínios correspondentes em paralelo.
3. Ambíguo: faça no máximo 1 pergunta de clarificação.
4. Nenhum domínio cobre: informe e sugira criar uma skill.

## Handoff
Envie HANDOFF ao sub-agente do domínio (`agents/domains/<domínio>/SYSTEM.md`, mapeamento em `agents/wiring/DOMAIN_MAP.md`; contrato em `agents/wiring/HANDOFF.md`). Agregue os RESULT e responda em linguagem natural.

## Escalonamento
- `escalated`: reclassifique ou encaminhe ao humano.
- `needs_clarification`: faça a pergunta única e reenvie.
"""
    write('director/SYSTEM.md', director)

    for d in DOMAINS:
        inv = '\n'.join(
            f'- `{name}`: {desc}\n  Arquivo: `refactored_skills/{d}/{name}/SKILL.md`'
            for name, desc in data[d]
        )
        sub = f"""# Sub-Agente: {d}

Especialista do domínio "{d}". Opera APENAS em `refactored_skills/{d}/`.

## Inventário (nome e description)
{inv}

> Carregue o `SKILL.md` completo somente quando a intenção bater com a description.

## Execução
1. Receba HANDOFF (task, domain, context, constraints, acceptance_criteria).
2. Selecione a skill correta pela description.
3. Siga os passos da skill; aplique a saída estruturada do contrato RESULT.
4. Valide contra acceptance_criteria.
5. Devolva RESULT (status, artifacts, summary, open_items).

## Restrições
- Não acesse outro domínio. Cruzamento: `status: escalated` com a razão.
- Não copie conteúdo de skills; referencie os arquivos.
"""
        write(f'domains/{d}/SYSTEM.md', sub)

    domain_map = ['| Domínio | Diretório de skills | Sub-Agente |', '|---|---|---|']
    for d in DOMAINS:
        domain_map.append(f'| {d} | `refactored_skills/{d}/` | `domains/{d}/SYSTEM.md` |')
    write('wiring/DOMAIN_MAP.md', '# Mapa de Domínios\n\n' + '\n'.join(domain_map) + '\n')

    handoff = """# Contrato de Handoff

## HANDOFF (roteador para sub-agente)
- task: string                  # tarefa precisa
- domain: string                # domínio alvo
- context: string[]             # arquivos ou trechos relevantes
- constraints: string[]         # restrições
- acceptance_criteria: string[] # critérios de aceite

## RESULT (sub-agente para roteador)
- status: success | failure | needs_clarification | escalated
- artifacts: string[]
- summary: string
- open_items: string[]
"""
    write('wiring/HANDOFF.md', handoff)

    invocation = f"""# Invocação

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
- Diretor: {len(DOMAINS)} domínios, {total} skills no índice, zero leitura de `SKILL.md`.
"""
    write('wiring/INVOCATION.md', invocation)

    index = '# Índice Global (1 linha por domínio)\n' + '\n'.join(index_lines) + '\n'
    write('index/INDEX.md', index)

    return data, total


def checks(data, total):
    problems = []
    for d in DOMAINS:
        text = (OUT / 'domains' / d / 'SYSTEM.md').read_text(encoding='utf-8')
        if 'Executa rotinas especializadas' in text:
            problems.append(f'boilerplate em {d}')
        for other in DOMAINS:
            if other != d and f'refactored_skills/{other}/' in text:
                problems.append(f'{d} cita outro domínio {other}')
    director = (OUT / 'director' / 'SYSTEM.md').read_text(encoding='utf-8')
    if 'SKILL.md' in director.replace('`SKILL.md`', '') and 'refactored_skills' in director:
        problems.append('diretor referencia skills')
    return problems


if __name__ == '__main__':
    data, total = build()
    problems = checks(data, total)
    print(f'domínios: {len(DOMAINS)}  sub-agentes: {len(DOMAINS)}  skills: {total}')
    for p in sorted(OUT.rglob('*.md')):
        print(f'{p.relative_to(ROOT)}: {len(p.read_text(encoding="utf-8").splitlines())} linhas')
    print('problemas:', problems if problems else 'nenhum')
    sys.exit(1 if problems else 0)
