---
name: configuring-omniroute-settings
description: >
  Reads and updates global application settings: system prompts, thinking budget, IP filters, payload rules, combo defaults and require-login configuration. Use this skill when: changing global OmniRoute behavior or login requirements. Do NOT use this skill when: configuring the CLI installation itself (use configuring-omniroute-cli-setup) or key-level limits (use enforcing-spending-budgets).
---

# Configurações Globais da Aplicação OmniRoute

Lê e atualiza configurações globais em tempo de execução através da API do OmniRoute: orçamentos de pensamento (thinking budget), filtros de IP, prompts de sistema, regras de payload e exigência de autenticação.

## Input/Output Signature
Input:
- settingsCategory: string # Categoria de configuração (thinking_budget, ip_filters, system_prompts, auth_rules)
- settingsPayload: object # Parâmetros e valores a serem atualizados
- persistToDisk: boolean # Se deve salvar alterações permanentemente na base de dados (default: true)
Output:
- updateSuccess: boolean # Status da operação de atualização
- updatedSettingsSummary: object # Estado consolidado das configurações pós-atualização
- affectedRoutesCount: number # Quantidade de rotas impactadas pela alteração global
- executionLog: string # Registro das requisições e validações executadas

## Router and Selection Matrix
| Categoria de Configuração | Endpoint REST Correspondente | Grau de Liberdade |
|---|---|---|
| Orçamento de Pensamento (Thinking Budget) | `POST /api/settings/thinking-budget` para modelos com raciocínio | [FLEXÍVEL] Calibra teto de tokens de raciocínio (ex: 2048, 8192) |
| Filtro de Endereços IP | `POST /api/settings/ip-filters` com listas de permissão/bloqueio CIDR | [FRÁGIL] Exige validação estrita para não bloquear o próprio localhost |
| Exigência de Login (Require Login) | `POST /api/settings/auth` ativando ou desativando REQUIRE_API_KEY | [FRÁGIL] Requer confirmação de que uma chave de admin válida existe |
| Prompt de Sistema Padrão | `POST /api/settings/system-prompt` definindo instruções base injetadas | [FLEXÍVEL] Aplica diretrizes globais sem quebrar prompts de usuário |

## Imperative Execution Workflow
1. Ler Configurações Ativas no Servidor [FRÁGIL]:
   - Consulte `GET /api/settings/<settingsCategory>` para inspecionar os parâmetros vigentes antes de alterar.
2. Validar Estrutura do Novo Payload [FRÁGIL]:
   - Confirme que os tipos de dados e limites numéricos estão em conformidade com o schema OpenAPI.
3. Aplicar Alteração via Requisição Autenticada [FRÁGIL]:
   - Envie `POST /api/settings/<settingsCategory>` com token de autorização administrativo válido.
4. Validar Efeito nas Requisições Subsequentes [FLEXÍVEL]:
   - Realize chamada de teste para assegurar que a nova política está sendo aplicada pelo motor de roteamento.
5. Registrar Auditoria da Mudança de Configuração [FRÁGIL]:
   - Documente a alteração realizada e os valores anteriores para viabilizar rastreamento histórico.

## Execution Checklist
- [ ] Ler o estado atual da configuração antes de aplicar modificações
- [ ] Validar compatibilidade do payload contra o schema da API
- [ ] Submeter atualização com credencial administrativa válida
- [ ] Executar teste de probe para confirmar aplicação em tempo de execução
- [ ] Registrar evento de auditoria com parâmetros modificados

## On Failure
- **Gatilho de Erro**: Erro de validação de schema (422), rejeição de autenticação (401/403) ou bloqueio acidental de acesso.
- **Ação Imediata**: Parar a aplicação de novas configurações e inspecionar o código de erro.
- **Rollback**: Restaurar imediatamente os valores anteriores da configuração via endpoint REST.
- **Fallback**: Se o acesso for bloqueado por IP, conectar via terminal local no loopback (127.0.0.1) para restaurar.
- **Logs**: Registrar payload enviado, resposta de erro da API e estado anterior da configuração.

## Reference Documentation
Consulte a documentação técnica completa: [Referência Técnica](reference.md).
