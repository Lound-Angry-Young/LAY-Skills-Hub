---
name: inspecting-resilience-circuits
description: >
  Inspects and manages circuit-breaker states, connection cooldowns, quota limits and backoff levels from the CLI, resets stuck providers and configures resilience thresholds. Use this skill when: a provider is stuck in cooldown or an open circuit must be reset or retuned. Do NOT use this skill when: only monitoring latency and health trends (use monitoring-omniroute-resilience).
---

# Inspeção e Gestão de Circuit Breakers e Resiliência via CLI

Inspeciona e gerencia o estado dos disjuntores de circuito (circuit breakers), períodos de cooldown, limites de quota e níveis de backoff a partir da interface de linha de comando do OmniRoute, com reset manual de provedores travados.

## Input/Output Signature
Input:
- managementAction: string # Ação a executar (status, reset, cooldown_clear, tune_thresholds)
- providerTargetId: string # Identificador do provedor alvo da intervenção
- failureThresholdOverrides: object # Limites numéricos para abertura de circuito (ex: consecutive_failures: 5)
Output:
- circuitBreakerStatus: string # Estado do disjuntor (closed, open, half_open)
- activeCooldownSecondsRemaining: number # Tempo residual de cooldown antes de nova tentativa
- resetOperationSuccess: boolean # Confirmação de que o estado do circuito foi zerado
- executionLog: string # Registro dos comandos executados

## Router and Selection Matrix
| Estado do Circuito / Cenário | Ação Recomendada | Grau de Liberdade |
|---|---|---|
| Disjuntor Aberto (Open / Cooldown) | Inspeciona motivo da abertura e taxa de falhas recentes | [FRÁGIL] Exige validação da saúde do provedor antes de resetar |
| Reset Manual de Provedor Travado | Executa `omniroute quota reset <providerId>` para reabrir tráfego | [FRÁGIL] Força transição controlada para estado half-open |
| Ajuste de Sensibilidade de Falhas | Modifica tolerância de falhas consecutivas antes de desarmar o circuito | [FLEXÍVEL] Balanceia proteção contra tráfego inútil e tolerância a ruído |
| Listagem de Circuitos do Sistema | Executa `omniroute quota` exibindo tabela completa de estados | [FLEXÍVEL] Visão panorâmica de todos os provedores em tempo real |

## Imperative Execution Workflow
1. Listar Estados dos Circuitos no Sistema [FRÁGIL]:
   - Execute `omniroute quota` para identificar quais provedores estão em estado de cooldown ou circuito aberto.
2. Identificar Causa-Raiz das Falhas Consecutivas [FLEXÍVEL]:
   - Analise se o desarme ocorreu por erro 429 de quota, erro 500 do provedor ou timeout de rede.
3. Testar Conectividade com o Provedor [FRÁGIL]:
   - Dispare chamada de teste isolada para assegurar que a instabilidade do provedor upstream já cessou.
4. Executar Reset Controlado do Disjuntor [FRÁGIL]:
   - Execute o subcomando CLI de reset para zerar o contador de falhas e recolocar o circuito em operação.
5. Confirmar Retorno de Tráfego sem Regressão [FLEXÍVEL]:
   - Monitore as primeiras requisições pós-reset garantindo que não ocorra reabertura imediata do circuito.

## Execution Checklist
- [ ] Inspecionar estados dos disjuntores de todos os provedores
- [ ] Avaliar a causa das falhas consecutivas que abriram o circuito
- [ ] Executar probe de teste antes de forçar o reset manual
- [ ] Disparar o comando de reset no provedor alvo
- [ ] Validar transição bem-sucedida para estado fechado (closed)

## On Failure
- **Gatilho de Erro**: Provedor continua falhando pós-reset e reabre o circuito imediatamente, ou comando CLI rejeitado.
- **Ação Imediata**: Manter o provedor em cooldown para evitar consumo inútil de retries.
- **Rollback**: Reabilitar o cooldown caso tenha sido desativado prematuramente.
- **Fallback**: Desviar o tráfego do provedor problemático reconfigurando o combo de roteamento.
- **Logs**: Registrar histórico de falhas consecutivas, timestamp da abertura e respostas recebidas do upstream.

## Reference Documentation
Consulte a documentação técnica completa: [Referência Técnica](reference.md).
