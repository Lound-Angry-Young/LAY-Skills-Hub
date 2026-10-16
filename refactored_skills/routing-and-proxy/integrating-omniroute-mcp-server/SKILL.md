---
name: integrating-omniroute-mcp-server
description: >
  Connects to the OmniRoute MCP server, with 110 tools over SSE, stdio or HTTP transports, covering routing, cache, compression, memory, skills, providers and audit tools across 33 permission scopes. Use this skill when: wiring an MCP client to OmniRoute. Do NOT use this skill when: only inspecting the MCP server from the terminal (use inspecting-mcp-server-cli).
---

# Integração com o Servidor OmniRoute MCP

Conecta clientes de IA ao servidor MCP (Model Context Protocol) do OmniRoute com suporte a mais de 110 ferramentas nativas em transportes SSE, stdio ou HTTP, abrangendo roteamento, memória, cache e auditoria.

## Input/Output Signature
Input:
- mcpClientType: string # Tipo do cliente MCP (claude_desktop, cursor, antigravity, custom_agent)
- transportProtocol: string # Protocolo de transporte pretendido (sse, stdio, http)
- requiredPermissionScopes: array # Escopos solicitados (routing, memory, cache, audit, providers, all)
- listenPortOrUrl: string # Endpoint ou porta do serviço MCP (ex: http://localhost:20128/api/mcp/sse)
Output:
- clientConfigurationSnippet: object # Bloco de configuração JSON para colar no cliente MCP
- connectionVerified: boolean # Status do teste de handshake e listagem de ferramentas
- availableToolsCount: number # Quantidade de ferramentas MCP expostas com os escopos autorizados
- executionLog: string # Registro dos procedimentos de conexão e validação

## Router and Selection Matrix
| Cliente MCP / Transporte | Formato de Configuração | Grau de Liberdade |
|---|---|---|
| Claude Desktop (SSE) | Registra URL do endpoint SSE com chave de autorização Bearer | [FRÁGIL] Exige URL absoluta e token válido nas opções de conexão |
| Antigravity / Cursor (Stdio) | Configura comando `omniroute mcp stdio` como processo filho | [FRÁGIL] Requer caminho do binário acessível e argumentos estritos |
| Restrição de Escopos de Segurança | Limita ferramentas visíveis com base nas permissões concedidas | [FRÁGIL] Proibido expor ferramentas administrativas a clientes de escopo restrito |
| Teste de Handshake de Ferramentas | Dispara chamada `tools/list` para validar funcionamento imediato | [FLEXÍVEL] Confirma que todas as ferramentas esperadas foram carregadas |

## Imperative Execution Workflow
1. Identificar Cliente e Protocolo de Transporte [FRÁGIL]:
   - Selecione se a integração utilizará streaming de eventos SSE via HTTP ou execução de processo stdio.
2. Definir Escopos de Ferramentas Autorizadas [FRÁGIL]:
   - Ajuste as permissões requeridas pelo cliente para garantir acesso somente às ferramentas necessárias.
3. Gerar Bloco de Configuração do Cliente [FRÁGIL]:
   - Monte o JSON de configuração do cliente MCP (ex: `claude_desktop_config.json`) com headers e URL exata.
4. Realizar Teste de Handshake e Inicialização [FRÁGIL]:
   - Envie requisição de inicialização MCP e valide a resposta de capacidades e ferramentas suportadas.
5. Auditar Registro de Chamadas no Painel MCP [FLEXÍVEL]:
   - Verifique que as invocações de teste foram registradas corretamente em `GET /api/mcp/audit`.

## Execution Checklist
- [ ] Definir transporte apropriado para o cliente MCP
- [ ] Delimitar escopos de permissão necessários
- [ ] Gerar JSON de configuração formatado para o cliente
- [ ] Executar teste de handshake e listar ferramentas disponíveis
- [ ] Confirmar que o serviço de auditoria MCP registra as chamadas

## On Failure
- **Gatilho de Erro**: Falha no handshake MCP, rejeição de autorização por escopo insuficiente ou porta indisponível.
- **Ação Imediata**: Interromper a tentativa de conexão e verificar os logs do servidor MCP.
- **Rollback**: Restaurar arquivo de configuração original do cliente MCP.
- **Fallback**: Comutar transporte de SSE para stdio caso haja bloqueio de porta de rede local.
- **Logs**: Registrar endpoint do transporte, resposta do handshake e ferramentas rejeitadas.

## Reference Documentation
Consulte a documentação técnica completa: [Referência Técnica](reference.md).
