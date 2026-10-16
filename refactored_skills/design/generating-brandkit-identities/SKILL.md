---
name: generating-brandkit-identities
description: >
  Generates complete brand-kit identities following agency-grade design standards: monogram meaning, metaphor fusion, calibrated palettes, negative space, typography pairings, and vector assets. Use this skill when: designing brand identities, monograms, logos, or brand systems from scratch. Do NOT use this skill when: writing marketing copy (use authoring-specifications-first) or generating single UI components (use engineering-frontend-interfaces).
---

# Geração de Brandkits e Identidades Visuais

Gera identidades visuais completas de padrão de agência global: fusão metafórica em monogramas, uso inteligente de espaço negativo, paleta de cores calibrada, tipografia de autoridade e ativos vetoriais.

## Input/Output Signature
Input:
- brandName: string # Nome da marca ou produto
- coreConceptKeywords: array # Palavras-chave do conceito central (ex: velocidade, segurança, precisão)
- aestheticArchetype: string # Arquétipo estético (dark-tech, luxury-craft, arcade-brutalist, neo-swiss)
- targetDeliverables: array # Entregáveis solicitados (monograma, logotipo, paleta, tipografia, tokens)
Output:
- brandbookSpec: object # Especificação completa da identidade visual em formato estruturado
- svgMonogramCode: string # Código vetorial SVG puro do monograma gerado
- colorPaletteTokens: object # Definições hexadecimais, HSL e papéis semânticos da paleta
- typographyPairing: object # Seleção de fontes para display, títulos e corpo com escala harmônica

## Router and Selection Matrix
| Arquétipo Estético | Diretriz de Criação | Grau de Liberdade |
|---|---|---|
| Dark-Tech / Cyber-Precision | Monograma geométrico afiado com linhas angulares e contrastes luminescentes | [FLEXÍVEL] Aplica geometria de precisão com acentos em tons ciano/neon |
| Luxury-Craft / Editorial | Monograma com serifa de alto contraste, espaçamento generoso e acabamento tátil | [FLEXÍVEL] Paleta quente, tons carvão profundo, bronze e ouro envelhecido |
| Neo-Swiss / Utilitário | Geometria pura sem ornamentos, foco em grid rígido e tipografia grotesca | [FRÁGIL] Exige rigor absoluto de alinhamento óptico e proporções áureas |
| Arcade / Gamificado | Formas pixel-density ou isometricidade controlada com estética retrô premium | [FLEXÍVEL] Contrastes vibrantes com preto absoluto e micro-detalhes |

## Imperative Execution Workflow
1. Mapear Fusão Metafórica e Conceito do Monograma [FLEXÍVEL]:
   - Combine a inicial da marca com uma metáfora funcional única (ex: letra 'L' + feixe óptico de precisão).
2. Construir Geometria Vetorial em Espaço Negativo [FRÁGIL]:
   - Projete as curvas do símbolo garantindo legibilidade tanto em favicon de 16px quanto em empenas gigantes.
3. Definir Paleta de Cores com Funções Semânticas [FRÁGIL]:
   - Estabeleça cor de fundo principal, superfícies elevadas, cor de texto primário e exatamente um acento vibrante.
4. Harmonizar Dupla Tipográfica de Autoridade [FRÁGIL]:
   - Selecione uma fonte de display distinta para títulos e uma sem serifa altamente legível com suporte a números tabulares.
5. Gerar Código SVG Puro e Manifesto de Tokens [FRÁGIL]:
   - Exporte o código SVG sem dependências externas e documente os tokens em formato CSS/Tailwind compatível.

## Execution Checklist
- [ ] Definir a metáfora central e a geometria do monograma
- [ ] Validar legibilidade do símbolo em escalas extremas (16px a 512px)
- [ ] Calibrar paleta com contraste estrito e funções semânticas claras
- [ ] Estabelecer par tipográfico com proporções e pesos balanceados
- [ ] Gerar arquivo vetorial SVG limpo e exportar tokens de estilo

## On Failure
- **Gatilho de Erro**: Símbolo genérico sem diferenciação, desenho ilegível em tamanhos reduzidos ou contraste de cor inadequado.
- **Ação Imediata**: Rejeitar a proposta gráfica e retornar à fase de fusão metafórica.
- **Rollback**: Descartar os arquivos SVG gerados e reverter tokens da paleta.
- **Fallback**: Optar por tratamento tipográfico puro (wordmark com tracking refinado) sem monograma complexo.
- **Logs**: Registrar palavras-chave analisadas, tentativas de traçado vetorial e motivos da rejeição.

## Reference Documentation
Consulte a documentação técnica completa: [Referência Técnica](reference.md).
