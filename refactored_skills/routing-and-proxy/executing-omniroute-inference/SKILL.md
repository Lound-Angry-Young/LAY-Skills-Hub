---
name: executing-omniroute-inference
description: >
  Executes OpenAI-compatible chat completions and streaming inference through OmniRoute: formats payloads, handles streaming responses, tests fallback routing and measures latency. Use this skill when: sending inference requests to OmniRoute from code or curl. Do NOT use this skill when: chatting interactively from the terminal (use chatting-via-omniroute-cli) or submitting batch jobs (use submitting-batch-inference-jobs).
---

# Execução de Inferência e Completions via OmniRoute

Executa requisições de inferência de linguagem e streaming compatíveis com a API da OpenAI através do gateway OmniRoute, formatando payloads, consumindo streams SSE e validando latência e roteamento de fallbacks.

## Input/Output Signature
Input:
- modelOrComboName: string # Nome do modelo ou combo de roteamento (ex: gpt-4o, claude-3-5-sonnet, auto-fast)
- messagesArray: array # Histórico de mensagens no formato canônico [{role: 'user', content: '...'}]
- streamResponse: boolean # Se deve consumir a resposta em streaming SSE (default: false)
- temperatureAndParams: object # Parâmetros adicionais (temperature, max_tokens, stop)
Output:
- completionResponseText: string # Texto final retornado pelo modelo de linguagem
- tokensUsageStats: object # Contagem de tokens de prompt, completion e total
- latencyMs: number # Tempo de resposta total da requisição em milissegundos
- executedProviderName: string # Provedor que efetivamente atendeu a requisição

## Router and Selection Matrix
| Formato de Resposta | Endpoint / Método | Grau de Liberdade |
|---|---|---|
| Requisição Bloqueante Padrão | `POST /v1/chat/completions` com `stream: false` | [FRÁGIL] Retorna objeto JSON completo com usage e choices |
| Streaming em Tempo Real (SSE) | `POST /v1/chat/completions` com `stream: true` | [FRÁGIL] Exige processamento de chunks `data: {...}` com delimitador `[DONE]` |
| Chamada para Combo com Fallback | Passa nome de combo no campo `model` para roteamento inteligente | [FLEXÍVEL] Ativa chaveamento automático em caso de erro 429 ou 5xx |
| Chamada com Ferramentas (Tool Calling) | Passa schema de ferramentas no campo `tools` | [FRÁGIL] Requer validação estrita do formato de tool_calls retornado |

## Imperative Execution Workflow
1. Formatar Payload Compatível com OpenAI [FRÁGIL]:
   - Monte o corpo JSON com `model`, `messages`, parâmetros de amostragem e autenticação Bearer.
2. Disparar Requisição HTTP para o Gateway [FRÁGIL]:
   - Envie requisição POST para `/v1/chat/completions` no endpoint ativo do OmniRoute com timeout calibrado.
3. Consumir Resposta ou Processar Stream SSE [FLEXÍVEL]:
   - Processe a resposta direta ou itere sobre os chunks de streaming concatenando o texto gerado.
4. Extrair Metadados de Uso e Provedor Efetivo [FRÁGIL]:
   - Capture cabeçalhos de resposta (`x-omniroute-provider`, `x-omniroute-latency`) e dados de consumo de tokens.
5. Retornar Resposta e Registrar Desempenho [FLEXÍVEL]:
   - Entregue o texto resultante validando que a resposta foi concluída sem truncamento indevido.

## Execution Checklist
- [ ] Formatar mensagens e parâmetros no padrão de chat completion
- [ ] Enviar requisição com token de autenticação válido
- [ ] Processar resposta completa ou stream de eventos SSE
- [ ] Extrair contagem de tokens consumidos e latência medida
- [ ] Validar integridade da resposta gerada pelo modelo

## On Failure
- **Gatilho de Erro**: Erro 429 (Rate Limit), erro 500 do provedor upstream, quebra no stream SSE ou timeout de conexão.
- **Ação Imediata**: Capturar o código de status e verificar se o fallback de combo foi acionado.
- **Rollback**: Não aplicável; a chamada de inferência é idempotente e de leitura.
- **Fallback**: Chavear para modelo alternativo ou reexecutar com provedor de menor latência.
- **Logs**: Registrar modelo solicitado, provedor que falhou, código HTTP retornado e payload de erro.

## Reference Documentation
Consulte a documentação técnica completa: [Referência Técnica](reference.md).
