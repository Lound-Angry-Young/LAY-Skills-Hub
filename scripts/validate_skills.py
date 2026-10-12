#!/usr/bin/env python3
"""Valida uma árvore de skills contra docs/PADRAO_DE_SKILLS.md.

Uso:
  python scripts/validate_skills.py                       # refactored_skills/ público
  python scripts/validate_skills.py --root <pasta>        # outra árvore (ex.: cofre privado)
  python scripts/validate_skills.py --private --root <pasta>
  python scripts/validate_skills.py --stats               # regenera refactored_skills/refactor_stats.json

--private desliga as checagens que só fazem sentido para o repositório público
(marca, lista de skills retiradas, agentes) e mantém todas as de estrutura.
Sai com código 1 se houver erro.
"""
import argparse
import glob
import json
import os
import re
import sys
from pathlib import Path

import yaml

REPO = Path(__file__).resolve().parent.parent
BOIL = re.compile(r"Executa rotinas especializadas para|targetPath: string|Executar Ação Principal|Executar rotina atômica de|Executa fluxo padrão|Do NOT use this skill when: a tarefa exigir outro domínio")
# Marcador de rascunho deixado por scripts/nova_skill.py até o autor preencher o corpo.
PLACEHOLDER = re.compile(r'\[PREENCHER[^\]]*\]')
FILLER = re.compile(r"Documentação e especificações aprofundadas|Siga os procedimentos prescritos|## Modelos e Blocos de Código Extraídos|## Visão Geral e Especificações")
# Termos de identidade e lista de skills retiradas ficam no cofre local (não versionados), para não expô-los aqui.
_MARCA = REPO / 'skills-privadas-lay' / 'tools' / 'marca.json'
BRAND = re.compile('|'.join(re.escape(t) for t in json.loads(_MARCA.read_text(encoding='utf-8'))['termos'])) if _MARCA.exists() else None
_RETIRADAS = REPO / 'skills-privadas-lay' / 'tools' / 'retiradas.json'
RETIRADAS_DO_PUBLICO = json.loads(_RETIRADAS.read_text(encoding='utf-8'))['skills'] if _RETIRADAS.exists() else []
DOMINIOS_PUBLICOS = ['routing-and-proxy', 'frontend', 'engineering', 'context', 'devops', 'qa', 'security',
                     'creative-3d', 'documentation', 'design', 'database']
LINK = re.compile(r'\]\((?!https?://|#|mailto:)([^)\s]+?)(?:#[^)]*)?\)')
OPCIONAIS = ['## Input/Output Signature', '## Imperative Execution Workflow', '## On Failure']


def visivel(texto):
    """Texto sem blocos de código e sem código inline: só links clicáveis contam."""
    saida, cerca = [], False
    for linha in texto.split('\n'):
        if linha.startswith('```'):
            cerca = not cerca
            continue
        if not cerca:
            saida.append(re.sub(r'`[^`]*`', '', linha))
    return '\n'.join(saida)


def frontmatter(caminho):
    texto = caminho.read_text(encoding='utf-8')
    m = re.match(r'---\n(.*?)\n---\n', texto, re.S)
    return (yaml.safe_load(m.group(1)) if m else None), texto


class Validador:
    def __init__(self, raiz, privado):
        self.raiz = raiz
        self.privado = privado
        self.erros = []

    def erro(self, msg):
        self.erros.append(msg)

    def links(self, md, onde):
        for lk in LINK.findall(visivel(md.read_text(encoding='utf-8'))):
            if not os.path.exists(os.path.normpath(md.parent / lk)):
                self.erro(f'{onde}: link quebrado em {md.relative_to(self.raiz)} -> {lk}')

    def skills(self):
        validadas, ausentes = [], 0
        for sk in sorted(self.raiz.glob('*/*/SKILL.md')):
            dominio, pasta = sk.parts[-3], sk.parts[-2]
            onde = f'{dominio}/{pasta}'
            validadas.append(sk)
            meta, texto = frontmatter(sk)
            if meta is None:
                self.erro(f'{onde}: sem frontmatter YAML')
                continue
            nome, desc = meta.get('name'), meta.get('description')
            if nome != pasta:
                self.erro(f'{onde}: name {nome!r} != pasta')
            if not re.fullmatch(r'[a-z0-9-]{1,64}', str(nome)):
                self.erro(f'{onde}: name fora do padrão')
            elif not re.search(r'(^|-)[a-z]+ing(-|$)', str(nome)):
                self.erro(f'{onde}: name sem gerúndio (-ing), ver docs/PADRAO_DE_SKILLS.md, seção 1')
            if not isinstance(desc, str):
                self.erro(f'{onde}: description não é texto')
                continue
            desc = desc.strip()
            if len(desc) > 1024:
                self.erro(f'{onde}: description {len(desc)} > 1024')
            if 'Use this skill when:' not in desc:
                self.erro(f'{onde}: sem "Use this skill when:"')
            if 'Do NOT use this skill when:' not in desc:
                self.erro(f'{onde}: sem "Do NOT use this skill when:"')
            if BOIL.search(texto):
                self.erro(f'{onde}: boilerplate da Fase 1')
            if PLACEHOLDER.search(texto):
                self.erro(f'{onde}: marcador [PREENCHER] não preenchido')
            if FILLER.search(texto):
                self.erro(f'{onde}: preenchimento genérico')
            if not self.privado and BRAND and BRAND.search(texto):
                self.erro(f'{onde}: marca LAY no texto público')
            if not all(s in texto for s in OPCIONAIS):
                ausentes += 1
            for md in sk.parent.glob('**/*.md'):
                self.links(md, onde)
            ref = sk.parent / 'reference.md'
            if ref.exists():
                rt = ref.read_text(encoding='utf-8')
                if not rt.startswith('## Table of Contents\n'):
                    self.erro(f'{onde}: reference.md não começa com ## Table of Contents')
                if FILLER.search(rt) or BOIL.search(rt):
                    self.erro(f'{onde}: reference.md com conteúdo genérico')
                if 'reference.md' not in texto:
                    self.erro(f'{onde}: reference.md não é apontado pelo SKILL.md')
            elif 'reference.md' in texto:
                self.erro(f'{onde}: cita reference.md que não existe')
        return validadas, ausentes

    def roteadores(self):
        dominios = sorted(d.name for d in self.raiz.iterdir() if d.is_dir() and (d / 'SKILL.md').exists())
        if not self.privado and dominios != sorted(DOMINIOS_PUBLICOS):
            self.erro(f'domínios públicos diferentes do esperado: {dominios}')
        for dominio in dominios:
            d = self.raiz / dominio
            meta, texto = frontmatter(d / 'SKILL.md')
            if meta is None or not str(meta.get('name', '')).startswith('routing-'):
                self.erro(f'{dominio}: roteador sem name routing-*')
            elif 'Use this skill when:' not in str(meta.get('description')) or 'Do NOT use this skill when:' not in str(meta.get('description')):
                self.erro(f'{dominio}: roteador sem gatilhos')
            if BOIL.search(texto):
                self.erro(f'{dominio}: roteador com boilerplate')
            roteados = set(re.findall(r'\[([^\]]+)\]\(\./\1/SKILL\.md\)', texto))
            pastas = {f.name for f in d.iterdir() if f.is_dir()}
            if roteados != pastas:
                self.erro(f'{dominio}: roteador não lista todas as pastas: faltam {sorted(pastas - roteados)} sobram {sorted(roteados - pastas)}')
            self.links(d / 'SKILL.md', dominio)
            if (d / 'reference.md').exists():
                self.links(d / 'reference.md', dominio)
        return dominios

    def estrutura(self):
        for p in self.raiz.rglob('*'):
            if p.is_dir() and not any(p.iterdir()):
                self.erro(f'pasta vazia: {p.relative_to(self.raiz)}')
        if not self.privado and RETIRADAS_DO_PUBLICO:
            for p in RETIRADAS_DO_PUBLICO:
                if list(self.raiz.glob(f'*/{p}')):
                    self.erro(f'skill retirada do público presente: {p}')
            for f in (REPO / 'agents').rglob('*.md'):
                if BOIL.search(f.read_text(encoding='utf-8')):
                    self.erro(f'{f.relative_to(REPO)}: boilerplate')


def estatisticas(validador, skills):
    dominios = {}
    for d in sorted(p for p in validador.raiz.iterdir() if p.is_dir()):
        nomes = sorted(s.parent.name for s in d.glob('*/SKILL.md'))
        if nomes:
            dominios[d.name] = {'count': len(nomes), 'skills': nomes}
    stats = {
        'total_refactored_skills': len(skills),
        'total_domains': len(dominios),
        'skills_with_reference': len(list(validador.raiz.glob('*/*/reference.md'))),
        'skills_with_reference_pointer': sum(1 for s in skills if 'reference.md' in s.read_text(encoding='utf-8')),
        'excluded_from_public_count': len(RETIRADAS_DO_PUBLICO),
        'domain_details': dominios,
    }
    (validador.raiz / 'refactor_stats.json').write_text(json.dumps(stats, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


def main():
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')
    ap = argparse.ArgumentParser()
    ap.add_argument('--root', type=Path, default=REPO / 'refactored_skills')
    ap.add_argument('--private', action='store_true')
    ap.add_argument('--stats', action='store_true')
    args = ap.parse_args()
    raiz = args.root.resolve()
    if not raiz.is_dir():
        print(f'raiz inexistente: {raiz}')
        return 1
    v = Validador(raiz, args.private)
    skills, ausentes = v.skills()
    dominios = v.roteadores()
    v.estrutura()
    print(f'raiz: {raiz}')
    print(f'skills validadas: {len(skills)}  domínios: {len(dominios)}')
    print(f'skills sem as seções opcionais (I/O, Workflow, On Failure): {ausentes} — ver docs/PADRAO_DE_SKILLS.md, seção 8')
    if args.stats:
        estatisticas(v, skills)
        print('refactor_stats.json regenerado')
    print(f'erros: {len(v.erros)}')
    for e in v.erros[:100]:
        print('  ERRO', e)
    return 1 if v.erros else 0


if __name__ == '__main__':
    sys.exit(main())
