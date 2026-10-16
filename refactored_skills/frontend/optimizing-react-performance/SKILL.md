---
name: optimizing-react-performance
description: >
  Applies React and Next.js performance guidelines from Vercel Engineering when writing, reviewing or refactoring components, pages, data fetching or bundles. Use this skill when: writing, reviewing or refactoring React or Next.js code for performance, bundle size or data fetching. Do NOT use this skill when: the task is component API design (use architecting-react-composition) or React Native (use building-react-native-interfaces).
---

# Otimização de Performance em React e Next.js

Aplica as diretrizes oficiais de engenharia de performance da Vercel para React 19 e Next.js: eliminação de re-renderizações inúteis, otimização de busca de dados (data fetching), divisão de código (code-splitting) e minimização de bundle.

## Input/Output Signature
Input:
- targetSourceFilePath: string # Caminho do componente, página ou hook a ser otimizado
- suspectedIssueType: string # Categoria do gargalo (excessive_rerenders, large_bundle_size, waterfall_fetching)
- profilingEvidence: object # Dados de renderização do React Profiler ou relatório de bundle
Output:
- optimizationSuccess: boolean # Status da aplicação das melhorias de desempenho
- eliminatedRerendersCount: number # Quantidade estimada de ciclos de renderização eliminados
- savedBundleBytes: number # Tamanho reduzido em bytes no pacote compilado
- appliedRefactorSummary: string # Resumo das técnicas aplicadas (memo, dynamic import, server component)

## Router and Selection Matrix
| Diagnóstico de Performance | Técnica de Otimização Recomendada | Grau de Liberdade |
|---|---|---|
| Re-renderizações Desnecessárias em Cadeia | Empurra o estado para as folhas da árvore ou eleva o conteúdo como `children` | [FRÁGIL] Prefere composição de componentes a encher o código de `useMemo` cego |
| Cascata de Requisições (Waterfall Fetching) | Dispara buscas de dados em paralelo com `Promise.all` ou no servidor | [FRÁGIL] Proibido encadear awaits sequenciais que não dependem do resultado anterior |
| Bundle Inicial Pesado por Bibliotecas | Substitui por `next/dynamic` com `ssr: false` para componentes secundários | [FLEXÍVEL] Carrega modais, editores e gráficos apenas sob demanda |
| Dependências Voláteis em Efeitos | Remove `useEffect` que apenas sincroniza estados derivados e calcula em linha | [FRÁGIL] Elimina ciclos de renderização adicionais pós-montagem |

## Imperative Execution Workflow
1. Diagnosticar Ciclos de Renderização com o React Profiler [FRÁGIL]:
   - Isole quais componentes renderizam repetidamente e identifique qual propriedade ou contexto mudou de referência.
2. Reestruturar Arquitetura de Estado e Composição [FLEXÍVEL]:
   - Mova estados locais para o componente mais próximo que realmente os utiliza, isolando o restante da árvore.
3. Eliminar Cascatas Assíncronas de Busca de Dados [FRÁGIL]:
   - Paralelize requisições no servidor ou adote carregamento em streaming com componentes React Suspense.
4. Aplicar Code-Splitting em Componentes Pesados [FLEXÍVEL]:
   - Utilize importação dinâmica (`React.lazy` ou `dynamic()`) para bibliotecas de visualização e componentes ocultos.
5. Mensurar Tamanho de Pacote e Tempo de Interação [FRÁGIL]:
   - Valide que o bundle da rota reduziu e que o tempo de resposta aos cliques melhorou sem regressão funcional.

## Execution Checklist
- [ ] Identificar a causa real de re-renderização através de métricas
- [ ] Aplicar composição com children para blindar componentes estáticos
- [ ] Paralelizar buscas de dados assíncronas independentes
- [ ] Carregar componentes secundários pesados de forma preguiçosa (lazy)
- [ ] Validar que todos os fluxos e testes unitários continuam funcionando

## On Failure
- **Gatilho de Erro**: Regressão de funcionalidade, referências obsoletas presas em fechamentos (stale closures) ou erros de hidratação.
- **Ação Imediata**: Reverter a otimização no hook ou componente problemático.
- **Rollback**: Restaurar a versão anterior do componente via Git.
- **Fallback**: Manter a renderização original e focar a otimização apenas no carregamento preguiçoso de assets estáticos.
- **Logs**: Registrar closures com dependência faltante e discrepâncias de hidratação identificadas.

## Reference Documentation
Consulte a documentação técnica completa: [Referência Técnica](reference.md).
