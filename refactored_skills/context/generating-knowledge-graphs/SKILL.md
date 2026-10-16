---
name: generating-knowledge-graphs
description: >
  Transforms codebases into persistent knowledge graphs using Graphify: extracts AST nodes, analyzes dependencies, clusters modules, and surfaces high-coupling god nodes for safe refactoring. Use this skill when: exploring an unfamiliar codebase, mapping module dependencies, planning architectural refactors, or tracing cross-file relationships. Do NOT use this skill when: running unit tests (use driving-test-driven-development) or doing single-file edits.
---

# Geração de Grafos de Conhecimento de Código

Utiliza o Graphify para transformar repositórios em grafos de conhecimento estruturados, analisando AST, acoplamento entre módulos, comunidades de código e nós centralizadores (god nodes).

## Input/Output Signature
Input:
- repoPath: string # Caminho absoluto do repositório a ser mapeado
- outputFormat: string # Formato de saída do grafo (json, graphml, markdown)
- incrementalUpdate: boolean # Se verdadeiro, atualiza apenas arquivos modificados (default: false)
- clusterOnly: boolean # Se verdadeiro, reexecuta apenas detecção de comunidades (default: false)
Output:
- graphArtifactPath: string # Caminho do arquivo de grafo persistido
- godNodesReport: array # Lista de arquivos com centralidade crítica e alto acoplamento
- clusterCount: number # Número de comunidades funcionais detectadas
- totalNodesCount: number # Total de entidades mapeadas no grafo

## Router and Selection Matrix
| Condição / Cenário | Ação Recomendada | Grau de Liberdade |
|---|---|---|
| Repositório Inédito | Executa extração AST completa e constrói o grafo persistente do zero | [FRÁGIL] Exige caminhos absolutos do interpretador e CLI do Graphify |
| Mudança Incremental | Executa varredura com flag `--update` apenas sobre diffs de commits | [FLEXÍVEL] Atualiza apenas os nós e arestas afetados |
| Refatoração de Arquitetura | Analisa métricas de modularidade e identifica god nodes de risco | [FLEXÍVEL] Gera recomendações de quebra de acoplamento |
| Inspeção de Navegação | Gera visualização sintética e exporta matriz de adjacência | [FLEXÍVEL] Cria representação navegável para agentes |

## Imperative Execution Workflow
1. Localizar Interpretador e Binário do Graphify [FRÁGIL]:
   - Utilize o caminho absoluto do executável Python e do Graphify CLI registrados no ecossistema local.
2. Definir Escopo de Diretórios e Exclusões [FRÁGIL]:
   - Configure exclusão explícita de `node_modules`, `.git`, `.venv`, pastas de build e artefatos binários.
3. Disparar Análise AST e Extração de Relações [FRÁGIL]:
   - Execute o comando do Graphify para processar chamadas, heranças, imports e tipagens no repositório `repoPath`.
4. Mapear Comunidades e Nós de Alto Acoplamento [FLEXÍVEL]:
   - Execute o algoritmo de clusterização para identificar grupos de módulos e apontar arquivos com acoplamento crítico.
5. Exportar Artefato e Integrar ao Repositório [FRÁGIL]:
   - Grave o grafo no diretório apropriado e disponibilize o sumário estruturado para navegação de agentes.

## Execution Checklist
- [ ] Validar executável do Graphify por caminho absoluto
- [ ] Configurar regras de exclusão de pastas de dependência e build
- [ ] Executar rotina de extração AST
- [ ] Analisar comunidades detectadas e listar god nodes
- [ ] Persistir arquivo do grafo gerado e validar integridade

## On Failure
- **Gatilho de Erro**: Erro de sintaxe impedindo análise AST, falta do binário do Graphify ou estouro de memória em monorepos.
- **Ação Imediata**: Interromper o processo de indexação e isolar o arquivo sintaticamente quebrado.
- **Rollback**: Limpar arquivos temporários parciais gerados na pasta de destino do grafo.
- **Fallback**: Usar inventário local estruturado de arquivos com busca textual indexada como substituto temporário.
- **Logs**: Registrar stack trace do analisador sintático, arquivo problemático e parâmetros da chamada.

## Reference Documentation
Consulte a documentação técnica completa: [Referência Técnica](reference.md).
