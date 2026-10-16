---
name: authoring-specifications-first
description: >
  Creates specifications before coding: objectives, scope, requirements, PRDs and a capability map of independently testable modules when a requirement spans several capabilities. Use this skill when: starting a new project, feature or significant change with no specification, or when requirements are vague or ambiguous. Do NOT use this skill when: the specification already exists and only needs implementation (use implementing-incremental-slices).
---

# Especificação Orientada a Contratos (Spec-First)

Elabora especificações técnicas e PRDs completos antes de qualquer implementação de código: objetivos, histórias de usuário, requisitos funcionais e não-funcionais, mapa de capacidades testáveis e contratos de interface.

## Input/Output Signature
Input:
- featureIntentDescription: string # Intenção de negócio ou funcionalidade desejada
- targetScopeBoundary: object # Limites de escopo inclusos e expressamente excluídos
- systemConstraints: array # Restrições de stack, dependências e padrões arquiteturais
Output:
- specificationDocumentPath: string # Caminho do documento de especificação gerado (ex: SPEC.md)
- capabilityMap: array # Lista de módulos e capacidades independentemente testáveis
- apiContracts: array # Definições formais de interfaces de entrada, saída e erro
- status: string # Estado da especificação (drafted, reviewed, approved)

## Router and Selection Matrix
| Complexidade da Demanda | Nível de Especificação | Grau de Liberdade |
|---|---|---|
| Nova Funcionalidade Ampla | PRD completo com mapa de capacidades, contratos de API e plano de testes | [FRÁGIL] Exige validação de requisitos não-funcionais (latência, segurança) |
| Ajuste ou Extensão de Módulo | Mini-especificação com diff de contratos e impacto em dependentes | [FLEXÍVEL] Foca nas assinaturas de interface alteradas |
| Requisitos Vagos ou Conflitantes | Stop-the-line imediato para alinhamento antes de redigir o documento | [FRÁGIL] Proibido assumir premissas não validadas em contratos |
| Funcionalidade Multi-Módulo | Decomposição em mapa de capacidades independentes e fatiadas | [FRÁGIL] Cada capacidade deve possuir critérios de aceite isolados |

## Imperative Execution Workflow
1. Isolar Problema e Objetivos de Negócio [FLEXÍVEL]:
   - Defina com precisão o problema real a ser resolvido, o público-alvo e o critério de sucesso mensurável.
2. Mapear Requisitos Funcionais e Não-Funcionais [FRÁGIL]:
   - Liste comportamentos esperados (entradas, saídas, erros) e requisitos de performance, escalabilidade e segurança.
3. Projetar Contratos de Interface e Dados [FRÁGIL]:
   - Esboce schemas JSON/TypeScript para todas as entradas e saídas públicas antes de pensar na lógica interna.
4. Construir Mapa de Capacidades Independentes [FLEXÍVEL]:
   - Divida o escopo em unidades autônomas que possam ser implementadas e testadas sem dependência mútua estrita.
5. Consolidar Documento de Especificação (SPEC.md) [FRÁGIL]:
   - Salve a especificação estruturada contendo critérios de aceitação objetivos e passe para aprovação.

## Execution Checklist
- [ ] Definir o problema e os objetivos centrais da entrega
- [ ] Mapear requisitos funcionais e restrições não-funcionais
- [ ] Estabelecer contratos de interface tipados e schemas de dados
- [ ] Criar mapa de capacidades decompostas e testáveis
- [ ] Gravar SPEC.md estruturado e pronto para planejamento de tarefas

## On Failure
- **Gatilho de Erro**: Requisitos conflitantes, escopo infinito não delimitado ou ausência de critérios objetivos de validação.
- **Ação Imediata**: Pausar a redação e listar os pontos ambíguos para resolução direta.
- **Rollback**: Descartar rascunhos de contratos baseados em suposições não confirmadas.
- **Fallback**: Conduzir sessão de alinhamento com `interviewing-user-requirements` para sanar as dúvidas.
- **Logs**: Registrar requisitos em conflito, premissas descartadas e pontos em aberto.

## Reference Documentation
Consulte a documentação técnica completa: [Referência Técnica](reference.md).
