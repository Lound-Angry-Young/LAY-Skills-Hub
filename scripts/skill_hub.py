#!/usr/bin/env python3
"""LAY skill hub. Python >=3.10, standard library only; upstream is data."""
from __future__ import annotations

import argparse
import concurrent.futures
from contextlib import redirect_stdout
import hashlib
import io
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
from datetime import datetime, timezone

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')

ROOT = Path(__file__).resolve().parents[1]
BEGIN = '<!-- LAY-SKILLS:BEGIN -->'
END = '<!-- LAY-SKILLS:END -->'
MANAGED_END = '<!-- LAY-MANAGED:END -->'
SKIP = {'.git', '__pycache__', 'node_modules', '.venv', '.state', '.pytest_cache'}
DESTINATIONS = {'codex': '.agents/skills', 'claude': '.claude/skills',
                'antigravity': '.gemini/config/skills'}
RULES = {'codex': '.codex/AGENTS.md', 'claude': '.claude/CLAUDE.md',
         'antigravity': '.gemini/GEMINI.md'}


def destinations(agent):
    result = [DESTINATIONS[agent]]
    if agent == 'antigravity':
        result.append('.gemini/antigravity-cli/skills')
    return result
CATEGORIES = {
    'seguranca': ('security', 'semgrep', 'hardening', 'vulnerab', 'audit'),
    'design': ('design', 'taste', 'brand', 'frontend', 'impeccable', 'ui-ux', 'soft-skill', 'stitch', 'brutalist', 'minimalist', 'composition', 'react'),
    'testes': ('test', 'quality', 'review', 'playwright', 'debug'),
    'contexto': ('graphify', 'caveman', 'context', 'orchestrat', 'using-agent', 'ponytail'),
    'produto': ('idea', 'interview', 'planning', 'spec-', 'constraint'),
    'engenharia': ('api', 'implementation', 'simplification', 'source-driven', 'migration', 'performance', 'doubt'),
    'operacoes': ('deploy', 'shipping', 'observability', 'ci-cd', 'git-workflow', 'omniroute', 'vercel-cli'),
    'midia': ('watermark', 'imagegen', 'image-to-code'),
    'pesquisa': ('generative', 'brag', 'research'),
    'documentacao': ('documentation', 'writing', 'output'),
}


def now():
    return datetime.now(timezone.utc).isoformat()


def read_json(path, default=None):
    return json.loads(path.read_text(encoding='utf-8-sig')) if path.exists() else default


def write(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    if not isinstance(data, str):
        data = json.dumps(data, ensure_ascii=False, indent=2) + '\n'
    if path.is_file() and path.read_text(encoding='utf-8') == data:
        return
    with tempfile.NamedTemporaryFile('w', encoding='utf-8', newline='\n', dir=path.parent, delete=False) as f:
        f.write(data)
        temp = Path(f.name)
    os.replace(temp, path)


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def confined(base, relative):
    path = (base / relative).resolve()
    if not path.is_relative_to(base.resolve()) or path == base.resolve():
        raise ValueError(f'Caminho fora da raiz: {relative}')
    return path


def run(args, cwd=None, timeout=60, check=True):
    env = os.environ.copy()
    env['GIT_TERMINAL_PROMPT'] = '0'
    env['GCM_INTERACTIVE'] = 'never'
    result = subprocess.run([str(a) for a in args], cwd=cwd, env=env,
                            capture_output=True, text=True, encoding='utf-8', errors='replace', timeout=timeout)
    if check and result.returncode:
        # Do not echo remote error bodies: credentialed URLs can occur there.
        raise RuntimeError(f'{args[0]} {args[1]} falhou (exit {result.returncode})')
    return result


def git(root, *args, **kw):
    return run(['git', '-c', 'core.hooksPath=' + os.devnull, '-C', root, *args], **kw).stdout.strip()


def sources(root):
    data = read_json(root / 'registry/sources.json')
    if not data or not data.get('sources'):
        raise ValueError('registry/sources.json ausente ou vazio')
    return data


def files(root):
    for directory, dirs, names in os.walk(root, followlinks=False):
        dirs[:] = sorted(d for d in dirs if d not in SKIP and not (Path(directory) / d).is_symlink())
        for name in sorted(names):
            p = Path(directory) / name
            if name != '.git' and not p.is_symlink():
                yield p


def frontmatter(path):
    text = path.read_text(encoding='utf-8-sig', errors='replace')
    if not text.startswith('---'):
        return {}, text
    parts = text.split('---', 2)
    if len(parts) != 3:
        return {}, text
    result = {}
    lines = parts[1].splitlines()
    for i, line in enumerate(lines):
        match = re.match(r'^(name|description):\s*(.*)$', line)
        if not match:
            continue
        key, value = match.groups()
        if value in ('>', '|', '>-', '|-') or not value:
            chunks = []
            for following in lines[i+1:]:
                if following and not following[0].isspace():
                    break
                chunks.append(following.strip())
            value = ' '.join(chunks)
        result[key] = value.strip().strip('"\'')
    return result, parts[2]


def slug(value):
    value = re.sub('[^a-z0-9-]+', '-', value.lower()).strip('-')
    return value if len(value) <= 63 else value[:54].rstrip('-') + '-' + hashlib.sha256(value.encode()).hexdigest()[:8]


REFACTORED = 'refactored_skills'
PRIVATE_REFACTORED = 'skills-privadas-lay/refactored'
DOMAIN_CATEGORY = {
    'routing-and-proxy': 'operacoes', 'devops': 'operacoes', 'database': 'operacoes',
    'frontend': 'design', 'design': 'design', 'creative-3d': 'design',
    'engineering': 'engenharia', 'context': 'contexto', 'qa': 'testes',
    'security': 'seguranca', 'documentation': 'documentacao',
}


def skill_entries(root, base_rel, source, version):
    """Uma entrada por skill em <base_rel>/<dominio>/<skill>/SKILL.md; roteadores de domínio ficam de fora."""
    base = root / base_rel
    entries, seen = [], set()
    for skill in sorted(base.glob('*/*/SKILL.md')):
        domain, name = skill.parent.parent.name, skill.parent.name
        if domain not in DOMAIN_CATEGORY:
            raise ValueError(f'Domínio sem categoria: {domain}')
        meta, _ = frontmatter(skill)
        if meta.get('name') != name:
            raise ValueError(f"name {meta.get('name')!r} difere da pasta {name!r}: {skill}")
        identity = slug('lay-' + name)
        if identity in seen:
            raise ValueError(f'Identidade duplicada: {identity}')
        seen.add(identity)
        digest = sha(skill)
        entries.append({'id': identity, 'name': name,
                        'description': re.sub(r'\s+', ' ', meta.get('description', '')).strip(),
                        'source': source, 'path': skill.relative_to(root).as_posix(), 'kind': 'skill',
                        'categories': sorted({DOMAIN_CATEGORY[domain], *(c for c, keys in CATEGORIES.items() if any(k in name for k in keys))}),
                        'version': version, 'commit': 'content-' + digest[:12],
                        'sha256': digest, 'url': ''})
    return entries


def refactored_entries(root=ROOT):
    return skill_entries(root, REFACTORED, 'local', 'refactored')


def private_entries(root=ROOT):
    """Skills LAY reservadas, em skills-privadas-lay/refactored (cofre local, ignorado pelo Git).
    Entram só na instalação local; nunca no catálogo público, no hub ou nos agentes do repositório."""
    if not (root / PRIVATE_REFACTORED).is_dir():
        return []
    return skill_entries(root, PRIVATE_REFACTORED, 'private', 'private')


def build_catalog(root=ROOT):
    entries = refactored_entries(root)
    if not entries:
        raise ValueError(f'{REFACTORED}/ vazio ou ausente')
    result = {'schema_version': 1, 'skills': entries}
    write(root / 'catalog/skills.json', result)
    lines = ['# Catálogo instalável', '',
             'Gerado por `python scripts/skill_hub.py catalog`. Skills refatoradas e validadas em `refactored_skills/`; '
             'fontes originais e proveniência ficam em `upstream/` e nos bundles de `~/.lay-skills/`.', '']
    for category in CATEGORIES:
        lines += [f'## {category}', '', '| ID global | Skill | Domínio | Versão |', '|---|---|---|---|']
        for e in entries:
            if category in e['categories']:
                lines.append(f"| `{e['id']}` | [{e['name']}](../{e['path']}) | {e['path'].split('/')[1]} | {e['version']} |")
        lines.append('')
    write(root / 'docs/CATALOGO.md', '\n'.join(lines))
    return result


# Findings are indicators for human/agent review, never a certificate of safety.
SCAN_RULES = [
    ('private-key', 'high', re.compile(r'-----BEGIN (?:RSA |EC |OPENSSH |DSA )?PRIVATE KEY-----')),
    ('credential-pattern', 'high', re.compile(r'\b(?:gh[pousr]_[A-Za-z0-9]{30,}|AKIA[0-9A-Z]{16}|sk-(?:proj-)?[A-Za-z0-9_-]{40,})\b')),
    ('remote-shell', 'review', re.compile(r'(?:curl|wget|irm|Invoke-WebRequest|Invoke-RestMethod).{0,250}\|\s*(?:bash|sh|iex|Invoke-Expression)', re.I)),
    ('destructive-command', 'review', re.compile(r'\brm\s+-[a-zA-Z]*r[a-zA-Z]*f|Remove-Item.{0,120}-Recurse', re.I)),
    ('instruction-override', 'review', re.compile(r'(?:ignore|override|disregard)\s+(?:all\s+)?(?:previous|system|prior)\s+instructions', re.I)),
    ('permission-bypass', 'review', re.compile(r'dangerously-skip-permissions|bypassPermissions|--yolo\b')),
]


def scan(root=ROOT):
    findings, scanned, skipped = [], 0, 0
    for base in [root / 'skills', *(root / s['path'] for s in sources(root)['sources'])]:
        for path in files(base):
            if path.stat().st_size > 2_000_000:
                skipped += 1
                continue
            raw = path.read_bytes()
            if b'\0' in raw[:4096]:
                skipped += 1
                continue
            scanned += 1
            for line_no, line in enumerate(raw.decode('utf-8', errors='replace').splitlines(), 1):
                for rule, severity, pattern in SCAN_RULES:
                    if pattern.search(line):
                        findings.append({'rule': rule, 'severity': severity,
                                         'path': path.relative_to(root).as_posix(), 'line': line_no})
    report = {'schema_version': 1, 'scanned_at': now(), 'text_files': scanned, 'skipped_binary_or_large': skipped,
              'scope': 'Inspeção estática por padrões; não executa scripts; exemplos/testes podem ser falsos positivos. Não é SAST completo, antivírus ou auditoria de dependências.',
              'findings': findings}
    write(root / '.state/security-scan.json', report)
    counts = {level: sum(f['severity'] == level for f in findings) for level in ('high', 'review')}
    print(f"🔎 Scan: {scanned} textos; {counts['high']} indicadores de credencial/chave, {counts['review']} pontos de revisão. Relatório: {root / '.state/security-scan.json'}")
    return report


def bundle_tree(source, target):
    """Copy complete source contents, except Git administration; preserve safe symlinks."""
    if target.exists():
        return
    target.parent.mkdir(parents=True, exist_ok=True)
    staged = Path(tempfile.mkdtemp(prefix='.bundle-', dir=target.parent))
    try:
        for p in source.rglob('*'):
            if '.git' in p.relative_to(source).parts:
                continue
            if p.is_symlink() and not p.resolve().is_relative_to(source.resolve()):
                raise ValueError(f'Link sai da fonte: {p}')
        shutil.copytree(source, staged, dirs_exist_ok=True, symlinks=True, ignore=shutil.ignore_patterns('.git'))
        os.replace(staged, target)
    finally:
        if staged.exists():
            shutil.rmtree(staged)


def managed_write(path, content, hub):
    if path.exists() and path.read_text(encoding='utf-8') != content:
        backup = hub / 'backups' / datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%f') / path.name
        backup.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(path, backup)
    write(path, content)


def update_block(path, body, hub):
    old = path.read_text(encoding='utf-8') if path.exists() else ''
    if old.count(BEGIN) != old.count(END) or old.count(BEGIN) > 1:
        raise ValueError(f'Marcadores ambíguos: {path}')
    block = BEGIN + '\n' + body.rstrip() + '\n' + END
    if BEGIN in old:
        new = old[:old.index(BEGIN)] + block + old[old.index(END)+len(END):]
    else:
        new = old + ('\n\n' if old and not old.endswith('\n\n') else '') + block + '\n'
    managed_write(path, new, hub)


def hook_command(home, agent, runtime):
    # No Windows o Codex executa o hook pelo PowerShell, que só aceita caminho entre aspas com o operador &.
    prefix = '& ' if agent == 'codex' and os.name == 'nt' else ''
    return f'{prefix}"{sys.executable}" "{runtime / "scripts/skill_hub.py"}" hook --agent {agent} --home "{home}"'


def install_hook(home, agent, runtime, hub):
    command = hook_command(home, agent, runtime)
    if agent == 'claude':
        path = home / '.claude/settings.json'
        data = read_json(path, {})
        if not isinstance(data, dict) or not isinstance(data.get('hooks', {}), dict):
            raise ValueError(f'Formato de hooks não suportado: {path}')
        hooks = data.setdefault('hooks', {})
        entries = hooks.setdefault('SessionStart', [])
        if not isinstance(entries, list):
            raise ValueError(f'Formato SessionStart não suportado: {path}')
        entries[:] = [g for g in entries if not any('skill_hub.py" hook --agent claude' in h.get('command', '') for h in g.get('hooks', []) if isinstance(h, dict))]
        entries.append({'matcher': 'startup|resume', 'hooks': [{'type': 'command', 'command': command, 'timeout': 120000}]})
    elif agent == 'codex':
        path = home / '.codex/hooks.json'
        data = read_json(path, {})
        if not isinstance(data, dict) or not isinstance(data.get('hooks', {}), dict):
            raise ValueError(f'Formato de hooks não suportado: {path}')
        hooks = data.setdefault('hooks', {})
        entries = hooks.setdefault('SessionStart', [])
        if not isinstance(entries, list):
            raise ValueError(f'Formato SessionStart não suportado: {path}')
        entries[:] = [g for g in entries if not any('skill_hub.py" hook --agent codex' in h.get('command', '') for h in g.get('hooks', []) if isinstance(h, dict))]
        entries.append({'matcher': 'startup|resume', 'hooks': [{'type': 'command', 'command': command, 'timeout': 120, 'statusMessage': 'Consultando LAY Skills'}]})
    else:
        path = home / '.gemini/config/hooks.json'
        data = read_json(path, {})
        if not isinstance(data, dict):
            raise ValueError(f'Formato de hooks não suportado: {path}')
        if 'lay-skills' in data and not any('skill_hub.py" hook --agent antigravity' in h.get('command', '') for h in data['lay-skills'].get('PreInvocation', []) if isinstance(h, dict)):
            raise ValueError(f'Hook lay-skills existente não gerenciado: {path}')
        data['lay-skills'] = {'PreInvocation': [{'type': 'command', 'command': command, 'timeout': 120}]}
    managed_write(path, json.dumps(data, ensure_ascii=False, indent=2) + '\n', hub)


def hook(home, agent):
    try:
        # Os agentes enviam JSON em UTF-8; no Windows sys.stdin decodifica em cp1252 e corrompe
        # caminhos com acento (ex.: 'Sessão'), o que fazia o diagnóstico falhar com ValueError.
        raw = sys.stdin.buffer.read() if hasattr(sys.stdin, 'buffer') else sys.stdin.read().encode('utf-8')
        event = json.loads(raw.decode('utf-8-sig') or '{}')
        if agent == 'antigravity' and event.get('invocationNum', 0) != 0:
            print('{}')
            return
        paths = event.get('workspacePaths') or []
        project = Path(paths[0]) if agent == 'antigravity' and paths else Path(event.get('cwd') or os.getcwd())
        with redirect_stdout(io.StringIO()) as capture:
            start(home, project)
        content = capture.getvalue().strip()
        if agent == 'antigravity':
            print(json.dumps({'injectSteps': [{'ephemeralMessage': content}]} if content else {}, ensure_ascii=False))
        else:
            print(json.dumps({'hookSpecificOutput': {'hookEventName': 'SessionStart',
                                                       'additionalContext': content, **({'reloadSkills': True} if agent == 'claude' else {})}}, ensure_ascii=False))
    except Exception as exc:
        # A failed update cannot prevent the user opening the agent.
        note = f'LAY Skills: diagnóstico automático indisponível ({type(exc).__name__}); execute start manualmente.'
        if agent == 'antigravity':
            print(json.dumps({'injectSteps': [{'ephemeralMessage': note}]}))
        else:
            print(json.dumps({'hookSpecificOutput': {'hookEventName': 'SessionStart', 'additionalContext': note}}))


def ensure_graphify(hub, root, source):
    if not source:
        return
    source_root = confined(root, source['path'])
    if not (source_root / 'pyproject.toml').exists():
        return
    tool = hub / 'tools/graphify'
    python = tool / ('Scripts/python.exe' if os.name == 'nt' else 'bin/python')
    executable = tool / ('Scripts/graphify.exe' if os.name == 'nt' else 'bin/graphify')
    marker = tool / 'source.json'
    current = read_json(marker, {})
    if current.get('commit') == source['commit'] and executable.exists() and run([python, '-c', 'import graphify'], check=False).returncode == 0:
        return
    if not python.exists():
        run([sys.executable, '-m', 'venv', tool], timeout=120)
    run([python, '-m', 'pip', 'install', '--no-input', '--disable-pip-version-check', str(source_root)], timeout=600)
    if run([python, '-c', 'import graphify'], check=False).returncode != 0 or not executable.exists():
        raise RuntimeError('Graphify instalado sem CLI funcional')
    write(marker, {'commit': source['commit'], 'version': source['version'], 'executable': str(executable)})
    print(f"✅ Graphify instalado versão {source['version']} em {executable}.")


AGENTS_FERRAMENTAS = {'Read', 'Grep', 'Glob', 'Bash', 'Edit', 'Write'}
AGENTS_DOMINIOS = ['routing-and-proxy', 'frontend', 'engineering', 'context', 'devops', 'qa',
                   'security', 'creative-3d', 'documentation', 'design', 'database']
AGENTE_NOME = re.compile(r'[a-z0-9-]{1,64}')


def load_profiles(root=ROOT):
    """Perfis de subagente: core/perfis.json é a autoridade única (SSOT)."""
    core_f = root / 'core/perfis.json'
    target = core_f if core_f.exists() else (root / 'agents/perfis.json')
    perfis = json.loads(target.read_text(encoding='utf-8'))['perfis']
    if sorted(p['dominio'] for p in perfis) != sorted(AGENTS_DOMINIOS):
        raise ValueError('perfis não cobrem exatamente os domínios esperados')
    nomes = [p['nome'] for p in perfis]
    if len(set(nomes)) != len(nomes):
        raise ValueError('nomes de subagente duplicados')
    readonly_profiles = {'lay-contexto', 'lay-seguranca', 'lay-banco-de-dados'}
    allowed_readonly_tools = {'Read', 'Grep', 'Glob'}
    for p in perfis:
        if not AGENTE_NOME.fullmatch(p['nome']):
            raise ValueError(f"nome de subagente inválido: {p['nome']}")
        if len(p['descricao']) > 1024 or 'Use quando:' not in p['descricao'] or 'Não use para:' not in p['descricao']:
            raise ValueError(f"description sem gatilhos ou longa demais: {p['nome']}")
        if not set(p['ferramentas']) <= AGENTS_FERRAMENTAS:
            raise ValueError(f"ferramentas fora do conjunto permitido: {p['nome']}")
        if p['nome'] in readonly_profiles:
            violacoes = set(p['ferramentas']) - allowed_readonly_tools
            if violacoes:
                raise ValueError(
                    f"Violação de salvaguarda: {p['nome']} é estritamente somente-leitura, "
                    f"mas possui ferramentas não autorizadas: {sorted(violacoes)}"
                )
    return perfis


def claude_agent_text(perfil, skills):
    """Arquivo de subagente do Claude Code: frontmatter (name, description, tools) e instruções de atuação."""
    partes = [
        '---',
        'name: ' + perfil['nome'],
        'description: ' + json.dumps(perfil['descricao'], ensure_ascii=False),
        'tools: ' + ', '.join(perfil['ferramentas']),
        '---',
        '',
        '# ' + perfil['nome'],
        '',
        perfil['descricao'],
        '',
        '## Skills do domínio',
        '',
        'Abra o SKILL.md original de uma skill só quando a tarefa bater com a descrição dela. Caminhos:',
        '',
    ]
    for nome, original, desc in skills:
        partes.append('- `' + nome + '`: `' + original + '`')
        partes.append('  ' + desc[:240])
    partes += [
        '',
        '## Regras de atuação',
        '',
        '1. Use só as skills deste domínio. Se o pedido for de outro domínio, responda com status `escalated`, a razão e o domínio sugerido.',
        '2. Escolha a skill pela descrição, abra o SKILL.md original e siga os passos dela.',
        '3. Não invente capacidade: afirme só o que verificou (arquivo lido, comando executado, saída observada).',
        '4. Pergunte só se a resposta depender de informação que você não tem. Faça uma pergunta por vez.',
        '5. Ações externas ou irreversíveis (enviar mensagens, publicar, apagar, sobrescrever com perda) só com confirmação explícita do usuário.',
        '6. Em projeto existente, mostre prioridades e evidências antes de editar.',
        '7. Escreva em português direto, sem rodeio.',
        '',
        '## Resposta (RESULT)',
        '',
        '- status: success | failure | needs_clarification | escalated',
        '- artifacts: arquivos ou saídas produzidas',
        '- summary: 2 a 4 frases',
        '- open_items: pendências',
        '',
    ]
    return '\n'.join(partes)


def claude_routing_index(perfis):
    """Índice que vai para o bloco gerenciado do CLAUDE.md global: qual subagente atende cada domínio."""
    linhas = ['', '## Subagentes LAY (Claude Code)', '',
              'Subagentes globais em ~/.claude/agents. Escolha pelo domínio do pedido e delegue. '
              'Subagentes não chamam outros subagentes: o roteamento é desta conversa.', '']
    linhas += ['- ' + p['dominio'] + ': `' + p['nome'] + '`' for p in perfis]
    return '\n'.join(linhas) + '\n'


class BackupManager:
    """Gerencia backups timestampados com manifesto antes de alterações em arquivos do usuário."""
    def __init__(self, hub, dry_run=False):
        self.hub = Path(hub)
        self.dry_run = dry_run
        self.timestamp = datetime.now(timezone.utc).strftime('%Y%m%d-%H%M%S')
        self.backup_dir = self.hub / 'backups' / f'pre-install-{self.timestamp}'
        self.manifest = []
        self.created = []
        self._backed_up = set()

    def backup_file(self, target_path):
        target = Path(target_path)
        if not target.exists() or self.dry_run:
            return
        res = str(target.resolve())
        if res in self._backed_up:
            return
        self.backup_dir.mkdir(parents=True, exist_ok=True)
        backup_name = f"{target.parent.name}_{target.name}"
        backup_dest = self.backup_dir / backup_name
        idx = 1
        while backup_dest.exists():
            backup_dest = self.backup_dir / f"{target.parent.name}_{target.stem}_{idx}{target.suffix}"
            idx += 1
        shutil.copy2(target, backup_dest)
        self.manifest.append({
            "original": res,
            "backup": str(backup_dest.resolve()),
            "sha256": sha(target)
        })
        self._backed_up.add(res)

    def record_created(self, target_path, content_sha):
        if self.dry_run:
            return
        target = Path(target_path).resolve()
        self.created.append({
            "path": str(target),
            "sha256": content_sha
        })

    def finalize(self):
        if (self.manifest or self.created) and not self.dry_run:
            self.backup_dir.mkdir(parents=True, exist_ok=True)
            write(self.backup_dir / 'manifest.json', {
                "created_at": now(),
                "files": self.manifest,
                "created": self.created
            })
            return self.backup_dir
        return None


def rollback(home, backup_dir=None):
    """Restaura arquivos pré-existentes e remove apenas novos criados sem modificação posterior."""
    home = Path(home).resolve()
    hub = home / '.lay-skills'
    backups_root = hub / 'backups'
    if not backups_root.exists():
        raise ValueError(f'Nenhum backup encontrado em {backups_root}')
    if backup_dir:
        b_dir = Path(backup_dir).resolve()
    else:
        candidates = sorted([p for p in backups_root.iterdir() if p.is_dir() and p.name.startswith('pre-install-')])
        if not candidates:
            raise ValueError(f'Nenhum diretório pre-install-* encontrado em {backups_root}')
        b_dir = candidates[-1]

    manifest_file = b_dir / 'manifest.json'
    if not manifest_file.exists():
        raise ValueError(f'Manifesto de backup ausente em: {manifest_file}')
    manifest = json.loads(manifest_file.read_text(encoding='utf-8'))
    restored = 0
    for entry in manifest.get('files', []):
        orig = Path(entry['original'])
        b_path = Path(entry['backup'])
        if b_path.exists():
            orig.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(b_path, orig)
            restored += 1
            print(f'  [ROLLBACK] Restaurado: {orig} a partir de {b_path.name}')

    removed_created = 0
    for entry in manifest.get('created', []):
        c_path = Path(entry['path'])
        if c_path.is_file():
            current_sha = sha(c_path)
            if current_sha == entry['sha256']:
                c_path.unlink()
                removed_created += 1
                print(f'  [ROLLBACK] Removido arquivo novo não modificado: {c_path}')
            else:
                print(f'  [ROLLBACK] PRESERVADO (modificado pelo usuário após instalação): {c_path}')

    print(f'✅ Rollback concluído: {restored} arquivo(s) restaurado(s), {removed_created} novo(s) removido(s) de {b_dir.name}.')
    return {"restored": restored, "removed_created": removed_created}


def detect_clients(home):
    """Detecta clientes instalados no sistema host."""
    home = Path(home).resolve()
    detected = []
    if shutil.which('claude') or (home / '.claude').exists():
        detected.append('claude')
    local_app_data = os.environ.get('LOCALAPPDATA', '')
    codex_exe = Path(local_app_data) / 'Programs/OpenAI/Codex/bin/codex.exe' if local_app_data else None
    if shutil.which('codex') or (home / '.codex').exists() or (codex_exe and codex_exe.exists()):
        detected.append('codex')
    if shutil.which('agy') or (home / '.gemini').exists():
        detected.append('antigravity')
    return detected


def update_rules_file(path, new_managed_content, backup_mgr=None, dry_run=False):
    """Atualiza arquivo de regras de usuário preservando instruções pessoais antes e depois."""
    path = Path(path)
    if dry_run:
        print(f"  [DRY-RUN] Atualizaria arquivo de regras: {path}")
        return

    existed = path.exists()
    old = path.read_text(encoding='utf-8') if existed else ''
    if existed and backup_mgr:
        backup_mgr.backup_file(path)

    begin_marker = '<!-- LAY-SKILLS:BEGIN -->'
    end_marker = '<!-- LAY-MANAGED:END -->'

    if not old:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(new_managed_content, encoding='utf-8', newline='\n')
        if not existed and backup_mgr:
            backup_mgr.record_created(path, sha(path))
        return

    if begin_marker in old:
        prefix = old[:old.index(begin_marker)]
        if end_marker in old:
            suffix = old[old.index(end_marker) + len(end_marker):]
        else:
            suffix = ''
        new_content = prefix + new_managed_content + suffix.lstrip('\r\n')
    else:
        new_content = new_managed_content + '\n\n' + old

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(new_content, encoding='utf-8', newline='\n')
    if not existed and backup_mgr:
        backup_mgr.record_created(path, sha(path))


def link_junctions(workspace, hub, domain=None, skill=None):
    """Cria Directory Junctions NTFS individuais (.agents/skills/<skill-name>) para descoberta no Codex (depth=1)."""
    workspace = Path(workspace).resolve()
    if not workspace.is_dir():
        raise ValueError(f'Workspace inválido: {workspace}')
    hub = Path(hub).resolve()
    runtime_skills = hub / 'runtime' / 'refactored_skills'
    if not runtime_skills.is_dir():
        runtime_skills = ROOT / 'refactored_skills'
        if not runtime_skills.is_dir():
            raise ValueError(f'Diretório de skills não encontrado em {hub / "runtime" / "refactored_skills"} nem em {ROOT / "refactored_skills"}')

    skills_to_link = []
    if skill:
        found = list(runtime_skills.glob(f'*/{skill}'))
        if not found or not (found[0] / 'SKILL.md').exists():
            raise ValueError(f"Skill '{skill}' não encontrada com SKILL.md em {runtime_skills}")
        skills_to_link.append(found[0])
    elif domain:
        domain_dir = runtime_skills / domain
        if not domain_dir.is_dir():
            raise ValueError(f'Domínio de skills não encontrado: {domain_dir}')
        for s_dir in sorted(domain_dir.iterdir()):
            if s_dir.is_dir() and (s_dir / 'SKILL.md').exists():
                skills_to_link.append(s_dir)
        if not skills_to_link:
            raise ValueError(f'Nenhuma skill válida encontrada no domínio: {domain}')
    else:
        domain_dir = runtime_skills / 'frontend'
        if not domain_dir.is_dir():
            raise ValueError(f'Domínio frontend não encontrado em {runtime_skills}')
        for s_dir in sorted(domain_dir.iterdir()):
            if s_dir.is_dir() and (s_dir / 'SKILL.md').exists():
                skills_to_link.append(s_dir)

    agents_skills_dir = workspace / '.agents' / 'skills'
    agents_skills_dir.mkdir(parents=True, exist_ok=True)

    linked = 0
    for s_path in skills_to_link:
        target_dir = agents_skills_dir / s_path.name
        source_dir = s_path.resolve()
        if target_dir.exists():
            print(f'  [JUNCTION] Já existe: {target_dir.name}')
            continue

        if os.name == 'nt':
            cmd = ['cmd', '/c', 'mklink', '/J', str(target_dir), str(source_dir)]
            res = subprocess.run(cmd, capture_output=True, text=True)
            if res.returncode != 0:
                raise RuntimeError(f'Falha ao criar Directory Junction NTFS para {s_path.name}: {res.stderr or res.stdout}')
            print(f'  ✅ Junction criada (depth 1): .agents/skills/{s_path.name} -> {source_dir}')
            linked += 1
        else:
            target_dir.symlink_to(source_dir, target_is_directory=True)
            print(f'  ✅ Symlink criado (depth 1): .agents/skills/{s_path.name} -> {source_dir}')
            linked += 1

    print(f'✅ Descoberta Codex: {linked} junction(s) configurada(s) em {agents_skills_dir}.')
    return linked


def install_claude_agents_v2(home, hub, mode='complete', dry_run=False, backup_mgr=None, root=ROOT):
    pasta = home / '.claude/agents'
    source_dir = (root / 'adapters/claude/agents') if (root / 'adapters/claude/agents').exists() else (ROOT / 'adapters/claude/agents')
    if not source_dir.exists():
        raise ValueError(f'Diretório canônico de subagentes não encontrado: {source_dir}')

    runtime_str = (hub / 'runtime').as_posix()
    templates = sorted(source_dir.glob('*.md'))
    if not templates:
        raise ValueError(f'Nenhum template de subagente encontrado em: {source_dir}')

    marker = hub / 'installation.json'
    previous = read_json(marker, {}) if marker.exists() else {}
    registrados = {}
    for entry in previous.get('claude_agents', []):
        p_str = entry.get('path', '')
        if p_str:
            registrados[str(Path(p_str).resolve())] = entry.get('sha256', '')
            registrados[p_str] = entry.get('sha256', '')

    for tmpl_file in templates:
        dest = pasta / tmpl_file.name
        dest_res = str(dest.resolve())
        if dest.exists():
            if dest_res not in registrados and str(dest) not in registrados:
                raise ValueError(f'Colisão preservada: {dest}')
            reg_sha = registrados.get(dest_res) or registrados.get(str(dest))
            if reg_sha != sha(dest):
                raise ValueError(f'Subagente local modificado; preservado: {dest}')

    novos = []
    for tmpl_file in templates:
        dest = pasta / tmpl_file.name
        content = tmpl_file.read_text(encoding='utf-8')
        content = content.replace('{{LAY_RUNTIME_DIR}}', runtime_str)

        if mode == 'public':
            content = re.sub(r'<!-- LAY-PRIVATE-SKILLS:BEGIN -->.*?<!-- LAY-PRIVATE-SKILLS:END -->\n?', '', content, flags=re.DOTALL)
        else:
            content = content.replace('<!-- LAY-PRIVATE-SKILLS:BEGIN -->\n', '').replace('<!-- LAY-PRIVATE-SKILLS:END -->\n', '')
            content = content.replace('<!-- LAY-PRIVATE-SKILLS:BEGIN -->', '').replace('<!-- LAY-PRIVATE-SKILLS:END -->', '')

        if dry_run:
            print(f"  [DRY-RUN] Instalaria subagente Claude: {dest}")
            novos.append({'path': str(dest), 'sha256': hashlib.sha256(content.encode('utf-8')).hexdigest()})
            continue

        existed = dest.exists()
        if existed and backup_mgr:
            backup_mgr.backup_file(dest)

        pasta.mkdir(parents=True, exist_ok=True)
        dest.write_text(content, encoding='utf-8', newline='\n')
        content_sha = sha(dest)
        if not existed and backup_mgr:
            backup_mgr.record_created(dest, content_sha)
        novos.append({'path': str(dest), 'sha256': content_sha})

    return novos


def install_claude_adapter_v2(home, hub, mode='complete', dry_run=False, backup_mgr=None, root=ROOT):
    claude_dir = home / '.claude'
    source_dir = (root / 'adapters/claude') if (root / 'adapters/claude').exists() else (ROOT / 'adapters/claude')
    runtime_str = (hub / 'runtime').as_posix()
    home_str = home.as_posix()

    tmpl_claude = source_dir / 'CLAUDE.md'
    if tmpl_claude.exists():
        content = tmpl_claude.read_text(encoding='utf-8')
        content = content.replace('{{PYTHON_EXE}}', sys.executable)
        content = content.replace('{{LAY_RUNTIME_DIR}}', runtime_str)
        content = content.replace('{{USER_HOME}}', home_str)
        dest = claude_dir / 'CLAUDE.md'
        update_rules_file(dest, content, backup_mgr=backup_mgr, dry_run=dry_run)

    return install_claude_agents_v2(home, hub, mode=mode, dry_run=dry_run, backup_mgr=backup_mgr, root=root)


def install_codex_adapter_v2(home, hub, dry_run=False, backup_mgr=None, root=ROOT):
    codex_dir = home / '.codex'
    source_dir = (root / 'adapters/codex') if (root / 'adapters/codex').exists() else (ROOT / 'adapters/codex')
    runtime_str = (hub / 'runtime').as_posix()
    home_str = home.as_posix()

    tmpl_agents = source_dir / 'AGENTS.md'
    if tmpl_agents.exists():
        content = tmpl_agents.read_text(encoding='utf-8')
        content = content.replace('{{PYTHON_EXE}}', sys.executable)
        content = content.replace('{{LAY_RUNTIME_DIR}}', runtime_str)
        content = content.replace('{{USER_HOME}}', home_str)
        dest = codex_dir / 'AGENTS.md'
        update_rules_file(dest, content, backup_mgr=backup_mgr, dry_run=dry_run)

    profiles_dir = source_dir / 'profiles'
    if profiles_dir.exists():
        for p_file in profiles_dir.glob('*.toml'):
            dest = codex_dir / p_file.name
            if dry_run:
                print(f"  [DRY-RUN] Copiaria perfil Codex: {dest}")
            else:
                codex_dir.mkdir(parents=True, exist_ok=True)
                existed = dest.exists()
                if existed and backup_mgr:
                    backup_mgr.backup_file(dest)
                shutil.copy2(p_file, dest)
                if not existed and backup_mgr:
                    backup_mgr.record_created(dest, sha(dest))


def install_antigravity_adapter_v2(home, hub, mode='complete', domain=None, dry_run=False, backup_mgr=None, root=ROOT):
    ag_dir = home / '.gemini'
    source_dir = (root / 'adapters/antigravity') if (root / 'adapters/antigravity').exists() else (ROOT / 'adapters/antigravity')
    runtime_str = (hub / 'runtime').as_posix()
    home_str = home.as_posix()
    agents_src_dir = source_dir / 'agents'
    target_agents_dir = ag_dir / 'config' / 'agents'

    # 0. Verificação antecipada de colisão e modificações manuais (aplica antes de qualquer alteração)
    marker = hub / 'installation.json'
    previous = read_json(marker, {}) if marker.exists() else {}
    registrados = {}
    for entry in previous.get('antigravity_agents', []):
        p_str = entry.get('path', '')
        if p_str:
            registrados[str(Path(p_str).resolve())] = entry.get('sha256', '')
            registrados[p_str] = entry.get('sha256', '')

    if agents_src_dir.exists():
        agent_files = sorted(agents_src_dir.glob('*.md'))
        for a_file in agent_files:
            dest = target_agents_dir / a_file.name
            dest_res = str(dest.resolve())
            if dest.exists():
                if dest_res not in registrados and str(dest) not in registrados:
                    raise ValueError(f'Colisão preservada: {dest}')
                reg_sha = registrados.get(dest_res) or registrados.get(str(dest))
                if reg_sha != sha(dest):
                    raise ValueError(f'Subagente local modificado; preservado: {dest}')

    # 1. Regras GEMINI.md
    tmpl_gemini = source_dir / 'GEMINI.md'
    if tmpl_gemini.exists():
        content = tmpl_gemini.read_text(encoding='utf-8')
        content = content.replace('{{PYTHON_EXE}}', sys.executable)
        content = content.replace('{{LAY_RUNTIME_DIR}}', runtime_str)
        content = content.replace('{{USER_HOME}}', home_str)
        dest = ag_dir / 'GEMINI.md'
        update_rules_file(dest, content, backup_mgr=backup_mgr, dry_run=dry_run)

    # 2. Manifesto de skills ~/.gemini/config/skills.json
    manifest_name = f'skills-{domain}.json' if domain else 'skills-full.json'
    manifest_src = source_dir / 'manifests' / manifest_name
    if not manifest_src.exists() and domain:
        manifest_src = source_dir / 'manifests' / 'skills-full.json'

    if manifest_src.exists():
        content = manifest_src.read_text(encoding='utf-8')
        content = content.replace('{{LAY_RUNTIME_DIR}}', runtime_str)
        try:
            m_data = json.loads(content)
            entries = m_data.get('entries', [])
            if mode == 'public':
                entries = [e for e in entries if 'skills-privadas-lay' not in e.get('path', '')]
            if domain:
                entries = [e for e in entries if e.get('path', '').endswith(f'/{domain}')]
            # Deduplicação de entries preservando ordem
            seen_paths = set()
            dedup_entries = []
            for e in entries:
                p = e.get('path')
                if p not in seen_paths:
                    seen_paths.add(p)
                    dedup_entries.append(e)
            m_data['entries'] = dedup_entries
            content = json.dumps(m_data, indent=2, ensure_ascii=False) + '\n'
        except Exception:
            pass

        config_dir = ag_dir / 'config'
        dest = config_dir / 'skills.json'
        if dry_run:
            print(f"  [DRY-RUN] Instalaria manifesto Antigravity: {dest}")
        else:
            config_dir.mkdir(parents=True, exist_ok=True)
            existed = dest.exists()
            if existed and backup_mgr:
                backup_mgr.backup_file(dest)
            dest.write_text(content, encoding='utf-8', newline='\n')
            if not existed and backup_mgr:
                backup_mgr.record_created(dest, sha(dest))

    # 3. Template de subagentes Antigravity (compatibilidade/transitório)
    subagents_src = source_dir / 'agents' / 'subagents-definition-template.json'
    if subagents_src.exists():
        dest = ag_dir / 'antigravity' / 'agents' / 'subagents-definition-template.json'
        if dry_run:
            print(f"  [DRY-RUN] Copiaria template de subagentes Antigravity: {dest}")
        else:
            dest.parent.mkdir(parents=True, exist_ok=True)
            existed = dest.exists()
            if existed and backup_mgr:
                backup_mgr.backup_file(dest)
            shutil.copy2(subagents_src, dest)
            if not existed and backup_mgr:
                backup_mgr.record_created(dest, sha(dest))

    # 4. Subagentes persistentes ~/.gemini/config/agents/*.md
    installed_agents = []
    agents_src_dir = source_dir / 'agents'
    target_agents_dir = ag_dir / 'config' / 'agents'
    if agents_src_dir.exists():
        agent_files = sorted(agents_src_dir.glob('*.md'))
        for a_file in agent_files:
            dest = target_agents_dir / a_file.name
            if dry_run:
                print(f"  [DRY-RUN] Instalaria subagente Antigravity: {dest}")
                continue
            target_agents_dir.mkdir(parents=True, exist_ok=True)
            content = a_file.read_text(encoding='utf-8')
            content = content.replace('{{LAY_RUNTIME_DIR}}', runtime_str)
            if mode == 'public':
                content = re.sub(r'<!-- LAY-PRIVATE-SKILLS:BEGIN -->.*?<!-- LAY-PRIVATE-SKILLS:END -->\s*([^\n]+\n)?', '', content, flags=re.DOTALL)
            existed = dest.exists()
            if existed and backup_mgr:
                backup_mgr.backup_file(dest)
            dest.write_text(content, encoding='utf-8', newline='\n')
            if not existed and backup_mgr:
                backup_mgr.record_created(dest, sha(dest))
            installed_agents.append({'name': a_file.name, 'path': str(dest), 'sha256': sha(dest)})

    return installed_agents


def install(home, agents, root=ROOT, skip_tools=False, mode='complete', domain=None, dry_run=False):
    home = home.resolve()
    hub = home / '.lay-skills'

    if mode not in ('complete', 'public'):
        raise ValueError(f"Modo inválido: {mode}. Escolha 'complete' ou 'public'.")
    if mode == 'complete':
        if not (root / PRIVATE_REFACTORED).is_dir():
            raise ValueError(
                "Modo 'complete' solicitado, mas o diretório autorizado de skills privadas "
                "('skills-privadas-lay/refactored') não está presente no repositório. "
                "Use '--mode public' para instalar apenas as skills públicas do catálogo."
            )

    if dry_run:
        print("=== [DRY-RUN] SIMULAÇÃO DE INSTALAÇÃO DO LAY SKILLS HUB ===")
        print(f"  Target Home: {home}")
        print(f"  Hub Runtime: {hub / 'runtime'}")
        print(f"  Clientes solicitados: {agents}")
        print(f"  Modo: {mode}")
        print(f"  Clientes detectados: {detect_clients(home)}")

    backup_mgr = BackupManager(hub, dry_run=dry_run)
    catalog = build_catalog(root)
    if mode == 'complete':
        installed = catalog['skills'] + private_entries(root)
    else:
        installed = catalog['skills']

    ids = [e['id'] for e in installed]
    if len(ids) != len(set(ids)):
        raise ValueError('Identidade duplicada entre catálogo público e skills privadas')

    reg_sources = root / 'registry/sources.json'
    if reg_sources.exists():
        for source in sources(root).get('sources', []):
            source_root = root / source.get('path', '')
            if not (source_root / '.git').exists():
                continue
            if git(source_root, 'status', '--porcelain', '--untracked-files=no'):
                raise ValueError(f"Fonte modificada: {source['id']}; preserve/revise alterações antes de instalar")

    runtime = hub / 'runtime'
    if not dry_run:
        hub.mkdir(parents=True, exist_ok=True)
        if root.resolve() != runtime.resolve():
            copy_dirs = ['scripts', 'skills', 'docs', 'catalog', 'registry', 'templates', 'tecnologias', REFACTORED]
            if mode == 'complete':
                copy_dirs.append(PRIVATE_REFACTORED)
            for directory in copy_dirs:
                src_d = root / directory
                if not src_d.exists():
                    continue
                for p in files(src_d):
                    dst = runtime / p.relative_to(root)
                    dst.parent.mkdir(parents=True, exist_ok=True)
                    if not dst.exists() or sha(dst) != sha(p):
                        shutil.copy2(p, dst)
            for name in ('README.md', 'AGENTS.md', 'CLAUDE.md', 'GEMINI.md'):
                if (root / name).exists():
                    shutil.copy2(root / name, runtime / name)
            for d in ('adapters', 'core'):
                if (root / d).exists():
                    for p in files(root / d):
                        dst = runtime / p.relative_to(root)
                        dst.parent.mkdir(parents=True, exist_ok=True)
                        if not dst.exists() or sha(dst) != sha(p):
                            shutil.copy2(p, dst)
        write(runtime / 'catalog/installed.json', {'schema_version': 1, 'mode': mode, 'skills': installed})
    else:
        print(f"  [DRY-RUN] Provisionaria runtime em {runtime} ({len(installed)} skills)")

    if not skip_tools and not dry_run:
        graph_source = next((s for s in sources(root)['sources'] if 'graphify' in s['id']), None)
        ensure_graphify(hub, root, graph_source)

    claude_agents = []
    if 'claude' in agents:
        claude_agents = install_claude_adapter_v2(home, hub, mode=mode, dry_run=dry_run, backup_mgr=backup_mgr, root=root)
    if 'codex' in agents:
        install_codex_adapter_v2(home, hub, dry_run=dry_run, backup_mgr=backup_mgr, root=root)
    antigravity_agents = []
    if 'antigravity' in agents:
        antigravity_agents = install_antigravity_adapter_v2(home, hub, mode=mode, domain=domain, dry_run=dry_run, backup_mgr=backup_mgr, root=root)

    backup_dir = backup_mgr.finalize()
    if backup_dir:
        print(f"  [BACKUP] Backup preventivo salvo em: {backup_dir.name}")

    if not dry_run:
        state = {
            'schema_version': 2,
            'owner': 'lay-skills',
            'installed_at': now(),
            'source_root': str(root.resolve()),
            'home': str(home),
            'agents': sorted(agents),
            'mode': mode,
            'catalog_count': len(installed),
            'python': sys.executable,
            'claude_agents': claude_agents,
            'antigravity_agents': antigravity_agents
        }
        marker = hub / 'installation.json'
        write(marker, state)
        print(f"✅ Instalação concluída com sucesso ({mode}: {len(installed)} skills) para clientes: {', '.join(agents)}.")
        return state
    else:
        print(f"✅ [DRY-RUN] Simulação concluída com sucesso. Zero alterações em disco.")
        return {'dry_run': True, 'mode': mode, 'agents': agents}



def sync(root=ROOT, apply=False):
    """Parent first; never reset/stash/force or merge a divergent working tree."""
    events = []
    try:
        git(root, 'fetch', '--quiet', 'origin', timeout=45)
        before = git(root, 'rev-parse', 'HEAD')
        remote = git(root, 'rev-parse', '@{upstream}')
        dirty = bool(git(root, 'status', '--porcelain', '--untracked-files=no'))
        base = git(root, 'merge-base', before, remote)
        behind = before != remote and base == before
        ahead = before != remote and base == remote
        if behind and apply and not dirty:
            git(root, 'merge', '--ff-only', '@{upstream}')
            # New parent code/schema must be used on a subsequent invocation.
            print(f'✅ Repositório pai atualizado versão {remote[:12]}; executando versão atual.')
            result = run([sys.executable, root / 'scripts/skill_hub.py', 'sync', '--apply', '--parent-checked'], cwd=root, timeout=600)
            print(result.stdout, end='')
            return result.returncode == 0
        if before == remote:
            status = 'já atual'
        elif behind:
            status = 'atualização pendente; alterações locais preservadas' if dirty else 'atualização disponível'
        elif ahead:
            status = 'revisão local à frente do remoto; preservada'
        else:
            status = 'histórico divergente; requer revisão'
        print(f"{'ℹ️' if before == remote or ahead else '⚠️'} Repositório pai {status} ({before[:12]}).")
        events.append({'source': 'parent', 'status': status, 'commit': before})
    except (RuntimeError, subprocess.TimeoutExpired) as exc:
        print(f'⚠️ Consulta ao pai indisponível: {exc}. Fontes não atualizadas nesta tentativa.')
        return False
    return sync_sources(root, apply, events)


def sync_sources(root, apply, events=None):
    data = sources(root)
    success = True
    events = events or []
    def fetch(source):
        path = confined(root, source['path'])
        if not (path / '.git').exists():
            # Without its own checkout git would resolve the parent repo and report a false "current".
            if source.get('kind') == 'repertorio':
                listing = git(root, 'ls-remote', source['url'], 'HEAD', timeout=45)
                return source, None, listing.split()[0]
            raise ValueError(f"submódulo não inicializado; rode git submodule update --init {source['path']}")
        git(path, 'fetch', '--quiet', 'origin', timeout=45)
        # remote HEAD is resolved afresh; do not guess main/master.
        listing = git(path, 'ls-remote', '--symref', 'origin', 'HEAD', timeout=45)
        match = re.search(r'^ref: refs/heads/(.+)\s+HEAD$', listing, re.M)
        if not match:
            raise ValueError(f"Branch remoto não identificado: {source['id']}")
        branch = match.group(1)
        git(path, 'fetch', '--quiet', 'origin', branch, timeout=45)
        return source, path, git(path, 'rev-parse', 'FETCH_HEAD')
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
        jobs = [(s, pool.submit(fetch, s)) for s in data['sources']]
        for source, job in jobs:
            try:
                source, path, target = job.result()
                if path is None:
                    note = 'igual ao registrado' if target == source.get('commit') else f'registrado {source.get("version")}'
                    print(f"ℹ️ {source['id']}: repertório sem checkout local; remoto {target[:12]} ({note}).")
                    events.append({'source': source['id'], 'status': 'reference', 'target': target})
                    continue
                current = git(path, 'rev-parse', 'HEAD')
                if target == current:
                    print(f"ℹ️ {source['id']} já atual, versão {source.get('version', current[:12])}.")
                    status = 'current'
                elif git(path, 'merge-base', current, target) != current:
                    print(f"⚠️ {source['id']}: histórico divergente; revisão local preservada.")
                    status = 'diverged'
                elif apply and not git(path, 'status', '--porcelain', '--untracked-files=no'):
                    git(path, 'checkout', '--quiet', '--detach', target)
                    if (path / '.gitmodules').exists():
                        git(path, 'submodule', 'update', '--init', '--recursive', timeout=300)
                    source['commit'] = target
                    source['version'] = git(path, 'describe', '--tags', '--always')
                    print(f"✅ Skill {source['id']} atualizada versão {source['version']}.")
                    status = 'updated'
                else:
                    if apply:
                        print(f"⚠️ {source['id']}: atualização disponível {target[:12]}; alterações em arquivos rastreados preservadas.")
                    else:
                        print(f"⚠️ {source['id']}: atualização disponível {target[:12]}; aplique com sync --apply.")
                    status = 'pending'
                events.append({'source': source['id'], 'status': status, 'target': target})
            except (RuntimeError, ValueError, subprocess.TimeoutExpired) as exc:
                success = False
                print(f"⚠️ {source['id']}: consulta falhou ({exc}).")
    if apply:
        run([sys.executable, root / 'scripts/refresh_registry.py'], cwd=root, timeout=120)
        build_catalog(root)
    write(root / '.state/update-report.json', {'checked_at': now(), 'complete': success, 'events': events})
    return success


def project_report(project):
    project = project.resolve()
    if not project.is_dir():
        raise ValueError(f'Projeto não existe: {project}')
    inventory = []
    for p in files(project):
        rel = p.relative_to(project)
        if len(rel.parts) <= 5 and rel.parts[0] not in {'upstream', 'graphify-out', 'dist', 'build', 'coverage', '.next'}:
            inventory.append(rel.as_posix())
        if len(inventory) >= 12000:
            break
    active = any(p.endswith(('.py', '.tsx', '.ts', '.js', '.jsx', '.go', '.rs', '.java', '.cs', '.html')) for p in inventory)
    stack = [name for name in ('package.json', 'pyproject.toml', 'Cargo.toml', 'go.mod', 'pom.xml', 'composer.json') if name in inventory]
    graph = project / 'graphify-out/graph.json'
    rows = [('P0', 'Contexto', 'Confirmar objetivo, público e restrições ausentes', 'interviewing-user-requirements / refining-raw-product-ideas'),
            ('P1', 'Arquitetura', 'Consultar grafo e validar referências' if graph.exists() else 'Grafo ausente; mapear e gerar Graphify conforme stack', 'generating-knowledge-graphs'),
            ('P1', 'Segurança', 'Examinar autenticação, entradas, segredos e dependências; sem falha presumida', 'auditing-code-security / scanning-dependency-vulnerabilities'),
            ('P2', 'Qualidade', 'Identificar testes e comandos existentes antes de executar', 'reviewing-multi-axis-code-quality / automating-browser-tests')]
    if any(p.endswith(('.tsx', '.jsx', '.html', '.vue', '.svelte', '.css')) for p in inventory):
        rows.append(('P2', 'Design', 'Avaliar fluxo, identidade, acessibilidade e desempenho', 'taste / impeccable / web-design-guidelines'))
    lines = [f"Projeto {'existente' if active else 'novo ou sem código reconhecido'}: {project}",
             f"Manifestos: {', '.join(stack) or 'nenhum reconhecido'}. Arquivos inventariados: {len(inventory)}.", '',
             '| Prioridade | Área | Próxima ação fundamentada no inventário | Skills |', '|---|---|---|---|']
    lines += [f'| {priority} | {area} | {action} | {skills} |' for priority, area, action, skills in rows]
    lines += ['', 'Triagem de oportunidades, não diagnóstico de vulnerabilidades. Nenhum arquivo do projeto foi alterado.',
              'Novo projeto: esclarecer contexto que mude decisões; acionar repertório apenas na etapa correspondente.']
    return '\n'.join(lines), inventory


def start(home, project, refresh=False, offline=False):
    hub = home / '.lay-skills'
    state = read_json(hub / 'installation.json', {})
    if not state:
        raise ValueError('Instalação global ausente. Execute install primeiro.')
    key = hashlib.sha256(str(project.resolve()).encode()).hexdigest()[:24]
    cache_path = hub / 'projects' / (key + '.json')
    previous = read_json(cache_path, {})
    if previous.get('updates_checked') and not refresh:
        print(f"ℹ️ Verificação inicial já realizada para este projeto ({previous['checked_at']}); --refresh consulta novamente.")
        report, _ = project_report(project)
        print(report)
        return
    checked = False
    if offline:
        print('⚠️ Modo offline: fontes não verificadas; usando catálogo instalado.')
    else:
        source_root = Path(state['source_root'])
        if (source_root / '.git').exists():
            # Regra: o início de sessão só consulta. Não altera arquivos do repositório nem reinstala;
            # atualizações são aplicadas explicitamente com `sync --apply` e commitadas.
            result = run([state.get('python', sys.executable), source_root / 'scripts/skill_hub.py', 'sync', '--check'], timeout=600, check=False)
            print(result.stdout, end='')
            checked = result.returncode == 0
        else:
            print('⚠️ Clone pai indisponível; catálogo local preservado. Reinstale a partir de um clone para atualizar.')
    report, inventory = project_report(project)
    print(report)
    write(cache_path, {'project': str(project.resolve()), 'checked_at': now(), 'updates_checked': checked,
                       'inventory': inventory, 'report': report})


def doctor(home):
    hub = home / '.lay-skills'
    state = read_json(hub / 'installation.json', {})
    errors = []
    if not state:
        errors.append('Instalação ausente')
        print('❌ Instalação ausente')
        return False

    print(f"=== LAY Skills Doctor ({state.get('mode', 'legado')}: {state.get('catalog_count', 0)} skills) ===")
    print(f"  Home: {home}")
    print(f"  Hub: {hub}")

    for entry in state.get('claude_agents', []):
        p = Path(entry['path'])
        if not p.exists():
            errors.append(f'Subagente ausente: {p}')
        elif sha(p) != entry['sha256']:
            errors.append(f'Subagente modificado: {p}')

    for entry in state.get('antigravity_agents', []):
        p = Path(entry['path'])
        if not p.exists():
            errors.append(f'Subagente Antigravity ausente: {p}')
        elif sha(p) != entry['sha256']:
            errors.append(f'Subagente Antigravity modificado: {p}')

    for agent in state.get('agents', []):
        rule_f = home / RULES.get(agent, '')
        if rule_f.exists():
            print(f"  ✅ Regras {agent}: {rule_f}")
        else:
            errors.append(f'Arquivo de regras ausente: {rule_f}')

    for entry in state.get('wrappers', []):
        p = Path(entry['path']) / 'SKILL.md'
        if not p.exists() or sha(p) != entry['sha256']:
            errors.append(f'Wrapper ausente/modificado: {p}')

    print("\nFerramentas do sistema:")
    for command in ('git', 'python', 'claude', 'codex', 'antigravity'):
        found = shutil.which(command)
        if command == 'python' and not found:
            found = sys.executable
        print(f"  {'✅' if found else '⚠️ '} {command}: {found or 'não encontrado no PATH'}")

    if errors:
        print(f"\n❌ {len(errors)} problemas detectados:")
        for err in errors:
            print(f"  - {err}")
        return False
    else:
        print(f"\n✅ Todos os componentes e subagentes verificados com sucesso!")
        return True


def uninstall(home):
    hub = home / '.lay-skills'
    state = read_json(hub / 'installation.json', {})
    kept = []
    for entry in state.get('wrappers', []):
        p = Path(entry['path'])
        allowed = [confined(home, d) for agent_name in DESTINATIONS for d in destinations(agent_name)]
        if p.parent.resolve() not in allowed or p.is_symlink():
            raise ValueError(f'Destino de remoção inválido: {p}')
        if p.exists():
            if (p / 'SKILL.md').exists() and (p / '.lay-managed.json').exists() and sha(p / 'SKILL.md') == entry['sha256'] and {f.name for f in p.iterdir()} <= {'SKILL.md', '.lay-managed.json'}:
                (p / 'SKILL.md').unlink()
                (p / '.lay-managed.json').unlink()
                p.rmdir()
            else:
                kept.append(entry)
    for agent in state.get('agents', []):
        path = home / RULES[agent]
        if path.exists():
            old = path.read_text(encoding='utf-8')
            if old.count(BEGIN) == 1 and old.count(END) == 1:
                new = old[:old.index(BEGIN)] + old[old.index(END)+len(END):]
                managed_write(path, new, hub)
    for entry in state.get('claude_agents', []):
        p = Path(entry['path'])
        if p.parent == home / '.claude/agents' and p.exists() and sha(p) == entry['sha256']:
            p.unlink()
    state['claude_agents'] = []
    for entry in state.get('antigravity_agents', []):
        p = Path(entry['path'])
        if p.parent == home / '.gemini/config/agents' and p.exists() and sha(p) == entry['sha256']:
            p.unlink()
    state['antigravity_agents'] = []
    state['wrappers'] = kept
    state['agents'] = []
    for agent, path in [('claude', home / '.claude/settings.json'), ('codex', home / '.codex/hooks.json'), ('antigravity', home / '.gemini/config/hooks.json')]:
        if not path.exists():
            continue
        data = read_json(path, {})
        if agent == 'antigravity':
            group = data.get('lay-skills', {})
            if any('skill_hub.py" hook --agent antigravity' in h.get('command', '') for h in group.get('PreInvocation', []) if isinstance(h, dict)):
                data.pop('lay-skills', None)
        else:
            groups = data.get('hooks', {}).get('SessionStart', [])
            data['hooks']['SessionStart'] = [g for g in groups if not any(f'skill_hub.py" hook --agent {agent}' in h.get('command', '') for h in g.get('hooks', []) if isinstance(h, dict))]
        managed_write(path, json.dumps(data, ensure_ascii=False, indent=2) + '\n', hub)
    write(hub / 'installation.json', state)
    print(f'✅ Entradas gerenciadas removidas; {len(kept)} modificadas preservadas. Bundles e backups mantidos em {hub}.')


def main():
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='command', required=True)
    for command in ('install', 'doctor', 'uninstall', 'start', 'hook', 'rollback', 'link-junctions'):
        p = sub.add_parser(command)
        p.add_argument('--home', type=Path, default=Path.home())
        if command == 'install':
            p.add_argument('--agents', default='all', help='all ou codex,claude,antigravity')
            p.add_argument('--mode', choices=['complete', 'public'], default='complete', help='modo de instalação: complete (todas as skills, incluindo cofre privado) ou public (apenas skills públicas)')
            p.add_argument('--dry-run', action='store_true', help='simular instalação sem modificar o disco')
            p.add_argument('--domain', default=None, help='domínio específico de skills para Antigravity (ex: frontend)')
            p.add_argument('--skip-tools', action='store_true', help='pular instalação isolada do Graphify')
        if command == 'rollback':
            p.add_argument('--backup-dir', type=Path, default=None, help='caminho do diretório de backup a restaurar')
        if command == 'link-junctions':
            p.add_argument('--workspace', type=Path, required=True, help='caminho do workspace para criar a junction')
            p.add_argument('--domain', default=None, help='domínio de skills a linkar (ex: frontend)')
            p.add_argument('--skill', default=None, help='skill individual a linkar')
        if command == 'start':
            p.add_argument('--project', type=Path, required=True)
            p.add_argument('--refresh', action='store_true')
            p.add_argument('--offline', action='store_true')
        if command == 'hook':
            p.add_argument('--agent', choices=DESTINATIONS, required=True)
    sub.add_parser('catalog')
    sub.add_parser('scan')
    p = sub.add_parser('search')
    p.add_argument('query')
    p = sub.add_parser('sync')
    mode = p.add_mutually_exclusive_group()
    mode.add_argument('--apply', action='store_true')
    mode.add_argument('--check', action='store_true')
    p.add_argument('--parent-checked', action='store_true', help=argparse.SUPPRESS)

    # Subcomando task (LAY Orchestrator)
    p_task = sub.add_parser('task', help='Gerenciamento local de tarefas do LAY Orchestrator')
    task_sub = p_task.add_subparsers(dest='task_action', required=True)

    # task create
    p_tc = task_sub.add_parser('create', help='Criar nova tarefa com classificação heurística')
    p_tc.add_argument('--workspace', type=Path, default=Path.cwd(), help='Diretório raiz do workspace')
    p_tc.add_argument('--title', required=True, help='Título descritivo da tarefa')
    p_tc.add_argument('--domain', default='engineering', help='Domínio da tarefa (ex: frontend, engineering, security)')
    p_tc.add_argument('--complexity', choices=['low', 'medium', 'high', 'critical'], default=None, help='Classificação explícita de complexidade')
    p_tc.add_argument('--context', nargs='*', default=[], help='Caminhos de contexto ou arquivos relevantes')
    p_tc.add_argument('--constraints', nargs='*', default=[], help='Restrições técnicas')
    p_tc.add_argument('--acceptance-criteria', nargs='*', default=[], help='Critérios de aceite')
    p_tc.add_argument('--client', default='local', help='Cliente executor (claude, antigravity, codex, local)')

    # task list
    p_tl = task_sub.add_parser('list', help='Listar tarefas do workspace')
    p_tl.add_argument('--workspace', type=Path, default=Path.cwd(), help='Diretório raiz do workspace')
    p_tl.add_argument('--status', choices=['pending', 'in_progress', 'completed', 'failed', 'blocked', 'escalated'], default=None, help='Filtrar por status')

    # task show
    p_ts = task_sub.add_parser('show', help='Exibir detalhes de uma tarefa')
    p_ts.add_argument('task_id', help='Identificador da tarefa (ex: task-12345678)')
    p_ts.add_argument('--workspace', type=Path, default=Path.cwd(), help='Diretório raiz do workspace')

    # task assign
    p_ta = task_sub.add_parser('assign', help='Atribuir responsável e modalidade de execução')
    p_ta.add_argument('task_id', help='Identificador da tarefa')
    p_ta.add_argument('--workspace', type=Path, default=Path.cwd(), help='Diretório raiz do workspace')
    p_ta.add_argument('--specialist', required=True, help='Nome do especialista (ex: lay-frontend, lay-seguranca)')
    p_ta.add_argument('--mode', choices=['session', 'subagent', 'cross_client', 'arbitrator'], default='session', help='Modalidade de execução')
    p_ta.add_argument('--reason', default=None, help='Justificativa objetiva da delegação (obrigatória para subagent/arbitrator)')

    # task recommend
    p_tr = task_sub.add_parser('recommend', aliases=['route'], help='Consultar recomendação de roteamento para uma tarefa')
    p_tr.add_argument('--task-id', default=None, help='Identificador da tarefa existente')
    p_tr.add_argument('--workspace', type=Path, default=Path.cwd(), help='Diretório raiz do workspace')
    p_tr.add_argument('--title', default=None, help='Título descritivo da tarefa (se sem task-id)')
    p_tr.add_argument('--domain', default=None, help='Domínio pretendido')
    p_tr.add_argument('--client', default='local', help='Cliente executor (claude, antigravity, codex, local)')
    p_tr.add_argument('--target-client', choices=['claude', 'antigravity', 'codex', 'local'], default=None, help='Cliente alvo pretendido para handoff')
    p_tr.add_argument('--complexity', choices=['low', 'medium', 'high', 'critical'], default=None, help='Complexidade explícita')
    p_tr.add_argument('--specialist', default=None, help='Especialista pretendido')

    # task complete
    p_tcp = task_sub.add_parser('complete', help='Concluir tarefa com contrato RESULT')
    p_tcp.add_argument('task_id', help='Identificador da tarefa')
    p_tcp.add_argument('--workspace', type=Path, default=Path.cwd(), help='Diretório raiz do workspace')
    p_tcp.add_argument('--summary', required=True, help='Resumo conclusivo da entrega')
    p_tcp.add_argument('--result-status', choices=['success', 'failure', 'needs_clarification', 'escalated'], default='success', help='Status da entrega RESULT')
    p_tcp.add_argument('--artifacts', nargs='*', default=[], help='Arquivos ou artefatos gerados')
    p_tcp.add_argument('--open-items', nargs='*', default=[], help='Pendências ou itens em aberto')

    # task resume
    p_trsm = task_sub.add_parser('resume', help='Retomar execução de tarefa em blocked/failed/escalated')
    p_trsm.add_argument('task_id', help='Identificador da tarefa')
    p_trsm.add_argument('--workspace', type=Path, default=Path.cwd(), help='Diretório raiz do workspace')
    p_trsm.add_argument('--clarification', default=None, help='Esclarecimento fornecido para desbloqueio')
    p_trsm.add_argument('--reason', default=None, help='Motivo da retomada')

    # task arbitrate
    p_tarb = task_sub.add_parser('arbitrate', help='Preparar pacote estruturado para arbitragem')
    p_tarb.add_argument('task_id', help='Identificador da tarefa')
    p_tarb.add_argument('--workspace', type=Path, default=Path.cwd(), help='Diretório raiz do workspace')
    p_tarb.add_argument('--problem', required=True, help='Descrição do problema / impasse arquitetural')
    p_tarb.add_argument('--alternatives', nargs='+', required=True, help='Ao menos 2 alternativas concorrentes')
    p_tarb.add_argument('--evidences', nargs='*', default=[], help='Evidências técnicas observadas')
    p_tarb.add_argument('--constraints', nargs='*', default=[], help='Restrições técnicas ou de negócio')
    p_tarb.add_argument('--criteria', nargs='*', default=[], help='Critérios de decisão')

    # task handoff
    p_thd = task_sub.add_parser('handoff', help='Realizar handoff de tarefa entre clientes (Cross-Client)')
    p_thd.add_argument('task_id', help='Identificador da tarefa')
    p_thd.add_argument('--target-client', choices=['claude', 'antigravity', 'codex', 'local'], required=True, help='Cliente de destino')
    p_thd.add_argument('--reason', required=True, help='Justificativa técnica do handoff entre clientes')
    p_thd.add_argument('--authorized', action='store_true', default=False, help='Autorização explícita para cruzar fronteira de cliente')
    p_thd.add_argument('--workspace', type=Path, default=Path.cwd(), help='Diretório raiz do workspace')
    args = parser.parse_args()
    try:
        if args.command == 'install':
            agents = list(DESTINATIONS) if args.agents == 'all' else args.agents.split(',')
            if not agents or any(a not in DESTINATIONS for a in agents):
                raise ValueError('Agente inválido')
            install(args.home, agents, skip_tools=args.skip_tools, mode=args.mode, domain=args.domain, dry_run=args.dry_run)
        elif args.command == 'rollback':
            rollback(args.home, args.backup_dir)
        elif args.command == 'link-junctions':
            hub = args.home.resolve() / '.lay-skills'
            link_junctions(args.workspace, hub, domain=args.domain, skill=args.skill)
        elif args.command == 'catalog':
            print(f"✅ Catálogo: {len(build_catalog()['skills'])} entradas.")
        elif args.command == 'scan':
            scan()
        elif args.command == 'sync':
            return 0 if (sync_sources(ROOT, args.apply) if args.parent_checked else sync(ROOT, args.apply)) else 1
        elif args.command == 'start':
            start(args.home.resolve(), args.project, args.refresh, args.offline)
        elif args.command == 'hook':
            hook(args.home.resolve(), args.agent)
        elif args.command == 'doctor':
            return 0 if doctor(args.home.resolve()) else 1
        elif args.command == 'uninstall':
            uninstall(args.home.resolve())
        elif args.command == 'search':
            data = read_json(ROOT / 'catalog/skills.json') or build_catalog()
            data = {'skills': data['skills'] + private_entries(ROOT)}
            query = args.query.lower()
            for e in data['skills']:
                if query in ' '.join([e['id'], e['name'], e['description'], *e['categories']]).lower():
                    print(f"{e['id']} | {', '.join(e['categories'])} | {e['description'][:220]}")
        elif args.command == 'task':
            try:
                import tasks
            except ImportError:
                from scripts import tasks
            ws = args.workspace.resolve()
            if args.task_action == 'create':
                t = tasks.create_task(
                    workspace=ws,
                    title=args.title,
                    domain=args.domain,
                    complexity=args.complexity,
                    context=args.context,
                    constraints=args.constraints,
                    acceptance_criteria=args.acceptance_criteria,
                    client=args.client
                )
                print(f"✅ Tarefa criada com sucesso: {t['id']}")
                print(f"   Título: {t['title']}")
                print(f"   Complexidade: {t['complexity']} (Modo sugerido: {t['routing']['execution_mode']})")
                print(f"   Status: {t['status']}")
            elif args.task_action == 'list':
                ts = tasks.list_tasks(workspace=ws, status_filter=args.status)
                if not ts:
                    print("Nenhuma tarefa encontrada.")
                else:
                    print(f"=== Tarefas ({len(ts)}) em {ws} ===")
                    for t in ts:
                        spec = t['routing'].get('target_specialist') or 'não atribuído'
                        print(f"- {t['id']} | [{t['status'].upper()}] | {t['complexity']:8} | {spec:15} | {t['title']}")
            elif args.task_action == 'show':
                t = tasks.get_task(workspace=ws, task_id=args.task_id)
                print(json.dumps(t, indent=2, ensure_ascii=False))
            elif args.task_action == 'assign':
                t = tasks.assign_task(
                    workspace=ws,
                    task_id=args.task_id,
                    specialist=args.specialist,
                    mode=args.mode,
                    reason=args.reason
                )
                print(f"✅ Tarefa {t['id']} atribuída:")
                print(f"   Especialista: {t['routing']['target_specialist']}")
                print(f"   Modalidade:   {t['routing']['execution_mode']}")
                print(f"   Status:       {t['status']}")
                if t['routing'].get('delegation_reason'):
                    print(f"   Justificativa:{t['routing']['delegation_reason']}")
            elif args.task_action in ('recommend', 'route'):
                if args.task_id:
                    task = tasks.get_task(workspace=ws, task_id=args.task_id)
                    rec = tasks.recommend_task_routing(
                        title=task['title'],
                        domain=task['handoff'].get('domain'),
                        client=task['routing'].get('client', 'local'),
                        explicit_complexity=task.get('complexity')
                    )
                elif args.title:
                    rec = tasks.recommend_task_routing(
                        title=args.title,
                        domain=args.domain,
                        client=args.client,
                        target_client=args.target_client,
                        explicit_complexity=args.complexity,
                        explicit_specialist=args.specialist
                    )
                else:
                    print("⚠️ Informe --task-id ou --title para obter recomendação.", file=sys.stderr)
                    return 1

                print("=== Decisão de Roteamento (Recomendação) ===")
                print(f"Complexidade Estimada:    {rec['complexity']}")
                print(f"Domínio Recomendado:      {rec['recommended_domain']}")
                print(f"Cliente Atual:            {rec['current_client']}")
                print(f"Modo Recomendado:         {rec['recommended_mode']}")
                print(f"Especialista Recomendado: {rec['recommended_specialist'] or 'nenhum'}")
                print(f"Autorização Necessária:   {'Sim' if rec['requires_authorization'] else 'Não'}")
                print(f"Delegação Permitida:      {'Sim' if rec['delegation_allowed'] else 'Não'}")
                print(f"Justificativa:            {rec['rationale']}")
                if rec['relevant_skills']:
                    print(f"Skills Relevantes:        {', '.join(rec['relevant_skills'])}")
            elif args.task_action == 'complete':
                t = tasks.complete_task(
                    workspace=ws,
                    task_id=args.task_id,
                    summary=args.summary,
                    result_status=args.result_status,
                    artifacts=args.artifacts,
                    open_items=args.open_items
                )
                if t['status'] == 'completed':
                    print(f"✅ Tarefa {t['id']} concluída com sucesso:")
                else:
                    print(f"✅ Resultado registrado para {t['id']}:")
                print(f"   Status Tarefa: {t['status']}")
                print(f"   Status RESULT: {t['result']['status']}")
                print(f"   Resumo:        {t['result']['summary']}")
                if t['result'].get('artifacts'):
                    print(f"   Artefatos:     {', '.join(t['result']['artifacts'])}")
                if t['result'].get('open_items'):
                    print(f"   Pendências:    {', '.join(t['result']['open_items'])}")
            elif args.task_action == 'resume':
                t = tasks.resume_task(
                    workspace=ws,
                    task_id=args.task_id,
                    clarification=args.clarification,
                    reason=args.reason
                )
                print(f"✅ Tarefa {t['id']} retomada com sucesso para 'in_progress':")
                print(f"   Status Atual:    {t['status']}")
                print(f"   Histórico:       {len(t.get('history') or [])} evento(s) registrado(s)")
                if args.clarification:
                    print(f"   Esclarecimento:  {args.clarification}")
            elif args.task_action == 'arbitrate':
                t = tasks.prepare_arbitration_package(
                    workspace=ws,
                    task_id=args.task_id,
                    problem=args.problem,
                    alternatives=args.alternatives,
                    evidences=args.evidences,
                    constraints=args.constraints,
                    criteria=args.criteria
                )
                pkg = t['arbitration']['packages'][-1]
                rounds_done = t['arbitration'].get('rounds_count', 0)
                print(f"✅ Pacote de arbitragem preparado com sucesso para {t['id']}:")
                print(f"   Rodada Alvo:              {pkg['round']} de 3 (executadas: {rounds_done})")
                print(f"   Status da Tarefa:         {t['status']}")
                print(f"   Alternativas ({len(pkg['alternatives'])}):        {', '.join(pkg['alternatives'])}")
                print(f"   Tokens Estimados:         ~{pkg['estimated_tokens']} (heurística)")
                print(f"   Autorização Obrigatória:  {'Sim' if pkg['requires_authorization'] else 'Não'}")
                print("   Nota: Subagente árbitro NÃO disparado automaticamente nesta etapa.")
            elif args.task_action == 'handoff':
                t = tasks.handoff_task(
                    workspace=ws,
                    task_id=args.task_id,
                    target_client=args.target_client,
                    reason=args.reason,
                    authorized=args.authorized,
                )
                print(f"✅ Handoff da tarefa {t['id']} realizado com sucesso:")
                print(f"   Origem:                   {t['routing'].get('source_client')}")
                print(f"   Destino:                  {t['routing']['client']}")
                print(f"   Status Atual:             {t['status']}")
                print(f"   Modo de Execução:         {t['routing']['execution_mode']}")
                print(f"   Especialista:             {t['routing'].get('target_specialist') or 'nenhum'}")
                print(f"   Justificativa:            {t['routing'].get('delegation_reason')}")
                print(f"   Histórico:                {len(t.get('history') or [])} evento(s) registrado(s)")
        return 0
    except (OSError, ValueError, RuntimeError, subprocess.TimeoutExpired) as exc:
        print(f'⚠️ {exc}', file=sys.stderr)
        return 1


if __name__ == '__main__':
    raise SystemExit(main())
