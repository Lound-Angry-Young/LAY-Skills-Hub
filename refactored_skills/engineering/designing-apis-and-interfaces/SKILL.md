---
name: designing-apis-and-interfaces
description: >
  Guides stable API and interface design: module boundaries, REST or GraphQL endpoints, type contracts between modules and the boundary between frontend and backend. Use this skill when: designing APIs, module boundaries or any public interface. Do NOT use this skill when: implementing the internals of an interface that is already designed (use implementing-incremental-slices).
---

# Design de APIs e Contratos de Interface

Projeta APIs e interfaces estáveis, coesas e expressivas: delimitação de fronteiras entre módulos, endpoints REST, tipagens bidirecionais entre frontend e backend e tratamento padronizado de erros.

## Input/Output Signature
Input:
- resourceDomainName: string # Nome do recurso ou entidade central (ex: auth, orders, billing)
- interfaceProtocol: string # Protocolo pretendido (rest_json, graphql, rpc, internal_types)
- supportedOperations: array # Lista de operações (create, read, update, delete, batch, stream)
- authModel: string # Modelo de autorização (bearer_token, session_cookie, api_key, internal)
Output:
- apiContractSpec: object # Especificação formal do contrato (OpenAPI schema ou tipos TypeScript)
- endpointRegistry: array # Relação de rotas, métodos HTTP, códigos de status e payloads
- standardErrorPayloads: object # Estrutura canônica de respostas de erro (RFC 7807)
- status: string # Estado do design (drafted, validated, finalized)

## Router and Selection Matrix
| Tipo de Interface | Padrão Recomendado | Grau de Liberdade |
|---|---|---|
| REST API Pública / Externa | Substantivos no plural, verbos HTTP canônicos e envelopes semânticos | [FRÁGIL] Exige códigos HTTP padronizados (200, 201, 204, 400, 401, 404, 422) |
| Contrato Frontend/Backend | Tipagem TypeScript compartilhada de ponta a ponta com validação Zod | [FRÁGIL] Requer schema de runtime para validação de borda |
| Operações em Lote / Bulk | Endpoints dedicados com retorno de status individual por item | [FLEXÍVEL] Permite falhas parciais detalhadas por registro |
| Tratamento de Erros | Esquema compatível com RFC 7807 (`type`, `title`, `status`, `detail`) | [FRÁGIL] Proibido retornar erro genérico com status 200 |

## Imperative Execution Workflow
1. Delimitar Entidades e Recursos Canônicos [FLEXÍVEL]:
   - Identifique as entidades de domínio, identificadores únicos e relacionamentos de sub-recursos.
2. Definir Verbos HTTP e Mapeamento de Rotas [FRÁGIL]:
   - Utilize métodos idempotentes (`GET`, `PUT`, `DELETE`) e não-idempotentes (`POST`) de forma estrita.
3. Especificar Payloads de Requisição e Resposta [FRÁGIL]:
   - Modele schemas de dados detalhados para cada cenário de sucesso com tipos de dados explícitos.
4. Estruturar Respostas de Erro Padronizadas [FRÁGIL]:
   - Adote formato RFC 7807 com detalhes acionáveis de validação de campos sem vazar stack traces internos.
5. Validar Paginação, Filtros e Idempotência [FLEXÍVEL]:
   - Defina parâmetros de paginação por cursor ou offset e suporte a cabeçalho `Idempotency-Key` para mutações críticas.

## Execution Checklist
- [ ] Mapear substantivos de recursos e verbos HTTP correspondentes
- [ ] Definir schemas de entrada e saída fortemente tipados
- [ ] Configurar modelo uniforme de resposta de erros (RFC 7807)
- [ ] Especificar parâmetros de paginação, ordenação e filtros
- [ ] Validar compatibilidade de tipos entre cliente e servidor

## On Failure
- **Gatilho de Erro**: Ambiguidade nos formatos de dados, códigos de status em conflito com a semântica HTTP ou falta de validação de schemas.
- **Ação Imediata**: Interromper o fechamento da interface e revisar o modelo conceitual de rotas.
- **Rollback**: Reverter modificações nas definições OpenAPI ou arquivos de tipos compartilhados.
- **Fallback**: Adotar convenção RESTful estrita fundamentada nos padrões da RFC correspondente.
- **Logs**: Registrar rotas em desacordo, conflitos de nomenclatura de payload e tipos incompatíveis.

## Reference Documentation
Consulte a documentação técnica completa: [Referência Técnica](reference.md).
