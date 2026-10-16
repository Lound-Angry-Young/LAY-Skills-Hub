---
name: interacting-with-a2a-cli
description: >
  Interacts with the OmniRoute A2A server from the CLI: sends tasks, inspects skill execution history and tests the JSON-RPC 2.0 agent-to-agent protocol interactively. Use this skill when: testing A2A tasks from the terminal. Do NOT use this skill when: an agent integrates with A2A programmatically (use coordinating-omniroute-a2a).
---

# Interação com o Protocolo A2A via CLI

Testa e executa tarefas de comunicação Agent-to-Agent (A2A) baseadas em JSON-RPC 2.0 a partir do CLI do OmniRoute, inspecionando histórico de execução, despacho de competências e respostas interativas.

## Input/Output Signature
Input:
- a2aCommandAction: string # Ação A2A a executar (send, list, inspect, skills)
- targetSkillName: string # Habilidade A2A a ser invocada no agente par (ex: smart-routing, quota-management)
- taskParametersPayload: object # Parâmetros da tarefa enviados na mensagem JSON-RPC
Output:
- a2aExecutionSuccess: boolean # Status da execução da tarefa pelo agente par
- rpcResponseResult: object # Resultado retornado no corpo da resposta JSON-RPC 2.0
- latencyDurationMs: number # Tempo de processamento da tarefa entre agentes
- executionLog: string # Registro das mensagens enviadas e recebidas no terminal

## Router and Selection Matrix
| Ação A2A | Comando CLI Recomendado | Grau de Liberdade |
|---|---|---|
| Envio de Tarefa Interativa | Executa `omniroute a2a send <skill> --payload "..."` | [FRÁGIL] Exige validação estrita do payload JSON contra a skill alvo |
| Listagem de Habilidades Remotas | Executa `omniroute a2a skills` listando capacidades expostas pelo par | [FLEXÍVEL] Mapeia descrições e esquemas de parâmetros das skills |
| Inspeção de Histórico de Tarefas | Executa `omniroute a2a list` para auditar tarefas executadas recentemente | [FLEXÍVEL] Exibe status, durações e identificadores de correlação |
| Teste de Conectividade do Protocolo | Dispara requisição probe de ping JSON-RPC para validar o canal | [FRÁGIL] Confirma disponibilidade do servidor A2A antes de enviar tarefas |

## Imperative Execution Workflow
1. Verificar Disponibilidade do Servidor A2A [FRÁGIL]:
   - Confirme que o serviço A2A do OmniRoute está ativo e escutando no endpoint configurado.
2. Validar Parâmetros da Habilidade A2A [FRÁGIL]:
   - Verifique que o payload JSON atende aos tipos e campos obrigatórios da habilidade remota solicitada.
3. Disparar Comando CLI de Envio de Tarefa [FRÁGIL]:
   - Execute `omniroute a2a send` passando o nome da skill e os argumentos estruturados.
4. Processar e Validar Resposta JSON-RPC 2.0 [FRÁGIL]:
   - Inspecione a resposta verificando que contém o campo `result` sem o objeto `error`.
5. Apresentar Resultado Estruturado [FLEXÍVEL]:
   - Exiba a saída gerada pelo agente remoto com detalhamento de tempo de execução e artefatos.

## Execution Checklist
- [ ] Confirmar conectividade com o servidor A2A local ou remoto
- [ ] Validar compatibilidade do payload contra o esquema da skill
- [ ] Executar comando CLI de despacho de tarefa A2A
- [ ] Verificar ausência de erros na resposta JSON-RPC 2.0
- [ ] Capturar resultado e tempo de resposta da operação

## On Failure
- **Gatilho de Erro**: Erro JSON-RPC retornado pelo agente par, timeout na execução da tarefa ou falha de rede.
- **Ação Imediata**: Interromper o fluxo e capturar o código e mensagem do erro retornado.
- **Rollback**: Não aplicável; a operação é orientada a despacho de tarefas assíncronas.
- **Fallback**: Tentar execução local direta da funcionalidade sem delegar para o protocolo A2A.
- **Logs**: Registrar ID da mensagem JSON-RPC, payload transmitido e código de erro retornado.

## Reference Documentation
Consulte a documentação técnica completa: [Referência Técnica](reference.md).
