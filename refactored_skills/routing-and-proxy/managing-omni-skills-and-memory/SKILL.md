---
name: managing-omni-skills-and-memory
description: >
  Manages Omni Skills (list, install, test, remove), plugins (create, configure) and persistent memory (search, add, clear) from the CLI. Use this skill when: installing or removing skills and plugins or managing persistent memory entries. Do NOT use this skill when: importing skills from GitHub (use importing-github-agent-skills) or invoking an installed CLI tool plugin (use invoking-cli-tool-plugins).
---

# Gestão de Skills, Plugins e Memória Persistente via CLI

Gerencia o ciclo de vida de Omni Skills, extensões de plugins e base de memória persistente através do CLI do OmniRoute: instalação, remoção, busca semântica em memória e parametrização.

## Input/Output Signature
Input:
- managementDomain: string # Área de atuação (skills, plugins, memory)
- subActionCommand: string # Ação a executar (list, install, remove, search, add, clear)
- entityIdentifierOrQuery: string # Nome da skill/plugin ou termo de busca na memória
- entryContentPayload: object # Dados da entrada para inserção ou atualização
Output:
- operationSuccess: boolean # Status da execução da ação
- affectedEntitiesCount: number # Quantidade de registros ou pacotes impactados
- queryResultsList: array # Resultados retornados em buscas ou listagens
- executionLog: string # Registro dos comandos CLI e saídas

## Router and Selection Matrix
| Domínio / Ação | Comando CLI Recomendado | Grau de Liberdade |
|---|---|---|
| Gestão de Memória Persistente | Executa `omniroute memory [search|add|clear]` manipulando entradas | [FLEXÍVEL] Permite busca por similaridade semântica ou exata |
| Instalação de Nova Omni Skill | Executa `omniroute skills install <nome>` registrando no catálogo | [FRÁGIL] Exige validação de integridade do pacote da skill |
| Configuração de Plugins | Executa `omniroute plugins configure <id>` atualizando parâmetros | [FRÁGIL] Requer schema de configuração válido para o plugin |
| Purga de Memória de Sessão | Executa `omniroute memory clear` com confirmação explícita | [FRÁGIL] Limpeza irreversível; requer cautela para não apagar dados vitais |

## Imperative Execution Workflow
1. Identificar Domínio de Operação (Skills, Plugins ou Memória) [FRÁGIL]:
   - Determine qual subsistema do OmniRoute será gerenciado com base na solicitação do usuário.
2. Executar Consulta Inicial de Estado [FLEXÍVEL]:
   - Liste os itens existentes (`omniroute memory list` ou `omniroute skills list`) para verificar presença prévia.
3. Disparar Comando CLI com Parâmetros Validados [FRÁGIL]:
   - Execute a ação pretendida passando flags de identificação, chaves e payloads estruturados.
4. Validar Efeito da Alteração [FRÁGIL]:
   - Confirme que o item foi adicionado, modificado ou removido com sucesso através de uma leitura subsequente.
5. Registrar Confirmação Operacional [FLEXÍVEL]:
   - Apresente o sumário atualizado do inventário com o novo estado consolidado.

## Execution Checklist
- [ ] Definir o subsistema alvo (memória, skills ou plugins)
- [ ] Verificar estado atual antes de aplicar alterações
- [ ] Executar comando CLI com parâmetros validados
- [ ] Confirmar aplicação da alteração através de nova leitura
- [ ] Registrar log de saída com o resultado obtido

## On Failure
- **Gatilho de Erro**: Item não encontrado, falha de integridade do plugin ou erro de persistência em memória.
- **Ação Imediata**: Pausar a operação e inspecionar a saída de erro do CLI.
- **Rollback**: Restaurar backup da memória persistente caso uma operação de limpeza indevida ocorra.
- **Fallback**: Usar comandos de reparo do banco de dados local via `omniroute doctor`.
- **Logs**: Registrar comando disparado, argumentos fornecidos e mensagem de erro do terminal.

## Reference Documentation
Consulte a documentação técnica completa: [Referência Técnica](reference.md).
