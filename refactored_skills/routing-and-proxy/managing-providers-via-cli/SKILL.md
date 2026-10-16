---
name: managing-providers-via-cli
description: >
  Manages provider connections from the CLI: lists available and configured providers, adds, tests, validates and rotates API keys, and views per-provider metrics. Use this skill when: adding, testing or rotating a provider connection from the terminal. Do NOT use this skill when: working through the REST API (use managing-omniroute-providers).
---

# Gerenciamento de Provedores de IA via Terminal CLI

Gerencia conexões, credenciais e métricas de provedores de IA diretamente na linha de comando: cadastro de chaves, rotação de credenciais, validação de conectividade e auditoria de modelos.

## Input/Output Signature
Input:
- providerCliCommand: string # Subcomando CLI (list, add, test, rotate, metrics)
- targetProviderName: string # Identificador do provedor (openai, anthropic, gemini, groq)
- apiKeyCredential: string # Chave de API a cadastrar ou rotacionar
- customBaseUrl: string # Endpoint customizado opcional para provedores compatíveis
Output:
- cliExecutionSuccess: boolean # Status da execução do comando CLI
- providerValidationStatus: string # Resultado do teste de conexão (valid, invalid_key, unreachable)
- registeredModelsCount: number # Quantidade de modelos identificados na conexão
- executionLog: string # Saída do terminal com credenciais estritamente mascaradas

## Router and Selection Matrix
| Operação no Terminal | Comando CLI Recomendado | Grau de Liberdade |
|---|---|---|
| Listagem de Provedores | Executa `omniroute provider list` exibindo conexões ativas | [FLEXÍVEL] Apresenta tabela com status de saúde e latência |
| Adição de Nova Chave | Executa `omniroute provider add <name> --key ...` com teste automático | [FRÁGIL] Exige validação prévia de conexão antes de salvar |
| Rotação de Credenciais | Executa `omniroute provider rotate <name> --key ...` substituindo chave | [FRÁGIL] Atualiza a credencial sem interromper tráfego ativo |
| Visualização de Métricas | Executa `omniroute provider metrics <name>` exibindo consumo e erros | [FLEXÍVEL] Relata percentis de latência e contagem de requisições |

## Imperative Execution Workflow
1. Verificar Conexões Existentes no CLI [FLEXÍVEL]:
   - Execute `omniroute provider list` para inspecionar os provedores cadastrados e seus status.
2. Preparar Comando com Mascaramento de Entrada [FRÁGIL]:
   - Monte o comando assegurando que a chave de API não seja gravada em histórico aberto de shell sem necessidade.
3. Disparar Teste de Conexão com o Provedor [FRÁGIL]:
   - O CLI executa probe imediato confirmando se o upstream aceita a chave e autoriza inferência.
4. Confirmar Persistência Segura da Credencial [FRÁGIL]:
   - Valide que o provedor foi gravado na base de conexões com status ativo.
5. Inspecionar Métricas de Latência Iniciais [FLEXÍVEL]:
   - Execute o comando de métricas para conferir que o provedor responde dentro do tempo esperado.

## Execution Checklist
- [ ] Listar provedores cadastrados para conferir duplicidade
- [ ] Executar comando CLI de adição ou rotação de chave
- [ ] Validar resultado do teste automático de conectividade
- [ ] Confirmar que as credenciais são exibidas com máscara no terminal
- [ ] Verificar inclusão dos modelos suportados na lista do sistema

## On Failure
- **Gatilho de Erro**: Chave de API inválida, erro de rede com o provedor upstream ou falha de escrita no banco local.
- **Ação Imediata**: Abortar o cadastro e exibir a mensagem de erro do upstream sem expor a chave.
- **Rollback**: Manter a chave anterior em funcionamento em caso de falha na rotação.
- **Fallback**: Orientar o usuário a conferir permissões da chave no painel web do provedor.
- **Logs**: Registrar código de retorno HTTP do upstream e nome do provedor rejeitado.

## Reference Documentation
Consulte a documentação técnica completa: [Referência Técnica](reference.md).
