---
name: optimizing-vercel-deployments
description: >
  Optimizes the cost and performance of deployed Vercel projects, especially Next.js, SvelteKit, Nuxt and limited Astro apps, by collecting Vercel metrics, usage, project configuration and code scan results. Use this skill when: reducing Vercel cost or improving the performance of a deployed project. Do NOT use this skill when: performing the deployment itself (use deploying-to-vercel-platform).
---

# Otimização de Custos e Performance na Vercel

Analisa métricas de produção, tempos de resposta, consumo de funções serverless, estratégias de cache (ISR/Edge) e peso de bundles para reduzir faturas e acelerar aplicações na Vercel.

## Input/Output Signature
Input:
- projectConfigPath: string # Caminho dos arquivos de configuração (next.config.js, vercel.json)
- targetMetricFocus: string # Foco principal (cost_reduction, cold_start_speed, bandwidth_saving)
- bundleAnalysisReportPath: string # Caminho opcional do relatório do bundle analyzer
Output:
- optimizationPlan: array # Lista de ações recomendadas com impacto estimado em custo e latência
- cachingStrategies: object # Diretrizes de cabeçalhos de cache, stale-while-revalidate e ISR
- functionSizingDirectives: object # Ajustes recomendados de alocação de memória e timeout para serverless
- executionLog: string # Registro da auditoria das configurações atuais

## Router and Selection Matrix
| Foco de Otimização | Ação Recomendada | Grau de Liberdade |
|---|---|---|
| Redução de Custos Serverless | Converte rotas dinâmicas frequentes para ISR ou Static Site Generation | [FLEXÍVEL] Aplica revalidação incremental periódica |
| Otimização de Cold Start | Reduz alocação de memória excessiva e remove dependências pesadas de rotas | [FRÁGIL] Exige benchmark de latência antes e depois do ajuste |
| Economia de Largura de Banda | Ativa compressão moderna de imagens e otimiza fontes nativas via CDN | [FLEXÍVEL] Limita formatos permitidos e domínios remotos |
| Execução em Edge Runtime | Move funções leves de autenticação e redirecionamento para o Edge | [FRÁGIL] Requer compatibilidade estrita com Web Standard APIs |

## Imperative Execution Workflow
1. Coletar e Auditar Configurações Atuais [FRÁGIL]:
   - Analise `next.config.js` ou `vercel.json` avaliando headers de cache, otimizadores de imagem e redirects.
2. Identificar Gargalos de Execução Serverless [FLEXÍVEL]:
   - Isole rotas com tempo de execução prolongado ou alocações de memória desnecessariamente altas (ex: 3GB para operações de IO simples).
3. Desenhar Estratégia de Caching e Invalidação [FRÁGIL]:
   - Configure políticas de `Cache-Control: s-maxage` e revalidação sob demanda para poupar chamadas repetidas de backend.
4. Otimizar Tamanho de Bundles e Imports [FLEXÍVEL]:
   - Substitua bibliotecas monolíticas por importações modulares específicas para reduzir o tamanho dos pacotes compilados.
5. Consolidar Recomendações e Métricas Alvo [FLEXÍVEL]:
   - Documente o plano de otimização detalhando a estimativa percentual de redução na fatura e ganho nos Web Vitals.

## Execution Checklist
- [ ] Auditar configurações de cache e presets de framework ativos
- [ ] Avaliar consumo de memória e tempo de execução das rotas serverless
- [ ] Aplicar políticas de revalidação incremental de páginas estáticas
- [ ] Otimizar entrega de imagens, fontes e ativos estáticos
- [ ] Documentar o plano de economia de custos e melhoria de performance

## On Failure
- **Gatilho de Erro**: Incompatibilidade de API ao migrar para Edge Runtime, quebra de revalidação de dados ou aumento de latência.
- **Ação Imediata**: Reverter alterações de runtime nas rotas afetadas.
- **Rollback**: Restaurar as diretivas originais de `next.config.js` e `vercel.json`.
- **Fallback**: Manter runtime Node.js tradicional com caching otimizado em memória no servidor de origem.
- **Logs**: Registrar rotas que apresentaram regressão de latência e consumo medido de CPU.

## Reference Documentation
Consulte a documentação técnica completa: [Referência Técnica](reference.md).
