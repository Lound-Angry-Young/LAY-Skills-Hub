---
name: managing-cli-context-pipelines
description: >
  Manages context engineering configurations, RTK filter sets and conversation sessions from the CLI, applying context-relay settings and inspecting active context pipelines. Use this skill when: inspecting or changing context pipelines or sessions from the terminal. Do NOT use this skill when: configuring filters through the API (use optimizing-rtk-prompt-contexts).
---

# Gerenciamento de Pipelines de Contexto via CLI

Opera e inspeciona pipelines de contexto, conjuntos de filtros RTK e sessões de comunicação entre agentes diretamente a partir da interface de linha de comando do OmniRoute.

## Input/Output Signature
Input:
- subcommand: string # Subcomando CLI a executar (list, show, filter, clear, stats)
- pipelineTarget: string # Identificador do pipeline ou sessão alvo
- filterOptions: array # Flags e opções operacionais do filtro (ex: --rtk, --caveman, --limit)
Output:
- executionStatus: string # Estado de saída do comando (success, failed, invalid_args)
- commandOutput: string # Texto de retorno padrão gerado pelo CLI
- activeFilters: array # Lista de filtros configurados no pipeline inspecionado
- sessionMetrics: object # Métricas de tokens e eventos da sessão

## Router and Selection Matrix
| Condição / Cenário | Ação Recomendada | Grau de Liberdade |
|---|---|---|
| Listagem de Pipelines | Executa comando CLI de listagem de pipelines ativas | [FLEXÍVEL] Permite paginação ou filtros por status |
| Inspeção de Configuração | Executa comando de detalhe com exibição de cadeia de filtros | [FRÁGIL] Exige ID exato do pipeline alvo |
| Aplicação de Filtros RTK | Executa comando de vinculação de regras RTK ao pipeline | [FRÁGIL] Requer flags específicas de compressão |
| Limpeza de Sessão | Executa purga de histórico de sessão com confirmação | [FRÁGIL] Requer verificação prévia para evitar perda indevida |

## Imperative Execution Workflow
1. Verificar Disponibilidade do CLI do OmniRoute [FRÁGIL]:
   - Confirme a acessibilidade do binário `omniroute` e conectividade com a instância local.
2. Identificar Pipeline ou Sessão Alvo [FLEXÍVEL]:
   - Execute a listagem de pipelines para selecionar o identificador correto a ser inspecionado ou alterado.
3. Disparar Comando de Configuração de Contexto [FRÁGIL]:
   - Execute o subcomando CLI apropriado passando flags e parâmetros exatos conforme especificado.
4. Validar Aplicação das Regras de Filtragem [FRÁGIL]:
   - Inspecione a saída do comando e confirme que os filtros de contexto foram registrados com sucesso.
5. Registrar Métricas de Operação [FLEXÍVEL]:
   - Capture o log de execução e retorne as métricas atualizadas de consumo e compressão do pipeline.

## Execution Checklist
- [ ] Confirmar funcionamento e conectividade do binário do OmniRoute CLI
- [ ] Obter identificador correto do pipeline ou sessão alvo
- [ ] Executar comando CLI com flags e argumentos validados
- [ ] Confirmar aplicação dos filtros sem mensagens de erro
- [ ] Registrar métricas operacionais atualizadas

## On Failure
- **Gatilho de Erro**: Código de saída diferente de zero no CLI, pipeline não encontrado ou falha de comunicação com o daemon.
- **Ação Imediata**: Parar a sequência de comandos e inspecionar a mensagem de erro do terminal.
- **Rollback**: Reexecutar comando com parâmetros originais caso uma alteração parcial tenha corrompido o pipeline.
- **Fallback**: Recorrer à API REST equivalente ou reiniciar o daemon do OmniRoute se houver travamento.
- **Logs**: Registrar o comando executado, código de saída e stderr detalhado da operação.

## Reference Documentation
Consulte a documentação técnica completa: [Referência Técnica](reference.md).
