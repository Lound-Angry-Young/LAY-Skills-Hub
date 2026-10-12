#!/usr/bin/env python3
"""Gera o pacote das skills privadas para envio manual, a partir do cofre local.

O pacote é gerado dentro de skills-privadas-lay/export/ (ignorado pelo Git). Antes de
gerar, valida a árvore com scripts/validate_skills.py --private; se houver erro, não gera.
Nada é enviado: o envio é uma ação sua.
"""
import hashlib
import json
import os
import subprocess
import sys
import zipfile
from datetime import date
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
COFRE = REPO / 'skills-privadas-lay'
ORIGEM = COFRE / 'refactored'
SAIDA = COFRE / 'export'
PREFIXO = 'lay-skills-privadas'

LEIA_ME = """# Skills LAY privadas — instalação manual

Este pacote contém skills da LAY. Use-as apenas dentro do que foi combinado com quem as recebe.

## Conteúdo

- `<dominio>/<skill>/SKILL.md`: a skill. Quando o corpo é longo, há também `reference.md`, que contém o conteúdo completo.
- `<dominio>/SKILL.md`: roteador do domínio. Lista as skills do domínio com o link de cada uma.
- `MANIFESTO.json`: nome, domínio e hash de cada skill, para conferir a integridade do envio.

## Instalação manual

Copie a pasta de cada skill (a que contém o `SKILL.md`) para a pasta de skills do agente:

- Claude Code: `~/.claude/skills/<skill>/`
- Antigravity: `~/.gemini/config/skills/<skill>/`

Os roteadores de domínio são opcionais: servem para navegar pela lista de skills de cada área.

## Limitações

- Arquivos de fonte (`.ttf`) não estão no pacote, por licenciamento. Os trechos que os usam indicam a pasta `fonts/` ao lado da skill.
- Confira o `MANIFESTO.json` contra os hashes recebidos antes de usar.
"""


def validar():
    resultado = subprocess.run(
        [sys.executable, str(REPO / 'scripts' / 'validate_skills.py'), '--private', '--root', str(ORIGEM)],
        capture_output=True, text=True, encoding='utf-8', errors='replace', env={**os.environ, 'PYTHONIOENCODING': 'utf-8'})
    if resultado.returncode != 0:
        raise SystemExit('Validação falhou; pacote não gerado:\n' + resultado.stdout + resultado.stderr)
    return resultado.stdout.strip().splitlines()[-2:]


def manifesto():
    itens = []
    for sk in sorted(ORIGEM.glob('*/*/SKILL.md')):
        digest = hashlib.sha256(sk.read_bytes()).hexdigest()
        itens.append({'skill': sk.parent.name, 'dominio': sk.parent.parent.name,
                      'sha256_SKILL_md': digest,
                      'arquivos': sorted(p.relative_to(ORIGEM).as_posix() for p in sk.parent.rglob('*') if p.is_file())})
    return {'pacote': PREFIXO, 'gerado_em': date.today().isoformat(), 'skills': itens}


def main():
    resumo = validar()
    SAIDA.mkdir(parents=True, exist_ok=True)
    destino = SAIDA / f'{PREFIXO}-{date.today():%Y%m%d}.zip'
    dados = manifesto()
    with zipfile.ZipFile(destino, 'w', compression=zipfile.ZIP_DEFLATED) as zf:
        for arq in sorted(p for p in ORIGEM.rglob('*') if p.is_file()):
            zf.write(arq, f'{PREFIXO}/' + arq.relative_to(ORIGEM).as_posix())
        zf.writestr(f'{PREFIXO}/MANIFESTO.json', json.dumps(dados, ensure_ascii=False, indent=2))
        zf.writestr(f'{PREFIXO}/LEIA-ME.md', LEIA_ME)
    print('validação:', ' | '.join(resumo))
    print(f"pacote: {destino} ({len(dados['skills'])} skills)")
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
