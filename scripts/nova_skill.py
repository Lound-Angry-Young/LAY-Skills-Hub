#!/usr/bin/env python3
"""Adiciona skills no padrão de docs/PADRAO_DE_SKILLS.md e regenera o que depende delas.

Uso:
  python scripts/nova_skill.py dominios
  python scripts/nova_skill.py nova <nome> --dominio <dominio> --descricao "<texto>" [--corpo <arquivo.md>] [--privada] [--sem-regerar]
  python scripts/nova_skill.py lote <pasta> [--privada] [--sem-regerar]
  python scripts/nova_skill.py regenerar

<pasta> do lote espelha o repositório: <pasta>/<dominio>/<nome>/SKILL.md (e reference.md, se houver).
Tudo ou nada: nada é gravado se a árvore inteira deixar de validar.
--privada grava no cofre local (skills-privadas-lay/, fora do Git).
Guia completo: docs/ADICIONAR_SKILLS.md
"""
import argparse
import re
import shutil
import subprocess
import sys
import textwrap
from pathlib import Path

import yaml

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO))

from scripts.skill_hub import build_catalog, load_profiles  # noqa: E402
from scripts.validate_skills import Validador  # noqa: E402

PUBLICO = REPO / 'refactored_skills'
COFRE = REPO / 'skills-privadas-lay' / 'refactored'
NOME_VALIDO = re.compile(r'[a-z0-9]+(-[a-z0-9]+)*')
GATILHOS = ('Use this skill when:', 'Do NOT use this skill when:')


def dominios_validos(raiz):
    """Domínios com roteador (SKILL.md na raiz da pasta): só eles recebem skills."""
    if not raiz.is_dir():
        return []
    return sorted(d.name for d in raiz.iterdir() if d.is_dir() and (d / 'SKILL.md').exists())


def subagente_do(dominio):
    for perfil in load_profiles(REPO):
        if perfil['dominio'] == dominio:
            return perfil['nome']
    return None


def erros_de_nome(nome):
    if len(nome) > 64 or not NOME_VALIDO.fullmatch(nome):
        return [f'nome {nome!r}: use minúsculas, números e hífens (máx. 64), sem hífen no início ou no fim']
    if not re.search(r'(^|-)[a-z]+ing(-|$)', nome):
        return [f'nome {nome!r}: falta um segmento em gerúndio, ex.: auditing-code-security']
    return []


def erros_de_descricao(descricao):
    limpa = ' '.join(descricao.split())
    erros = [f'descrição com {len(limpa)} caracteres (máx. 1024)'] if len(limpa) > 1024 else []
    erros += [f'descrição sem "{g}"' for g in GATILHOS if g not in limpa]
    return erros


def montar_skill_md(nome, descricao, corpo):
    """SKILL.md com frontmatter no formato do repositório (description em bloco dobrado)."""
    linhas = textwrap.wrap(' '.join(descricao.split()), width=96)
    cabecalho = ['---', f'name: {nome}', 'description: >'] + [f'  {linha}' for linha in linhas] + ['---', '']
    return '\n'.join(cabecalho) + '\n' + corpo.strip() + '\n'


def corpo_rascunho(nome):
    """Esqueleto com marcadores [PREENCHER: …]. O validador recusa a skill até todos serem preenchidos."""
    return '\n'.join([
        f'# {nome}',
        '',
        '[PREENCHER: uma frase sobre o que a skill faz e para quem]',
        '',
        '## Imperative Execution Workflow',
        '1. [PREENCHER: primeiro passo, imperativo e verificável]',
        '2. [PREENCHER: segundo passo]',
        '',
        '## On Failure',
        '- **Gatilho de Erro**: [PREENCHER: condição que dispara a falha]',
        '- **Ação Imediata**: [PREENCHER: o que interromper]',
        '- **Rollback**: [PREENCHER: como reverter]',
        '- **Fallback**: [PREENCHER: rota alternativa]',
        '- **Logs**: [PREENCHER: o que registrar]',
        '',
    ])


def proposito(descricao):
    """Texto da coluna de finalidade: a descrição antes dos gatilhos."""
    antes = ' '.join(descricao.split()).split('Use this skill when:')[0]
    return antes.strip().rstrip('.').replace('|', '\\|')


def atualizar_roteadores(raiz, dominio, nome, descricao, avisos):
    """Acrescenta a skill às tabelas de roteamento do domínio (SKILL.md e reference.md). Preserva a quebra de linha."""
    alterados = []
    for arquivo in ('SKILL.md', 'reference.md'):
        caminho = raiz / dominio / arquivo
        if not caminho.exists():
            continue
        bruto = caminho.read_bytes().decode('utf-8')
        eol = '\r\n' if '\r\n' in bruto else '\n'
        linhas = bruto.replace('\r\n', '\n').split('\n')
        if any(f'](./{nome}/SKILL.md)' in linha for linha in linhas):
            continue
        posicoes = [i for i, linha in enumerate(linhas) if re.match(r'^\|.*\]\(\./[^)]+/SKILL\.md\)', linha)]
        if not posicoes:
            avisos.append(f'{dominio}/{arquivo}: sem tabela de roteamento; acrescente {nome} à mão')
            continue
        if arquivo == 'SKILL.md':
            destino = f'`./{nome}/SKILL.md`'
        else:
            destino = f'`[./{nome}/SKILL.md](./{nome}/SKILL.md)`'
        linhas.insert(posicoes[-1] + 1, f'| [{nome}](./{nome}/SKILL.md) | {proposito(descricao)} | {destino} |')
        caminho.write_bytes(eol.join(linhas).encode('utf-8'))
        alterados.append(f'{dominio}/{arquivo}')
    return alterados


def conferir_pacotes(raiz, pacotes):
    erros = []
    for dominio, nome, _, _ in pacotes:
        if dominio not in dominios_validos(raiz):
            erros.append(f'domínio {dominio!r} sem roteador em {raiz.name}/')
        elif (raiz / dominio / nome).exists():
            erros.append(f'{dominio}/{nome} já existe: edite a skill existente em vez de criar outra')
    return erros


def desfazer(criadas, anteriores):
    """Volta ao estado anterior: apaga as pastas criadas e restaura os roteadores como estavam."""
    for pasta in reversed(criadas):
        shutil.rmtree(pasta, ignore_errors=True)
    for caminho, bruto in anteriores.items():
        caminho.write_bytes(bruto)


def aplicar(raiz, pacotes, privado):
    """pacotes: lista de (dominio, nome, texto_do_SKILL_md, pasta_de_extras ou None).

    Grava no próprio `raiz` (os links relativos continuam válidos), valida a árvore inteira
    e, se algo falhar, desfaz tudo. Devolve (erros, avisos, caminhos_alterados_relativos_a_raiz).
    """
    erros = conferir_pacotes(raiz, pacotes)
    avisos, alterados, criadas, anteriores = [], [], [], {}
    if erros:
        return erros, avisos, []
    concluido = False
    try:
        for dominio, nome, texto, extras in pacotes:
            for arquivo in ('SKILL.md', 'reference.md'):
                roteador = raiz / dominio / arquivo
                if roteador.exists() and roteador not in anteriores:
                    anteriores[roteador] = roteador.read_bytes()
            pasta = raiz / dominio / nome
            pasta.mkdir(parents=True)
            criadas.append(pasta)
            (pasta / 'SKILL.md').write_text(texto, encoding='utf-8', newline='\n')
            if extras is not None:
                for origem in extras.iterdir():
                    if origem.name == 'SKILL.md':
                        continue
                    if origem.is_dir():
                        shutil.copytree(origem, pasta / origem.name)
                    else:
                        shutil.copy2(origem, pasta / origem.name)
            alterados.append(f'{dominio}/{nome}')
            alterados += atualizar_roteadores(raiz, dominio, nome, descricao_de(texto), avisos)
        validador = Validador(raiz, privado)
        validador.skills()
        validador.roteadores()
        validador.estrutura()
        erros = validador.erros
        concluido = not erros
    finally:
        if not concluido:
            desfazer(criadas, anteriores)
    return erros, avisos, list(dict.fromkeys(alterados)) if concluido else []


def descricao_de(texto):
    """Descrição do frontmatter (para a linha do roteador); vazia se o frontmatter não existir."""
    frontmatter = re.match(r'---\n(.*?)\n---\n', texto, re.S)
    if not frontmatter:
        return ''
    return str(yaml.safe_load(frontmatter.group(1)).get('description', ''))


def regenerar():
    """Recalcula o que depende das skills públicas: estatísticas, catálogo, hub e subagentes."""
    validacao = subprocess.run([sys.executable, str(REPO / 'scripts/validate_skills.py'), '--stats'],
                               capture_output=True, text=True, encoding='utf-8')
    if validacao.returncode != 0:
        raise SystemExit('validação falhou; nada regenerado:\n' + validacao.stdout)
    catalogo = build_catalog(REPO)
    from scripts import build_agents
    build_agents.main()  # antes do hub: hub/agentes.js confere os arquivos de .claude/agents/
    from scripts import build_hub
    build_hub.build_data()
    return len(catalogo['skills'])


def pacotes_do_lote(pasta):
    pacotes = []
    for sk in sorted(pasta.glob('*/*/SKILL.md')):
        pacotes.append((sk.parent.parent.name, sk.parent.name, sk.read_text(encoding='utf-8'), sk.parent))
    return pacotes


def mostrar(erros, avisos, alterados):
    for aviso in avisos:
        print(f'⚠️  {aviso}')
    if erros:
        print('❌ nada foi gravado. Corrija:')
        for erro in erros:
            print(f'   - {erro}')
        return False
    for caminho in alterados:
        print(f'   gravado: {caminho}')
    return True


def fechar(privada, pacotes, regerar):
    for dominio, nome, _, _ in pacotes:
        print(f'✅ {nome} → domínio {dominio} → subagente {subagente_do(dominio) or "(sem subagente)"}')
    if privada:
        print('Skill privada: fica no cofre local e entra só na instalação local.')
        print('Instale: python scripts/skill_hub.py install --agents all')
        return
    if regerar:
        total = regenerar()
        print(f'✅ regenerado: catálogo com {total} skills, hub, subagentes e docs/CATALOGO.md')
    print('Instale nos agentes: python scripts/skill_hub.py install --agents all')


def cmd_dominios(_args):
    for raiz, rotulo in ((PUBLICO, 'público'), (COFRE, 'privado')):
        print(f'{rotulo} ({raiz.relative_to(REPO).as_posix()}):')
        for dominio in dominios_validos(raiz):
            quantas = sum(1 for _ in (raiz / dominio).glob('*/SKILL.md'))
            print(f'  {dominio:<20} {quantas:>3} skills  subagente: {subagente_do(dominio) or "—"}')


def cmd_nova(args):
    raiz = COFRE if args.privada else PUBLICO
    if not NOME_VALIDO.fullmatch(args.nome):
        print(f'❌ nome {args.nome!r} inválido para pasta')
        return 1
    if args.dominio not in dominios_validos(raiz):
        print(f'❌ domínio {args.dominio!r} inexistente. Disponíveis: {", ".join(dominios_validos(raiz))}')
        return 1
    if args.corpo:
        conteudo = Path(args.corpo).read_text(encoding='utf-8')
    else:
        conteudo = None
    if conteudo is not None and conteudo.startswith('---'):
        texto = conteudo
    else:
        if not args.descricao:
            print('❌ informe --descricao (ou um --corpo que já seja o SKILL.md completo)')
            return 1
        pre = erros_de_nome(args.nome) + erros_de_descricao(args.descricao)
        if pre:
            print('❌ nada foi gravado. Corrija:')
            for erro in pre:
                print(f'   - {erro}')
            return 1
        corpo = conteudo if conteudo is not None else corpo_rascunho(args.nome)
        texto = montar_skill_md(args.nome, args.descricao, corpo)
    erros, avisos, alterados = aplicar(raiz, [(args.dominio, args.nome, texto, None)], args.privada)
    if not mostrar(erros, avisos, alterados):
        return 1
    fechar(args.privada, [(args.dominio, args.nome, texto, None)], not args.sem_regerar)
    return 0


def cmd_lote(args):
    raiz = COFRE if args.privada else PUBLICO
    pasta = Path(args.pasta).resolve()
    pacotes = pacotes_do_lote(pasta)
    if not pacotes:
        print(f'❌ nenhuma skill em {pasta}/<dominio>/<nome>/SKILL.md')
        return 1
    erros, avisos, alterados = aplicar(raiz, pacotes, args.privada)
    if not mostrar(erros, avisos, alterados):
        return 1
    fechar(args.privada, pacotes, not args.sem_regerar)
    return 0


def cmd_regenerar(_args):
    validador = Validador(PUBLICO, False)
    validador.skills()
    validador.roteadores()
    validador.estrutura()
    if validador.erros:
        print('❌ corrija antes de regenerar:')
        for erro in validador.erros:
            print(f'   - {erro}')
        return 1
    total = regenerar()
    print(f'✅ regenerado: catálogo com {total} skills, hub, subagentes e docs/CATALOGO.md')
    return 0


def main():
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest='comando', required=True)
    sub.add_parser('dominios', help='lista domínios, skills e subagente de cada um')
    nova = sub.add_parser('nova', help='cria uma skill no padrão')
    nova.add_argument('nome')
    nova.add_argument('--dominio', required=True)
    nova.add_argument('--descricao', help='description: 3ª pessoa, com "Use this skill when:" e "Do NOT use this skill when:"')
    nova.add_argument('--corpo', help='arquivo .md com o corpo, ou com o SKILL.md completo')
    nova.add_argument('--privada', action='store_true')
    nova.add_argument('--sem-regerar', action='store_true')
    lote = sub.add_parser('lote', help='adiciona um lote: pasta <dominio>/<nome>/SKILL.md')
    lote.add_argument('pasta')
    lote.add_argument('--privada', action='store_true')
    lote.add_argument('--sem-regerar', action='store_true')
    sub.add_parser('regenerar', help='valida e regenera catálogo, hub e subagentes')
    args = ap.parse_args()
    comandos = {'dominios': cmd_dominios, 'nova': cmd_nova, 'lote': cmd_lote, 'regenerar': cmd_regenerar}
    return comandos[args.comando](args)


if __name__ == '__main__':
    sys.exit(main())
