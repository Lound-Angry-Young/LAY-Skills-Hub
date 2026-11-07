#!/usr/bin/env python3
"""Gera a configuração de subagentes do projeto, documentação de agents/ e templates de adaptadores.

- .claude/agents/<nome>.md: subagentes do Claude Code deste repositório, com caminhos relativos
  às skills públicas (refactored_skills/). Versionados com o projeto.
- agents/: documentação (índice, mapa de domínios, invocação).
- adapters/: sincronização dos templates dos adaptadores (Claude especialistas, manifestos Antigravity
  e subagentes Antigravity) preservando modelos, ferramentas, regras e salvaguardas.

A instalação global (~/.claude/agents, ~/.gemini, ~/.codex) é feita por
scripts/skill_hub.py install. Os perfis vêm de core/perfis.json (SSOT).
"""
import json
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO))

from scripts.skill_hub import (AGENTS_DOMINIOS, PRIVATE_REFACTORED, REFACTORED,  # noqa: E402
                               claude_agent_text, load_profiles, private_entries,
                               skill_entries)


def skills_publicas(root=REPO):
    """Skills públicas por domínio, com caminho relativo ao repositório."""
    por_dominio = {}
    for e in skill_entries(root, REFACTORED, 'local', 'refactored'):
        dominio = e['path'].split('/')[1]
        por_dominio.setdefault(dominio, []).append((e['name'], e['path'], e['description']))
    return por_dominio


def subagentes_do_projeto(root=REPO):
    """Nome do arquivo -> texto do subagente, prontos para .claude/agents/."""
    perfis = load_profiles(root)
    por_dominio = skills_publicas(root)
    return {p['nome'] + '.md': claude_agent_text(p, por_dominio.get(p['dominio'], [])) for p in perfis}


def escrever(caminho, texto):
    caminho.parent.mkdir(parents=True, exist_ok=True)
    caminho.write_text(texto, encoding='utf-8', newline='\n')


def update_adapters(root=REPO):
    """Atualiza as seções de skills nos adaptadores de clientes (Claude e Antigravity).

    Preserva integralmente frontmatter, modelos, ferramentas, regras de atuação e salvaguardas.
    Codex descobre skills dinamicamente via junctions em .agents/skills/ (link-junctions).
    """
    perfis = load_profiles(root)
    public_entries = skill_entries(root, REFACTORED, 'local', 'refactored')
    public_by_domain = {}
    for e in public_entries:
        d = e['path'].split('/')[1]
        public_by_domain.setdefault(d, []).append((e['name'], e['description']))

    private_by_domain = {}
    if (root / PRIVATE_REFACTORED).is_dir():
        for e in private_entries(root):
            d = e['path'].split('/')[2]
            private_by_domain.setdefault(d, []).append((e['name'], e['description']))
    else:
        # Preserva skills privadas já presentes nos templates quando o cofre não estiver presente
        for p in perfis:
            agent_file = root / 'adapters/claude/agents' / (p['nome'] + '.md')
            if agent_file.exists():
                txt = agent_file.read_text(encoding='utf-8')
                for m in re.finditer(r'<!-- LAY-PRIVATE-SKILLS:BEGIN -->\s*- `([^`]+)`: `[^`]+/([^/]+)/SKILL\.md`\s*<!-- LAY-PRIVATE-SKILLS:END -->\s*([^\n]+)', txt):
                    sk_name, sk_dom, sk_desc = m.group(1), p['dominio'], m.group(3).strip()
                    private_by_domain.setdefault(sk_dom, []).append((sk_name, sk_desc))

    # 1. Adaptadores Claude Code (11 especialistas)
    for p in perfis:
        agent_file = root / 'adapters/claude/agents' / (p['nome'] + '.md')
        if not agent_file.exists():
            continue
        domain = p['dominio']
        pub = [(name, desc, False) for name, desc in public_by_domain.get(domain, [])]
        priv = [(name, desc, True) for name, desc in private_by_domain.get(domain, [])]
        all_skills = sorted(pub + priv, key=lambda x: x[0])
        lines = []
        for name, desc, is_priv in all_skills:
            clean_desc = desc[:240].rstrip()
            if is_priv:
                lines.append('<!-- LAY-PRIVATE-SKILLS:BEGIN -->')
                lines.append(f'- `{name}`: `{{{{LAY_RUNTIME_DIR}}}}/skills-privadas-lay/refactored/{domain}/{name}/SKILL.md`')
                lines.append('<!-- LAY-PRIVATE-SKILLS:END -->')
                lines.append(f'  {clean_desc}')
            else:
                lines.append(f'- `{name}`: `{{{{LAY_RUNTIME_DIR}}}}/refactored_skills/{domain}/{name}/SKILL.md`')
                lines.append(f'  {clean_desc}')
        gen_block = '\n'.join(lines)

        raw_f = agent_file.read_bytes()
        eol_f = '\r\n' if b'\r\n' in raw_f else '\n'
        txt = raw_f.decode('utf-8').replace('\r\n', '\n')
        prefix = '## Skills do domínio\n\nAbra o SKILL.md original de uma skill só quando a tarefa corresponder à sua descrição. Caminhos:\n\n'
        suffix = '\n## Regras de atuação'
        if prefix in txt and suffix in txt:
            start = txt.find(prefix) + len(prefix)
            end = txt.find(suffix)
            new_txt = txt[:start] + gen_block + '\n' + txt[end:]
            agent_file.write_bytes(new_txt.replace('\n', eol_f).encode('utf-8'))

    # 2. Manifestos Antigravity
    def build_manifest(domains):
        entries = []
        for d in sorted(domains):
            if d in public_by_domain and public_by_domain[d]:
                entries.append({
                    "path": f"{{{{LAY_RUNTIME_DIR}}}}/refactored_skills/{d}",
                    "include_only": sorted(name for name, _ in public_by_domain[d])
                })
            if d in private_by_domain and private_by_domain[d]:
                entries.append({
                    "path": f"{{{{LAY_RUNTIME_DIR}}}}/skills-privadas-lay/refactored/{d}",
                    "include_only": sorted(name for name, _ in private_by_domain[d])
                })
        return {"entries": entries}

    manifests_dir = root / 'adapters/antigravity/manifests'
    if manifests_dir.exists():
        for fname, doms in [
            ('skills-frontend.json', ['frontend']),
            ('skills-engineering.json', ['engineering']),
            ('skills-full.json', set(public_by_domain.keys()) | set(private_by_domain.keys()))
        ]:
            mpath = manifests_dir / fname
            raw_m = mpath.read_bytes() if mpath.exists() else b''
            eol_m = '\r\n' if b'\r\n' in raw_m else '\n'
            content = json.dumps(build_manifest(doms), indent=2, ensure_ascii=False) + '\n'
            mpath.write_bytes(content.replace('\n', eol_m).encode('utf-8'))

    # 3. Template de subagentes Antigravity
    ag_tmpl_path = root / 'adapters/antigravity/agents/subagents-definition-template.json'
    if ag_tmpl_path.exists():
        raw_t = ag_tmpl_path.read_bytes()
        eol_t = '\r\n' if b'\r\n' in raw_t else '\n'
        tmpl_data = json.loads(raw_t.decode('utf-8'))
        new_subs = []
        for sub in tmpl_data.get('subagents', []):
            name = sub.get('Name')
            if name == 'lay-arbitro':
                new_subs.append(sub)
                continue
            perfil = next((p for p in perfis if p['nome'] == name), None)
            if not perfil:
                new_subs.append(sub)
                continue
            domain = perfil['dominio']
            all_sk = sorted(public_by_domain.get(domain, []) + private_by_domain.get(domain, []), key=lambda x: x[0])
            top_skills = all_sk[:15]
            skill_lines = [f"- {sk_name}: {sk_desc[:140]}" for sk_name, sk_desc in top_skills]
            marker = 'Skills do domínio disponíveis para consulta conceitual:\n'
            if marker in sub['SystemPrompt']:
                base_prompt = sub['SystemPrompt'].split(marker)[0]
                new_prompt = base_prompt + marker + '\n'.join(skill_lines)
                updated = dict(sub)
                updated['SystemPrompt'] = new_prompt
                new_subs.append(updated)
            else:
                new_subs.append(sub)
        content = json.dumps({'subagents': new_subs}, indent=2, ensure_ascii=False) + '\n'
        ag_tmpl_path.write_bytes(content.replace('\n', eol_t).encode('utf-8'))


def main():
    perfis = load_profiles(REPO)
    total = sum(len(v) for v in skills_publicas(REPO).values())

    for nome, texto in subagentes_do_projeto(REPO).items():
        escrever(REPO / '.claude/agents' / nome, texto)

    indice = ['# Índice de subagentes (1 linha por domínio)', '']
    indice += [f'- {p["dominio"]}: {len(skills_publicas(REPO).get(p["dominio"], []))} skills públicas, subagente `{p["nome"]}`' for p in perfis]
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
        'Um subagente por domínio de skills, gerado a partir de `core/perfis.json`.', '',
        '- `core/perfis.json`: fonte autoritativa de perfis (nome, description com gatilhos, ferramentas).',
        '- `agents/perfis.json`: espelho sincronizado para compatibilidade legada.',
        '- `.claude/agents/`: subagentes do projeto (versionados), com as skills públicas.',
        '- `adapters/`: templates canônicos dos adaptadores de clientes (Claude, Codex, Antigravity).',
        '- `scripts/skill_hub.py install`: subagentes e adaptadores globais em `~/.claude`, `~/.codex` e `~/.gemini`.',
        '- `scripts/build_agents.py`: valida, gera `.claude/agents/`, documentação e atualiza adaptadores.',
        '- `CLAUDE.md`, seção "Orquestração de subagentes": roteamento domínio → subagente.',
        '- `wiring/`: mapa de domínios, contrato de handoff e invocação.',
        '- `index/INDEX.md`: índice de uma linha por domínio.', '',
    ])
    escrever(REPO / 'agents/README.md', leiame)

    update_adapters(REPO)

    print(f'domínios: {len(perfis)}  subagentes do projeto: {len(perfis)}  skills públicas: {total}')
    print('gerado: .claude/agents/, documentação em agents/ e adaptadores em adapters/')


if __name__ == '__main__':
    main()
