---
name: redesigning-legacy-interfaces
description: >
  Upgrades dated, cluttered or generic UIs to contemporary standards while preserving all existing functionality: design audit, fix priorities, typography upgrades, contrast fixes and layout cleanup. Use this skill when: modernizing an existing interface or redesigning an older screen. Do NOT use this skill when: reviewing code without redesigning (use auditing-web-design-guidelines) or starting a new design from scratch (use elevating-frontend-taste).
---

# Redesenho e Modernização de Interfaces Legadas

Moderniza telas e componentes visuais datados ou sobrecarregados sem alterar a regra de negócio: auditoria de débitos visuais, hierarquia tipográfica contemporânea, alinhamento óptico e remoção de poluição visual.

## Input/Output Signature
Input:
- legacyComponentFilePath: string # Caminho do arquivo ou tela legada a ser redesenhada
- targetDesignDirection: string # Estilo pretendido (modern_minimal, dark_tech, contemporary_clean)
- preserveContractProps: boolean # Se as propriedades e assinaturas públicas do componente devem ser mantidas (default: true)
Output:
- redesignSuccess: boolean # Status da modernização visual
- eliminatedLegacyTropesList: array # Lista de vícios estéticos antigos purgados (sombras duras, gradientes de 2010, bordas espessas)
- modernizedComponentCode: string # Código fonte atualizado com estilização contemporânea
- executionLog: string # Registro dos passos de refatoração visual

## Router and Selection Matrix
| Vício Visual Legado | Técnica de Modernização | Grau de Liberdade |
|---|---|---|
| Bordas Espessas e Sombras Escuras Difusas | Substitui por bordas sutis de 1px em baixa opacidade e superfícies tonais | [FRÁGIL] Melhora a elegância e reduz a poluição visual imediata |
| Falta de Contraste Tipográfico | Amplia contraste entre títulos e corpo, ajusta line-height e tracking | [FLEXÍVEL] Garante leitura fluida e hierarquia clara |
| Alinhamento Central Monótono | Realinha conteúdos à esquerda em grid estruturado com ancoragem visual | [FLEXÍVEL] Melhora a velocidade de escaneamento visual da página |
| Botões e Controles Sem Estados | Implementa estados refinados de hover, foco visível, disabled e active | [FRÁGIL] Preserva acessibilidade WCAG sem alterar lógica de clique |

## Imperative Execution Workflow
1. Executar Auditoria Visual do Componente Legado [FRÁGIL]:
   - Mapeie todos os elementos em tela conferindo contraste de cores, espaçamentos inconsistentes e clichês visuais ultrapassados.
2. Preservar Regras de Negócio e Assinaturas [FRÁGIL]:
   - Isole handlers de clique, chamadas de API e props públicas garantindo que nenhuma funcionalidade seja perdida.
3. Atualizar Paleta de Superfícies e Bordas [FLEXÍVEL]:
   - Substitua fundos planos ou gradientes pesados por superfícies sofisticadas com separadores delicados.
4. Refatorar Hierarquia Tipográfica e Espaçamento [FLEXÍVEL]:
   - Aplique escala proporcional coerente com espaçamentos múltiplos de 4px ou 8px para consistência rítmica.
5. Validar Acessibilidade e Paridade Funcional [FRÁGIL]:
   - Teste todos os fluxos de interação do componente e certifique-se de que a nova interface é 100% equivalente à original.

## Execution Checklist
- [ ] Mapear todas as ações e comportamentos do componente original
- [ ] Eliminar bordas pesadas, sombras agressivas e gradientes antigos
- [ ] Aplicar escala tipográfica contemporânea e espaçamento harmônico
- [ ] Implementar estados completos de interação e foco
- [ ] Confirmar que todas as propriedades e eventos originais continuam funcionando

## On Failure
- **Gatilho de Erro**: Perda de evento de clique, quebra de layout responsivo ou remoção acidental de funcionalidade existente.
- **Ação Imediata**: Parar a estilização e conferir a árvore DOM contra o código original.
- **Rollback**: Restaurar o código do componente original a partir do repositório.
- **Fallback**: Aplicar a modernização em pequenos incrementos visuais, mantendo o markup original.
- **Logs**: Registrar funcionalidades que divergiram e propriedades perdidas durante o redesenho.

## Reference Documentation
Consulte a documentação técnica completa: [Referência Técnica](reference.md).
