---
name: breaking-down-task-plans
description: >
  Breaks a spec or clear requirements into ordered, implementable tasks, estimating scope and identifying work that can run in parallel when a task is too large to start. Use this skill when: a spec exists and the work must be split into tasks, a task feels too large to start or parallel work is possible. Do NOT use this skill when: the requirements are still unclear (use interviewing-user-requirements or authoring-specifications-first).
---

# Quebra de Planos de Tarefas

Decompõe especificações e requisitos aprovados em tarefas atômicas, ordenadas topologicamente e testáveis de forma incremental, mapeando fatias paralelas seguras.

## Input/Output Signature
Input:
- specPath: string # Caminho do documento de especificação ou PRD de referência
- maxTaskDurationHours: number # Limite máximo de esforço estimado por tarefa (default: 4)
- enableParallelTracks: boolean # Se deve identificar trilhas de trabalho paralelizáveis (default: true)
Output:
- taskList: array # Lista ordenada de tarefas com critérios de aceite e esforço
- planDocumentPath: string # Caminho do arquivo de plano gerado (ex: TASKS.md)
- parallelTracks: array # Trilhas de execução independente que não compartilham bloqueios
- totalEstimatedHours: number # Estimativa consolidada de horas do plano

## Router and Selection Matrix
| Condição / Cenário | Ação Recomendada | Grau de Liberdade |
|---|---|---|
| Especificação Completa | Fatiamento atômico orientado a contratos com dependências ordenadas | [FRÁGIL] Exige validação de todos os requisitos do documento base |
| Funcionalidade Monolítica | Decomposição em fatias verticais finas ponta a ponta | [FRÁGIL] Cada fatia deve ter testes unitários e integração independente |
| Componentes Independentes | Mapeamento de trilhas de execução paralela desacopladas | [FLEXÍVEL] Agrupa tarefas por camada ou módulo sem bloqueio mútuo |
| Especificação Incompleta | Stop-the-line imediato e encaminhamento para alinhamento | [FRÁGIL] Rejeita planejamento com premissas vagas |

## Imperative Execution Workflow
1. Analisar Especificação e Requisitos [FRÁGIL]:
   - Leia o documento de especificação em `specPath` e extraia a lista completa de módulos e capacidades requeridas.
2. Dimensionar Granularidade das Fatias [FLEXÍVEL]:
   - Decomponha cada módulo em tarefas pequenas de no máximo 2 a 4 horas de execução, com escopo estritamente delimitado.
3. Mapear Grafo de Dependências [FRÁGIL]:
   - Ordene as tarefas topologicamente garantindo que cada etapa dependa apenas de código e testes concluídos na etapa anterior.
4. Identificar Trilhas Paralelizáveis [FLEXÍVEL]:
   - Destaque tarefas ortogonais (ex: design de contratos vs infraestrutura) que podem ser executadas em paralelo com segurança.
5. Redigir Documento de Tarefas (TASKS.md) [FRÁGIL]:
   - Formate o arquivo de saída com seções numeradas, checklists copiáveis `- [ ]` e comandos de validação específicos por tarefa.

## Execution Checklist
- [ ] Validar cobertura integral dos requisitos do documento de especificação
- [ ] Dimensionar cada tarefa em incremento atômico de no máximo 4 horas
- [ ] Estabelecer ordem topológica rigorosa de dependências entre tarefas
- [ ] Documentar critérios objetivos de validação e comandos de teste por tarefa
- [ ] Gerar TASKS.md estruturado e pronto para execução

## On Failure
- **Gatilho de Erro**: Dependência circular entre tarefas, escopo ambíguo no PRD ou tarefas excedendo o limite de esforço.
- **Ação Imediata**: Parar a geração do plano e reportar a inconsistência estrutural encontrada.
- **Rollback**: Remover arquivo de plano parcial gerado para evitar execuções baseadas em tarefas inconsistentes.
- **Fallback**: Notificar o orquestrador e recomendar execução prévia de `authoring-specifications-first`.
- **Logs**: Registrar lista de dependências circulares e módulos cuja quebra violou o dimensionamento máximo.

## Reference Documentation
Consulte a documentação técnica completa: [Referência Técnica](reference.md).
