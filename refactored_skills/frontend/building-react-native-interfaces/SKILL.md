---
name: building-react-native-interfaces
description: >
  Applies React Native and Expo best practices for performant mobile apps: component structure, list performance, animations and native module usage. Use this skill when: building React Native components, optimizing list performance, implementing animations or working with Expo and native platform APIs. Do NOT use this skill when: the target is a web React or Next.js app (use optimizing-react-performance or engineering-frontend-interfaces).
---

# Construção de Interfaces Móveis em React Native e Expo

Desenvolve componentes e telas para aplicativos móveis nativos com React Native e Expo, aplicando otimizações de listas com FlashList, animações nativas fluidas via Reanimated e manipulação segura de APIs de plataforma.

## Input/Output Signature
Input:
- componentFilePath: string # Caminho do componente React Native a ser construído ou otimizado
- isExpoProject: boolean # Se o projeto utiliza o ecossistema Expo e Expo Router (default: true)
- interfaceType: string # Tipo de interface (list_screen, form, animated_dashboard, navigation_tab)
- targetPlatform: string # Plataforma pretendida (ios, android, cross_platform)
Output:
- buildSuccess: boolean # Status da implementação do componente
- performanceOptimizationsApplied: array # Lista de melhorias de performance aplicadas (memo, flashlist, worklet)
- nativeModulesLinked: array # Módulos nativos ou dependências de plataforma configuradas
- executionLog: string # Registro da validação do componente e dependências

## Router and Selection Matrix
| Tipo de Componente | Padrão Recomendado | Grau de Liberdade |
|---|---|---|
| Listas Longas ou Rolagem Infinita | Utiliza `@shopify/flash-list` com `estimatedItemSize` calibrado | [FRÁGIL] Proibido usar ScrollView ou FlatList sem reciclagem para listas grandes |
| Animações e Gestos | Implementa com `react-native-reanimated` e `react-native-gesture-handler` | [FRÁGIL] Todas as animações devem rodar na thread nativa (UI thread via worklet) |
| Layout e Dimensões | Utiliza Flexbox nativo e dimensões relativas respeitando SafeAreaView | [FRÁGIL] Exige uso de safe areas nativas para evitar recortes de tela |
| Estados de Toque e Feedback | Utiliza `Pressable` com feedback háptico via `expo-haptics` | [FLEXÍVEL] Calibra intensidade da vibração conforme relevância da ação |

## Imperative Execution Workflow
1. Configurar Estrutura de Contêiner com Zonas Seguras [FRÁGIL]:
   - Utilize componentes de SafeAreaProvider e configure margens para barras de status e gestos do sistema.
2. Otimizar Renderização de Itens em Listas [FRÁGIL]:
   - Aloque FlashList isolando cada linha em componente puro memoizado (`React.memo`) para evitar re-renderizações em lote.
3. Escrever Animações Executadas na Thread Nativa [FRÁGIL]:
   - Utilize hooks `useAnimatedStyle` e `withSpring` garantindo que nenhuma animação bloqueie a thread JavaScript.
4. Tratar Diferenças de Plataforma (iOS vs Android) [FLEXÍVEL]:
   - Aplique ajustes específicos via `Platform.select` para fontes, sombras (`elevation` vs `shadowColor`) e comportamentos de teclado.
5. Validar Consumo de Memória e Queda de Quadros [FRÁGIL]:
   - Confirme ausência de vazamento de listeners e garanta taxa estável de 60/120 FPS nas rolagens e transições.

## Execution Checklist
- [ ] Envolver tela com suporte adequado a safe areas nativas
- [ ] Empregar FlashList com tamanho estimado para listas de dados
- [ ] Executar animações na thread de UI através do Reanimated
- [ ] Adicionar feedback háptico e estados visuais em botões de toque
- [ ] Validar compatibilidade consistente em iOS e Android

## On Failure
- **Gatilho de Erro**: Queda de frames abaixo de 30 FPS, vazamento de memória em listas longas ou erro nativo de módulo não linkado.
- **Ação Imediata**: Parar a execução e simplificar a hierarquia do componente.
- **Rollback**: Reverter para implementação anterior mais leve ou remover animações complexas.
- **Fallback**: Substituir animações dinâmicas por transições de opacidade diretas e desativar efeitos de blur pesados.
- **Logs**: Registrar perfil de FPS, tempo gasto na thread JS vs UI e alertas de re-renderização emitidos pelo profiler.

## Reference Documentation
Consulte a documentação técnica completa: [Referência Técnica](reference.md).
