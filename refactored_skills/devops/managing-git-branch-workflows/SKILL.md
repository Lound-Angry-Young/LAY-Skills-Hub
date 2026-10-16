---
name: managing-git-branch-workflows
description: >
  Manages Git workflows: atomic branches, interactive rebase, splitting tangled commits and rigorous conflict resolution. Use this skill when: organizing task branches, rebasing, splitting messy commits or resolving conflicts. Do NOT use this skill when: only writing commit messages (use authoring-conventional-commits) or cutting a release tag (use tagging-semantic-releases).
---

# Gerenciamento de Branches e Fluxos de Trabalho Git

Gerencia ciclos de trabalho com Git: criação de branches atômicas, rebase interativo contra a branch principal, divisão de commits emaranhados e resolução sistemática de conflitos sem perda de histórico.

## Input/Output Signature
Input:
- operationType: string # Tipo de operação (create_branch, rebase_interactive, resolve_conflict, split_commit)
- branchName: string # Nome da branch de trabalho (ex: feat/auth-tokens, fix/query-timeout)
- baseBranch: string # Branch base de comparação e rebase (default: main)
- targetCommitHash: string # Hash de commit específico quando operando em histórico
Output:
- operationSuccess: boolean # Status da operação Git
- currentBranch: string # Nome da branch ativa após a conclusão
- rebasedCommitsCount: number # Quantidade de commits reorganizados no histórico
- executionLog: string # Histórico dos comandos Git executados

## Router and Selection Matrix
| Operação / Cenário | Ação Recomendada | Grau de Liberdade |
|---|---|---|
| Nova Funcionalidade / Correção | Cria branch atômica padronizada a partir da base atualizada | [FRÁGIL] Exige prefixos convencionais (`feat/`, `fix/`, `chore/`) |
| Atualização contra a Base | Executa `git fetch` seguido de `git rebase baseBranch` | [FRÁGIL] Mantém histórico linear sem commits de merge supérfluos |
| Conflitos de Rebase | Analisa conflitos arquivo a arquivo, resolve e roda `git rebase --continue` | [FRÁGIL] Proibido usar force push sem conferência prévia |
| Limpeza de Commits de Rascunho | Rebase interativo para condensar (`squash`) e reescrever mensagens | [FLEXÍVEL] Organiza o trabalho em unidades semânticas atômicas |

## Imperative Execution Workflow
1. Inspecionar Estado da Working Tree e Staging [FRÁGIL]:
   - Execute `git status -s` e garanta que não existem arquivos não commitados antes de manipular branches.
2. Atualizar Referências Remotas da Base [FRÁGIL]:
   - Dispare `git fetch origin <baseBranch>` garantindo que a base de comparação esteja sincronizada.
3. Criar ou Alternar para a Branch de Trabalho [FLEXÍVEL]:
   - Crie a branch temática no formato canônico (`git checkout -b <branchName> origin/<baseBranch>`).
4. Reorganizar Histórico via Rebase Linear [FRÁGIL]:
   - Quando for integrar alterações recentes da base, execute `git rebase origin/<baseBranch>` preservando a ordem dos commits.
5. Resolver Conflitos com Validação Estrita [FRÁGIL]:
   - Inspecione blocos conflitantes, preserve o comportamento pretendido, execute testes locais e confirme com `git rebase --continue`.

## Execution Checklist
- [ ] Confirmar que o diretório de trabalho está limpo antes de iniciar
- [ ] Atualizar branch base a partir do repositório remoto
- [ ] Utilizar convenção semântica padronizada no nome da branch
- [ ] Manter histórico linear através de rebase limpo
- [ ] Validar que todos os testes e builds passam após resolução de conflitos

## On Failure
- **Gatilho de Erro**: Conflito insolúvel em rebase, tentativa de rebase em branch suja ou perda acidental de referências.
- **Ação Imediata**: Pausar a operação e avaliar o estado do processo Git.
- **Rollback**: Se o rebase estiver em estado inconsistente, execute imediatamente:
  ```bash
  git rebase --abort
  ```
- **Fallback**: Usar o `git reflog` para resgatar o ponteiro de commit original antes da tentativa.
- **Logs**: Registrar lista de arquivos em conflito e hash do commit onde ocorreu a interrupção.

## Reference Documentation
Consulte a documentação técnica completa: [Referência Técnica](reference.md).
