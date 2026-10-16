---
name: managing-omniroute-providers
description: >
  Manages provider connections, API keys, OAuth flows and connection tests through the REST API: lists, adds, updates, removes and tests AI provider integrations across the provider catalog. Use this skill when: adding or changing a provider connection via the API. Do NOT use this skill when: doing the same from the CLI (use managing-providers-via-cli) or configuring upstream network proxies (use configuring-network-proxies).
---

# Gerenciamento de Provedores de IA via API REST

Gerencia conexões com provedores de modelos de IA através da API REST do OmniRoute: cadastro de credenciais, atualização de chaves de API, fluxos OAuth, testes de conectividade e matriz de saúde.

## Input/Output Signature
Input:
- providerOperation: string # Operação a executar (list, add, update, remove, test_connection)
- providerId: string # Identificador do provedor (openai, anthropic, google, openrouter, custom)
- providerConnectionConfig: object # Configuração contendo apiKey, baseUrl e opções de conexão
Output:
- operationSuccess: boolean # Status da operação de provedor
- providerHealthStatus: object # Resultado do teste de conectividade e latência medida
- activeProviderList: array # Relação de provedores configurados e seus status atuais
- executionLog: string # Registro das chamadas à API REST com credenciais mascaradas

## Router and Selection Matrix
| Operação com Provedor | Endpoint REST Correspondente | Grau de Liberdade |
|---|---|---|
| Adicionar Nova Conexão | `POST /api/providers` com validação prévia de credencial | [FRÁGIL] Exige teste de probe antes de ativar o provedor para tráfego |
| Atualizar Chave ou Endpoint | `PUT /api/providers/{id}` atualizando credenciais de forma atômica | [FRÁGIL] Mascara chaves antigas e novas em todos os retornos |
| Teste de Conexão Isolado | `POST /api/providers/{id}/refresh` disparando requisição de verificação | [FRÁGIL] Confirma autorização válida sem debitar saldo expressivo |
| Matriz de Saúde e Métricas | `GET /api/providers/health-matrix` inspecionando disponibilidade | [FLEXÍVEL] Relata disponibilidade percentual e taxas de erro |

## Imperative Execution Workflow
1. Inspecionar Provedor e Parâmetros de Conexão [FRÁGIL]:
   - Valide se o `baseUrl` é válido e se a chave de API fornecida atende ao formato esperado do provedor.
2. Executar Teste de Conectividade Antes de Gravar [FRÁGIL]:
   - Submeta requisição de teste para confirmar que as credenciais são aceitas pela API do upstream.
3. Persistir Conexão na Base do OmniRoute [FRÁGIL]:
   - Envie requisição REST autenticada para registrar o provedor com encriptação das credenciais em disco.
4. Mapear Modelos Disponíveis no Novo Provedor [FLEXÍVEL]:
   - Consulte o catálogo do provedor para vincular os modelos suportados às rotas de inferência.
5. Validar Disponibilidade na Matriz de Saúde [FRÁGIL]:
   - Confirme através de `GET /api/providers/health-matrix` que o novo provedor consta com status saudável.

## Execution Checklist
- [ ] Validar formato de URL e chave de API do provedor
- [ ] Realizar teste de conexão e autorização antes da persistência
- [ ] Gravar configuração com chaves criptografadas em repouso
- [ ] Atualizar catálogo de modelos suportados
- [ ] Confirmar status saudável na matriz de provedores ativos

## On Failure
- **Gatilho de Erro**: Chave de API inválida (401), quota esgotada no upstream ou endpoint inalcançável.
- **Ação Imediata**: Rejeitar o cadastro do provedor e notificar o motivo da recusa.
- **Rollback**: Não salvar configurações que falharam no teste de conectividade inicial.
- **Fallback**: Manter a conexão anterior ativa caso uma tentativa de atualização falhe.
- **Logs**: Registrar código de erro HTTP do upstream com a chave de API devidamente mascarada.

## Reference Documentation
Consulte a documentação técnica completa: [Referência Técnica](reference.md).
