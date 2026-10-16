---
name: managing-api-keys
description: >
  Creates, lists, rotates and revokes OmniRoute API keys, controlling per-key scopes, spending limits, expiration and model allowlists. Use this skill when: managing the lifecycle or permissions of OmniRoute API keys. Do NOT use this skill when: authenticating a request with an existing key (use authenticating-api-sessions) or managing keys from the CLI (use managing-cli-keys).
---

# Managing API Keys

Gerencia o ciclo de vida completo de chaves de API na API REST do OmniRoute. Abrange a criação de novas chaves com escopos restritos, listagem e auditoria de chaves ativas, rotação controlada de segredos e revogação imediata de credenciais comprometidas ou obsoletas.

## Input/Output Signature

- **Inputs**:
  - `keyOperation: "create" | "list" | "rotate" | "revoke"` - Ação a ser executada no gerenciador de chaves.
  - `keyNameIdentifier?: string` - Rótulo descritivo para identificação da chave (ex.: `prod-backend-service`).
  - `assignedScopes?: string[]` - Lista de escopos autorizados (`inference`, `models.read`, `combos.read`, `admin`).
  - `spendingQuotaLimit?: number` - Limite financeiro ou de tokens associado à chave.
  - `targetKeyId?: string` - Identificador da chave para operações de rotação ou revogação.
- **Outputs**:
  - `rawSecretApiKey?: string` - Token em texto puro gerado, visível unicamente no momento da criação.
  - `persistedKeyRecord?: ApiKeyMetadata` - Registro contendo ID, nome, prefixo, escopos, data de criação e expiração.
  - `activeKeysCatalog?: ApiKeySummary[]` - Relação de chaves ativas e seus status de autorização.

## Router and Selection Matrix

| Condição de Ativação | Skill Alternativa | Racional de Roteamento |
| :--- | :--- | :--- |
| Gerenciar chaves via linha de comando no terminal | `managing-cli-keys` | Operações interativas locais pertencem à ferramenta de terminal OmniRoute. |
| Autenticar requisição com chave ou obter cookie de sessão | `authenticating-api-sessions` | Utilizar credenciais para autenticar chamadas pertence ao fluxo de sessões. |
| Definir limites de gasto orçamentário por chave ou global | `enforcing-spending-budgets` | Configuração de tetos orçamentários e limites pertence à governança de gastos. |

## Imperative Execution Workflow

1. Autenticar Chamada com Privilégio de Administração [FRÁGIL]:
   - Certifique-se de fornecer Bearer token com escopo administrativo no endpoint `/api/keys`.
2. Executar Operação Conforme Parâmetro Solicitado [FRÁGIL]:
   - Criar: Envie POST para `/api/keys` com corpo `{"name": "<keyNameIdentifier>", "scopes": assignedScopes, "limit": spendingQuotaLimit}`.
   - Listar: Envie GET para `/api/keys` para recuperar metadados de todas as chaves cadastradas.
   - Rotacionar: Envie POST para `/api/keys/<targetKeyId>/rotate` para gerar novo segredo e invalidar o anterior.
   - Revogar: Envie DELETE para `/api/keys/<targetKeyId>` para revogação permanente imediata.
3. Capturar e Entregar Segredo Gerado de Forma Segura [FRÁGIL]:
   - Obtenha o campo `key` da resposta de criação e armazene-o imediatamente; o segredo não será retornado novamente.
4. Validar Restrições e Escopos Associados [FLEXÍVEL]:
   - Verifique se a chave gerada reflete os limites de taxa, restrições de modelos e escopos solicitados.

## Execution Checklist

- [ ] Autenticar com token de escopo administrativo antes de operar no endpoint de chaves
- [ ] Aplicar o princípio do menor privilégio na definição de escopos
- [ ] Capturar a chave bruta no momento da criação para guarda segura imediata
- [ ] Confirmar remoção de chaves obsoletas através do endpoint DELETE
- [ ] Registrar evento de criação ou rotação na trilha de auditoria

## On Failure

- **Gatilho de Erro**: Retorno 401/403 de autorização, payload inválido, conflito de nome ou falha no banco de dados.
- **Ação Imediata**: Bloquear a criação ou modificação da credencial e reportar mensagem de erro.
- **Rollback**: Caso a rotação falhe antes da emissão da nova chave, manter a chave original ativa e acessível.
- **Fallback**: Utilizar a CLI `omniroute keys` se a API HTTP estiver inoperante.
- **Logs**: Registrar ID da chave, operação solicitada, status code e timestamp sem expor segredos nos logs.

## Reference Documentation
Consulte a documentação técnica completa: [Referência Técnica](reference.md)
