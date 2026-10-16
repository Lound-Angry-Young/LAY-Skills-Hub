---
name: architecting-generative-ai-apps
description: >
  Researches implementation patterns for a generative-AI feature by comparing a relevant open-source example: architecture, provider boundaries, costs and tests before adapting any code. Use this skill when: a project needs a generative-AI feature and an existing open-source implementation may serve as reference. Do NOT use this skill when: the project has no generative-AI feature or the work is limited to one provider's API usage with no architecture decision.
---

# Arquitetura de Aplicações com IA Generativa

Pesquisa e estrutura padrões de arquitetura para recursos de IA generativa, avaliando fronteiras de provedores, separação de responsabilidades, trade-offs de custo e latência e suítes de avaliação automatizada.

## Input/Output Signature
Input:
- featureRequirement: string # Descrição da funcionalidade de IA generativa desejada
- targetProvider: string # Provedor inicial pretendido (OpenAI, Anthropic, Gemini, local)
- latencyBudgetMs: number # Orçamento máximo de latência em milissegundos
- costTargetPerCall: number # Custo alvo máximo por requisição
- evaluationCriteria: array # Critérios objetivos de qualidade e acurácia da resposta
Output:
- architecturePattern: string # Padrão selecionado (RAG, loop agêntico, pipeline encadeado, cache semântico)
- providerContract: object # Esquema do adaptador desacoplado do provedor
- costLatencyTradeoff: object # Análise comparativa de latência vs custo por modelo
- evaluationPlan: string # Estratégia de testes de regressão e avaliação contínua

## Router and Selection Matrix
| Condição / Cenário | Ação Recomendada | Grau de Liberdade |
|---|---|---|
| Pipeline RAG / Embeddings | Avalia chunking, cache semântico e busca híbrida | [FLEXÍVEL] Ajusta pesos de similaridade conforme o domínio |
| Loop Agêntico / Tool-Calling | Modela runtime isolado com timeout e limite estrito de iterações | [FRÁGIL] Exige validação de esquema de entrada e saída das ferramentas |
| Abstração Multi-Provedor | Projeta interface canônica desacoplada com chaveamento transparente | [FRÁGIL] Requer contratos canônicos sem vazamento de SDK específico |
| Otimização de Custo | Aplica prompt caching, roteamento em cascata e modelos flash | [FLEXÍVEL] Balanceia precisão semântica com redução de custo |

## Imperative Execution Workflow
1. Delimitar Requisitos e Restrições [FRÁGIL]:
   - Registre dados de entrada e saída, orçamento de latência, teto de custo por chamada e requisitos de privacidade.
2. Analisar Exemplos de Referência [FLEXÍVEL]:
   - Inspecione arquiteturas consolidadas no catálogo de fontes abertas e isole a menor unidade estrutural reutilizável.
3. Definir Fronteiras e Contrato de Provedores [FRÁGIL]:
   - Modele um adaptador agnóstico a provedor com suporte a retries com backoff, circuit breaker e fallback transparente.
4. Estruturar Pipeline de Avaliação e Testes [FRÁGIL]:
   - Defina fixtures com entradas representativas e métricas quantitativas de acurácia antes de escrever o código de produção.
5. Consolidar Documento de Decisão Arquitetural [FLEXÍVEL]:
   - Formalize os trade-offs de custo e latência, detalhando etapas de fatiamento incremental para implementação.

## Execution Checklist
- [ ] Mapear limites de latência, privacidade e custo por requisição
- [ ] Isolar arquitetura do provedor através de adaptadores tipados
- [ ] Configurar políticas de resiliência e failover transparente
- [ ] Definir critérios e fixtures reproduzíveis para avaliação
- [ ] Documentar padrão arquitetural selecionado e trade-offs

## On Failure
- **Gatilho de Erro**: Provedor não atende às metas de latência/custo, quebra de contrato de API ou custos projetados acima do teto orçamentário.
- **Ação Imediata**: Parromper a definição arquitetural e emitir diagnóstico com os limites violados.
- **Rollback**: Descartar rascunhos de interfaces que violem as premissas de custo ou latência.
- **Fallback**: Propor modelos mais leves (flash/lite), cache semântico agressivo ou execução em segundo plano (batch).
- **Logs**: Registrar projeção de tokens, modelos avaliados e limites excedidos para posterior auditoria.
