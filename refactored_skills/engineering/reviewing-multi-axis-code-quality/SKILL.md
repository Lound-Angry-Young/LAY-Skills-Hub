---
name: reviewing-multi-axis-code-quality
description: >
  Conducts multi-axis code review across quality dimensions before a change enters the main branch, covering code written by yourself, another agent or a human, including diffs pasted inline. Use this skill when: asked to review a diff or pull request, or before merging any change. Do NOT use this skill when: the review is about minimalism or over-engineering (use reviewing-code-minimalism).
---

# Revisão de Código Multi-Eixo (Multi-Axis Review)

Executa revisão sistemática de código em cinco eixos de qualidade antes da integração à branch principal: Corretude Funcional, Segurança e Blindagem, Desempenho e Recursos, Operabilidade e Manutenibilidade.

## Input/Output Signature
Input:
- targetDiffOrPrPath: string # Caminho do diff git ou PR a ser inspecionada
- relatedContextFiles: array # Arquivos de contexto e especificações de referência
- qualityAxesToEvaluate: array # Eixos ativados (correctness, security, performance, operability, maintainability)
Output:
- reviewVerdict: string # Parecer final da revisão (approved, changes_requested, blocked)
- axisEvaluations: object # Avaliação detalhada com pontuação e notas por eixo
- blockingDefectsList: array # Lista de defeitos impeditivos com localização exata e sugestão de correção
- reviewSummaryReport: string # Relatório consolidado formatado para o mantenedor

## Router and Selection Matrix
| Eixo de Avaliação | Critério Bloqueante de Rejeição | Grau de Liberdade |
|---|---|---|
| Eixo 1: Corretude e Lógica | Falhas em casos de borda, condições de corrida ou quebra de contratos de tipo | [FRÁGIL] Qualquer bug lógico bloqueia aprovação da mudança |
| Eixo 2: Segurança (AppSec) | Injeção de SQL, XSS, tokens expostos ou validação de entrada ausente | [FRÁGIL] Tolerância zero para falhas mapeadas no OWASP Top 10 |
| Eixo 3: Performance | Consultas N+1, leaks de memória, operações pesadas bloqueando event loop | [FLEXÍVEL] Exige justificativa e correção para regressões mensuráveis |
| Eixo 4: Operabilidade | Falta de logs estruturados em erros, ausência de métricas em novos fluxos | [FLEXÍVEL] Requer visibilidade suficiente para diagnóstico em produção |
| Eixo 5: Manutenibilidade | Complexidade ciclomática excessiva, código duplicado ou nomes enganosos | [FLEXÍVEL] Solicita refatoração para legibilidade e clareza |

## Imperative Execution Workflow
1. Mapear Intenção da Mudança contra Requisitos [FLEXÍVEL]:
   - Confronte o diff contra a especificação da tarefa garantindo que o código faz exatamente o pretendido.
2. Auditar Eixo de Corretude e Casos de Borda [FRÁGIL]:
   - Teste mentalmente entradas vazias, nulas, limites de paginação, concorrência e caminhos de erro.
3. Auditar Eixo de Segurança e Sanitização [FRÁGIL]:
   - Verifique validação de parâmetros, escape de saídas, checagem de autorização e proteção de segredos.
4. Avaliar Impacto em Performance e Recursos [FLEXÍVEL]:
   - Analise complexidade de tempo de execução, consumo de memória e ciclos de renderização desnecessários.
5. Formular Parecer com Sugestões Concretas [FRÁGIL]:
   - Para cada apontamento bloqueante, forneça o trecho exato sugerido de correção pronto para aplicação.

## Execution Checklist
- [ ] Validar conformidade lógica contra a especificação original
- [ ] Checar vetores de segurança e validação de dados de entrada
- [ ] Auditar tempo de resposta, consumo de memória e consultas de banco
- [ ] Confirmar presença de logs e telemetria para suporte em produção
- [ ] Emitir parecer objetivo com correções pontuais sugeridas

## On Failure
- **Gatilho de Erro**: Defeito bloqueante de corretude lógica, vulnerabilidade de segurança ou regressão crítica de desempenho.
- **Ação Imediata**: Emitir parecer `changes_requested` bloqueando o avanço do merge da branch.
- **Rollback**: Não aplicável; a revisão atua como portão de leitura sem modificar código de produção.
- **Fallback**: Realizar sessão de alinhamento com o autor apresentando as correções recomendadas.
- **Logs**: Registrar arquivos inspecionados, lista de violações por eixo e evidências da reprovação.

## Reference Documentation
Consulte a documentação técnica completa: [Referência Técnica](reference.md).
