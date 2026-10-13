# Adicionar skills

Passo a passo para incluir **uma skill** ou **um lote** de skills no padrão. Tudo que depende delas (validação, roteadores, catálogo, hub e subagentes) é regenerado pelo mesmo comando.

Regras de formato: [PADRAO_DE_SKILLS.md](PADRAO_DE_SKILLS.md). Este guia diz **como** aplicá-las.

## 1. Escolha o domínio

O domínio decide para qual subagente a skill vai e em qual categoria do catálogo ela aparece.

```bash
python scripts/nova_skill.py dominios
```

| Domínio | Subagente | Categoria base no catálogo |
| :--- | :--- | :--- |
| `routing-and-proxy` | `lay-omniroute` | `operacoes` |
| `frontend` | `lay-frontend` | `design` |
| `engineering` | `lay-engenharia` | `engenharia` |
| `context` | `lay-contexto` | `contexto` |
| `devops` | `lay-devops` | `operacoes` |
| `qa` | `lay-qa` | `testes` |
| `security` | `lay-seguranca` | `seguranca` |
| `creative-3d` | `lay-3d` | `design` |
| `documentation` | `lay-documentacao` | `documentacao` |
| `design` | `lay-design` | `design` |
| `database` | `lay-banco-de-dados` | `operacoes` |

A categoria base vem do domínio. Palavras-chave no nome da skill (ex.: `test`, `deploy`, `audit`) podem acrescentar outras categorias: veja `CATEGORIES` em `scripts/skill_hub.py`.

Não há skill "solta": se nenhum domínio serve, veja [Criar um domínio novo](#criar-um-dominio-novo).

## 2. Escreva a skill

Formato mínimo do `SKILL.md`:

```markdown
---
name: auditing-form-accessibility
description: >
  Audits form fields for labels, error messages and keyboard flow. Use this skill when: reviewing a form before release or after a redesign. Do NOT use this skill when: styling a form without changing its behavior.
---

# Auditando acessibilidade de formulários

## Imperative Execution Workflow
1. [FRÁGIL] Liste os campos e confirme o rótulo de cada um.
2. [FLEXÍVEL] Teste a navegação só com teclado.
```

Regras que o validador confere:

- **`name`**: minúsculas, números e hífens, máx. 64 caracteres, igual ao nome da pasta, com um segmento em gerúndio (`auditing-…`, `creating-…`, `engineering-…`).
- **`description`**: 3ª pessoa, máx. 1024 caracteres, com `Use this skill when:` e `Do NOT use this skill when:`.
- **Uma competência por skill.** Ação dupla (ex.: "testar e publicar") vira duas skills.
- **Sem marcador `[PREENCHER: …]`.** É o marcador de rascunho e bloqueia a inclusão.
- Corpo com mais de 100 linhas de código ou template: mova para `reference.md`, que começa com `## Table of Contents`, e aponte para ele no `SKILL.md`.
- Skills que executam ações: incluem `## Input/Output Signature` e `## On Failure` (PADRAO, seção 8). Skills de orientação mantêm só o conteúdo real.

Modelo para copiar: [templates/SKILL.template.md](../templates/SKILL.template.md).

## 3. Adicione uma skill

Com o corpo pronto num arquivo `.md`:

```bash
python scripts/nova_skill.py nova auditing-form-accessibility --dominio qa --descricao "Audits form fields for labels, error messages and keyboard flow. Use this skill when: reviewing a form before release. Do NOT use this skill when: styling a form without changing its behavior." --corpo caminho/corpo.md
```

Sem `--corpo`, o comando cria um rascunho com marcadores `[PREENCHER: …]`, que **não passa** na validação. O arquivo `--corpo` pode ser só o corpo ou o `SKILL.md` completo.

## 4. Adicione um lote

Monte uma pasta que espelha o repositório:

```text
meu-lote/
└── qa/
    ├── auditing-form-accessibility/
    │   ├── SKILL.md
    │   └── reference.md        (opcional)
    └── testing-keyboard-flows/
        └── SKILL.md
```

```bash
python scripts/nova_skill.py lote meu-lote
```

O lote é **tudo ou nada**: se uma skill falhar, nenhuma é gravada, e o relatório lista todos os erros de uma vez. Skill que já existe no repositório é recusada: edite-a à mão.

## 5. O que o comando faz

1. Grava a skill (e o `reference.md`, se houver) no domínio.
2. Acrescenta a linha nas tabelas de roteamento do domínio: `SKILL.md` (roteador) e `reference.md`. Se a linha já existir, não duplica.
3. Valida a árvore inteira com `scripts/validate_skills.py`. Se houver erro, desfaz tudo.
4. Regenera: `docs/CATALOGO.md` e `catalog/skills.json`, o hub (`hub/data.js`, `hub/conteudo.js`, `hub/agentes.js` e `hub/totais.js`) e os subagentes (`.claude/agents/`, `agents/`).
5. Mostra o subagente que recebe a skill.

Para só validar e gravar, sem regenerar: adicione `--sem-regerar`. Para regenerar depois, sem adicionar nada:

```bash
python scripts/nova_skill.py regenerar
```

## 6. Instale nos agentes

O repositório fica pronto no passo anterior. Para os agentes locais usarem a skill:

```bash
python scripts/skill_hub.py install --agents all
python scripts/skill_hub.py doctor
```

Os subagentes globais (`~/.claude/agents/`) são atualizados pela mesma instalação.

## 7. Skill privada

Skills da identidade LAY ficam no cofre local `skills-privadas-lay/` (ignorado pelo Git). Use `--privada`, ou `lote --privada`:

```bash
python scripts/nova_skill.py nova governing-brand-voice --dominio design --descricao "…" --corpo corpo.md --privada
```

A validação do cofre é separada e não entra no catálogo público, no dashboard nem nos subagentes do repositório. Para instalar localmente, rode `install --agents all`.

## 8. Commit

Depois de adicionar, o repositório mostra as mudanças. Um commit por área, no padrão de [`authoring-conventional-commits`](../refactored_skills/devops/authoring-conventional-commits/SKILL.md), por exemplo:

```text
feat(qa): adicionar auditoria de acessibilidade de formulários
chore(catalogo): regenerar catálogo, hub e subagentes
```

Antes de publicar, rode os testes: `python -m unittest discover -s tests -p "test_*.py"`.

## Criar um domínio novo

Não é automático, porque um domínio mexe em subagente, categoria e validador. Passos:

1. Crie `refactored_skills/<dominio>/SKILL.md` (roteador `routing-<dominio>-skills`, com `Use this skill when:` e `Do NOT use this skill when:`) e `reference.md` com `## Table of Contents`.
2. Adicione o domínio em `agents/perfis.json` (nome do subagente, descrição com gatilhos, ferramentas).
3. Adicione o domínio em `DOMAIN_CATEGORY` (`scripts/skill_hub.py`) e em `DOMINIOS_PUBLICOS` (`scripts/validate_skills.py`).
4. Rode `python scripts/nova_skill.py regenerar`, depois as skills do domínio com `nova` ou `lote`.
5. Rode os testes.
