---
name: orchestrating-staged-rollouts
description: >
  Orchestrates gradual production releases with canary traffic, active monitoring of error metrics and instant rollback triggers. Use this skill when: releasing a new version to a subset of users or monitoring the stability of live traffic. Do NOT use this skill when: running the pre-launch checklist (use verifying-prelaunch-readiness) or a full CD pipeline (use automating-cd-deployments).
---

# Orquestração de Implantações Graduais e Canary

Orquestra lançamentos graduais de versões em produção através de divisão percentual de tráfego (canary), monitorando taxas de erro em tempo real e aplicando reversão imediata em caso de anomalia.

## Input/Output Signature
Input:
- candidateReleaseTag: string # Tag da versão candidata a ser avaliada em tráfego real
- rolloutSteps: array # Escalonamento de percentual de tráfego (ex: [5, 25, 50, 100])
- soakTimeMinutesPerStep: number # Tempo de observação em minutos para cada degrau de tráfego
- maxToleratedErrorRatePercent: number # Taxa máxima aceitável de erros HTTP 5xx (default: 0.5)
Output:
- rolloutCompleted: boolean # Indica se a versão candidata atingiu 100% com sucesso
- currentActiveTrafficPercent: number # Percentual de tráfego ativo na nova versão
- observedErrorRatePercent: number # Taxa real de erros observada durante a janela
- executionLog: string # Histórico das etapas de escalonamento e telemetria

## Router and Selection Matrix
| Degrau de Tráfego / Cenário | Ação Recomendada | Grau de Liberdade |
|---|---|---|
| Canary Inicial (5% a 10%) | Roteia tráfego restrito e monitora telemetria básica e logs de exceção | [FRÁGIL] Exige validação estrita dos primeiros minutos de requisições |
| Escalonamento Intermediário (25% a 50%) | Aumenta carga e avalia saturação de banco de dados e latência p95/p99 | [FLEXÍVEL] Permite ajuste do tempo de observação conforme estabilidade |
| Promoção Plena (100%) | Roteia a totalidade do tráfego e desativa versão anterior após estabilização | [FRÁGIL] Requer confirmação de ausência de regressões acumuladas |
| Pico de Erros ou Latência | Zera o tráfego do canary imediatamente e aciona reversão | [FRÁGIL] Reversão incondicional ao ultrapassar o limite de erros |

## Imperative Execution Workflow
1. Configurar Regras de Roteamento de Tráfego [FRÁGIL]:
   - Defina o split inicial de tráfego (ex: 5%) no balanceador de carga ou gateway da aplicação.
2. Monitorar Métricas de Saúde e Taxa de Erros [FRÁGIL]:
   - Colete métricas de códigos HTTP 5xx, saturação de memória e latência p99 ao longo do tempo estipulado.
3. Avaliar Critérios de Aceite do Degrau [FRÁGIL]:
   - Se a taxa de erros permanecer abaixo de `maxToleratedErrorRatePercent`, aprove a transição para o próximo nível.
4. Incrementar Percentual de Tráfego Progressivamente [FLEXÍVEL]:
   - Avance os degraus subsequentes (25%, 50%, 100%) respeitando os intervalos de observação definidos.
5. Consolidar Release e Descomissionar Versão Antiga [FRÁGIL]:
   - Ao atingir 100% de estabilidade comprovada, marque o release como definitivo e encerre o monitoramento canary.

## Execution Checklist
- [ ] Estabelecer limite máximo tolerado de taxa de erros e latência
- [ ] Iniciar roteamento no menor degrau de tráfego estabelecido
- [ ] Monitorar logs de exceção e métricas de desempenho em tempo real
- [ ] Validar estabilidade antes de avançar cada degrau de tráfego
- [ ] Concluir migração integral ou executar corte imediato do canary

## On Failure
- **Gatilho de Erro**: Taxa de erros HTTP 5xx excedendo o limite estipulado, regressão crítica de latência p99 ou crash de pods.
- **Ação Imediata**: Retornar o roteamento de tráfego para 0% no canary imediatamente.
- **Rollback**: Restaurar 100% do tráfego para a versão anterior estável no balanceador de carga.
- **Fallback**: Isolar a versão defeituosa para depuração em ambiente fechado de staging.
- **Logs**: Registrar série temporal de erros observados, volume de requisições afetadas e stack traces capturados.

## Reference Documentation
Consulte a documentação técnica completa: [Referência Técnica](reference.md).
