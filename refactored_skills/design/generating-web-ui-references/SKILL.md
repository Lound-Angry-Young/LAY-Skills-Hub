---
name: generating-web-ui-references
description: >
  Generates combinatorially varied, high-agency web UI references: asymmetric editorial layouts, 2-line minimal hero directives, dramatic dark-tech contrasts, and anti-slop guidelines. Use this skill when: conceptualizing web layouts, landing pages, or digital product interfaces before coding. Do NOT use this skill when: writing implementation code directly (use engineering-frontend-interfaces) or designing mobile apps (use generating-mobile-ui-mockups).
---

# Geração de Referências de Interfaces Web

Gera conceitos e especificações de layouts web de vanguarda, aplicando a regra de hero minimalista em 2 linhas, grids assimétricos editoriais, contrastes dramáticos dark-tech e variação combinatória anti-slop.

## Input/Output Signature
Input:
- productTrope: string # Nicho do produto (ex: ai-gateway, dev-infrastructure, luxury-fintech, creative-studio)
- visualAtmosphere: string # Atmosfera pretendida (dark-tech, industrial-minimal, high-fashion-editorial)
- primaryActionGoal: string # Ação principal esperada do visitante (ex: testar demo, instalar CLI, solicitar acesso)
Output:
- layoutSpecification: object # Estrutura completa da página dividida por seções numeradas
- heroArchitecture: object # Redação e diagramação estrita da seção hero com título em 2 linhas
- typographyAndColorRules: object # Definição de escala tipográfica assimétrica e paleta de alto contraste
- interactiveSectionsGuide: array # Guia detalhado de microinterações, carrosséis e efeitos de scroll

## Router and Selection Matrix
| Atmosfera Visual | Princípio de Composição | Grau de Liberdade |
|---|---|---|
| Dark-Tech / Developer Tools | Fundo preto puro ou carvão (#080808), tipografia mono pontual, linhas de 1px e badges | [FLEXÍVEL] Aplica grid técnico sem poluição visual |
| Editorial / Minimalismo Utilitário | Tipografia de display em escala dramática, espaços em branco generosos e colunas assimétricas | [FLEXÍVEL] Cria tensão visual equilibrada com blocos de texto concisos |
| Industrial / Neo-Brutalist | Tipografia condensada em caixa alta, separadores marcados, molduras evidentes e alto contraste | [FRÁGIL] Rejeita gradientes pastéis suaves e cantos arredondados genéricos |
| Luxury / High-Agency | Grids elegantes com microinterações refinadas, tipografia com contraste óptico e assets táteis | [FRÁGIL] Baniu elementos genéricos de templates SaaS comuns |

## Imperative Execution Workflow
1. Configurar Regra de Hero em 2 Linhas [FRÁGIL]:
   - Redija o título principal do hero em exatamente duas linhas com impacto direto, seguido de parágrafo explicativo conciso.
2. Definir Padrão de Variação Combinatória [FLEXÍVEL]:
   - Selecione a combinação única de fonte de display, paleta de acento e estrutura de grid para escapar de fórmulas previsíveis.
3. Estruturar Hierarquia de Seções em AIDA [FRÁGIL]:
   - Organize a página: Atenção (Hero), Interesse (Recurso Chave / Métricas), Desejo (Bento Grid com Provas), Ação (CTA Claro).
4. Diagramar Seções Bento com Assimetria Funcional [FLEXÍVEL]:
   - Crie cartões de diferentes proporções (2x1, 1x1, 1x2) onde cada bloco revela um detalhe técnico ou interativo único.
5. Validar Diretivas Anti-Slop e Performance [FRÁGIL]:
   - Elimine gradientes genéricos em mesh, mockups flutuantes vazios e carrosséis infinitos sem controle manual.

## Execution Checklist
- [ ] Aplicar a regra de título do hero em 2 linhas concisas
- [ ] Estabelecer paleta de alto contraste sem gradientes clichês
- [ ] Desenhar seções bento com variação proporcional assimétrica
- [ ] Garantir posicionamento claro e desobstruído da chamada para ação
- [ ] Auditar o conceito contra as diretrizes anti-slop

## On Failure
- **Gatilho de Erro**: Hero prolixo excedendo 2 linhas, layout parecendo template genérico de SaaS ou contraste insuficiente de leitura.
- **Ação Imediata**: Reescrever o hero e reformular a diagramação da primeira dobra.
- **Rollback**: Descartar estruturas de layout convencionais que reproduzam clichês visuais.
- **Fallback**: Adotar diagramação minimalista pura focada em tipografia editorial austera e terminal de código.
- **Logs**: Registrar títulos reprovados, seções descartadas e justificativa da quebra de padrão.

## Reference Documentation
Consulte a documentação técnica completa: [Referência Técnica](reference.md).
