---
name: instrumenting-code-observability
description: >
  Instruments code so production behavior is visible and diagnosable: logging, metrics, tracing and alerting, with evidence that shipped features work. Use this skill when: adding logging, metrics, tracing or alerts, or when production issues cannot be explained from the available data. Do NOT use this skill when: the work is performance tuning without an observability gap (use optimizing-fullstack-performance).
---

# Instrumentação de Observabilidade e Telemetria

Instrumenta aplicações para diagnósticos operacionais em produção: logs estruturados em JSON, métricas de contagem e latência, rastreamento distribuído (tracing) e alertas acionáveis orientados a sintomas.

## Input/Output Signature
Input:
- targetModuleOrEndpoint: string # Módulo, rota ou serviço alvo da instrumentação
- telemetryTypesRequired: array # Tipos de observabilidade (structured_logs, metrics, distributed_trace, health_check)
- sensitiveFieldsToMask: array # Lista de campos sensíveis com máscara obrigatória (password, token, apiKey, cpf)
Output:
- instrumentationSuccess: boolean # Status da aplicação dos instrumentos
- addedLogEvents: array # Lista de novos eventos de log estruturados introduzidos
- exportedMetricsSummary: object # Contadores, histogramas e gauges declarados no código
- executionLog: string # Registro das alterações e testes de telemetria

## Router and Selection Matrix
| Sinal de Telemetria | Padrão Recomendado | Grau de Liberdade |
|---|---|---|
| Logs de Aplicação | Logs estruturados em formato JSON com `level`, `timestamp`, `traceId` e `message` | [FRÁGIL] Proibido usar console.log livre ou concatenar dados sensíveis |
| Métricas de Desempenho | Histogramas de latência e contadores de requisições por status HTTP | [FLEXÍVEL] Mantém cardinalidade de tags/labels baixa e controlada |
| Rastreamento Distribuído | Propagação de cabeçalhos de contexto W3C Trace Context (`traceparent`) | [FRÁGIL] Garante continuidade do ID de rastreamento entre serviços |
| Sanitização de Dados (PII) | Mascaramento determinístico de chaves e dados pessoais antes da emissão | [FRÁGIL] Tolerância zero para vazamento de senhas ou tokens em logs |

## Imperative Execution Workflow
1. Identificar Lacunas de Visibilidade no Módulo [FLEXÍVEL]:
   - Avalie onde falhas silenciosas ou gargalos de latência ocorrem sem emissão de telemetria adequada.
2. Inserir Logs Estruturados nos Pontos de Transição [FRÁGIL]:
   - Adicione eventos de log com dados contextuais relevantes nos pontos de entrada, saída e captura de exceções.
3. Declarar e Registrar Métricas de Operação [FLEXÍVEL]:
   - Configure contadores de erros, contadores de eventos de negócio e medidores de tempo de execução.
4. Propagar Identificadores de Rastreamento (Trace ID) [FRÁGIL]:
   - Assegure que requisições assíncronas e chamadas para serviços externos preservem o contexto de rastreio.
5. Validar Mascaramento de Informações Sensíveis [FRÁGIL]:
   - Confirme através de testes que dados confidenciais (chaves, senhas, cartões) são omitidos ou mascarados.

## Execution Checklist
- [ ] Mapear eventos críticos e fronteiras que necessitam de telemetria
- [ ] Adicionar logs estruturados em formato JSON com níveis apropriados
- [ ] Registrar métricas de latência e contadores de sucesso/erro
- [ ] Garantir propagação do trace ID através das chamadas de rede
- [ ] Validar máscara obrigatória de informações sensíveis e PII

## On Failure
- **Gatilho de Erro**: Vazamento de segredo em log de telemetria, explosão de cardinalidade em métricas ou sobrecarga de IO.
- **Ação Imediata**: Desativar o emissor de log ruidoso ou com vazamento imediatamente.
- **Rollback**: Remover campos sensíveis não mascarados e restaurar sanitizador padrão.
- **Fallback**: Reduzir nível de log para `ERROR` ou aplicar amostragem (sampling) para reduzir volume.
- **Logs**: Registrar padrão de dado sensível interceptado e contagem de eventos emitidos na janela.

## Reference Documentation
Consulte a documentação técnica completa: [Referência Técnica](reference.md).
