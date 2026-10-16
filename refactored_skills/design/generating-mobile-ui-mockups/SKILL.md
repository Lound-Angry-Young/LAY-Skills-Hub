---
name: generating-mobile-ui-mockups
description: >
  Generates complete, high-impact mobile UI mockups: screen-first layouts, strict safe-area handling, tactile micro-interactions, mobile bento grids, and calibrated contrast for iOS and Android. Use this skill when: designing mobile application interfaces, mobile web experiences, or native mobile screens. Do NOT use this skill when: designing desktop-only dashboards (use generating-web-ui-references) or implementing mobile code directly (use building-react-native-interfaces).
---

# Geração de Mockups de Interfaces Mobile

Projeta telas de aplicativos móveis de alto impacto visual (iOS e Android), aplicando zonas seguras (safe areas), ergonomia de polegar, grids bento móveis e microinterações táteis expressivas.

## Input/Output Signature
Input:
- mobilePlatform: string # Plataforma alvo (ios, android, responsive_mobile_web)
- screenFlowName: string # Nome do fluxo de telas (ex: onboarding, checkout, dashboard_carteira)
- designTheme: string # Tema visual (dark_luxury, minimal_tech, vibrant_arcade)
- requiredScreenCount: number # Quantidade de telas consecutivas no fluxo (mínimo 3)
Output:
- screenMockupSpecs: array # Especificações detalhadas de layout de cada tela do fluxo
- safeAreaDirectives: object # Coordenadas de entalhe (notch), barra de status e barra de navegação
- tactileInteractionsMap: array # Mapeamento de gestos, estados de toque (press) e feedback
- colorAndTypographyTokens: object # Tokens tipográficos e paleta ajustados para displays OLED

## Router and Selection Matrix
| Plataforma / Tipo de Tela | Diretriz Ergonômica | Grau de Liberdade |
|---|---|---|
| iOS Human Interface | Respeita raio de cantos squircle, Dynamic Island e safe areas inferiores de 34pt | [FRÁGIL] Exige áreas de toque mínimas de 44x44pt |
| Android Material You | Adota elevações tonais, navegação por gestos de borda e safe areas de câmera | [FRÁGIL] Exige áreas de toque mínimas de 48x48dp |
| Fluxo Contínuo / Carrossel | Garante pistas visuais de continuidade lateral (peek) para guiar o polegar | [FLEXÍVEL] Ajusta percentual de visibilidade do próximo card |
| Modais e Bottom Sheets | Utiliza gavetas inferiores expansíveis com alça de arraste e overlay com blur | [FLEXÍVEL] Aplica física de mola para fechamento e ancoragem |

## Imperative Execution Workflow
1. Mapear Jornada do Fluxo de Telas [FLEXÍVEL]:
   - Estabeleça a sequência narrativa das telas (ex: entrada de dados -> confirmação visual -> recibo de conclusão).
2. Configurar Zonas Seguras e Grid Base [FRÁGIL]:
   - Calibre as margens para evitar sobreposição com barras de status, recortes de câmera e barras de navegação do sistema.
3. Posicionar Ações Primárias na Zona do Polegar [FRÁGIL]:
   - Aloque botões principais de ação e controles interativos críticos na metade inferior da tela para alcance fácil com uma mão.
4. Estruturar Grids Bento e Cartões com Hierarquia Clara [FLEXÍVEL]:
   - Agrupe informações relacionadas em cards modulares com bordas sutis e tipografia escalonada para telas menores.
5. Mapear Estados Interativos de Toque e Transições [FRÁGIL]:
   - Descreva estados visuais para `active`, `pressed` com leve redução de escala (0.97) e feedback de transição entre telas.

## Execution Checklist
- [ ] Definir o fluxo narrativo de telas completas
- [ ] Isolar áreas de safe area superior e inferior
- [ ] Posicionar chamadas de ação primárias na zona ergonômica de alcance do polegar
- [ ] Organizar o conteúdo em cards e bento grids modulares
- [ ] Especificar transições de tela e estados visuais táteis

## On Failure
- **Gatilho de Erro**: Botões vitais fora da zona de alcance, sobreposição com elementos nativos do sistema ou densidade excessiva.
- **Ação Imediata**: Redesenhar a hierarquia da tela e realocar os controles de ação.
- **Rollback**: Descartar propostas de layouts com zonas de toque comprimidas abaixo dos padrões mínimos.
- **Fallback**: Quebrar uma tela sobrecarregada em duas etapas progressivas (wizard linear).
- **Logs**: Registrar dimensões de áreas de toque rejeitadas e elementos em conflito com safe areas.

## Reference Documentation
Consulte a documentação técnica completa: [Referência Técnica](reference.md).
