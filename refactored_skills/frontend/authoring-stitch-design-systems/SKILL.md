---
name: authoring-stitch-design-systems
description: >
  Generates semantic DESIGN.md files for Google Stitch that enforce premium, anti-generic UI standards: strict typography, calibrated color, asymmetric layouts, perpetual micro-motion and hardware-accelerated performance. Use this skill when: producing a DESIGN.md design system for Stitch screen generation. Do NOT use this skill when: the target is not Stitch or the task is implementing code directly (use engineering-frontend-interfaces).
---

# Autoria de Design Systems para Google Stitch

Elabora especificações formais de sistemas de design (DESIGN.md) otimizadas para o motor do Google Stitch, estabelecendo regras tipográficas rigorosas, paletas calibradas, layouts assimétricos e microinterações de alto padrão.

## Input/Output Signature
Input:
- productIdentityName: string # Nome do produto ou projeto para o qual o design system será gerado
- visualVibeDirection: string # Direção estética (dark_tech_luxury, neo_brutalist, refined_minimal, arcade_craft)
- targetPlatformOutput: string # Plataforma principal de destino das telas do Stitch (web, mobile, cross_platform)
Output:
- designMdFilePath: string # Caminho do arquivo DESIGN.md gerado e formatado
- designTokensManifest: object # Definições estruturadas de cores, fontes, espaçamentos e raios
- generatedLayoutRules: array # Diretrizes de diagramação e microinterações persistentes
- executionLog: string # Registro da geração e validação da especificação

## Router and Selection Matrix
| Direção Visual | Especificação DESIGN.md | Grau de Liberdade |
|---|---|---|
| Dark-Tech Luxury | Paleta preta profunda, acentos ciano/âmbar de precisão, fontes sans geométricas e mono | [FLEXÍVEL] Define regras de cards de vidro escuro e linhas de 1px |
| Neo-Brutalist Industrial | Cores de alto impacto, molduras evidentes, sombras duras (box-shadow sólida) e tipografia caixa alta | [FRÁGIL] Baniu cantos arredondados suaves e transições pastéis |
| Refined Minimalist | Espaçamento generoso, contraste tipográfico editorial, paleta monocromática quente | [FLEXÍVEL] Foco em proporções e hierarquia visual desobstruída |
| Arcade Craft | Cores saturadas sobre preto absoluto, detalhes em pixel e microinterações gamificadas | [FLEXÍVEL] Estipula feedback visual sonoro e tátil nas ações |

## Imperative Execution Workflow
1. Mapear Identidade e Pilares Visuais [FLEXÍVEL]:
   - Defina os 3 adjetivos inegociáveis que descrevem a sensação da interface gerada pelo Stitch.
2. Declarar Paleta Semântica e Tokens de Superfície [FRÁGIL]:
   - Especifique valores hexadecimais para fundo, cartões, texto primário, texto atenuado e cor de acento principal.
3. Estabelecer Escala Tipográfica e Par de Fontes [FRÁGIL]:
   - Determine fonte de display com personalidade marcante e fonte de corpo com suporte completo a pesos e números tabulares.
4. Estruturar Diretrizes de Layout e Diagramação [FLEXÍVEL]:
   - Documente regras de grid assimétrico, seções bento, hero minimalista em 2 linhas e zonas seguras.
5. Consolidar e Salvar o Arquivo DESIGN.md [FRÁGIL]:
   - Grave o arquivo estruturado na raiz ou pasta de documentação pronto para leitura dos prompts do Stitch.

## Execution Checklist
- [ ] Definir pilares estéticos e vocabulário visual do produto
- [ ] Especificar tokens de cor calibrados com papéis semânticos claros
- [ ] Estabelecer par de fontes e escala tipográfica harmônica
- [ ] Detalhar padrões de layout, grids bento e regras de microinteração
- [ ] Salvar arquivo DESIGN.md formatado e pronto para consumo do Stitch

## On Failure
- **Gatilho de Erro**: Especificação genérica sem personalidade marcante, tokens de cor em conflito ou ausência de regras de layout.
- **Ação Imediata**: Interromper a geração e reforçar as restrições anti-slop no documento.
- **Rollback**: Descartar versões de DESIGN.md que utilizem padrões de template convencionais.
- **Fallback**: Adotar o arquétipo dark-tech utilitário como padrão de base seguro.
- **Logs**: Registrar tópicos ausentes na especificação e regras que precisaram ser recalculadas.

## Reference Documentation
Consulte a documentação técnica completa: [Referência Técnica](reference.md).
