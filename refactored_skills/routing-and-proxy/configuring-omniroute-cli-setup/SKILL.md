---
name: configuring-omniroute-cli-setup
description: >
  Runs initial OmniRoute setup, configures global CLI settings, manages environment variables, checks for updates and configures autostart through the CLI setup and config commands. Use this skill when: installing or first-configuring the OmniRoute CLI or changing its global settings. Do NOT use this skill when: changing application settings through the API (use configuring-omniroute-settings).
---

# Configuração Inicial e Gerenciamento do OmniRoute CLI

Executa o provisionamento inicial, parametrização global, variáveis de ambiente, verificação de atualizações e inicialização automática do OmniRoute através de sua interface de linha de comando.

## Input/Output Signature
Input:
- setupCommandAction: string # Ação a executar (init, autostart, env, update, status)
- serverListenPort: number # Porta configurada para o servidor OmniRoute (default: 20128)
- enableAutostart: boolean # Se deve registrar o serviço na inicialização do sistema operacional
- environmentOverrides: object # Dicionário de variáveis de ambiente a gravar na configuração
Output:
- cliSetupSuccess: boolean # Status da configuração do CLI
- activeConfigPath: string # Caminho do arquivo de configuração global utilizado
- daemonAutostartRegistered: boolean # Confirmação de registro no inicializador do SO
- executionLog: string # Registro dos comandos CLI executados

## Router and Selection Matrix
| Ação de Setup | Comando CLI Recomendado | Grau de Liberdade |
|---|---|---|
| Inicialização Limpa (First-Time Setup) | Executa `omniroute setup` gerando diretórios e arquivos de configuração | [FRÁGIL] Exige criação de diretórios de dados com permissões corretas |
| Habilitação de Autostart no Boot | Executa `omniroute autostart enable` criando serviço de sistema ou atalho | [FRÁGIL] Registra inicializador conforme o sistema operacional (Windows/Linux/macOS) |
| Ajuste de Variáveis de Ambiente | Executa `omniroute env set KEY=VALUE` gravando no arquivo de configuração local | [FLEXÍVEL] Valida sintaxe antes de persistir chaves e portas |
| Verificação de Atualizações | Executa `omniroute update --check` comparando versão instalada e upstream | [FLEXÍVEL] Relata changelog e orienta comando de atualização |

## Imperative Execution Workflow
1. Verificar Presença e Permissões do CLI [FRÁGIL]:
   - Confirme a acessibilidade do binário `omniroute` no PATH do sistema operacional.
2. Criar ou Atualizar Arquivo de Configuração Global [FRÁGIL]:
   - Execute o procedimento de inicialização criando diretórios em `%APPDATA%\omniroute` ou `~/.omniroute`.
3. Injetar Variáveis Operacionais e Portas [FLEXÍVEL]:
   - Defina porta de escuta, caminhos de banco de dados e modo de operação (local ou compartilhado).
4. Configurar Autostart e Registro de Sistema [FRÁGIL]:
   - Quando solicitado, crie atalho na pasta Inicializar do Windows ou serviço de inicialização headless.
5. Validar Execução com Comando de Diagnóstico [FRÁGIL]:
   - Execute `omniroute status` para confirmar que as configurações foram lidas com êxito pelo runtime.

## Execution Checklist
- [ ] Checar disponibilidade do binário omniroute no ambiente
- [ ] Inicializar diretório de configuração e banco de dados local
- [ ] Configurar porta de comunicação e parâmetros de ambiente
- [ ] Registrar autostart no sistema operacional se requerido
- [ ] Confirmar leitura correta através de comando de status

## On Failure
- **Gatilho de Erro**: Falha de permissão para gravar no diretório de configuração, porta ocupada ou erro de registro de serviço.
- **Ação Imediata**: Parar a rotina de setup e reportar a causa do bloqueio de escrita.
- **Rollback**: Restaurar arquivos de configuração anteriores em caso de corrupção.
- **Fallback**: Executar OmniRoute em modo portable apontando diretório de dados para pasta do usuário local.
- **Logs**: Registrar caminho do arquivo de configuração, código de saída e stderr emitido pelo CLI.

## Reference Documentation
Consulte a documentação técnica completa: [Referência Técnica](reference.md).
