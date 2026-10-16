---
name: restoring-cli-snapshots
description: >
  Restores backup files and database snapshots into the local CLI runtime, with a pre-restore integrity check and a safety rollback. Use this skill when: recovering CLI databases after corruption or syncing an instance from an archived snapshot. Do NOT use this skill when: creating backups (use backing-up-cli-data) or restoring the OmniRoute server (use restoring-omniroute-databases).
---

# Restauração de Snapshots do CLI OmniRoute

Restaura bancos de dados SQLite e arquivos de estado do CLI do OmniRoute a partir de snapshots de backup, executando validação prévia de integridade e mantendo ponto de restauração para reversão segura.

## Input/Output Signature
Input:
- snapshotArchiveFilePath: string # Caminho completo do arquivo de backup a ser restaurado
- targetDataDir: string # Diretório de dados de destino do runtime local
- forceOverwrite: boolean # Se deve sobrescrever o estado atual sem confirmação interativa (default: false)
Output:
- restoreSuccess: boolean # Status da operação de restauração
- restoredTimestamp: string # Timestamp do snapshot que foi aplicado
- safetyBackupFilePath: string # Caminho da cópia de segurança criada antes da restauração
- executionLog: string # Registro dos passos executados e validações estruturais

## Router and Selection Matrix
| Cenário de Restauração | Ação Recomendada | Grau de Liberdade |
|---|---|---|
| Recuperação Pós-Corrupção | Valida integridade do snapshot antes de substituir dados corrompidos | [FRÁGIL] Exige validação estrita de checksum antes da descompactação |
| Sincronização entre Ambientes | Aplica snapshot criando ponto de restauração do estado local prévio | [FRÁGIL] Obrigatório gerar snapshot de segurança antes da mutação |
| Modo Simulação (Dry-Run) | Inspeciona tabelas e versões do snapshot sem alterar arquivos em disco | [FLEXÍVEL] Modo seguro de leitura para conferência de esquemas |
| Reversão Imediata (Rollback) | Restaura cópia de segurança após falha em migração ou integridade | [FRÁGIL] Execução atômica de troca de arquivos |

## Imperative Execution Workflow
1. Validar Checksum e Integridade do Arquivo de Backup [FRÁGIL]:
   - Verifique o hash SHA-256 do arquivo `snapshotArchiveFilePath` contra o manifesto gravado na criação.
2. Criar Cópia de Segurança do Estado Local Atual [FRÁGIL]:
   - Faça uma cópia atômica dos bancos SQLite ativos em `targetDataDir` para um arquivo temporário de segurança.
3. Desconectar Processos Ativos e Travar Bancos [FRÁGIL]:
   - Assegure que nenhuma instância CLI do OmniRoute esteja gravando nos bancos durante o procedimento.
4. Descompactar e Aplicar Snapshot de Dados [FRÁGIL]:
   - Execute `omniroute backup restore <snapshotArchiveFilePath>` substituindo as tabelas e arquivos de configuração.
5. Executar Verificação de Integridade Pós-Restauração [FRÁGIL]:
   - Rode `PRAGMA integrity_check` nos bancos restaurados e teste a leitura de chaves e histórico de configurações.

## Execution Checklist
- [ ] Validar integridade e assinatura do arquivo de snapshot
- [ ] Gerar backup de segurança dos dados locais atuais
- [ ] Garantir ausência de processos concorrentes travando os bancos
- [ ] Aplicar restauração de tabelas e arquivos de estado
- [ ] Validar integridade estrutural pós-restauração

## On Failure
- **Gatilho de Erro**: Falha no checksum do arquivo, corrupção de schema detectada no `PRAGMA` ou erro ao descompactar.
- **Ação Imediata**: Abortar o procedimento de restauração imediatamente.
- **Rollback**: Restaurar o estado local anterior a partir da cópia de segurança criada no passo 2.
- **Fallback**: Notificar o usuário com a lista de snapshots íntegros disponíveis no repositório local.
- **Logs**: Registrar o erro exato de validação, hash esperado vs obtido e arquivos impactados.

## Reference Documentation
Consulte a documentação técnica completa: [Referência Técnica](reference.md).
