---
name: inspecting-spending-costs-cli
description: >
  Views cost breakdowns, token usage and call logs from the CLI, filtered by provider, model or date range, exporting usage reports and inspecting per-connection spending. Use this skill when: checking spend from the terminal or exporting a usage report. Do NOT use this skill when: setting budgets or limits (use enforcing-spending-budgets) or using the HTTP analytics surface (use analyzing-usage-call-logs).
---

# Inspeção de Custos e Consumo Financeiro via CLI

Inspeciona relatórios de custos financeiros, consumo acumulado de tokens e histórico de faturamento diretamente no terminal a partir do CLI do OmniRoute, filtrando por provedor, modelo e período.

## Input/Output Signature
Input:
- dateRangeFilter: string # Intervalo de consulta (today, yesterday, this_week, this_month, all)
- targetProviderId: string # Filtro opcional por provedor de IA específico
- exportOutputFilePath: string # Caminho opcional para exportação de relatório (ex: relatorio-custos.csv)
Output:
- totalSpendAmountUsd: number # Valor total consumido no período em dólares
- totalTokensConsumed: number # Total agregado de tokens consumidos
- spendBreakdownByProvider: object # Relação de despesas detalhada por provedor e conexão
- executionLog: string # Registro dos comandos CLI executados

## Router and Selection Matrix
| Escopo da Consulta | Comando CLI Recomendado | Grau de Liberdade |
|---|---|---|
| Custo Acumulado do Dia / Mês | Executa `omniroute cost` exibindo resumo financeiro e total de tokens | [FLEXÍVEL] Apresenta tabela formatada com separação por provedores |
| Detalhamento por Conexão de Chave | Adiciona flag de detalhamento por conexão individual | [FRÁGIL] Exige correspondência precisa do ID da conexão |
| Exportação de Extrato Financeiro | Dispara exportação de extrato detalhado para arquivo CSV ou JSON | [FLEXÍVEL] Grava dados tabulares para auditoria contábil |
| Auditoria de Provedor Específico | Filtra exclusivamente os custos gerados por uma API de provedor | [FRÁGIL] Isola custos de inferência de chamadas auxiliares |

## Imperative Execution Workflow
1. Executar Comando CLI de Apuração de Custos [FRÁGIL]:
   - Execute `omniroute cost` passando o parâmetro de período selecionado (`--period this_month`).
2. Analisar Distribuição de Despesas por Provedor [FLEXÍVEL]:
   - Compare quais provedores concentram a maior fatia do orçamento e identifique modelos mais caros.
3. Verificar Média de Custo por Milhão de Tokens [FLEXÍVEL]:
   - Calcule a eficiência financeira da operação contrastando tokens gerados contra dólares despendidos.
4. Exportar Extrato Consolidado [FLEXÍVEL]:
   - Se solicitado, exporte o relatório completo para arquivo local em `exportOutputFilePath`.
5. Apresentar Sumário Financeiro Claro [FLEXÍVEL]:
   - Exiba os números consolidados com destaque para o total consumido e projeção até o fim do ciclo.

## Execution Checklist
- [ ] Disparar comando de consulta de custos com o período desejado
- [ ] Analisar a proporção de gastos entre os diferentes provedores
- [ ] Checar se algum modelo causou consumo atípico no período
- [ ] Gerar arquivo de exportação caso solicitado
- [ ] Formular sumário conciso com os valores apurados

## On Failure
- **Gatilho de Erro**: Banco de histórico de custos inacessível, erro no comando CLI ou inconsistência nos cálculos de precificação.
- **Ação Imediata**: Parar a consulta e verificar integridade do banco de dados local.
- **Rollback**: Não aplicável; a operação é estritamente consultiva.
- **Fallback**: Consultar os endpoints da API REST `/api/usage/analytics` como alternativa de leitura.
- **Logs**: Registrar comando disparado, código de saída e erro emitido pelo terminal.

## Reference Documentation
Consulte a documentação técnica completa: [Referência Técnica](reference.md).
