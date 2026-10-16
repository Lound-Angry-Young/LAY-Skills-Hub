---
name: managing-cli-keys
description: >
  Creates, lists, rotates and revokes OmniRoute API keys from the CLI, manages OAuth flows for provider authentication and inspects key scopes and expiration. Use this skill when: handling API keys or provider OAuth through the OmniRoute CLI. Do NOT use this skill when: calling the HTTP API directly (use managing-api-keys) or authenticating a request (use authenticating-api-sessions).
---

# Managing CLI Keys

Administra credenciais, chaves de API e autenticação OAuth de provedores através da linha de comando do OmniRoute. Permite listar chaves ativas, criar novas credenciais de acesso, realizar rotação segura, revogar acessos e inicializar fluxos OAuth para provedores integrados.

## Input/Output Signature

- **Inputs**:
  - `cliKeyAction: "list" | "create" | "rotate" | "revoke" | "oauth"` - Subcomando de gerenciamento de chaves na CLI.
  - `keyDescriptorLabel?: string` - Nome ou descrição atribuída à chave a ser criada.
  - `keyScopesList?: string[]` - Conjunto de escopos autorizados para a chave.
  - `targetKeyIdentifier?: string` - ID da chave alvo para operações de rotação ou revogação.
  - `targetProviderName?: string` - Nome do provedor de IA para autenticação via OAuth (ex.: `openai`, `anthropic`, `google`).
- **Outputs**:
  - `commandExitCode: number` - Código de retorno do processo da CLI (0 para sucesso).
  - `newSecretKeyString?: string` - Chave gerada exibida na saída do terminal.
  - `keysOverviewTable?: string` - Tabela formatada contendo as chaves cadastradas e seus atributos.

## Router and Selection Matrix

| Condição de Ativação | Skill Alternativa | Racional de Roteamento |
| :--- | :--- | :--- |
| Gerenciar chaves programaticamente via API REST | `managing-api-keys` | Automações via chamadas HTTP utilizam a API REST de chaves. |
| Configurar autenticação de requisições ou sessões ativas | `authenticating-api-sessions` | Fornecimento de credencial para chamadas ativas pertence a autenticação de sessões. |
| Gerenciar conexões de provedores de IA e suas credenciais | `managing-providers-via-cli` | Configuração de credenciais de provedores upstream pertence à gestão de provedores. |

## Imperative Execution Workflow

1. Checar Disponibilidade do Binário da CLI OmniRoute [FRÁGIL]:
   - Execute `omniroute --version` para assegurar que a ferramenta de linha de comando está instalada e acessível.
2. Executar Subcomando de Chaves Apropriado [FRÁGIL]:
   - Para listar chaves: `omniroute keys` ou `omniroute keys list`.
   - Para criar nova chave: `omniroute keys create --name "<keyDescriptorLabel>" --scopes <keyScopesList>`.
   - Para rotacionar chave existente: `omniroute keys rotate <targetKeyIdentifier>`.
   - Para revogar chave: `omniroute keys revoke <targetKeyIdentifier>`.
   - Para fluxo OAuth: `omniroute keys oauth <targetProviderName>`.
3. Coletar e Exibir Chave Gerada com Alerta de Segurança [FLEXÍVEL]:
   - Capture a chave recém-gerada e notifique o operador para salvá-la em local seguro, alertando que ela não poderá ser recuperada.
4. Testar Autorização da Chave Recém-Emitida [FRÁGIL]:
   - Execute requisição de verificação utilizando a chave criada para confirmar permissões ativas.

## Execution Checklist

- [ ] Verificar presença e versão compatível do executável omniroute
- [ ] Atribuir nome representativo e escopos mínimos para a nova chave
- [ ] Exibir o segredo gerado e instruir o armazenamento seguro imediato
- [ ] Validar encerramento imediato de acesso para chaves revogadas
- [ ] Confirmar conclusão bem-sucedida de fluxos OAuth no navegador

## On Failure

- **Gatilho de Erro**: Binário omniroute ausente, erro de permissão no banco SQLite local ou falha de comunicação com o daemon.
- **Ação Imediata**: Interromper o comando e reportar o erro emitido no stderr.
- **Rollback**: Restaurar chave anterior em caso de interrupção inesperada durante rotina de rotação.
- **Fallback**: Operar diretamente via API REST HTTP com `managing-api-keys` caso a CLI falhe.
- **Logs**: Registrar linha de comando chamada, código de saída e mensagens de erro do processo.

## Reference Documentation
Consulte a documentação técnica completa: [Referência Técnica](reference.md)
