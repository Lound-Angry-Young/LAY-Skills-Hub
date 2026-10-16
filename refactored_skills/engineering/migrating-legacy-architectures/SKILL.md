---
name: migrating-legacy-architectures
description: >
  Migrates database schemas, architecture flows and infrastructure dependencies with expand/contract patterns and no downtime, including subsystem rewrites and shifting production traffic. Use this skill when: migrating data schemas, rewriting subsystems or moving production traffic without unavailability. Do NOT use this skill when: only marking methods with deprecation warnings without a physical migration (use deprecating-obsolete-apis).
---

# Migração Segura de Arquiteturas Legadas (Expand/Contract)

Executa migrações de arquitetura, esquemas de banco de dados e substituição de subsistemas legados sem tempo de inatividade (zero-downtime), aplicando padrões de expansão e contração, escrita dupla e tráfego espelho.

## Input/Output Signature
Input:
- legacySubsystemName: string # Identificador do serviço ou tabela legado a ser substituído
- targetModernSubsystemName: string # Identificador da nova implementação de destino
- migrationPhase: string # Fase atual da migração (expand, double_write, backfill, contract)
- trafficCutoverPercentage: number # Percentual de leitura roteado para o novo sistema
Output:
- migrationPlanStatus: string # Estado do ciclo de migração
- dualWriteVerified: boolean # Confirmação de integridade e equivalência de dados entre sistemas
- backfillProgressPercent: number # Percentual de dados históricos já reconciliados
- executionLog: string # Registro dos procedimentos de transição e validações

## Router and Selection Matrix
| Fase da Migração | Estratégia de Execução | Grau de Liberdade |
|---|---|---|
| Fase 1: Expandir (Expand) | Cria novas tabelas ou rotas em paralelo mantendo suporte à interface antiga | [FRÁGIL] Proibido remover campos ou alterar assinaturas existentes |
| Fase 2: Escrita Dupla (Double-Write) | Grava simultaneamente no banco antigo e no novo com tratamento de falhas | [FRÁGIL] Garante sincronia atômica sem impactar a latência do usuário |
| Fase 3: Backfill Histórico | Reconcilia dados passados em segundo plano com validação de checksums | [FLEXÍVEL] Ajusta taxa de migração por lotes para não saturar IO |
| Fase 4: Contrair (Contract) | Remove o subsistema legado após confirmação de 100% de tráfego estável | [FRÁGIL] Exige validação de ausência absoluta de leituras no legado |

## Imperative Execution Workflow
1. Desenhar Estratégia de Expansão sem Quebra [FRÁGIL]:
   - Adicione novas colunas como opcionais (nullable) e crie novos endpoints sem alterar contratos vigentes.
2. Habilitar Escrita Dupla com Isolamento de Erros [FRÁGIL]:
   - Configure a persistência para gravar no sistema primário legado e assincronamente no novo repositório.
3. Executar Carga Histórica em Lotes (Backfill) [FLEXÍVEL]:
   - Dispare rotinas de migração de registros antigos com controle de taxa e relatórios de discrepâncias.
4. Rotear Tráfego de Leitura Gradualmente [FRÁGIL]:
   - Direcione porcentagens de leitura via feature flag, comparando respostas em modo sombra (shadow-read).
5. Contrair Arquitetura e Limpar Código Morto [FRÁGIL]:
   - Após estabilização total, desative a escrita dupla, desmonte tabelas obsoletas e elimine shims legados.

## Execution Checklist
- [ ] Aplicar novas estruturas preservando total retrocompatibilidade
- [ ] Implementar e validar mecanismo de escrita dupla
- [ ] Concluir reconciliação e validação dos dados históricos
- [ ] Migrar leituras gradualmente através de tráfego sombra e canary
- [ ] Executar contração segura com remoção de dependências legadas

## On Failure
- **Gatilho de Erro**: Divergência de dados entre legado e novo sistema, perda de sincronia na escrita dupla ou aumento de latência.
- **Ação Imediata**: Suspender a virada de tráfego e retornar leituras para o sistema legado imediatamente.
- **Rollback**: Desativar a escrita dupla para o novo sistema preservando a integridade do banco legado.
- **Fallback**: Manter o subsistema legado como autoritativo até reanálise das regras de reconciliação de dados.
- **Logs**: Registrar IDs de registros divergentes, percentual de discrepâncias e latência comparada.

## Reference Documentation
Consulte a documentação técnica completa: [Referência Técnica](reference.md).
