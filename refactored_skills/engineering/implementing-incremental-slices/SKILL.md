---
name: implementing-incremental-slices
description: >
  Delivers changes incrementally in thin, verifiable slices, rolling out behind feature flags and breaking large tasks into steps that each land on their own. Use this skill when: implementing a change that touches more than one file, picking up the next task from a plan, or when a task feels too big to land in one step. Do NOT use this skill when: the specification is still missing (use authoring-specifications-first).
---

# Implementação em Fatias Incrementais (Vertical Slicing)

Entrega alterações de software em fatias verticais finas e ponta a ponta: cada incremento é funcional, isolado por feature flags, possui suíte de testes própria e pode ser integrado à branch principal com segurança.

## Input/Output Signature
Input:
- taskDefinitionFromPlan: object # Definição da tarefa atômica extraída do plano geral
- targetFilesBoundary: array # Arquivos e componentes afetados por esta fatia de implementação
- featureFlagKey: string # Chave opcional de feature flag para isolar a funcionalidade em produção
Output:
- sliceImplementationStatus: string # Estado da fatia (implemented, tested, validated, ready_for_commit)
- modifiedFilesList: array # Relação de arquivos criados ou modificados no incremento
- passingTestsSummary: object # Resultado dos testes unitários e de integração da fatia
- executionLog: string # Registro dos comandos e validações executadas

## Router and Selection Matrix
| Escopo da Fatia | Estratégia de Fatiamento | Grau de Liberdade |
|---|---|---|
| Fatia Vertical Completa (DB + API + UI) | Implementa o caminho feliz mínimo ponta a ponta com cobertura de testes | [FRÁGIL] Exige validação de tipos e integração entre camadas |
| Alteração Multi-Arquivos Ampla | Decompõe a alteração em passos unitários de no máximo 2 a 3 arquivos por vez | [FLEXÍVEL] Mantém cada sub-etapa compilável e verde |
| Funcionalidade Oculta em Produção | Envolve pontos de entrada em feature flag desativada por padrão | [FRÁGIL] Garante ausência de impacto no comportamento de usuários existentes |
| Próxima Tarefa do Plano | Lê requisitos em TASKS.md e avança um item de cada vez sem saltar etapas | [FRÁGIL] Respeita estritamente a ordem topológica do plano |

## Imperative Execution Workflow
1. Isolar Escopo Estrito da Próxima Fatia [FRÁGIL]:
   - Selecione exatamente uma tarefa do plano e delimite os arquivos necessários para sua conclusão.
2. Proteger com Feature Flag ou Isolamento de Rota [FLEXÍVEL]:
   - Garanta que código novo incompleto não seja exposto diretamente no fluxo principal de produção.
3. Implementar a Menor Lógica Funcional [FLEXÍVEL]:
   - Escreva o código estritamente necessário para atender aos critérios de aceitação da fatia atual.
4. Escrever e Rodar Testes Automatizados da Fatia [FRÁGIL]:
   - Crie testes unitários ou de integração que validem o comportamento introduzido e mantenha-os verdes.
5. Validar Compilação e Linters Locais [FRÁGIL]:
   - Execute a checagem de tipos e lint confirmando que a base compila sem nenhum erro residual.

## Execution Checklist
- [ ] Selecionar a próxima tarefa atômica do plano de execução
- [ ] Isolar funcionalidade atrás de feature flag se for parcial
- [ ] Implementar a fatia vertical mínima funcional
- [ ] Adicionar testes automatizados cobrindo a nova lógica
- [ ] Confirmar que tipos, linters e testes passam com sucesso

## On Failure
- **Gatilho de Erro**: Fatia quebrada em tempo de compilação, testes falhando ou escopo vazando para outros módulos.
- **Ação Imediata**: Parar a expansão da fatia e concentrar a atenção exclusivamente no ponto com erro.
- **Rollback**: Reverter arquivos modificados para o início da fatia caso a abordagem tenha se mostrado inviável.
- **Fallback**: Quebrar a fatia atual em duas etapas ainda menores (ex: contrato primeiro, persistência depois).
- **Logs**: Registrar arquivos alterados, falha de asserção observada e dependências pendentes.

## Reference Documentation
Consulte a documentação técnica completa: [Referência Técnica](reference.md).
