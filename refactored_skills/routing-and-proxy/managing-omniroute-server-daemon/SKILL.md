---
name: managing-omniroute-server-daemon
description: >
  Starts, stops and restarts the OmniRoute server from the CLI, managing daemon mode, port configuration, auto-recovery, system tray integration and the dashboard shortcut. Use this skill when: running the OmniRoute server as a daemon or changing its port or recovery behavior. Do NOT use this skill when: configuring the embedded services (use managing-embedded-service-versions).
---

# Gerenciamento do Daemon e Servidor OmniRoute

Controla o ciclo de vida do servidor daemon do OmniRoute via terminal: inicialização em segundo plano, encerramento gracioso, reinicialização, configuração de porta e atalhos para o dashboard.

## Input/Output Signature
Input:
- daemonAction: string # Ação a executar (start, stop, restart, status, dashboard)
- serverListenPort: number # Porta de rede para escuta do serviço (default: 20128)
- runAsDaemon: boolean # Se deve executar desanexado do terminal atual (default: true)
Output:
- daemonOperationalStatus: string # Estado do daemon (running, stopped, restarting)
- serverProcessPid: number # Identificador de processo (PID) do servidor ativo
- activeListenUrl: string # URL local do servidor em execução (ex: http://localhost:20128)
- executionLog: string # Registro dos comandos de ciclo de vida executados

## Router and Selection Matrix
| Ação de Controle | Comando CLI Recomendado | Grau de Liberdade |
|---|---|---|
| Iniciar em Segundo Plano | Executa `omniroute start --daemon` desanexando o processo | [FRÁGIL] Exige verificação prévia de que a porta alvo está desocupada |
| Encerramento Gracioso | Executa `omniroute stop` aguardando a finalização de requisições ativas | [FRÁGIL] Evita encerramento abrupto com perda de dados em disco |
| Reinicialização com Nova Config | Executa `omniroute restart` aplicando novas variáveis de ambiente | [FRÁGIL] Confirma reinício bem-sucedido monitorando o novo PID |
| Abertura do Painel Visual | Executa `omniroute dashboard` abrindo navegador na porta ativa | [FLEXÍVEL] Facilita inspeção visual interativa do sistema |

## Imperative Execution Workflow
1. Inspecionar Estado Atual do Processo [FRÁGIL]:
   - Execute `omniroute status` para conferir se já existe uma instância do servidor rodando e em qual porta.
2. Verificar Disponibilidade da Porta de Rede [FRÁGIL]:
   - Se for iniciar ou alterar porta, confirme que a porta configurada não está sendo usada por outro processo.
3. Disparar Comando de Controle de Ciclo de Vida [FRÁGIL]:
   - Execute o subcomando CLI apropriado (`start`, `stop`, `restart`) monitorando mensagens do terminal.
4. Aguardar Inicialização e Validar Conectividade [FRÁGIL]:
   - Aguarde o tempo de warmup e realize requisição de probe para confirmar resposta HTTP 200 no health-check.
5. Registrar PID e URL de Acesso do Servidor [FLEXÍVEL]:
   - Capture o identificador de processo gerado e disponibilize a URL do dashboard local.

## Execution Checklist
- [ ] Checar estado atual e PID da instância existente
- [ ] Validar desocupação da porta de rede selecionada
- [ ] Disparar comando de inicialização, parada ou reinício
- [ ] Testar requisição de saúde na URL local após inicialização
- [ ] Confirmar que o processo permanece ativo em segundo plano

## On Failure
- **Gatilho de Erro**: Conflito de porta de rede (EADDRINUSE), crash de inicialização por banco corrompido ou falha de parada.
- **Ação Imediata**: Identificar o processo concorrente ocupando a porta e reportar o conflito.
- **Rollback**: Se a reinicialização falhar, tentar subir a versão estável na porta padrão anterior.
- **Fallback**: Iniciar o servidor em modo foreground (sem flag `--daemon`) para capturar o log de erro no stdout.
- **Logs**: Registrar código de saída do processo, arquivo de log do supervisor e porta em conflito.

## Reference Documentation
Consulte a documentação técnica completa: [Referência Técnica](reference.md).
