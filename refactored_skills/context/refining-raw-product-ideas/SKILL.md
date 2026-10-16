---
name: refining-raw-product-ideas
description: >
  Refines raw ideas into sharp, actionable concepts through divergent and convergent thinking, stress-testing assumptions and expanding options before converging on one. Use this skill when: an idea is still vague, assumptions need stress-testing or options should be expanded before a plan. Do NOT use this skill when: the idea is already defined and needs requirements or a spec (use authoring-specifications-first).
---

# Refinamento de Ideias Brutas de Produto

Refina propostas conceituais em visões de produto afiadas e acionáveis, aplicando pensamento divergente para expandir alternativas e convergente para testar premissas e selecionar o núcleo viável.

## Input/Output Signature
Input:
- rawConceptDescription: string # Ideia inicial, rascunho ou oportunidade descrita pelo usuário
- targetAudience: string # Público-alvo, personas ou segmento atendido
- differentiationFocus: string # Foco pretendido de diferenciação (velocidade, simplicidade, estética, nicho)
Output:
- refinedProductConcept: object # Conceito estruturado com proposta de valor, público e mecânica
- criticalAssumptions: array # Lista de suposições críticas que precisam de validação
- killSwitches: array # Condições objetivas que determinariam o abandono ou pivot da ideia
- recommendedDirection: string # Direção recomendada fundamentada em evidências e trade-offs

## Router and Selection Matrix
| Condição / Cenário | Ação Recomendada | Grau de Liberdade |
|---|---|---|
| Ideia Ampla e Difusa | Fase Divergente: Explora 3 a 5 variações conceituais com propostas distintas | [FLEXÍVEL] Estimula exploração de ângulos não convencionais |
| Modelo Dependente de Premissas Frágeis | Teste de Estresse: Isola premissas que se falsas derrubam o produto | [FRÁGIL] Exige validação rigorosa das hipóteses centrais |
| Múltiplas Alternativas em Disputa | Fase Convergente: Compara trade-offs e seleciona a direção de maior viabilidade | [FRÁGIL] Aplica critérios objetivos de simplicidade e execução |
| Conceito Lapidado | Estrutura documento conceitual e encaminha para especificação | [FLEXÍVEL] Entrega base pronta para escrita de PRD e contratos |

## Imperative Execution Workflow
1. Isolar o Problema Central da Ideia [FLEXÍVEL]:
   - Separe o problema que vale a pena resolver das soluções superficiais sugeridas no pedido inicial.
2. Mapear Premissas Fundamentais (Kill-Switches) [FRÁGIL]:
   - Identifique as suposições críticas sobre comportamento do usuário ou viabilidade técnica cujo erro inviabiliza o produto.
3. Explorar Variações Estratégicas [FLEXÍVEL]:
   - Crie 3 direções distintas: a mais simples possível, a de maior diferenciação técnica e a de menor atrito operacional.
4. Aplicar Teste de Estresse e Redução ao Essencial [FRÁGIL]:
   - Corte todos os recursos que não fazem parte do ciclo de valor primário até restar apenas o motor indispensável.
5. Formalizar Tese do Produto e Próximos Passos [FLEXÍVEL]:
   - Redija a tese consolidada com justificativa da escolha e encaminhe para criação da especificação técnica.

## Execution Checklist
- [ ] Definir com clareza o problema resolvido e público alvo
- [ ] Mapear as suposições críticas que matariam o produto se falsas
- [ ] Formular e comparar direções conceituais divergentes
- [ ] Reduzir a proposta ao seu núcleo funcional essencial
- [ ] Formalizar conceito refinado e pronto para especificação

## On Failure
- **Gatilho de Erro**: Proposta que não resolve uma dor identificável, premissas centrais comprovadamente inviáveis ou escopo inseparável de dependências externas intransponíveis.
- **Ação Imediata**: Apontar formalmente a inviabilidade do conceito e listar os bloqueadores estruturais.
- **Rollback**: Descartar qualquer detalhamento de arquitetura ou engenharia derivado do conceito inviável.
- **Fallback**: Propor pivot em direção a um problema adjacente viável ou retorno ao usuário com novas perguntas de negócio.
- **Logs**: Registrar as suposições refutadas, ângulos analisados e razões do veto conceitual.

## Reference Documentation
Consulte a documentação técnica completa: [Referência Técnica](reference.md).
