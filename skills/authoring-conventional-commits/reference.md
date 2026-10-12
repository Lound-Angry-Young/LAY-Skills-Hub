# Referência Técnica: authoring-conventional-commits

> **Origem e Atribuição:** Baseado no guia de **[Padrões de Commits (iuricode/padroes-de-commits)](https://github.com/iuricode/padroes-de-commits)** e na especificação oficial do **[Conventional Commits v1.0.0](https://www.conventionalcommits.org/pt-br)**.

## Table of Contents
1. [Estrutura Canônica da Mensagem](#estrutura-canônica-da-mensagem)
2. [Tabela de Tipos Semânticos e Emojis](#tabela-de-tipos-semânticos-e-emojis)
3. [Regras de Redação da Descrição](#regras-de-redação-da-descrição)
4. [Validador com Git Hook commit-msg](#validador-com-git-hook-commit-msg)
5. [Regex de Validação](#regex-de-validação)

---

## Estrutura Canônica da Mensagem

A mensagem de commit semântico possui os seguintes elementos estruturais:

```text
<tipo>(<escopo opcional>)<! opcional>: <descrição concisa>

[corpo explicativo opcional - motivação da mudança e contraste com comportamento anterior]

[rodapé opcional - BREAKING CHANGE: descrição ou refs de issues #123]
```

### Exemplos:
- `feat(auth): adicionar autenticação via OAuth2 do Google`
- `fix(checkout): corrigir cálculo de frete para região norte`
- `refactor(api)!: reestruturar payload de resposta da rota de usuários`
- `docs: atualizar instruções de deploy no README`

---

## Tabela de Tipos Semânticos e Emojis

| Tipo | Emoji | Finalidade / Significado | Impacto SemVer |
|---|---|---|---|
| `feat` | ✨ / 🦄 | Inclui uma nova funcionalidade no sistema | **MINOR** |
| `fix` | 🐛 | Corrige um erro ou defeito (bug fix) | **PATCH** |
| `docs` | 📚 / 📜 | Alterações exclusivamente na documentação | N/A |
| `style` | 💄 | Formatação de código, semicolons, trailing spaces, indentação (sem alterar lógica) | N/A |
| `refactor` | ♻️ | Refatoração de código que não altera comportamento nem conserta bug | N/A |
| `perf` | ⚡ | Mudança de código focada estritamente em melhoria de desempenho | **PATCH** |
| `test` | 🧪 | Criação, modificação ou exclusão de testes unitários ou de integração | N/A |
| `build` | 📦 | Modificações em scripts de build, empacotamento ou dependências externas | N/A |
| `ci` | 👷 | Alterações em arquivos de configuração de integração contínua (ex: GitHub Actions) | N/A |
| `chore` | 🔧 | Atualização de tarefas rotineiras, configs administrativas ou `.gitignore` | N/A |
| `raw` | 🗃️ | Mudanças relacionadas a dados estáticos, configs puras ou tabelas de parâmetros | N/A |
| `cleanup` | 🧹 | Remoção de código comentado, trechos mortos ou limpeza de legibilidade | N/A |
| `remove` | 🗑️ | Exclusão de arquivos, diretórios ou rotinas obsoletas não utilizadas | N/A |
| `revert` | ⏪ | Reversão de um commit prévio | Conforme commit revertido |

---

## Regras de Redação da Descrição

1. **Tom Imperativo**: Redija no presente do indicativo ("adicionar", "corrigir", "implementar", "remover"), não no gerúndio ou passado ("adicionado", "corrigindo").
2. **Caixa Baixa**: Comece a descrição com letra minúscula após os dois-pontos e espaço.
3. **Sem Ponto Final**: A primeira linha (título) não deve conter ponto final.
4. **Tamanho Limite**: Título com no máximo 50–72 caracteres.
5. **Corpo Explicativo**: Quando a mudança exigir justificativa, pule uma linha em branco e explique *o que* e *por que*, não *como* (o diff já mostra o como).

---

## Validador com Git Hook commit-msg

Script bash para validação automática no `.git/hooks/commit-msg`:

```bash
#!/usr/bin/env bash

# Caminho do arquivo da mensagem de commit fornecido pelo Git
COMMIT_MSG_FILE=$1

# Lê o conteúdo da mensagem de commit
COMMIT_MSG=$(cat "$COMMIT_MSG_FILE")

# Expressão regular de validação estrita
CONVENTIONAL_COMMIT_REGEX='^(feat|fix|docs|style|refactor|test|chore|build|ci|perf|raw|cleanup|remove|revert)(\([a-zA-Z0-9_.-]+\))?(!)?:\s.+$'

if ! [[ $COMMIT_MSG =~ $CONVENTIONAL_COMMIT_REGEX ]]; then
    echo "❌ ERRO: A mensagem de commit não segue o formato Conventional Commits."
    echo
    echo "Formato obrigatório: <tipo>(<escopo>): <descrição>"
    echo
    echo "Tipos aceitos: feat, fix, docs, style, refactor, test, chore, build, ci, perf, raw, cleanup, remove, revert"
    echo "Exemplo: feat(auth): adicionar suporte a login com GitHub"
    exit 1
fi

exit 0
```

### Instalação no Linux / macOS / Git Bash:
```bash
cp commit-msg.sh .git/hooks/commit-msg
chmod +x .git/hooks/commit-msg
```

### Instalação no Windows (PowerShell):
```powershell
Copy-Item -Path "commit-msg.sh" -Destination ".git/hooks/commit-msg"
```

---

## Regex de Validação

Expressão regular padrão para testes em linters e esteiras CI:
```regex
^(feat|fix|docs|style|refactor|test|chore|build|ci|perf|raw|cleanup|remove|revert)(\([a-zA-Z0-9_.-]+\))?(!)?:\s.+$
```
