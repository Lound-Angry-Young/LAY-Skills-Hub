---
name: authenticating-api-sessions
description: >
  Manages API key authentication and session tokens for the OmniRoute API: sends Bearer tokens, obtains session cookies and configures login requirements. Use this skill when: a request must be authenticated with a Bearer token or session cookie, or login requirements must be configured. Do NOT use this skill when: creating, rotating or revoking the keys themselves (use managing-api-keys or managing-cli-keys).
---

# Authenticating API Sessions

Gerencia o ciclo de autenticação de sessões e requisições na API do OmniRoute. Abrange o envio de Bearer tokens para endpoints de inferência e proxy, obtenção e renovação de cookies de sessão (`auth_token`) via login administrativo e validação de requisitos de acesso.

## Input/Output Signature

- **Inputs**:
  - `authStrategy: "bearer_token" | "session_cookie"` - Modalidade de autenticação requerida pelo cliente.
  - `apiSecretToken?: string` - Token de API no formato Bearer para chamadas programáticas à API.
  - `dashboardPassword?: string` - Senha mestra administrativa para obtenção do cookie de sessão do dashboard.
  - `targetEndpointUrl: string` - URL do endpoint a ser consumido com autenticação.
- **Outputs**:
  - `sessionCookieHeader?: string` - Cookie `auth_token=<token>` para inclusão no cabeçalho Cookie.
  - `authorizationHeader?: string` - Cabeçalho formatado `Authorization: Bearer <token>`.
  - `authenticationStatus: "authenticated" | "invalid_credentials" | "expired"` - Resultado da verificação da credencial.

## Router and Selection Matrix

| Condição de Ativação | Skill Alternativa | Racional de Roteamento |
| :--- | :--- | :--- |
| Criar, rotacionar ou revogar chaves de API | `managing-api-keys` | O ciclo de vida de chaves requer endpoints específicos de gestão de chaves. |
| Inspecionar trilha de auditoria e tentativas de login | `auditing-access-policies` | A análise forense de acessos e logins pertence à auditoria de políticas. |
| Configurar requisitos globais de autenticação no servidor | `configuring-omniroute-settings` | Alterar flags como require-login pertence à configuração global do servidor. |

## Imperative Execution Workflow

1. Selecionar Método de Autenticação Conforme o Alvo [FRÁGIL]:
   - Para consumo de API REST/Proxy: utilize Bearer token no cabeçalho `Authorization`.
   - Para acesso à interface web ou rotas de gerenciamento interno: realize autenticação de sessão via POST `/api/auth/login`.
2. Executar Login de Sessão Administrativa [FRÁGIL]:
   - Envie requisição POST para `/api/auth/login` com o corpo `{"password": "<dashboardPassword>"}`.
   - Capture o cookie retornado `auth_token` presente no cabeçalho `Set-Cookie`.
3. Montar Cabeçalhos de Requisição Autorizada [FLEXÍVEL]:
   - Para chamadas com token: injete `Authorization: Bearer <apiSecretToken>`.
   - Para chamadas com cookie: injete `Cookie: auth_token=<sessionCookie>`.
4. Validar Conexão Autorizada com Checagem de Status [FRÁGIL]:
   - Execute requisição GET em `/api/auth/status` ou `/api/keys` para confirmar que a resposta retorna status 200 OK.
   - Em caso de resposta 401 Unauthorized, marque a credencial como inválida ou expirada.

## Execution Checklist

- [ ] Definir a estratégia de autenticação correta (Bearer token vs Cookie de sessão)
- [ ] Enviar credenciais unicamente através de conexões HTTPS seguras
- [ ] Capturar e armazenar com segurança o cookie auth_token em requisições de dashboard
- [ ] Confirmar recepção de status 200 OK no endpoint de validação
- [ ] Tratar adequadamente códigos 401 Unauthorized com renovação de sessão

## On Failure

- **Gatilho de Erro**: Retorno 401 Unauthorized, credencial expirada, senha incorreta ou cabeçalho malformado.
- **Ação Imediata**: Bloquear requisições dependentes e invalidar a credencial em cache.
- **Rollback**: Purgar cookies ou tokens corrompidos do armazenamento de sessão local.
- **Fallback**: Solicitar fornecimento de novo token de API ou reautenticação manual com senha mestra.
- **Logs**: Registrar o endpoint chamado e o código HTTP de status sem registrar valores de tokens ou senhas.

## Reference Documentation
Consulte a documentação técnica completa: [Referência Técnica](reference.md)
