---
name: discovering-and-invoking-skills
description: >
  Discovers and invokes agent skills: the meta-skill that decides which skill or workflow applies when a session starts or a new piece of work begins. Use this skill when: starting a session or deciding which skill or workflow fits the work at hand. Do NOT use this skill when: the applicable skill is already known and only needs to run.
---

# Orquestrando e Invocando Agent Skills

Meta-skill que avalia o pedido do usuário, identifica a fase do ciclo de desenvolvimento e seleciona as skills do catálogo mais adequadas para guiar a execução.

## Input/Output Signature
Input:
- taskDescription: string # Descrição do objetivo, demanda ou problema relatado pelo usuário
- currentPhase: string # Fase atual do projeto (align, plan, implement, test, review, ship)
- constraints: array # Restrições técnicas, stack e convenções ativas no repositório
Output:
- selectedSkills: array # Lista ordenada de skills recomendadas para a tarefa
- phase: string # Fase de engenharia identificada no ciclo de vida
- executionPlan: array # Sequência imperativa de passos orientados pelas skills
- status: string # Estado da descoberta (matched, ambiguous, fallback)

## Router and Selection Matrix
| Fase / Demanda do Usuário | Skill Recomendada | Grau de Liberdade |
|---|---|---|
| Requisitos vagos ou não especificados | `interviewing-user-requirements` ou `refining-raw-product-ideas` | [FLEXÍVEL] Formula perguntas pontuais e clarifica escopo |
| Especificação e contratos iniciais | `authoring-specifications-first` e `enforcing-project-constraints` | [FRÁGIL] Exige definição estrita de escopo e qualidade |
| Quebra de escopo em tarefas | `breaking-down-task-plans` | [FRÁGIL] Fatiamento atômico com dependências ordenadas |
| Implementação de código e UI | `implementing-incremental-slices` ou `engineering-frontend-interfaces` | [FLEXÍVEL] Entregas finas testáveis incrementalmente |
| Correção de falhas e regressões | `debugging-root-causes` | [FRÁGIL] Stop-the-line e diagnóstico sistemático de causa-raiz |
| Revisão e fechamento de entrega | `reviewing-multi-axis-code-quality` e `authoring-conventional-commits` | [FRÁGIL] Verificação estrita de contratos e semântica git |

## Imperative Execution Workflow
1. Analisar Demanda e Identificar Fase [FLEXÍVEL]:
   - Examine a solicitação do usuário e determine a fase atual: alinhamento, especificação, planejamento, implementação, testes, revisão ou deploy.
2. Identificar Premissas e Ambiguidade [FRÁGIL]:
   - Explicite premissas técnicas antes de executar. Caso haja requisitos conflitantes ou vagos, pare imediatamente e solicite clarificação (Stop-the-line).
3. Mapear e Selecionar Habilidades Atômicas [FLEXÍVEL]:
   - Consulte o roteador do domínio correspondente no catálogo e selecione apenas a skill de menor escopo necessária para a tarefa.
4. Carregar Diretrizes e Executar com Disciplina [FRÁGIL]:
   - Ative a skill selecionada, aplicando seus passos imperativos e mantendo disciplina de escopo estrita (sem refatorações não solicitadas).
5. Consolidar Evidências e Fechar Ciclo [FLEXÍVEL]:
   - Valide os resultados obtidos, confirme que os testes e tipos passam e formule resposta direta em modo conciso.

## Execution Checklist
- [ ] Analisar a solicitação do usuário e mapear para a fase de desenvolvimento correta
- [ ] Explicitar suposições e eliminar ambiguidades antes da implementação
- [ ] Selecionar a skill atômica correspondente na matriz de roteamento
- [ ] Executar o fluxo imperativo com respeito aos graus de liberdade
- [ ] Validar conformidade de tipos, testes e evidências produzidas

## On Failure
- **Gatilho de Erro**: Pedido ambíguo não resolvido, ausência de skill correspondente para a tarefa ou execução fora do escopo.
- **Ação Imediata**: Interromper o avanço e congelar o estado de trabalho para evitar alterações desnecessárias.
- **Rollback**: Desfazer modificações especulativas realizadas antes da resolução da dúvida.
- **Fallback**: Notificar o usuário sobre a divergência, apresentar as opções mapeadas e solicitar direcionamento explícito.
- **Logs**: Registrar a fase identificada, as skills candidatas avaliadas e o ponto exato da divergência.

## Reference Documentation
Consulte a documentação técnica completa: [Referência Técnica](reference.md).
