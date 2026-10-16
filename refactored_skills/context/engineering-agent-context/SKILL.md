---
name: engineering-agent-context
description: >
  Optimizes agent context setup: starting new sessions, recovering from degraded output, switching between tasks and configuring rules files and context for a project. Use this skill when: starting a new session, output quality degrades, switching tasks or configuring a project's rules files. Do NOT use this skill when: the goal is only to compress messages or prompts (use compressing-agent-messages or configuring-prompt-compression).
---

# Engenharia de Contexto para Agentes

Configura e gerencia o contexto de agentes de IA: hierarquia de regras, isolamento de sessões, mitigação de degradação cognitiva e alternância eficiente entre tarefas.

## Input/Output Signature
Input:
- sessionType: string # Tipo de sessão (fresh, task_switch, recovery)
- projectRootPath: string # Caminho raiz do projeto com os arquivos de regras
- activeTaskDescription: string # Descrição da tarefa em andamento para foco de contexto
- forceContextReset: boolean # Se deve descartar histórico volátil anterior (default: false)
Output:
- contextHierarchy: object # Mapeamento da precedência de regras (global, projeto, local)
- loadedRuleFiles: array # Lista de arquivos de regras injetados no contexto
- memoryCleaned: boolean # Indica se estados voláteis anteriores foram expurgados
- status: string # Estado da configuração (configured, purged, failed)

## Router and Selection Matrix
| Condição / Cenário | Ação Recomendada | Grau de Liberdade |
|---|---|---|
| Início de Sessão | Injeta regras canônicas na ordem correta (`AGENTS.md`, `CLAUDE.md`, `.cursorrules`) | [FRÁGIL] Respeita estritamente a precedência de arquivos |
| Degradação Cognitiva / Drift | Purga histórico volátil e reinjeta apenas contratos essenciais e decisões | [FRÁGIL] Exige limpeza imediata para evitar alucinação repetida |
| Mudança de Tarefa | Descarrega arquivos não relacionados e carrega documentação da nova tarefa | [FLEXÍVEL] Mantém contratos globais e isola estado local |
| Sessão com Muitos Tokens | Recomenda e orienta o uso de compactação semântica (`/compact`) | [FLEXÍVEL] Remove saídas de ferramentas já validadas |

## Imperative Execution Workflow
1. Inspecionar Arquivos de Regras do Projeto [FRÁGIL]:
   - Localize e leia os arquivos `AGENTS.md`, `CLAUDE.md` e regras locais em `projectRootPath`.
2. Mapear Hierarquia e Precedência [FRÁGIL]:
   - Estabeleça a hierarquia estrita: instruções do usuário > regras do projeto > regras globais > defaults do modelo.
3. Purgação de Ruído e Histórico Volátil [FLEXÍVEL]:
   - Elimine saídas massivas de comandos, diffs obsoletos e conversas secundárias que não afetam a tarefa atual.
4. Estruturar Snapshot Operacional [FLEXÍVEL]:
   - Compile um resumo compacto com premissas confirmadas, decisões arquiteturais consolidadas e checklist atual.
5. Validar Foco e Alinhamento do Agente [FRÁGIL]:
   - Confirme que o agente opera dentro do escopo atômico sem reintroduzir arquivos ou premissas descartadas.

## Execution Checklist
- [ ] Ler arquivos de regras na raiz do projeto
- [ ] Validar precedência entre regras globais e locais
- [ ] Purgar histórico irrelevante para evitar contaminação de contexto
- [ ] Injetar estado estruturado da tarefa em andamento
- [ ] Confirmar alinhamento com as diretrizes do projeto

## On Failure
- **Gatilho de Erro**: Conflito irreconciliável entre arquivos de regras, estouro de contexto ou persistência de alucinações.
- **Ação Imediata**: Interromper o fluxo da sessão e congelar o estado para diagnóstico.
- **Rollback**: Restaurar snapshot de contexto prévio caso uma tentativa de reconfiguração falhe.
- **Fallback**: Recomendar ao usuário o encerramento da sessão atual e abertura de uma sessão limpa via novo prompt focado.
- **Logs**: Registrar contagem estimada de tokens, arquivos de regras conflitantes e sintoma de degradação.

## Reference Documentation
Consulte a documentação técnica completa: [Referência Técnica](reference.md).
