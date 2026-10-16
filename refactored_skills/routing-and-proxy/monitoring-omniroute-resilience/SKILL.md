---
name: monitoring-omniroute-resilience
description: >
  Monitors provider health, circuit-breaker states, p50/p95/p99 latency and budget guard alerts, inspecting connection cooldowns and model lockouts in real time. Use this skill when: watching latency trends, provider health or lockouts. Do NOT use this skill when: resetting a stuck provider or changing thresholds (use inspecting-resilience-circuits).
---

# Monitoramento de Resiliência e Saúde de Provedores

Monitora a resiliência operacional do gateway OmniRoute em tempo real: percentis de latência (p50, p95, p99), estados de circuit breakers, períodos de cooldown de conexões e alertas de saturação orçamentária.

## Input/Output Signature
Input:
- monitoringWindowMinutes: number # Janela temporal de análise de telemetria em minutos (default: 15)
- latencyThresholdAlertMs: number # Limite tolerável de latência p95 para geração de alerta (default: 2000)
- targetProvidersFilter: array # Lista opcional de provedores a monitorar (vazio para todos)
Output:
- overallSystemHealthStatus: string # Estado geral do sistema (healthy, degraded, critical)
- latencyPercentilesMap: object # Valores calculados de p50, p95 e p99 por provedor
- lockedProvidersList: array # Provedores atualmente bloqueados em cooldown ou com circuito aberto
- resilienceSummaryReport: string # Relatório consolidado com tendências e anomalias

## Router and Selection Matrix
| Sinal de Resiliência | Endpoint de Monitoramento | Grau de Liberdade |
|---|---|---|
| Saúde Geral dos Componentes | Consulta `GET /api/monitoring/health` avaliando banco, cache e rede | [FRÁGIL] Exige status 200 em todos os subsistemas essenciais |
| Percentis de Latência de Provedores | Consulta `GET /api/provider-metrics` calculando p50/p95/p99 | [FLEXÍVEL] Identifica degradação gradual antes de falhas catastróficas |
| Monitoramento de Compressão | Consulta `GET /api/monitoring/compression` avaliando taxa de economia | [FLEXÍVEL] Relata eficiência dos filtros RTK e Caveman ativos |
| Alertas de Teto Orçamentário | Avalia aproximação de 80% e 100% dos limites configurados por chave | [FRÁGIL] Alerta antes do corte abrupto de requisições por cota |

## Imperative Execution Workflow
1. Consultar Endpoint de Saúde Geral [FRÁGIL]:
   - Dispare requisição para `GET /api/monitoring/health` e capture o estado de cada componente do sistema.
2. Extrair Métricas de Latência dos Provedores [FLEXÍVEL]:
   - Obtenha dados de `GET /api/provider-metrics` e compile os percentis de tempo de resposta p50, p95 e p99.
3. Identificar Conexões em Cooldown ou Circuito Aberto [FRÁGIL]:
   - Isole provedores temporariamente bloqueados e contabilize o tempo restante até a próxima tentativa de probe.
4. Avaliar Alertas de Consumo e Orçamento [FLEXÍVEL]:
   - Verifique chaves de API com consumo acima de 80% do teto mensal estipulado para emissão de avisos.
5. Emitir Diagnóstico Consolidado de Resiliência [FLEXÍVEL]:
   - Apresente um resumo claro destacando anomalias de latência, provedores mais estáveis e riscos operacionais.

## Execution Checklist
- [ ] Consultar endpoint de saúde geral dos subsistemas
- [ ] Calcular percentis de latência para todos os provedores em uso
- [ ] Rastrear provedores em estado de cooldown ou falha repetida
- [ ] Verificar limites de alerta orçamentário
- [ ] Elaborar diagnóstico consolidado com parecer de estabilidade

## On Failure
- **Gatilho de Erro**: Endpoint de monitoramento inalcançável, latência p95 excedendo o teto ou múltiplos provedores fora do ar.
- **Ação Imediata**: Emitir alerta crítico de degradação do gateway e verificar tráfego dos combos.
- **Rollback**: Não aplicável; a rotina é estritamente de observação e monitoramento.
- **Fallback**: Usar comandos CLI locais de diagnóstico (`omniroute doctor`) para avaliar saúde do daemon.
- **Logs**: Registrar série histórica de latências, códigos de erro capturados e provedores indisponíveis.

## Reference Documentation
Consulte a documentação técnica completa: [Referência Técnica](reference.md).
