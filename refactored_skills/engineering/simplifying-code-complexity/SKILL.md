---
name: simplifying-code-complexity
description: >
  Simplifies code for clarity without changing behavior, reducing unnecessary complexity in code that works but is harder to read, maintain or extend. Use this skill when: refactoring for clarity or reviewing code that accumulated unnecessary complexity. Do NOT use this skill when: the code is wrong or its behavior must change (use debugging-root-causes).
---

# Simplificação de Código e Redução de Complexidade

Refatora código funcional para máxima clareza e legibilidade sem alterar o comportamento externo: redução de carga cognitiva, achatamento de aninhamentos profundos, eliminação de código morto e simplificação de fluxos.

## Input/Output Signature
Input:
- targetFilePath: string # Caminho do arquivo a ser simplificado
- codeSnippetToSimplify: string # Trecho específico de código com alta complexidade
- maxCyclomaticComplexityTarget: number # Meta máxima tolerada de complexidade ciclomática (default: 8)
Output:
- simplifiedCodeOutput: string # Código refatorado limpo e preservando contratos
- cyclomaticReductionPercent: number # Percentual de redução na complexidade ciclomática
- removedLinesCount: number # Linhas de código redundante ou morto eliminadas
- verificationStatus: string # Estado da validação de equivalência comportamental (verified_green, failed)

## Router and Selection Matrix
| Padrão de Complexidade | Estratégia de Simplificação | Grau de Liberdade |
|---|---|---|
| Aninhamento Profundo (Ifs dentro de Loops) | Utiliza cláusulas de guarda antecipadas (early return) para aplanar o fluxo | [FRÁGIL] Exige preservação de todas as condições de saída idênticas |
| Funções Gigantes / Multi-Propósito | Separa em funções puras focadas com nomes que expressam o que fazem | [FLEXÍVEL] Mantém acoplamento mínimo entre as partes divididas |
| Flags Booleanas Múltiplas | Converte combinações de booleanos em máquina de estados simples ou enums | [FLEXÍVEL] Reduz número exponencial de estados possíveis |
| Variáveis e Helpers de Uso Único | Inlinha código trivial que não agrega abstração e elimina variáveis temporárias | [FLEXÍVEL] Melhora fluxo linear de leitura de cima para baixo |

## Imperative Execution Workflow
1. Executar Testes Existentes e Garantir Estado Verde [FRÁGIL]:
   - Rode a suíte de testes do módulo antes de tocar em qualquer linha de código para estabelecer a base segura.
2. Identificar Fontes de Carga Cognitiva no Trecho [FLEXÍVEL]:
   - Isole cadeias de condições ternárias aninhadas, loops com múltiplos níveis de indentação e variáveis mutáveis.
3. Aplicar Cláusulas de Guarda e Retorno Antecipado [FRÁGIL]:
   - Trate erros e casos extremos no início da função, reduzindo a indentação do fluxo feliz para o nível principal.
4. Eliminar Código Morto e Indireções Inúteis [FLEXÍVEL]:
   - Remova blocos inalcançáveis, variáveis intermediárias sem função e comentários que apenas repetem o código.
5. Reexecutar Testes e Validar Equivalência Comportamental [FRÁGIL]:
   - Rode novamente a suíte de testes confirmando que 100% dos testes passam sem alteração de comportamento.

## Execution Checklist
- [ ] Confirmar que todos os testes passam antes de iniciar a refatoração
- [ ] Aplicar cláusulas de guarda para aplanar aninhamentos condicionais
- [ ] Eliminar variáveis temporárias redundantes e código morto
- [ ] Reorganizar a leitura do fluxo em sequência linear direta
- [ ] Validar que todos os testes permanecem verdes após a simplificação

## On Failure
- **Gatilho de Erro**: Falha em teste unitário após a refatoração, quebra de comportamento em casos extremos ou introdução de regressão.
- **Ação Imediata**: Reverter as alterações aplicadas imediatamente para retornar ao estado verde anterior.
- **Rollback**: Executar `git checkout` ou `git restore` no arquivo `targetFilePath`.
- **Fallback**: Aplicar simplificações em passos menores e isolados, testando a cada substituição atômica.
- **Logs**: Registrar o teste que falhou, asserção esperada vs obtida e diff rejeitado.

## Reference Documentation
Consulte a documentação técnica completa: [Referência Técnica](reference.md).
