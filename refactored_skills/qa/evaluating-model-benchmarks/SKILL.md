---
name: evaluating-model-benchmarks
description: >
  Creates and runs evaluation suites, watches live benchmark progress, views scorecards, compares model performance and integrates eval runs with CI workflows from the CLI. Use this skill when: benchmarking or comparing models through evaluation suites. Do NOT use this skill when: only checking that a model is reachable or configured (use querying-models-via-cli).
---

# Avaliação e Benchmarking de Modelos de IA

Cria, executa e analisa suítes de avaliação automatizada (evals) de modelos de linguagem a partir do CLI do OmniRoute, comparando métricas de acurácia, latência, custos e aderência a contratos.

## Input/Output Signature
Input:
- evalSuiteConfigPath: string # Caminho do arquivo de configuração da suíte de avaliação (ex: promptfooconfig.yaml)
- candidateModelsList: array # Modelos de IA a serem submetidos ao benchmark (ex: gpt-4o, claude-3-5-sonnet, gemini-1.5-pro)
- targetMetricThresholds: object # Metas mínimas de pontuação (pass_rate > 95%, max_cost, max_latency_ms)
Output:
- benchmarkCompleted: boolean # Status da execução do benchmark
- modelScorecardComparison: object # Matriz comparativa de notas, tempos de resposta e custos por modelo
- winningModelRecommendation: string # Modelo com melhor equilíbrio de acurácia, custo e velocidade
- executionLog: string # Registro dos testes executados e relatórios consolidados

## Router and Selection Matrix
| Objetivo da Avaliação | Estratégia de Benchmark | Grau de Liberdade |
|---|---|---|
| Comparação de Qualidade e Acurácia | Executa bateria de casos de teste com asserções semânticas e exatas | [FLEXÍVEL] Avalia conformidade contra respostas de referência |
| Auditoria de Latência e Throughput | Dispara requisições simultâneas medindo percentis p50, p95 e p99 | [FRÁGIL] Exige amostragem estatística consistente com múltiplos disparos |
| Otimização de Custos de Inferência | Compara consumo de tokens de entrada e saída e custo financeiro por tarefa | [FRÁGIL] Calcula custo total projetado para escala de produção |
| Integração com Pipeline de CI | Executa avaliação em modo headless e reprova pipeline se a nota cair | [FRÁGIL] Bloqueia merges caso o candidato cometa regressão de qualidade |

## Imperative Execution Workflow
1. Inspecionar Casos de Teste e Asserções da Suíte [FRÁGIL]:
   - Valide se o arquivo de configuração define variáveis representativas, prompts de teste e critérios de validação.
2. Configurar Modelos Candidatos e Credenciais [FRÁGIL]:
   - Assegure que as conexões e chaves para todos os provedores em `candidateModelsList` estejam ativas no OmniRoute.
3. Disparar Comando de Avaliação via CLI [FLEXÍVEL]:
   - Execute `omniroute eval run --config <evalSuiteConfigPath>` acompanhando a barra de progresso e streaming.
4. Compilar Cartão de Pontuação (Scorecard) [FRÁGIL]:
   - Extraia métricas de taxa de acerto (pass rate), latência média, variabilidade e consumo total de tokens.
5. Formular Parecer Técnico com Seleção de Modelo [FLEXÍVEL]:
   - Recomende o modelo ideal fundamentado nos trade-offs medidos para o caso de uso avaliado.

## Execution Checklist
- [ ] Validar arquivo de casos de teste e critérios de pontuação da suíte
- [ ] Confirmar conectividade e saldo com os provedores avaliados
- [ ] Disparar execução da suíte de benchmarking pelo CLI
- [ ] Compilar matriz de comparação de acurácia, velocidade e custo
- [ ] Emitir parecer conclusivo com recomendação fundamentada

## On Failure
- **Gatilho de Erro**: Provedor fora do ar durante o benchmark, taxa de aprovação abaixo do limiar estipulado ou esgotamento de quota.
- **Ação Imediata**: Pausar a execução da suíte e registrar os modelos que falharam.
- **Rollback**: Não há alteração de estado em produção por ser rotina consultiva de testes.
- **Fallback**: Repetir testes isolados dos modelos reprovados ou comutar para outro provedor equivalente.
- **Logs**: Registrar casos de teste reprovados, respostas reais obtidas e motivos de desqualificação.

## Reference Documentation
Consulte a documentação técnica completa: [Referência Técnica](reference.md).
