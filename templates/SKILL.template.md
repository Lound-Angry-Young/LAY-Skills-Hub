---
name: [gerund-name-max-64-chars]
description: >
  [Executa ação especializada em 3ª pessoa, máx 1024 caracteres].
  Use this skill when: [condições exatas de disparo].
  Do NOT use this skill when: [falsos positivos e limites de escopo].
---

## Input/Output Signature
Input:
- targetPath: string # Caminho absoluto ou relativo do recurso alvo
- parameters: object # Parâmetros operacionais e configurações de execução
- dryRun: boolean # Se verdadeiro, executa simulação não destrutiva (default: false)
Output:
- success: boolean # Indica se a operação foi executada com êxito
- status: string # Estado final (completed, failed, skipped)
- artifacts: array # Lista de arquivos ou dados gerados
- executionLog: string # Registro de saída e diagnóstico

## Router and Selection Matrix
| Condição / Cenário | Ação Recomendada | Grau de Liberdade |
|---|---|---|
| Cenário Principal | Executa fluxo padrão da habilidade | [FLEXÍVEL] Aplica heurísticas de decisão |
| Operação Sensível | Valida pré-condições estritas antes de aplicar mudanças | [FRÁGIL] Requer comandos e flags exatos |
| Modo Diagnóstico | Inspeciona estado sem aplicar mutações | [FLEXÍVEL] Modo seguro de leitura |

## Imperative Execution Workflow
1. Validar Pré-Requisitos [FRÁGIL]: Inspecione o ambiente alvo e garanta a existência de `targetPath` e dependências.
2. Analisar Contexto e Parâmetros [FLEXÍVEL]: Avalie os argumentos e delimite o escopo atômico de execução.
3. Executar Ação Central [FRÁGIL]: Dispare o comando exato ou procedimento operacional.
4. Validar Consistência e Integridade [FRÁGIL]: Confirme que os contratos e arquivos gerados estão válidos.
5. Consolidar Resultado [FLEXÍVEL]: Formate a resposta e retorne a assinatura de I/O estruturada.

## Execution Checklist
- [ ] Validar arquivos de entrada e permissões
- [ ] Configurar parâmetros operacionais e flags
- [ ] Disparar a rotina atômica
- [ ] Inspecionar integridade dos artefatos produzidos
- [ ] Registrar logs de auditoria e status final

## On Failure
- **Gatilho de Erro**: Falha de pré-condições, erro de sintaxe, exceção em tempo de execução ou timeout.
- **Ação Imediata**: Interromper o processo imediatamente para evitar corrupção de estado.
- **Rollback**: Restaurar arquivos modificados para o estado anterior.
- **Fallback**: Notificar o orquestrador com a mensagem exata do erro e sugerir rota de contingência.
- **Logs**: Registrar stack trace detalhado e parâmetros de entrada.

## Reference Documentation
<!-- Incluir apenas se houver código/template > 100 linhas extraído para reference.md -->
Consulte a documentação técnica detalhada: [Referência Técnica](reference.md).
