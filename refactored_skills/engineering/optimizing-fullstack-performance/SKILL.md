---
name: optimizing-fullstack-performance
description: >
  Optimizes application performance across frontend, backend, queries and databases: Core Web Vitals, load times, N+1 query patterns and bottlenecks revealed by profiling. Use this skill when: performance requirements exist, regressions are suspected or profiling shows bottlenecks. Do NOT use this skill when: the work is React-specific (use optimizing-react-performance) or adding observability (use instrumenting-code-observability).
---

# Otimização de Performance Fullstack

Otimiza desempenho de ponta a ponta em aplicações: Core Web Vitals no frontend, eliminação de consultas N+1 no banco de dados, índices otimizados, pooling de conexões e redução de tempo de resposta em APIs.

## Input/Output Signature
Input:
- targetPerformanceBottleneck: string # Sintoma ou gargalo identificado (high_lcp, slow_api_endpoint, database_high_cpu)
- performanceProfilingData: object # Dados de profiling, consultas lentas ou métricas de Web Vitals
- performanceBudgetTargets: object # Metas estritas de desempenho (ex: LCP < 2.5s, API p95 < 200ms)
Output:
- optimizationActionPlan: array # Lista priorizada de intervenções de performance com ganho estimado
- appliedOptimizationsDiff: string # Correções aplicadas em consultas, rotas e componentes
- benchmarkResultsComparison: object # Comparativo de latência/throughput antes e depois da intervenção
- status: string # Estado da otimização (budget_met, needs_further_work, blocked)

## Router and Selection Matrix
| Gargalo Identificado | Intervenção Recomendada | Grau de Liberdade |
|---|---|---|
| Consulta N+1 no Banco de Dados | Substitui loops por consultas com join ou cláusula `IN` e carrega dados em lote | [FRÁGIL] Exige validação de cardinalidade de registros e consumo de memória |
| Índices Faltantes em Tabelas | Cria índices compostos alinhados com filtros frequentes de cláusula `WHERE` | [FRÁGIL] Requer análise de impacto no custo de escrita da tabela |
| LCP Elevado no Frontend | Pré-carrega recursos críticos (preload de fontes/hero) e elimina bloqueios de renderização | [FLEXÍVEL] Aplica carregamento preguiçoso em seções abaixo da dobra |
| Alto Consumo de CPU em API | Implementa caching semântico ou em memória (Redis/in-memory) com TTL calibrado | [FLEXÍVEL] Balanceia taxa de acerto de cache e frescor dos dados |

## Imperative Execution Workflow
1. Coletar Dados de Profiling e Métricas de Referência [FRÁGIL]:
   - Meça tempos de resposta, planos de execução de consulta (`EXPLAIN ANALYZE`) e pontuações de Web Vitals atuais.
2. Identificar a Operação Mais Lenta no Caminho Crítico [FLEXÍVEL]:
   - Isole a instrução SQL ou função que consome a maior parcela do orçamento de tempo total da requisição.
3. Otimizar Consultas e Acesso a Dados [FRÁGIL]:
   - Elimine round-trips repetidos ao banco, utilize projeções com colunas necessárias e aplique índices específicos.
4. Otimizar Transporte e Caching de Resposta [FLEXÍVEL]:
   - Ative compressão gzip/brotli, ajuste cabeçalhos de controle de cache e evite payloads JSON inflados.
5. Executar Benchmark Pós-Otimização e Validar Metas [FRÁGIL]:
   - Meça novamente as métricas nas mesmas condições e confirme conformidade com os orçamentos de desempenho.

## Execution Checklist
- [ ] Estabelecer medição base de referência antes de alterar código
- [ ] Eliminar padrões de consulta N+1 e carregar dados em lote
- [ ] Validar planos de execução e índices nas tabelas críticas
- [ ] Reduzir peso de payloads e otimizar caminho crítico de renderização
- [ ] Comparar métricas pós-ajuste garantindo atendimento ao orçamento

## On Failure
- **Gatilho de Erro**: Otimização gera inconsistência de dados, quebra de cache ou índices degradam performance de escrita.
- **Ação Imediata**: Reverter alterações de consulta ou índice que causaram regressão.
- **Rollback**: Restaurar código de consulta e esquemas originais do banco de dados.
- **Fallback**: Aplicar cache temporário de leitura enquanto uma reformulação estrutural de dados é planejada.
- **Logs**: Registrar tempos de execução comparativos, planos de execução rejeitados e consumo de memória.

## Reference Documentation
Consulte a documentação técnica completa: [Referência Técnica](reference.md).
