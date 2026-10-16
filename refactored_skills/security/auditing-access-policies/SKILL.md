---
name: auditing-access-policies
description: >
  Audits access policies and activity from the OmniRoute CLI: inspects audit logs, telemetry and request history, filtering by event type, user or time range for compliance reviews. Use this skill when: reviewing who accessed what, investigating access events, or gathering compliance evidence about access policies. Do NOT use this skill when: creating or revoking API keys (use managing-api-keys) or authenticating a request (use authenticating-api-sessions).
---

# Auditing Access Policies

Inspeciona registros de auditoria, eventos de acesso e telemetria operacional via CLI do OmniRoute. Permite filtrar por tipo de evento, ator, intervalo temporal e código de resposta para investigação de incidentes e auditorias de conformidade.

## Input/Output Signature

- **Inputs**:
  - `eventFilter: string` - Tipo ou categoria de evento auditado (`auth`, `config`, `key`, `traffic`, `error`).
  - `actorIdentifier: string` - ID de usuário, prefixo de chave de API ou endereço IP de origem para filtro específico.
  - `timeRangeWindow: string` - Janela temporal para a auditoria (`24h`, `7d`, `30d` ou intervalo ISO8601).
  - `outputFormat: "table" | "json" | "csv"` - Formato de apresentação dos dados de auditoria.
- **Outputs**:
  - `auditEvents: AuditEventRecord[]` - Lista estruturada de eventos contendo timestamp, IP, ator, rota e status code.
  - `anomalousEventsCount: number` - Total de requisições rejeitadas (401/403/429) ou eventos com anomalia de padrão.
  - `complianceSummaryReport: string` - Resumo executivo dos acessos auditados e achados de segurança.

## Router and Selection Matrix

| Condição de Ativação | Skill Alternativa | Racional de Roteamento |
| :--- | :--- | :--- |
| Criar, listar, rotacionar ou revogar chaves de API | `managing-api-keys` | Ciclo de vida de credenciais é responsabilidade de gestão de chaves. |
| Autenticar requisição com Bearer token ou cookie de sessão | `authenticating-api-sessions` | Estabelecimento de credencial ativa pertence ao fluxo de autenticação. |
| Monitorar métricas de resiliência e circuit breakers em tempo real | `monitoring-omniroute-resilience` | Métricas operacionais em tempo real pertencem à resiliência do sistema. |

## Imperative Execution Workflow

1. Validar Permissões Administrativas na CLI do OmniRoute [FRÁGIL]:
   - Execute `omniroute audit` garantindo que o operador possua credenciais com escopo de auditoria.
2. Aplicar Filtros de Evento e Intervalo Temporal [FLEXÍVEL]:
   - Filtrar eventos com flags específicas: `omniroute audit --event <eventFilter> --since <timeRangeWindow>`.
   - Se houver investigação direcionada, filtrar por chave ou IP: `omniroute audit --key <actorIdentifier>`.
3. Analisar Tentativas Não Autorizadas e Padrões Suspeitos [FLEXÍVEL]:
   - Isolar requisições com código 401 (falha de autenticação), 403 (falha de permissão) e 429 (excesso de requisições).
   - Identificar picos repentinos de chamadas de um mesmo IP ou uso fora do horário padrão.
4. Exportar Dossiê de Auditoria Estruturado [FRÁGIL]:
   - Gerar exportação para consumo analítico: `omniroute audit --format json > audit_report.json`.
   - Assegurar que nenhum hash de senha ou segredo em texto puro seja vazado no relatório.

## Execution Checklist

- [ ] Confirmar credencial com permissão de auditoria antes da execução
- [ ] Aplicar filtros direcionados por período temporal e ator investigado
- [ ] Mapear eventos com falha de autorização (401/403) e anomalias de taxa (429)
- [ ] Cruzar timestamps de eventos suspeitos com logs do servidor de aplicação
- [ ] Exportar dossiê em formato estruturado sem expor credenciais em claro

## On Failure

- **Gatilho de Erro**: Banco de auditoria inacessível, permissão insuficiente na CLI ou falha de conexão com daemon local.
- **Ação Imediata**: Interromper a rotina de auditoria e exibir mensagem de erro explícita com código de status.
- **Rollback**: Purgar arquivos de exportação temporários gerados de forma parcial ou corrompida.
- **Fallback**: Consultar o banco SQLite local do OmniRoute diretamente em modo leitura ou inspecionar o log do daemon.
- **Logs**: Registrar comando executado, parâmetros de filtro, timestamp e stack trace em log de diagnóstico.

## Reference Documentation
Consulte a documentação técnica completa: [Referência Técnica](reference.md)
