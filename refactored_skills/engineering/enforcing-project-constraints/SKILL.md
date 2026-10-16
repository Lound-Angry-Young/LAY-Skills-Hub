---
name: enforcing-project-constraints
description: >
  Records the project's quality bar as a written contract in CONSTRAINTS.md and watches the diff for a weakened bar: new suppressions, skipped or deleted tests, stripped assertions, unimplemented stubs or lowered thresholds. Use this skill when: defining quality thresholds for a project or checking that agents are not quietly lowering the bar. Do NOT use this skill when: auditing the whole codebase for bugs (use auditing-codebase-bloat).
---

# Aplicação de Restrições de Qualidade de Projeto

Mantém o padrão de qualidade do projeto através do contrato escrito `CONSTRAINTS.md`, inspecionando diffs para impedir que agentes rebaixem a barra: supressões de linter, testes ignorados, asserções vazias ou stubs.

## Input/Output Signature
Input:
- constraintsFilePath: string # Caminho do arquivo de contrato de restrições (ex: CONSTRAINTS.md)
- gitDiffTarget: string # Diff ou branch a ser inspecionada contra o padrão de qualidade
- strictZeroTolerance: boolean # Se deve reprovar imediatamente diante de qualquer supressão nova (default: true)
Output:
- constraintsSatisfied: boolean # Status da validação de restrições
- detectedViolations: array # Lista detalhada de violações encontradas com arquivo e número de linha
- weakenedBarSummary: string # Diagnóstico dos pontos onde o padrão tentou ser rebaixado
- executionLog: string # Registro da auditoria do diff

## Router and Selection Matrix
| Tipo de Violação Detectada | Ação Recomendada | Grau de Liberdade |
|---|---|---|
| Supressão de Linter (`eslint-disable`, `@ts-ignore`) | Rejeita o diff e exige resolução estrutural da causa do erro | [FRÁGIL] Tolerância zero para novas supressões em código novo |
| Testes Ignorados (`skip`, `xit`, `test.todo`) | Bloqueia integração e exige execução real ou exclusão consciente | [FRÁGIL] Proibido desativar testes existentes para aprovar build |
| Asserções Esvaziadas / Mocks Cegos | Reprova a alteração e exige validação de valor ou exceção concreta | [FRÁGIL] Rejeita testes tautológicos que sempre passam |
| Criação de CONSTRAINTS.md Inicial | Extrai limites atuais de cobertura, linters e regras em contrato | [FLEXÍVEL] Estabelece a linha de base para auditorias futuras |

## Imperative Execution Workflow
1. Carregar Regras e Contratos de CONSTRAINTS.md [FRÁGIL]:
   - Leia o contrato de qualidade do projeto para identificar limites mínimos e proibições explícitas.
2. Inspecionar Diff Git contra a Base [FRÁGIL]:
   - Execute varredura no diff identificando linhas adicionadas contendo palavras-chave de supressão ou ignorância de testes.
3. Checar Integridade da Suíte de Testes [FRÁGIL]:
   - Verifique se a quantidade de testes aumentou ou permaneceu estável; qualquer queda no número total gera alerta bloqueante.
4. Auditar Tipos Any e Casts Forçados [FLEXÍVEL]:
   - Detecte introdução de tipos `any`, `as unknown as X` ou escape hatches que minem a segurança de tipos.
5. Emitir Parecer de Conformidade ou Bloqueio [FRÁGIL]:
   - Aprove o diff somente se nenhuma restrição foi violada; caso contrário, aponte a linha exata e a regra violada.

## Execution Checklist
- [ ] Ler o contrato CONSTRAINTS.md e identificar parâmetros de qualidade
- [ ] Inspecionar o diff em busca de flags de supressão de linter ou compilador
- [ ] Confirmar que nenhum teste existente foi ignorado ou teve asserções removidas
- [ ] Validar que novos módulos contam com tipagem estrita sem tipos any
- [ ] Emitir relatório com aprovação estrita ou lista de violações

## On Failure
- **Gatilho de Erro**: Introdução de nova supressão de linter, teste pulado via `skip`, remoção de asserções ou diminuição de cobertura.
- **Ação Imediata**: Bloquear a aceitação do diff imediatamente e apontar a regressão de qualidade.
- **Rollback**: Não há mutação permanente; o commit ou pull request permanece rejeitado.
- **Fallback**: Solicitar a correção da causa-raiz do aviso do linter ou reativação com correção do teste.
- **Logs**: Registrar linha, arquivo e trecho exato de código onde a violação de restrição foi detectada.

## Reference Documentation
Consulte a documentação técnica completa: [Referência Técnica](reference.md).
