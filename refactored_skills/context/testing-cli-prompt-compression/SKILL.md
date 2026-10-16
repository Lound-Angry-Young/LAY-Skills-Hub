---
name: testing-cli-prompt-compression
description: >
  Configures and tests prompt compression from the CLI: manages RTK filters and Caveman rules, stacked compression modes, and previews compression output with real prompts. Use this skill when: testing or previewing compression from the terminal. Do NOT use this skill when: configuring compression through the API (use configuring-prompt-compression).
---

# Teste de Compressão de Prompts via CLI

Avalia e testa rotinas de compressão de prompts na interface de linha de comando do OmniRoute, comparando taxas de redução de tokens e verificando a integridade de termos técnicos.

## Input/Output Signature
Input:
- promptSampleText: string # Texto representativo de prompt para o teste de compressão
- compressionMode: string # Modo a ser avaliado (rtk, caveman, stacked)
- targetReductionPercent: number # Meta mínima percentual de redução de tokens esperada (default: 50)
- criticalTokensToPreserve: array # Lista de termos, caminhos ou erros que devem permanecer intactos
Output:
- initialTokenCount: number # Quantidade de tokens no prompt original
- compressedTokenCount: number # Quantidade de tokens após compressão
- achievedReductionPercent: number # Percentual real de redução alcançado
- compressedOutputText: string # Texto final resultante da compressão
- isIntegrityPreserved: boolean # Confirmação de que nenhum termo crítico foi corrompido

## Router and Selection Matrix
| Condição / Cenário | Ação Recomendada | Grau de Liberdade |
|---|---|---|
| Teste de Saída de Ferramentas / Logs | Executa teste com perfil RTK focado em comandos e stacks | [FRÁGIL] Exige validação estrita de integridade de mensagens de erro |
| Teste de Linguagem Natural / Chat | Executa teste com perfil Caveman avaliando brevidade e clareza | [FLEXÍVEL] Tolera omissão de palavras estruturais mantendo o sentido |
| Teste de Compressão Combinada | Avalia modo stacked para máxima redução em pipelines pesados | [FRÁGIL] Requer conferência minuciosa contra perda de contexto |
| Verificação de Regressão Semântica | Compara texto original e comprimido contra lista de tokens protegidos | [FRÁGIL] Qualquer remoção de token protegido invalida o teste |

## Imperative Execution Workflow
1. Preparar Amostra de Teste Realista [FLEXÍVEL]:
   - Selecione um prompt representativo que contenha código, chamadas de ferramentas ou saídas de terminal reais.
2. Executar Comando CLI de Prévia de Compressão [FRÁGIL]:
   - Execute o comando `omniroute compress test --mode <compressionMode>` fornecendo a amostra de prompt.
3. Mensurar Métricas de Consumo de Tokens [FRÁGIL]:
   - Calcule a redução absoluta e percentual comparando a contagem inicial com o resultado comprimido.
4. Auditar Preservação de Termos Críticos [FRÁGIL]:
   - Verifique que caminhos de arquivos, números de porta, variáveis e mensagens de erro permaneçam íntegros.
5. Gerar Relatório Comparativo [FLEXÍVEL]:
   - Apresente a saída original e comprimida lado a lado com parecer objetivo de aprovação ou necessidade de ajuste.

## Execution Checklist
- [ ] Carregar prompt representativo com dados técnicos reais
- [ ] Disparar rotina de teste de compressão via CLI
- [ ] Mensurar contagem e proporção de tokens economizados
- [ ] Conferir integridade integral dos termos críticos protegidos
- [ ] Emitir relatório com parecer de aprovação ou reprovação

## On Failure
- **Gatilho de Erro**: Supressão de termos críticos protegidos, distorção do sentido semântico ou economia abaixo da meta mínima.
- **Ação Imediata**: Reprovar o perfil de compressão avaliado para aquela classe de prompts.
- **Rollback**: Não há alteração de estado no sistema por se tratar de rotina de teste.
- **Fallback**: Sugerir perfil de compressão mais brando (`lite`) ou incluir exceções nas regras de filtragem.
- **Logs**: Registrar o prompt de teste, a saída comprimida rejeitada e a lista de termos corrompidos.

## Reference Documentation
Consulte a documentação técnica completa: [Referência Técnica](reference.md).
