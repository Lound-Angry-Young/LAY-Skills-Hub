---
name: driving-test-driven-development
description: >
  Drives development with tests in a red-green-refactor loop when implementing logic, fixing a bug or changing behavior, to prove that the code works. Use this skill when: implementing any logic, fixing any bug or changing existing behavior. Do NOT use this skill when: the work is a browser-level check of a running page (use testing-in-browser-with-devtools) or a codebase quality scan (use scanning-codebase-quality).
---

# Desenvolvimento Guiado por Testes (TDD)

Conduz o desenvolvimento de software através do ciclo rigoroso Red-Green-Refactor: escreve um teste que falha antes de codificar (Vermelho), implementa o código estritamente necessário para passar (Verde) e refatora para clareza e simplicidade.

## Input/Output Signature
Input:
- behaviorToImplementOrFix: string # Descrição do comportamento, regra de negócio ou bug a ser tratado
- targetModuleFilePath: string # Caminho do arquivo de código que receberá a implementação
- testSuiteFilePath: string # Caminho do arquivo de testes correspondente
Output:
- tddCycleCompleted: boolean # Confirmação de que o ciclo Red-Green-Refactor foi concluído
- failingTestEvidence: string # Saída do executor de testes comprovando a falha inicial (Red)
- passingTestEvidence: string # Saída comprovando a aprovação após o código (Green)
- appliedRefactoringNotes: string # Resumo das simplificações feitas no passo de refatoração

## Router and Selection Matrix
| Etapa do Ciclo | Ação Obrigatória | Grau de Liberdade |
|---|---|---|
| Passo 1: Vermelho (Red) | Escreve teste unitário mínimo cobrindo o novo comportamento e roda esperando falha | [FRÁGIL] Proibido escrever código de produção antes de ver o teste falhar |
| Passo 2: Verde (Green) | Escreve o código mais simples e direto possível para fazer o teste passar | [FLEXÍVEL] Foco exclusivo em satisfazer a asserção sem especular abstrações |
| Passo 3: Refatorar (Refactor) | Limpa duplicações, renomeia variáveis e simplifica a lógica mantendo os testes verdes | [FLEXÍVEL] Mantém os testes executando a cada pequena alteração |
| Correção de Bug Existente | Reproduz o defeito com um teste específico que falha antes de qualquer fix | [FRÁGIL] O teste serve como prova cabal da regressão e de sua solução |

## Imperative Execution Workflow
1. Descobrir a Stack e Executor de Testes do Projeto [FRÁGIL]:
   - Identifique o framework de testes configurado no repositório (`vitest`, `jest`, `pytest`, `cargo test`).
2. Redigir Teste Unitário Mínimo e Focado [FRÁGIL]:
   - Escreva exatamente uma asserção clara que descreve o comportamento pretendido em `testSuiteFilePath`.
3. Executar o Teste e Confirmar a Falha Inicial (Red) [FRÁGIL]:
   - Dispare o comando de teste e confirme que ele falha pelo motivo correto (ex: método não implementado).
4. Implementar a Menor Solução Suficiente (Green) [FLEXÍVEL]:
   - Escreva a lógica estritamente necessária para satisfazer o teste e rode novamente até ver a barra verde.
5. Refatorar Código e Testes com Segurança (Refactor) [FLEXÍVEL]:
   - Remova duplicações e melhore a clareza sem alterar o comportamento externo, validando que a suíte segue verde.

## Execution Checklist
- [ ] Identificar o executor e a convenção de testes do projeto
- [ ] Escrever teste automatizado para o novo comportamento
- [ ] Executar o teste e registrar a evidência da falha esperada (Red)
- [ ] Implementar código mínimo necessário para obter aprovação (Green)
- [ ] Refatorar código e testes garantindo que continuam passando

## On Failure
- **Gatilho de Erro**: O teste passa antes de escrever o código (teste falso/tautológico), falha por motivo errado ou código quebra outros testes.
- **Ação Imediata**: Parar e reescrever a asserção do teste para capturar a intenção real.
- **Rollback**: Reverter implementações prematuras que não foram precedidas por um teste com falha comprovada.
- **Fallback**: Isolar a unidade em teste zombando dependências externas complexas para garantir determinismo.
- **Logs**: Registrar mensagem de falha inicial, diff de código implementado e tempo de execução dos testes.

## Reference Documentation
Consulte a documentação técnica completa: [Referência Técnica](reference.md).
