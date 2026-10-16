---
name: querying-models-via-cli
description: >
  Queries available AI models, lists aliases and browses the model catalog from the CLI, filtering by provider, searching by capability and resolving model name variants. Use this skill when: finding a model name or alias from the terminal. Do NOT use this skill when: querying models through the API (use querying-omniroute-models).
---

# Consulta de Catálogo de Modelos de IA via CLI

Consulta o catálogo consolidado de modelos de inteligência artificial disponíveis no OmniRoute através do terminal: busca por apelidos (aliases), filtragem por provedor, pesquisa por capacidades e teste de adição.

## Input/Output Signature
Input:
- searchFilterKeyword: string # Termo de busca por nome de modelo, capacidade ou arquitetura
- filterByProvider: string # Filtro opcional por provedor (openai, anthropic, google, all)
- resolveAliases: boolean # Se deve listar aliases e mapeamentos para nomes reais (default: true)
Output:
- matchedModelsCount: number # Quantidade de modelos encontrados correspondentes ao filtro
- modelCatalogList: array # Lista detalhada de modelos com capacidades, limites de contexto e preços
- resolvedAliasMappings: object # Mapeamento de apelidos comuns para nomes canônicos de API
- executionLog: string # Registro dos comandos CLI executados

## Router and Selection Matrix
| Tipo de Consulta | Comando CLI Recomendado | Grau de Liberdade |
|---|---|---|
| Listagem Completa do Catálogo | Executa `omniroute models` exibindo todos os modelos disponíveis | [FLEXÍVEL] Apresenta saída formatada com paginação no terminal |
| Filtro por Provedor Específico | Executa `omniroute models --provider <nome>` isolando o catálogo | [FLEXÍVEL] Permite navegação focada em uma única API |
| Busca por Capacidade (Vision/Tool) | Executa busca textual filtrando modelos com suporte a ferramentas ou imagens | [FLEXÍVEL] Auxilia na seleção do modelo ideal para a tarefa |
| Teste de Adição com Dry-Run | Executa `omniroute models test-add <model> --dry-run` para validar schema | [FRÁGIL] Confirma compatibilidade de modelo customizado sem mutação |

## Imperative Execution Workflow
1. Executar Comando CLI de Consulta de Modelos [FRÁGIL]:
   - Dispare `omniroute models` aplicando filtros de busca e provedor informados na entrada.
2. Resolver Apelidos e Mapeamentos Canônicos [FLEXÍVEL]:
   - Identifique quais aliases (ex: `fast`, `smart`, `coding`) estão apontando para quais modelos reais.
3. Analisar Limites de Janela de Contexto e Suporte [FLEXÍVEL]:
   - Extraia informações de contagem máxima de tokens de contexto, suporte a chamadas de ferramentas e custo por milhão.
4. Validar Disponibilidade em Provedores Ativos [FRÁGIL]:
   - Confirme se os modelos retornados pertencem a conexões que estão atualmente autenticadas e saudáveis.
5. Formatar Resposta para o Desenvolvedor [FLEXÍVEL]:
   - Apresente a lista organizada com nomes exatos de API prontos para uso em chamadas de inferência.

## Execution Checklist
- [ ] Executar comando de listagem de modelos com filtros adequados
- [ ] Resolver apelidos e aliases para os nomes oficiais de API
- [ ] Conferir janela de contexto e capacidades do modelo pesquisado
- [ ] Confirmar que o modelo pertence a uma conexão autenticada
- [ ] Retornar os nomes exatos prontos para parametrização

## On Failure
- **Gatilho de Erro**: Nenhum modelo correspondente ao filtro, provedor não configurado ou erro no comando CLI.
- **Ação Imediata**: Ampliar os termos de busca e remover restrições de provedor.
- **Rollback**: Não aplicável; a operação é de consulta.
- **Fallback**: Consultar endpoint da API REST `/v1/models` para leitura direta do catálogo.
- **Logs**: Registrar termo de busca que resultou vazio e provedores ativos no momento da consulta.

## Reference Documentation
Consulte a documentação técnica completa: [Referência Técnica](reference.md).
