---
name: documenting-architecture-decisions
description: >
  Records architecture and technical decisions using the Architecture Decision Record (ADR) format, keeping decisions discoverable, dated, and with context, alternatives considered, consequences, and current status. Use this skill when: a significant architecture decision is made, an existing decision is superseded, or technical context must be preserved for future developers. Do NOT use this skill when: writing end-user documentation or API references (use designing-apis-and-interfaces).
---

# Registro de Decisões de Arquitetura (ADR)

Documenta decisões arquiteturais e técnicas de engenharia no formato canônico ADR (Architecture Decision Record), registrando contexto, opções avaliadas, consequências e ciclo de vida.

## Input/Output Signature
Input:
- decisionTitle: string # Título claro e conciso da decisão arquitetural
- decisionStatus: string # Estado do registro (proposed, accepted, superseded, deprecated)
- decisionContext: string # Contexto do problema, forças em conflito e requisitos técnicos
- alternativesConsidered: array # Lista de abordagens avaliadas com prós e contras
- chosenSolutionRationale: string # Justificativa detalhada da solução escolhida e consequências
Output:
- adrFilePath: string # Caminho do arquivo ADR gerado (ex: docs/adr/0004-escolha-banco.md)
- adrNumber: number # Número sequencial atribuído ao registro de decisão
- indexUpdated: boolean # Confirmação de que o índice de decisões foi atualizado
- executionLog: string # Registro dos passos executados

## Router and Selection Matrix
| Status da Decisão | Ação Recomendada | Grau de Liberdade |
|---|---|---|
| Nova Decisão Proposta | Registra ADR com status `Proposed` para discussão da equipe | [FLEXÍVEL] Estimula levantamento de alternativas e trade-offs |
| Decisão Aprovada | Converte status para `Accepted` e detalha consequências positivas e negativas | [FRÁGIL] Exige clareza formal sobre impactos e restrições geradas |
| Decisão Substituída (Superseded) | Vincula novo ADR e marca o registro antigo com link bidirecional | [FRÁGIL] Obrigatório referenciar o número do ADR substituto |
| Decisão Rejeitada / Obsoleta | Atualiza status e registra os motivos técnicos que motivaram o descarte | [FLEXÍVEL] Mantém memória histórica para evitar discussões repetidas |

## Imperative Execution Workflow
1. Determinar Próximo Número Sequencial [FRÁGIL]:
   - Inspecione o diretório `docs/adr/` e identifique o próximo identificador numérico de quatro dígitos (ex: `0005`).
2. Estruturar Formato Canônico MADR [FRÁGIL]:
   - Monte o documento com as seções obrigatórias: Título, Status, Contexto, Opções Consideradas e Consequências.
3. Descrever Forças e Trade-offs Objetivamente [FLEXÍVEL]:
   - Documente o impacto em latência, custo, complexidade de código, suporte a longo prazo e segurança.
4. Gravar Arquivo de Registro de Decisão [FRÁGIL]:
   - Salve o arquivo em `docs/adr/NNNN-<slug-em-kebab-case>.md` utilizando codificação UTF-8 estrita.
5. Atualizar Índice Central de ADRs [FLEXÍVEL]:
   - Adicione o novo registro na tabela do índice principal (`docs/adr/README.md`) com link relativo válido.

## Execution Checklist
- [ ] Identificar o número sequencial correto para o novo registro
- [ ] Documentar o contexto técnico e as forças que motivaram a decisão
- [ ] Listar alternativas avaliadas com análise comparativa de prós e contras
- [ ] Detalhar consequências positivas e negativas da escolha
- [ ] Atualizar o índice geral de decisões de arquitetura

## On Failure
- **Gatilho de Erro**: Colisão de números de ADR, formatação fora do padrão canônico ou links quebrados no índice.
- **Ação Imediata**: Parar o salvamento do documento e corrigir a numeração sequencial.
- **Rollback**: Remover arquivo com numeração incorreta criado no diretório de decisões.
- **Fallback**: Solicitar revisão manual do índice para reconciliação de numeração duplicada.
- **Logs**: Registrar número em conflito, título da decisão e caminho do arquivo afetado.

## Reference Documentation
Consulte a documentação técnica completa: [Referência Técnica](reference.md).
