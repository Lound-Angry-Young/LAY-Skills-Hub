---
name: minimizing-code-overengineering
description: >
  Forces the laziest solution that works: asks whether the task needs to exist at all, reuses existing code, prefers the standard library and native platform features, and keeps each change to the minimum. Use this skill when: writing, adding, refactoring, fixing or reviewing any coding task where the solution may be overbuilt. Do NOT use this skill when: the task is a dedicated audit of the whole codebase (use auditing-codebase-bloat).
---

# Prevenção e Redução de Sob Engenharia (Anti-Overengineering)

Aplica rigorosamente o princípio da solução minimalista e pragmática: questiona a real necessidade da tarefa, reutiliza código existente, prioriza a biblioteca padrão e recursos nativos da plataforma e elimina complexidade acidental.

## Input/Output Signature
Input:
- proposedCodeSolution: string # Código, plano ou proposta técnica pretendida para resolver o problema
- activeTechStack: object # Bibliotecas nativas e dependências já instaladas no projeto
- taskCoreRequirement: string # A necessidade essencial e inegociável que precisa ser atendida
Output:
- minimalViableAlternative: string # Versão enxuta da solução com o mínimo de linhas e dependências
- eliminatedAbstractions: array # Lista de classes genéricas, factories ou camadas descartadas
- savedLinesCount: number # Quantidade de linhas de código evitadas ou deletadas
- complexityVerdict: string # Avaliação da solução (approved_minimal, overengineered, rejected)

## Router and Selection Matrix
| Nível na Escada Minimalista | Ação Recomendada | Grau de Liberdade |
|---|---|---|
| Nível 0: Não Fazer | Questiona se o recurso realmente precisa existir ou se resolve um problema falso | [FRÁGIL] Se a necessidade não for comprovada, cancela a tarefa |
| Nível 1: Reuso Interno | Reaproveita funções e módulos utilitários já presentes no repositório | [FLEXÍVEL] Evita duplicação de lógica e novos contratos |
| Nível 2: Biblioteca Padrão | Utiliza APIs nativas do Node/Browser (`fetch`, `crypto`, `URL`) sem pacotes npm | [FRÁGIL] Proibido instalar dependências externas para utilitários triviais |
| Nível 3: Abstração Mínima | Escreve código direto e plano sem hierarquias especulativas de herança | [FLEXÍVEL] Aplica princípio YAGNI (You Aren't Gonna Need It) |

## Imperative Execution Workflow
1. Questionar a Necessidade da Mudança [FRÁGIL]:
   - Questione se o problema pode ser resolvido com documentação, configuração existente ou se a demanda é prematura.
2. Identificar Código Reutilizável no Repositório [FLEXÍVEL]:
   - Busque funções e utilitários já testados no projeto antes de escrever novas linhas do zero.
3. Priorizar Recursos Nativos da Plataforma [FRÁGIL]:
   - Substitua sugestões de novas bibliotecas por APIs padrão do runtime (ex: `Intl` em vez de bibliotecas pesadas de data).
4. Podar Abstrações Especulativas [FLEXÍVEL]:
   - Elimine classes adaptadoras para múltiplos provedores hipotéticos se o projeto utiliza apenas um provedor real.
5. Mensurar Redução de Complexidade e Linhas [FRÁGIL]:
   - Valide que o código resultante é legível para qualquer engenheiro pleno e que não cria débitos de manutenção.

## Execution Checklist
- [ ] Questionar se a alteração é estritamente indispensável
- [ ] Verificar e reutilizar utilitários existentes no projeto
- [ ] Recorrer a APIs nativas antes de avaliar novas dependências
- [ ] Eliminar camadas de indireção, factories e interfaces especulativas
- [ ] Validar que o código atende ao objetivo com a menor complexidade viável

## On Failure
- **Gatilho de Erro**: Proposta introduz dependência desnecessária para lógica simples, cria hierarquia de classes ociosa ou duplica lógica interna.
- **Ação Imediata**: Vetar a solução sobrecarregada e apresentar alternativa enxuta.
- **Rollback**: Descartar rascunhos de arquiteturas especulativas geradas.
- **Fallback**: Adotar implementação direta em uma única função pura sem camadas adicionais.
- **Logs**: Registrar abstrações rejeitadas, dependências evitadas e linhas de código poupadas.

## Reference Documentation
Consulte a documentação técnica completa: [Referência Técnica](reference.md).
