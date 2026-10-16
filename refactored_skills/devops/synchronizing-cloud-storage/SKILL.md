---
name: synchronizing-cloud-storage
description: >
  Synchronizes OmniRoute configuration, provider connections and settings to and from cloud storage, managing cloud worker authentication and remote backup targets. Use this skill when: syncing OmniRoute configuration to cloud storage or configuring remote backup targets. Do NOT use this skill when: taking local database backups (use backing-up-omniroute-databases).
---

# Sincronização de Configurações em Nuvem

Sincroniza conexões de provedores, configurações globais e backups do OmniRoute com repositórios de armazenamento em nuvem, garantindo integridade criptográfica e replicação entre instâncias.

## Input/Output Signature
Input:
- syncDirection: string # Direção da sincronização (push_to_cloud, pull_from_cloud)
- storageTargetName: string # Nome do destino configurado (s3, cloudflare_r2, gcs, custom)
- encryptPayload: boolean # Se os dados exportados devem ser criptografados antes do upload (default: true)
Output:
- syncStatus: string # Estado final da operação (synced, aborted, auth_error)
- uploadedObjectsCount: number # Quantidade de arquivos sincronizados com a nuvem
- lastSyncTimestamp: string # Timestamp ISO 8601 da operação
- executionLog: string # Registro cronológico detalhado da transferência

## Router and Selection Matrix
| Direção da Sincronização | Ação Recomendada | Grau de Liberdade |
|---|---|---|
| Upload para Nuvem (Push) | Criptografa configurações locais e envia snapshot para o bucket remoto | [FRÁGIL] Exige máscara obrigatória de segredos e checagem de hash |
| Download da Nuvem (Pull) | Baixa snapshot remoto, valida assinatura e mescla configurações | [FRÁGIL] Requer snapshot de segurança local antes de sobrescrever |
| Validação de Conexão Remota | Testa leitura e escrita de arquivo temporário de probe no bucket | [FLEXÍVEL] Valida permissões e credenciais de acesso à nuvem |
| Resolução de Conflitos | Preserva versão com timestamp mais recente sob confirmação explícita | [FRÁGIL] Bloqueia sobrescrita cega em caso de divergência simultânea |

## Imperative Execution Workflow
1. Validar Credenciais de Armazenamento Remoto [FRÁGIL]:
   - Inspecione chaves de acesso, endpoints e permissões de escrita no provedor de armazenamento selecionado.
2. Preparar Manifesto e Criptografar Dados [FRÁGIL]:
   - Exporte as configurações ativas e aplique criptografia de envelope nas credenciais de provedores de IA.
3. Disparar Sincronização de Objetos [FLEXÍVEL]:
   - Execute o procedimento de upload ou download com suporte a retries automáticos em caso de oscilação de rede.
4. Validar Hashes e Integridade da Transferência [FRÁGIL]:
   - Compare o checksum SHA-256 dos dados locais com o metadado gravado no objeto em nuvem.
5. Atualizar Marcador de Sincronização Local [FLEXÍVEL]:
   - Grave o timestamp da última sincronização bem-sucedida no inventário de estado do sistema.

## Execution Checklist
- [ ] Validar credenciais de acesso ao bucket ou worker remoto
- [ ] Criptografar dados sensíveis antes da transmissão
- [ ] Executar transferência monitorando integridade de rede
- [ ] Verificar checksum dos artefatos transmitidos
- [ ] Atualizar registro de sincronização no sistema local

## On Failure
- **Gatilho de Erro**: Falha de autenticação no provedor de nuvem, divergência de checksum no download ou timeout de rede.
- **Ação Imediata**: Cancelar a transferência e abortar qualquer alteração nos dados locais.
- **Rollback**: Restaurar cópia de segurança local prévia caso um download parcial tenha corrompido arquivos.
- **Fallback**: Manter operações em modo local desconectado até reestabelecimento da conectividade de rede.
- **Logs**: Registrar endpoint do provedor de nuvem, código de erro retornado e arquivos afetados.

## Reference Documentation
Consulte a documentação técnica completa: [Referência Técnica](reference.md).
