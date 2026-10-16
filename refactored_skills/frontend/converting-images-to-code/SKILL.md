---
name: converting-images-to-code
description: >
  Converts a visually important website into code by first generating section-specific design images, analyzing them in depth and implementing the site to match them as closely as possible, with a clean, readable hero. Use this skill when: turning a website design image or mockup into implemented web code. Do NOT use this skill when: the target is a mobile app (use building-react-native-interfaces) or the request has no visual reference to match.
---

# Conversão de Imagens e Mockups de Design em Código Web

Converte referências visuais, mockups e imagens de design em código web limpo, semântico e responsivo (HTML/Tailwind/React), decompondo o layout seção por seção e preservando alinhamento e contraste fiéis.

## Input/Output Signature
Input:
- sourceDesignImagePath: string # Caminho da imagem, mockup ou captura de tela de referência
- targetFramework: string # Framework de destino (react_tailwind, nextjs, html_css, svelte)
- outputComponentPath: string # Caminho onde o código implementado será gravado
- enforcePixelAlignment: boolean # Se deve buscar fidelidade milimétrica de espaçamento e tipografia (default: true)
Output:
- conversionSuccess: boolean # Status da implementação do código
- generatedComponentPath: string # Caminho do componente final gerado
- extractedDesignTokens: object # Cores, tipografia e raios de borda identificados na imagem
- executionLog: string # Registro das etapas de decomposição visual e codificação

## Router and Selection Matrix
| Complexidade da Imagem | Abordagem de Conversão | Grau de Liberdade |
|---|---|---|
| Landing Page Completa de Alta Densidade | Decompõe em seções isoladas (Hero, Recursos, Bento, CTA, Footer) | [FRÁGIL] Exige implementação sequencial seção por seção para manter fidelidade |
| Componente ou Card Isolado | Extrai tokens exatos de cor e tipografia e codifica em componente único | [FLEXÍVEL] Ajusta responsividade para múltiplos tamanhos de container |
| Seção com Elementos Gráficos Complexos | Isola formas vetoriais em SVGs limpos e sobrepõe texto renderizado real | [FRÁGIL] Proibido fatiar texto como imagem; todo texto deve ser selecionável |
| Layout com Referência de Baixa Resolução | Reconstrói a estrutura lógica aplicando as regras de taste do ecossistema | [FLEXÍVEL] Realiza inferência inteligente de contraste e hierarquia |

## Imperative Execution Workflow
1. Analisar Estrutura Visual e Decompor Seções [FRÁGIL]:
   - Inspecione a imagem de referência e divida o layout nas dobras naturais: Cabeçalho, Hero, Conteúdo e Rodapé.
2. Extrair Tokens de Cor, Tipografia e Espaçamentos [FRÁGIL]:
   - Identifique cores exatas de fundo, texto primário, acentos e determine famílias de fontes e escalas proporcionais.
3. Implementar Estrutura de Grid e Alinhamento [FLEXÍVEL]:
   - Construa o esqueleto com Flexbox e CSS Grid respeitando as margens, espaçamentos e distribuição visual da referência.
4. Renderizar Textos Semânticos e Elementos Interativos [FRÁGIL]:
   - Garanta que todos os títulos, parágrafos e botões sejam elementos HTML reais acessíveis, com estados de hover e foco.
5. Comparar Renderização contra a Imagem Original [FRÁGIL]:
   - Ajuste paddings, tamanhos de fonte e contrastes até que a página renderizada corresponda fielmente à intenção visual.

## Execution Checklist
- [ ] Decompor a imagem de referência em seções estruturais lógicas
- [ ] Extrair e padronizar paleta de cores e tamanhos tipográficos
- [ ] Codificar o layout com HTML semântico e classes utilitárias modernas
- [ ] Assegurar que nenhum texto seja renderizado como imagem estática
- [ ] Validar fidelidade visual e responsividade em múltiplos viewports

## On Failure
- **Gatilho de Erro**: Layout quebrado em telas menores, texto ilegível por baixo contraste ou discrepância estrutural gritante.
- **Ação Imediata**: Pausar a implementação e revisar o mapa de grid da seção com defeito.
- **Rollback**: Restaurar versão anterior do componente e isolar a seção que diverge da referência.
- **Fallback**: Priorizar a hierarquia semântica e legibilidade sobre alinhamentos rígidos quando houver conflito de responsividade.
- **Logs**: Registrar seções que apresentaram divergência de espaçamento e tokens de cor corrigidos.

## Reference Documentation
Consulte a documentação técnica completa: [Referência Técnica](reference.md).
