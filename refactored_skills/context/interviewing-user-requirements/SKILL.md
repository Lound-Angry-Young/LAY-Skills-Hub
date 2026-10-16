---
name: interviewing-user-requirements
description: >
  Extracts what the user actually wants through a one-question-at-a-time interview, testing assumptions, establishing hard constraints and identifying must-haves versus nice-to-haves before designing or coding. Use this skill when: a new feature, project or significant change is requested, requirements are vague, or constraints are unstated. Do NOT use this skill when: the user has already provided clear, complete requirements and constraints (use planning-and-task-breakdown or authoring-specifications-first).
---

# Entrevista e Extração de Requisitos

Conduz alinhamento com o usuário por meio de perguntas objetivas, uma por vez, separando premissas de certezas e delimitando restrições rígidas antes de qualquer planejamento ou código.

## Input/Output Signature
Input:
- userPrompt: string # Pedido inicial ou descrição da demanda apresentada pelo usuário
- existingConstraints: object # Restrições técnicas e premissas já confirmadas no projeto
- currentRoundNumber: number # Número da rodada de entrevista atual (máx 5)
Output:
- gatheredRequirements: array # Lista de requisitos essenciais levantados e validados
- hardConstraints: array # Restrições inegociáveis (stack, budget, compatibilidade, prazos)
- scopeExclusions: array # Itens explicitamente declarados fora do escopo desta entrega
- isInterviewComplete: boolean # Indica se as ambiguidades foram sanadas

## Router and Selection Matrix
| Condição / Cenário | Ação Recomendada | Grau de Liberdade |
|---|---|---|
| Demanda Inicial Vaga | Formula uma única pergunta de múltipla escolha ou direta com foco na maior incerteza | [FRÁGIL] Proibido enviar questionários com múltiplas perguntas simultâneas |
| Suposição Técnica Não Confirmada | Apresenta a suposição claramente e solicita validação do usuário | [FLEXÍVEL] Oferece opções recomendadas com base nas melhores práticas |
| Trade-off de Escopo / Tempo | Apresenta alternativas contrastantes destacando prós e contras | [FLEXÍVEL] Auxilia o usuário a priorizar funcionalidades essenciais |
| Requisitos Consolidados | Sintetiza os achados em checklist e encerra a entrevista para avanço | [FRÁGIL] Exige validação explícita do resumo pelo usuário |

## Imperative Execution Workflow
1. Isolar a Maior Incerteza do Pedido [FLEXÍVEL]:
   - Examine a solicitação do usuário e identifique o fator mais ambíguo que impede uma decisão arquitetural firme.
2. Elaborar Pergunta Única e Acionável [FRÁGIL]:
   - Redija uma pergunta direta em português claro, fornecendo 2 a 3 alternativas factíveis quando aplicável.
3. Classificar Requisitos por Criticidade [FLEXÍVEL]:
   - Separe cada resposta entre `hard constraint` (mandatório) e `nice-to-have` (passível de postergação).
4. Delimitar Fronteiras Negativas de Escopo [FRÁGIL]:
   - Registre expressamente o que não será feito nesta iteração para blindar o projeto contra escopo inflado.
5. Consolidar Acordo e Habilitar Próxima Etapa [FRÁGIL]:
   - Apresente um resumo conciso dos requisitos consolidados e confirme a prontidão para a fase de especificação.

## Execution Checklist
- [ ] Identificar a lacuna crítica no pedido inicial
- [ ] Formular exatamente uma pergunta focada por interação
- [ ] Categorizar restrições mandatórias vs preferências secundárias
- [ ] Definir o que está fora do escopo da entrega
- [ ] Obter validação do resumo antes de passar para especificação ou código

## On Failure
- **Gatilho de Erro**: Respostas contraditórias do usuário, ausência de direcionamento ou mudança drástica de premissas.
- **Ação Imediata**: Pausar a entrevista e apontar a contradição de forma direta e respeitosa.
- **Rollback**: Reverter qualquer premissa técnica assumida que dependia da resposta conflitante.
- **Fallback**: Propor um MVP mínimo e conservador com escopo reduzido para validação passo a passo.
- **Logs**: Registrar o histórico de perguntas formuladas, respostas obtidas e pontos de incerteza residuais.

## Reference Documentation
Consulte a documentação técnica completa: [Referência Técnica](reference.md).
