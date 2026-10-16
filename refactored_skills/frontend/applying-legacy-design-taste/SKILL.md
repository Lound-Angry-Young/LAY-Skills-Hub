---
name: applying-legacy-design-taste
description: >
  Applies the original v1 taste guidance (design-taste-frontend-v1), kept for projects that depend on its exact behavior. Use this skill when: exact backward compatibility with taste-skill v1 is required. Do NOT use this skill when: a new project needs the current default taste guidance (use elevating-frontend-taste).
---

# Aplicação de Diretrizes de Design Taste v1 (Legado)

Aplica os padrões canônicos da versão 1 da especificação taste-skill: estética dark-tech austera, contrastes deliberados, tipografia de alta densidade técnica, grids assimétricos e regras estritas anti-slop.

## Input/Output Signature
Input:
- componentOrPagePath: string # Caminho do componente ou tela a receber as diretrizes de taste v1
- targetDensity: string # Densidade visual pretendida (compact, balanced, expansive)
- preserveExistingTokens: boolean # Se deve respeitar tokens já definidos no arquivo (default: true)
Output:
- tasteAppliedSuccess: boolean # Status da aplicação dos padrões visuais
- appliedDirectivesSummary: array # Lista de correções de viés estético aplicadas (anti-slop, contraste, tipografia)
- modifiedCodeSnippet: string # Trecho do componente formatado com as regras canônicas
- executionLog: string # Registro dos ajustes realizados

## Router and Selection Matrix
| Elemento Visual | Regra Canônica Taste v1 | Grau de Liberdade |
|---|---|---|
| Paleta de Fundo e Superfície | Preto profundo (#050505 a #0a0a0a) com bordas sutis em 1px (#222222) | [FRÁGIL] Baniu gradientes genéricos em mesh e fundos cinza lavados |
| Escala Tipográfica | Contraste dramático entre display e corpo com fontes mono em rótulos técnicos | [FLEXÍVEL] Aplica tracking refinado em títulos caixa alta |
| Botões e Ações Primárias | Estados interativos completos (hover, active, focus-visible) sem sombras infladas | [FRÁGIL] Exige contraste WCAG AA sobre a superfície |
| Bento Grids e Cards | Layouts modulares assimétricos com proporções funcionais e padding generoso | [FLEXÍVEL] Evita repetição simétrica monótona de cards idênticos |

## Imperative Execution Workflow
1. Inspecionar Código Atual contra Vieses Genéricos [FRÁGIL]:
   - Identifique e purgue gradientes pastéis, botões com sombras excessivas e layouts com alinhamento centralizado sem propósito.
2. Calibrar Paleta Tonal e Superfícies [FRÁGIL]:
   - Aplique cores de fundo ricas e escuras com hierarquia clara entre superfícies base, cards e modais.
3. Ajustar Hierarquia Tipográfica e Espaçamento [FLEXÍVEL]:
   - Configure tamanhos e pesos de fonte que guiem o olhar do usuário com clareza, utilizando fontes mono em metadados.
4. Implementar Estados Interativos Detalhados [FRÁGIL]:
   - Adicione feedback visual preciso para hover, clique ativo e anel de foco visível para acessibilidade por teclado.
5. Auditar Acabamento Visual e Contraste [FRÁGIL]:
   - Verifique que todo o texto secundário possui contraste mínimo legível e que o layout transmite autoridade técnica.

## Execution Checklist
- [ ] Purgar gradientes genéricos e sombras infladas de template
- [ ] Aplicar hierarquia tonal escura com bordas de precisão
- [ ] Configurar tipografia contrastante com tracking calibrado
- [ ] Garantir estados de hover, active e foco por teclado em todos os controles
- [ ] Validar conformidade contra as diretrizes do manifesto taste v1

## On Failure
- **Gatilho de Erro**: Contraste de texto insuficiente para leitura, layout parecendo cópia genérica ou regressão de acessibilidade.
- **Ação Imediata**: Ajustar valores de cor e elevar o contraste dos elementos de texto imediatamente.
- **Rollback**: Reverter estilos para a versão anterior do componente em caso de inconsistência visual.
- **Fallback**: Adotar esquema monocromático austero com alto contraste preto e branco.
- **Logs**: Registrar elementos com contraste deficiente e propriedades de estilo substituídas.

## Reference Documentation
Consulte a documentação técnica completa: [Referência Técnica](reference.md).
