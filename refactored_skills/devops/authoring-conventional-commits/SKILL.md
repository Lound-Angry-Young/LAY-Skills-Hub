---
name: authoring-conventional-commits
description: >
  Structures atomic semantic commits following the Conventional Commits convention: writes commit messages, prepares commits, installs commit-msg validation hooks and audits commit history. Use this skill when: structuring commit messages, preparing semantic commits in git, installing commit-msg validation hooks or auditing history. Do NOT use this skill when: resolving complex rebase conflicts (use managing-git-branch-workflows) or managing release tags and changelogs (use tagging-semantic-releases).
---

## Input/Output Signature
Input:
- changeType: string # Tipo semântico (feat, fix, docs, style, refactor, perf, test, build, ci, chore, raw, cleanup, remove)
- scope: string # Escopo opcional entre parênteses representando o módulo afetado (ex: auth, api, ui)
- description: string # Descrição concisa no imperativo afirmativo (máx 72 caracteres, minúsculas, sem ponto final)
- body: string # Contexto detalhado explicando o motivo da mudança e impacto (opcional)
- breakingChange: boolean # Se a alteração introduz quebra de compatibilidade retrógrada (default: false)
- stageFiles: array # Lista de caminhos de arquivos a serem adicionados ao stage (opcional)
Output:
- commitMessage: string # Mensagem de commit formatada conforme a convenção
- gitCommand: string # Comando git pronto para execução no terminal
- isValid: boolean # Status da validação sintática da mensagem
- executionStatus: string # Resultado da operação (validated, committed, rejected)

## Router and Selection Matrix
| Tipo / Cenário | Regra Semântica | Grau de Liberdade |
|---|---|---|
| Nova funcionalidade (`feat`) | Adiciona recurso ao produto (vinculado a MINOR em SemVer) | [FRÁGIL] Exige descrição clara de capacidade |
| Correção de erro (`fix`) | Corrige bug ou regressão (vinculado a PATCH em SemVer) | [FRÁGIL] Deve referenciar sintoma corrigido |
| Refatoração pura (`refactor`) | Altera código sem mudar comportamento externo nem corrigir bug | [FLEXÍVEL] Aplica melhoria de legibilidade/estrutura |
| Performance (`perf`) | Otimização estrita de tempo de resposta, memória ou bundle | [FRÁGIL] Requer justificativa de ganho mensurável |
| Documentação (`docs`) | Alterações exclusivas em README, guias ou comentários | [FLEXÍVEL] Sem impacto em código executável |
| Testes (`test`) | Adição, correção ou remoção de suítes de teste | [FLEXÍVEL] Sem impacto no código de produção |
| Limpeza / Remoção (`cleanup` / `remove`) | Elimina código morto, arquivos obsoletos ou comentários | [FRÁGIL] Exige confirmação de ausência de dependentes |
| Mudança Quebrante (`!`) | Qualquer tipo com `!` ou rodapé `BREAKING CHANGE:` (MAJOR) | [FRÁGIL] Requer justificativa explícita de quebra |

## Imperative Execution Workflow
1. Inspecionar Staging e Diff [FRÁGIL]:
   - Execute `git status -s` e `git diff --cached --stat` para examinar os arquivos prontos para commit.
   - Garanta que a alteração seja atômica (apenas uma intenção por commit).
2. Determinar Tipo Semântico e Escopo [FLEXÍVEL]:
   - Selecione o tipo correspondente na matriz (`feat`, `fix`, `docs`, `refactor`, etc.).
   - Se aplicável, identifique o escopo do subsistema (ex: `(auth)`, `(ui)`, `(router)`).
3. Redigir Mensagem Canônica [FRÁGIL]:
   - Monte a primeira linha no formato: `<tipo>(<escopo>): <descrição no imperativo e minúsculas>`.
   - Caso haja quebra de compatibilidade, adicione `!` antes dos dois-pontos: `<tipo>(<escopo>)!: <descrição>`.
   - Se necessário, pule uma linha e adicione o corpo explicativo detalhando a motivação.
4. Validar Sintaxe contra Regex Oficial [FRÁGIL]:
   - Teste a mensagem contra a regex: `^(feat|fix|docs|style|refactor|test|chore|build|ci|perf|raw|cleanup|remove|revert)(\([a-zA-Z0-9_.-]+\))?(!)?:\s.+$`.
   - Se reprovada, ajuste a mensagem imediatamente antes de disparar o Git.
5. Executar o Commit [FRÁGIL]:
   - Dispare o comando git formatado:
     ```bash
     git commit -m "<mensagem_formatada>"
     ```
   - Confirme a criação do commit com `git log -1 --oneline`.

## Execution Checklist
- [ ] Verificar atomicidade do stage (`git status -s`)
- [ ] Identificar o tipo semântico apropriado na convenção
- [ ] Definir escopo opcional representativo
- [ ] Redigir descrição no imperativo, em minúsculas e sem ponto final
- [ ] Validar conformidade com a regex estrita de commits semânticos
- [ ] Executar `git commit` e confirmar hash gerado no histórico

## On Failure
- **Gatilho de Erro**: Mensagem reprovada pelo hook `commit-msg`, regex inválida, stage vazio ou erro no comando Git.
- **Ação Imediata**: Abortar o commit sem alterar o índice (`index`) ou working tree do Git.
- **Rollback**: Nenhuma alteração é perdida em caso de aborto antes do commit. Caso o commit tenha sido criado com mensagem incorreta, use imediatamente:
  ```bash
  git commit --amend -m "<mensagem_corrigida>"
  ```
- **Fallback**: Exibir a mensagem rejeitada junto com a lista de tipos válidos da convenção e solicitar revisão do texto.
- **Logs**: Registrar a mensagem rejeitada e a causa da reprovação (excesso de caracteres, tipo desconhecido, formato quebrado).

## Reference Documentation
Consulte a tabela completa de emojis, convenções SemVer e o script de instalação do hook `commit-msg`: [Referência Técnica de Padrões de Commit](reference.md).
