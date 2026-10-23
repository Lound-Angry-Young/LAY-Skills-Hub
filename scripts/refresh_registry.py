#!/usr/bin/env python3
"""Refresh source lock metadata from the checked-out Git submodules."""
import json
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[1]
UPSTREAM = ROOT / 'upstream'
OUT = ROOT / 'registry/sources.json'
SPECIAL = {
    'safishamsi--graphify': ['graphify/SKILL.md'],
}


def git(path, *args):
    return subprocess.check_output(['git', '-C', str(path), *args], text=True, encoding='utf-8').strip()


def main():
    entries = []
    for folder in sorted(UPSTREAM.iterdir()):
        if not folder.is_dir() or not (folder / '.git').exists():
            continue
        source_id = folder.name
        if source_id in SPECIAL:
            skills = SPECIAL[source_id]
        else:
            skills = [p.relative_to(folder).as_posix() for p in folder.glob('skills/**/SKILL.md')]
            if (folder / 'SKILL.md').exists():
                skills.insert(0, 'SKILL.md')
        commit = git(folder, 'rev-parse', 'HEAD')
        version = git(folder, 'describe', '--tags', '--always')
        url = git(folder, 'config', '--get', 'remote.origin.url')
        repo = url.removesuffix('.git').split('github.com/')[-1]
        notes = []
        if not skills:
            notes.append('Repositório de repertório/aplicação sem SKILL.md público; README como entrada consultiva.')
        if source_id == 'safishamsi--graphify':
            notes.append('Fonte adicional da skill Graphify; inclui runtime e referências.')
        if source_id == 'leonxlnx--taste-skill':
            notes.append('URLs Leonxlnx/leonxlnx deduplicadas: GitHub trata o nome sem distinção de maiúsculas.')
        entries.append({'id': source_id, 'repo': repo, 'url': url,
                        'path': folder.relative_to(ROOT).as_posix(), 'commit': commit,
                        'version': version, 'kind': 'skills' if skills else 'repertorio',
                        'skill_paths': sorted(set(skills)), 'notes': notes})
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps({'schema_version': 1, 'sources': entries}, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(f'{len(entries)} fontes registradas em {OUT}')


if __name__ == '__main__':
    main()
