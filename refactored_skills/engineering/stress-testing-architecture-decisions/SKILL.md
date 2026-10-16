---
name: stress-testing-architecture-decisions
description: >
  Subjects non-trivial decisions to a fresh-context adversarial review, cross-examining assumptions and hidden failure modes before they stand. Use this skill when: stress-testing a plan, working in unfamiliar code, or when stakes are high (production auth, security-sensitive logic, high-stakes migrations, irreversible operations). Do NOT use this skill when: the decision is trivial and easily reversible.
---

# Teste de Estresse de Decisões Arquiteturais

Submete decisões arquiteturais complexas a uma revisão adversária com contexto renovado: questionamento sistemático de premissas ocultas, modos de falha sob concorrência, partições de rede e operações irreversíveis.

## Input/Output Signature
Input:
- architectureProposalDescription: string # Descrição da arquitetura, tecnologia ou migração proposta
- criticalComponentsInvolved: array # Módulos de alto risco (auth, transações_financeiras, banco_dados, cache)
- highRiskFailureScenarios: array # Cenários extremos a testar (queda_rede, deadlock, estouro_memoria, timeout_terceiro)
Output:
- adversarialVerdict: string # Parecer adversário (resilient_approved, vulnerabilities_found, rejected)
- identifiedHiddenFailureModes: array # Lista de modos de falha ocultos identificados
- mitigatingSafeguardsRequired: array # Salvaguardas mandatórias a implementar antes de aprovar
- executionLog: string # Registro dos testes conceituais e cenários simulados

## Router and Selection Matrix
| Área de Risco Crítico | Modo de Teste Adversário | Grau de Liberdade |
|---|---|---|
| Autenticação e Autorização | Simula roubo de sessão, expiração durante requisição, bypass de middleware | [FRÁGIL] Exige validação estrita em todas as bordas sem suposições |
| Transações e Integridade Financeira | Simula concorrência simultânea, débitos duplicados, timeouts de gateway | [FRÁGIL] Requer garantia de chave de idempotência e locks transacionais |
| Migração de Dados Irreversível | Simula perda de conexão durante script de dados, registros corrompidos | [FRÁGIL] Obrigatório teste de rollback e backup físico antes da execução |
| Comunicação Assíncrona / Filas | Simula mensagens fora de ordem, reprocessamento infinito e veneno na fila | [FLEXÍVEL] Avalia presença de dead-letter queues e circuit breakers |

## Imperative Execution Workflow
1. Assumir Papel Adversário e Desafiar Premissas [FRÁGIL]:
   - Rejeite argumentos de confiança cega ("isso nunca vai falhar", "o banco aguenta") e liste o pior cenário possível.
2. Simular Cenários de Falha de Rede e Latência Extrema [FLEXÍVEL]:
   - Questione o que acontece quando o serviço dependente responde em 30 segundos ou cai no meio da operação.
3. Inspecionar Condições de Corrida e Concorrência [FRÁGIL]:
   - Simule 100 requisições idênticas atingindo o mesmo recurso no mesmo milissegundo buscando falhas de estado.
4. Identificar Operações Irreversíveis e Pontos sem Retorno [FRÁGIL]:
   - Isole mutações que não podem ser revertidas por rollback e exija salvaguardas adicionais ou confirmação explícita.
5. Consolidar Parecer de Resiliência e Salvaguardas [FLEXÍVEL]:
   - Aprove a proposta apenas quando todos os modos de falha críticos contarem com mitigações concretas documentadas.

## Execution Checklist
- [ ] Mapear todas as premissas implícitas da arquitetura proposta
- [ ] Simular falhas parciais de rede, timeouts e indisponibilidade de dependências
- [ ] Testar cenários de concorrência massiva e disputas de recurso
- [ ] Isolar operações destrutivas ou irreversíveis
- [ ] Documentar plano de mitigação e salvaguardas necessárias

## On Failure
- **Gatilho de Erro**: Identificação de modo de falha crítico sem mitigação (ex: perda de dados silenciosa, brecha de auth, deadlock).
- **Ação Imediata**: Vetar a proposta de arquitetura e classificar como vulnerabilidade bloqueante.
- **Rollback**: Não aplicável; a revisão ocorre na fase de planejamento antes da implementação de código.
- **Fallback**: Redesenhar o fluxo utilizando arquitetura desacoplada com filas idempotentes ou confirmação em duas fases.
- **Logs**: Registrar modos de falha simulados, impacto estimado de catástrofe e mitigações ausentes.

## Reference Documentation
Consulte a documentação técnica completa: [Referência Técnica](reference.md).
