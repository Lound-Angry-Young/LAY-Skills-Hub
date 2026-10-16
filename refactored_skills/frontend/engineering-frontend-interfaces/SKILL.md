---
name: engineering-frontend-interfaces
description: >
  Architects and implements high-quality frontend interfaces: component hierarchy, state management, compound components, separation of concerns and robust typing. Use this skill when: building or refactoring frontend UI components and interfaces. Do NOT use this skill when: doing pure visual styling with no structural changes (use elevating-frontend-taste) or building mobile React Native apps (use building-react-native-interfaces).
---

# Engenharia de Interfaces Frontend

Projeta e implementa arquitetura robusta de componentes frontend: hierarquia limpa, padrões de componentes compostos (compound components), separação estrita de apresentação e estado, e tipagem estrita com TypeScript.

## Input/Output Signature
Input:
- componentDesignIntent: string # Descrição da funcionalidade do componente ou interface
- targetFrameworkStack: string # Stack utilizada (react_19, nextjs_app_router, vue_3, svelte_5)
- componentFilePath: string # Caminho onde o componente principal será implementado
Output:
- componentCodeOutput: string # Código fonte do componente implementado e tipado
- exportedInterfacesList: array # Lista de propriedades (Props) e tipos exportados
- stateManagementPattern: string # Padrão de estado aplicado (local, context, reducer, state_machine)
- status: string # Estado da implementação (ready, requires_test, failed)

## Router and Selection Matrix
| Complexidade do Componente | Padrão Arquitetural Recomendado | Grau de Liberdade |
|---|---|---|
| Componente com Múltiplas Partes (Modal, Dropdown) | Padrão de Componentes Compostos (ex: `Select.Root`, `Select.Trigger`, `Select.Item`) | [FRÁGIL] Exige compartilhamento de contexto interno sem prop drilling |
| Fluxo com Múltiplos Estados e Transições | Máquina de estados finitos ou `useReducer` tipado com uniões discriminadas | [FRÁGIL] Proibido usar múltiplos booleanos soltos que permitam estados impossíveis |
| Componente Presentacional Puro | Função pura que recebe dados e emite eventos sem estado interno | [FLEXÍVEL] Maximize reutilização e facilidade de teste unitário |
| Componente Conectado a Servidor / API | Separação entre container de dados e componente visual puro | [FRÁGIL] Mantém a lógica de busca isolada da renderização de interface |

## Imperative Execution Workflow
1. Delimitar Contrato de Propriedades (Props Interface) [FRÁGIL]:
   - Declare interfaces TypeScript estritas evitando propriedades genéricas ou aninhamentos desnecessários.
2. Isolar Lógica de Estado em Hook Customizado [FLEXÍVEL]:
   - Extraia a manipulação de dados, efeitos e eventos para um hook dedicado (ex: `useDisclosure`, `useFilterList`).
3. Construir Hierarquia de Componentes Coesos [FRÁGIL]:
   - Estruture o componente principal em sub-elementos com responsabilidade única facilitando composição flexível.
4. Garantir Acessibilidade e Semântica WAI-ARIA [FRÁGIL]:
   - Associe rótulos acessíveis, papéis de acessibilidade e manipulação completa de teclas (`Enter`, `Space`, `Escape`, setas).
5. Validar Tipos e Testes Unitários de Renderização [FRÁGIL]:
   - Execute o checador de tipos TypeScript e confirme que o componente renderiza corretamente em todos os estados.

## Execution Checklist
- [ ] Definir interfaces de propriedades estritamente tipadas com TypeScript
- [ ] Isolar a gestão de estado complexo em hooks customizados ou reducers
- [ ] Aplicar atributos ARIA adequados e navegação completa por teclado
- [ ] Manter componentes focados com separação clara de responsabilidades
- [ ] Validar compilação de tipos sem erros

## On Failure
- **Gatilho de Erro**: Prop drilling excessivo, renderizações cíclicas infinitas, erro de tipo TypeScript ou violação de acessibilidade.
- **Ação Imediata**: Interromper a implementação e simplificar a árvore de estado do componente.
- **Rollback**: Reverter alterações no arquivo de componente para o último commit limpo.
- **Fallback**: Quebrar o componente monolítico em dois componentes autônomos e mais simples.
- **Logs**: Registrar erro do compilador de tipos e rastreamento de re-renderizações problemáticas.

## Reference Documentation
Consulte a documentação técnica completa: [Referência Técnica](reference.md).
