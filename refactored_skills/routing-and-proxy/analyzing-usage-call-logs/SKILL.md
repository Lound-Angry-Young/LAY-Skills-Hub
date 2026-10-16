---
name: analyzing-usage-call-logs
description: >
  Accesses detailed call logs and usage analytics for OmniRoute, filtering by provider, model, time range, status and cost, exporting logs and aggregating token usage across connections. Use this skill when: analyzing request history, token consumption or cost per provider, model or time range. Do NOT use this skill when: viewing live health or circuit state (use checking-omniroute-server-health) or setting spending limits (use enforcing-spending-budgets).
---

# Análise de Logs de Chamadas e Métricas de Uso

Acessa e analisa logs históricos detalhados de requisições e telemetria de consumo do OmniRoute, filtrando por provedor, modelo de IA, intervalo de datas, status de execução e custos agregados.

## Input/Output Signature
Input:
- timeRangePeriod: string # Intervalo de consulta (1h, 24h, 7d, 30d, custom)
- providerFilter: string # Filtro opcional por provedor (openai, anthropic, gemini, all)
- modelFilter: string # Filtro opcional por modelo ou combo específico
- exportFormat: string # Formato de exportação do relatório (json, csv)
Output:
- totalTokensConsumed: number # Soma total de tokens de prompt e completion na janela
- aggregatedCostEstimate: number # Custo financeiro total acumulado no período
- requestCountByStatus: object # Relação de requisições por código de status (200, 429, 500)
- callLogsSummary: array # Lista paginada dos registros de chamadas filtrados

## Router and Selection Matrix
| Tipo de Análise | Endpoint ou Comando | Grau de Liberdade |
|---|---|---|
| Visão Geral de Consumo | Consulta `GET /api/usage/analytics` com agregação por provedor | [FLEXÍVEL] Agrupa métricas por hora ou dia |
| Inspeção de Chamadas Individuais | Consulta `GET /api/usage/call-logs` com filtros de paginação e status | [FRÁGIL] Exige validação de parâmetros de data ISO 8601 |
| Auditoria de Erros e 429s | Filtra logs por status `>= 400` para identificar provedores com falhas | [FRÁGIL] Isola códigos de rate limit e timeouts de rede |
| Exportação de Dados para BI | Gera exportação estruturada via `GET /api/usage/export` | [FLEXÍVEL] Retorna formato tabular pronto para análise |

## Imperative Execution Workflow
1. Definir Janela Temporal e Filtros de Pesquisa [FRÁGIL]:
   - Calibre as datas de início e fim no formato ISO e estabeleça os provedores ou modelos alvo.
2. Consultar Métricas Agregadas de Consumo [FRÁGIL]:
   - Dispare requisição para `GET /api/usage/analytics` capturando volume de tokens e custo consolidado.
3. Extrair Amostra de Logs de Chamada para Diagnóstico [FLEXÍVEL]:
   - Envie requisição a `GET /api/usage/call-logs` paginada para examinar latência e status de execuções recentes.
4. Identificar Picos Anômalos de Consumo ou Custos [FLEXÍVEL]:
   - Correlacione aumento repentino de requisições com modelos específicos ou chaves de API atípicas.
5. Consolidar Relatório de Uso e Recomendações [FLEXÍVEL]:
   - Formate o sumário com totais de requisições, provedor mais acionado e taxa média de erro.

## Execution Checklist
- [ ] Definir o intervalo temporal e filtros de consulta
- [ ] Obter métricas consolidadas através da API de analytics
- [ ] Inspecionar logs de chamada com códigos de erro ou alta latência
- [ ] Identificar anomalias de custo ou provedores saturados
- [ ] Consolidar relatório analítico com recomendações operacionais

## On Failure
- **Gatilho de Erro**: Timeout em consultas de grande volume, falha de autenticação ou banco de métricas inacessível.
- **Ação Imediata**: Reduzir a janela temporal da consulta para intervalos menores (ex: 24h em vez de 30d).
- **Rollback**: Não aplicável; a operação é estritamente de leitura.
- **Fallback**: Consultar métricas pontuais via CLI local (`omniroute cost`) para obter números consolidados.
- **Logs**: Registrar parâmetros de filtro utilizados, código HTTP retornado e tempo de resposta da API.

## Reference Documentation
Consulte a documentação técnica completa: [Referência Técnica](reference.md).
