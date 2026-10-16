---
name: elevating-frontend-taste
description: >
  Elevates frontend design taste: brief inference, three-dial configuration (expressiveness, density, polish), deliberate typographic pairings, custom color systems and layout variance to eliminate generic AI aesthetic tropes. Use this skill when: designing, writing or reviewing user-facing frontend code where aesthetics, personality or visual quality matters. Do NOT use this skill when: the task is purely structural or backend logic with no visual impact.
---

# Elevação de Padrão Estético de Frontend (Design Taste)

Eleva a direção de arte e o acabamento visual de interfaces web: leitura profunda do briefing, calibração dos três seletores (expressividade, densidade e acabamento), duplas tipográficas intencionais e eliminação radical de clichês visuais de IA.

## Input/Output Signature
Input:
- projectBrief: string # Descrição do produto, público e tom desejado
- targetComponentOrScreen: string # Arquivo da tela ou componente a ser elevado esteticamente
- activeDialsConfig: object # Configuração dos três seletores (expressiveness: 1-10, density: 1-10, polish: 1-10)
Output:
- elevatedDesignSystem: object # Sistema visual calibrado (fontes, paleta semântica, espaçamentos, microinterações)
- transformedComponentCode: string # Código atualizado livre de fórmulas genéricas
- eliminatedTropesList: array # Lista de clichês eliminados (mesh gradients, sombras infladas, centralização sem propósito)
- aestheticAuditReport: string # Diagnóstico fundamentado da nova postura visual

## Router and Selection Matrix
| Tom do Produto / Público | Calibração dos Seletores (Dials) | Grau de Liberdade |
|---|---|---|
| Infraestrutura / Ferramenta para Devs | Expressividade: 4, Densidade: 9, Acabamento: 9 (Dark-tech de precisão) | [FLEXÍVEL] Foco em tipografia mono, bordas de 1px e preto absoluto |
| Estúdio Criativo / Editorial | Expressividade: 9, Densidade: 4, Acabamento: 10 (Assimetria dramática) | [FLEXÍVEL] Tipografia expressiva gigante e espaços em branco deliberados |
| Fintech de Alto Padrão / Luxo | Expressividade: 6, Densidade: 6, Acabamento: 10 (Calmo e sólido) | [FRÁGIL] Exige paleta tonal quente e ausência de ornamentos estridentes |
| Aplicação com Estética Genérica | Elimina cartões brancos com sombras difusas e aplica contraste firme | [FRÁGIL] Banimento incondicional de templates SaaS previsíveis |

## Imperative Execution Workflow
1. Fazer Inferência Profunda do Briefing [FLEXÍVEL]:
   - Decodifique o que o produto realmente é e quem o utiliza; rejeite a tentação de aplicar a mesma estética a tudo.
2. Calibrar os Três Seletores Estéticos [FRÁGIL]:
   - Defina os níveis de Expressividade (quão ousado), Densidade (quão compacto) e Acabamento (nível de refinamento de microinterações).
3. Estabelecer Par Tipográfico Intencional [FRÁGIL]:
   - Escolha fontes que dialoguem com a proposta: contraste entre uma fonte de display cheia de voz e uma de leitura altamente neutra.
4. Construir Paleta com Tensão Visual Calibrada [FRÁGIL]:
   - Defina superfícies com profundidade real e eleja uma única cor de acento com papel estritamente funcional.
5. Injetar Variação Estrutural Anti-Slop [FLEXÍVEL]:
   - Quebre alinhamentos centralizados monótonos utilizando grids bento assimétricos e hierarquia visual evidente.

## Execution Checklist
- [ ] Analisar o nicho real do produto antes de escolher estilos
- [ ] Calibrar expressividade, densidade e acabamento
- [ ] Selecionar dupla tipográfica com contraste deliberado
- [ ] Aplicar paleta com funções semânticas claras e alto contraste
- [ ] Auditar a tela contra os clichês estéticos banidos pelo ecossistema

## On Failure
- **Gatilho de Erro**: Interface resultante parecendo template padrão de bootstrap/tailwind, contraste fraco ou dissonância com o público.
- **Ação Imediata**: Parar a estilização e reavaliar a calibração dos seletores estéticos.
- **Rollback**: Descartar classes de estilo genéricas adicionadas.
- **Fallback**: Adotar estética minimalista utilitária pura com foco em tipografia austera e preto e branco.
- **Logs**: Registrar clichês identificados e justificativa do redirecionamento artístico.

## Reference Documentation
Consulte a documentação técnica completa: [Referência Técnica](reference.md).
