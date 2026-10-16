---
name: backing-up-cli-data
description: >
  Creates incremental snapshots of local SQLite databases and state data from the OmniRoute CLI, archiving them and syncing to remote storage on demand or on a schedule. Use this skill when: making one-off or scheduled backups of CLI databases and configuration. Do NOT use this skill when: backing up the OmniRoute server databases (use backing-up-omniroute-databases) or restoring a snapshot (use restoring-cli-snapshots).
---

# Backup de Dados e Estado do CLI OmniRoute

Cria cópias de segurança e snapshots incrementais dos bancos SQLite locais, histórico de chamadas e arquivos de configuração do CLI do OmniRoute, com suporte a compressão e sincronização remota.

## Input/Output Signature
Input:
- backupTargetDir: string # Diretório de destino onde os arquivos de snapshot serão salvos
- includeHistoryLogs: boolean # Se deve incluir logs históricos detalhados de requisições (default: true)
- compressArchive: boolean # Se o arquivo gerado deve ser comprimido em gzip/tar (default: true)
Output:
- backupArchiveFilePath: string # Caminho completo do arquivo de backup gerado
- snapshotTimestamp: string # Timestamp ISO 8601 da criação da cópia
- backupSizeBytes: number # Tamanho total do artefato de backup em bytes
- checksumSha256: string # Hash criptográfico SHA-256 para validação de integridade

## Router and Selection Matrix
| Tipo de Operação | Ação Recomendada | Grau de Liberdade |
|---|---|---|
| Snapshot Imediato Pontual | Executa comando `omniroute backup create` capturando estado ativo | [FRÁGIL] Exige trava de escrita curta no SQLite para consistência |
| Backup Completo com Logs | Adiciona flags de inclusão de telemetria e histórico de chamadas | [FLEXÍVEL] Pode aplicar filtros de retenção temporal |
| Verificação Pós-Backup | Calcula hash SHA-256 e testa leitura do cabeçalho do arquivo gerado | [FRÁGIL] Falha se o arquivo estiver corrompido ou truncado |
| Sincronização em Nuvem | Envia artefato para armazenamento remoto configurado | [FLEXÍVEL] Suporta retries com backoff exponencial |

## Imperative Execution Workflow
1. Verificar Estado do Banco SQLite Local [FRÁGIL]:
   - Inspecione a integridade dos arquivos `.sqlite` e `.db` no diretório de dados do CLI usando `PRAGMA integrity_check`.
2. Criar Snapshot Consistente sob Trava [FRÁGIL]:
   - Execute `omniroute backup create --output <backupTargetDir>` garantindo que nenhuma transação concorrente corrompa o arquivo.
3. Comprimir Artefatos de Configuração e Estado [FLEXÍVEL]:
   - Compacte o snapshot e arquivos de credenciais mascaradas em arquivo de extensão `.tar.gz` ou `.bak`.
4. Calcular e Registrar Checksum de Integridade [FRÁGIL]:
   - Gere o hash SHA-256 do arquivo produzido e salve o manifesto correspondente `.sha256`.
5. Validar Gravabilidade e Registrar no Histórico [FLEXÍVEL]:
   - Confirme a presença do arquivo no índice de backups via `omniroute backup list`.

## Execution Checklist
- [ ] Realizar teste de integridade prévio nas tabelas SQLite
- [ ] Executar comando de criação de snapshot
- [ ] Compactar arquivos gerados no diretório de destino
- [ ] Calcular checksum criptográfico SHA-256 do arquivo gerado
- [ ] Registrar o novo backup no inventário de snapshots disponíveis

## On Failure
- **Gatilho de Erro**: Banco corrompido na leitura, espaço em disco insuficiente ou arquivo bloqueado por outro processo.
- **Ação Imediata**: Cancelar a criação do backup e registrar o código de erro retornado.
- **Rollback**: Excluir arquivos de backup parciais e corrompidos criados no diretório de destino.
- **Fallback**: Realizar cópia fria arquivo a arquivo com o processo do OmniRoute pausado temporariamente.
- **Logs**: Registrar caminho do arquivo que falhou, espaço livre em disco e saída detalhada do erro.

## Reference Documentation
Consulte a documentação técnica completa: [Referência Técnica](reference.md).
