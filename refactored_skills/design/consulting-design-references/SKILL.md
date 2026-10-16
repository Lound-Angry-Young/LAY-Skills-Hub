---
name: consulting-design-references
description: >
  Selects a product-specific visual direction from the awesome-design-md collection and compares design systems before an interface is implemented, consulting source designs selectively while preserving the project's brand. Use this skill when: choosing a visual direction for a product or comparing design systems before implementing an interface. Do NOT use this skill when: the project already has a defined design system to follow or the task is a pixel-level fix to existing UI.
---

# Consulta a Referências de Design e Sistemas Visuais

Pesquisa e analisa especificações de design systems modernos (DESIGN.md) curadas em repositórios de referência para extrair princípios tipográficos, paletas, densidade e padrões de interação sem copiar marcas registradas.

## Input/Output Signature
Input:
- productCategory: string # Segmento do produto (fintech, devtool, dark-tech, editorial, arcade)
- visualIntent: string # Intenção estética (minimalista, brutalista, corporativo de luxo, utilitário)
- currentBrandTokens: object # Tokens já estabelecidos de cor, fontes e raio de borda do projeto
Output:
- recommendedReferenceSpecs: array # Lista de arquivos DESIGN.md selecionados para estudo comparativo
- comparativeAnalysis: object # Matriz comparativa de tipografia, densidade, estados e acessibilidade
- adaptedDesignDirectives: array # Diretrizes visuais adaptadas para o design system local
- validationNotes: string # Parecer de contraste WCAG, ergonomia de leitura e foco por teclado

## Router and Selection Matrix
| Segmento / Intenção | Referência Recomendada | Grau de Liberdade |
|---|---|---|
| Dark-Tech / Desenvolvedores | Analisa especificações de produtos utilitários de alta densidade técnica | [FLEXÍVEL] Adota tipografia mono e bordas sutis sem imitar interfaces conhecidas |
| Editorial / Portfólio de Luxo | Analisa especificações focadas em tipografia expressiva e grids assimétricos | [FLEXÍVEL] Prioriza hierarquia vertical e contraste tonal quente |
| Dashboard Analítico / SaaS | Analisa sistemas de design orientados a densidade de dados e legibilidade | [FRÁGIL] Exige rigor em contraste de dados, status semânticos e estados de hover |
| Design System Existente | Compara apenas tokens e estados interativos preservando a identidade local | [FRÁGIL] Proibido substituir tokens consolidados por estéticas herdadas de fora |

## Imperative Execution Workflow
1. Delimitar Objetivo do Produto e Requisitos do Usuário [FLEXÍVEL]:
   - Registre público-alvo, tarefa principal do usuário, plataforma pretendida e restrições de acessibilidade.
2. Localizar e Selecionar Arquivos DESIGN.md Relevantes [FRÁGIL]:
   - Inspecione a pasta de referências de design do repositório e escolha no máximo 2 a 3 especificações pertinentes.
3. Executar Análise Comparativa de Tokens e Padrões [FLEXÍVEL]:
   - Compare escala tipográfica, tokens de espaçamento, hierarquia de cards, tratamento de sombras e microinterações.
4. Adaptar Diretrizes para o Design System Local [FRÁGIL]:
   - Traduza os aprendizados para a identidade e paleta do projeto, sem incorporar logotipos, nomes ou ativos protegidos.
5. Validar Acessibilidade e Ergonomia Visual [FRÁGIL]:
   - Confirme contraste de cores mínimo WCAG AA (4.5:1), indicadores visuais de foco por teclado e responsividade.

## Execution Checklist
- [ ] Mapear o público, objetivo do produto e tokens já estabelecidos
- [ ] Consultar seletivamente 2 a 3 referências no acervo de design systems
- [ ] Conduzir análise comparativa de hierarquia, tipografia e densidade
- [ ] Adaptar princípios para as variáveis e tokens do projeto atual
- [ ] Validar conformidade de contraste WCAG e navegação por teclado

## On Failure
- **Gatilho de Erro**: Cópia inadvertida de marcas registradas, tokens incompatíveis com a identidade existente ou contraste abaixo de WCAG AA.
- **Ação Imediata**: Parar a formulação de diretrizes e purgar menções a identidades de terceiros.
- **Rollback**: Restaurar as definições visuais originais do projeto.
- **Fallback**: Adotar estética neutra utilitária com escala tipográfica padrão e tokens monocromáticos seguros.
- **Logs**: Registrar referências analisadas, divergências de contraste e justificativa da adaptação.
