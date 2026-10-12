# Contrato de Handoff

## HANDOFF (roteador para sub-agente)
- task: string                  # tarefa precisa
- domain: string                # domínio alvo
- context: string[]             # arquivos ou trechos relevantes
- constraints: string[]         # restrições
- acceptance_criteria: string[] # critérios de aceite

## RESULT (sub-agente para roteador)
- status: success | failure | needs_clarification | escalated
- artifacts: string[]
- summary: string
- open_items: string[]
