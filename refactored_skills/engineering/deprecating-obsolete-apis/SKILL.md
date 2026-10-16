---
name: deprecating-obsolete-apis
description: >
  Plans and executes API and feature deprecations safely: marks deprecation notices, provides clear migration paths, establishes sunset timelines and verifies zero broken clients before removal. Use this skill when: obsoleting an API, function, parameter or feature. Do NOT use this skill when: actively migrating live infrastructure or data schemas (use migrating-legacy-architectures).
---

# Depreciação Segura de APIs e Interfaces

Planeja e executa a descontinuação segura de APIs, métodos e parâmetros: anotações de advertência, documentação de migração, janelas de sunset e auditoria de chamadores para remoção com zero impacto.

## Input/Output Signature
Input:
- targetApiIdentifier: string # Nome da função, classe, endpoint ou parâmetro a ser depreciado
- replacementApiIdentifier: string # Identificador da nova API ou método recomendado em substituição
- sunsetVersionOrDate: string # Versão planejada para remoção final ou data de término de suporte
Output:
- deprecationNoticeAdded: boolean # Confirmação de que anotações e avisos de runtime foram inseridos
- migrationGuideSummary: string # Instruções claras demonstrando como migrar do método antigo para o novo
- callersAuditReport: array # Lista de locais no repositório que ainda invocam a API obsoleta
- status: string # Estado do ciclo de vida da API (deprecated, sunset_pending, ready_to_remove)

## Router and Selection Matrix
| Tipo de Interface | Estratégia de Depreciação | Grau de Liberdade |
|---|---|---|
| Função / Método Interno | Adiciona anotação `@deprecated` em JSDoc/docstring e aponta alternativa | [FRÁGIL] Exige indicação explícita da nova função substituta |
| Endpoint HTTP / REST Público | Adiciona cabeçalho `Sunset` e `Deprecation` na resposta com link do guia | [FRÁGIL] Requer cumprimento dos padrões RFC 8594 para APIs públicas |
| Parâmetro de Função | Mantém suporte retrocompatível com aviso de log estruturado uma vez por sessão | [FLEXÍVEL] Emite warning sem poluir saídas repetidas de console |
| Remoção Definitiva | Executa exclusão apenas quando o relatório de chamadores estiver zerado | [FRÁGIL] Proibido remover código enquanto houver referências ativas |

## Imperative Execution Workflow
1. Mapear Consumidores e Chamadores Ativos [FRÁGIL]:
   - Realize busca em todo o repositório (`grep` estruturado) para listar todos os pontos que consom a API obsoleta.
2. Inserir Anotações de Depreciação Padronizadas [FRÁGIL]:
   - Adicione anotações `@deprecated` detalhando o motivo, o identificador substituto e a versão de remoção.
3. Configurar Avisos em Tempo de Execução [FLEXÍVEL]:
   - Inclua aviso de advertência (logger warning) com deduplicação para alertar desenvolvedores sem quebrar builds.
4. Elaborar Guia de Migração Antes/Depois [FLEXÍVEL]:
   - Redija exemplo lado a lado demonstrando a transição do padrão antigo para a nova convenção recomendada.
5. Auditar e Planejar Janela de Descomissionamento [FRÁGIL]:
   - Acompanhe a migração dos pontos mapeados até que nenhum consumidor interno invoque o método antigo.

## Execution Checklist
- [ ] Mapear todos os consumidores ativos da API a ser depreciada
- [ ] Inserir anotação formal de depreciação com link para a alternativa
- [ ] Configurar alertas de runtime não-bloqueantes
- [ ] Documentar guia de migração com exemplos de código antes e depois
- [ ] Confirmar que nenhum chamador interno permanece antes da remoção final

## On Failure
- **Gatilho de Erro**: Remoção prematura com chamadores ativos, quebra de contratos públicos sem aviso ou ciclo de sunset violado.
- **Ação Imediata**: Reverter a exclusão ou reabilitar o shim de compatibilidade imediatamente.
- **Rollback**: Restaurar o método depreciado original mantendo a ponte para o novo serviço.
- **Fallback**: Manter proxy ou wrapper de retrocompatibilidade com telemetria para identificar consumidores remanescentes.
- **Logs**: Registrar lista de chamadores afetados e chamadas capturadas em produção após tentativa de remoção.

## Reference Documentation
Consulte a documentação técnica completa: [Referência Técnica](reference.md).
