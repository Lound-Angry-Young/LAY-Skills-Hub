---
name: animating-react-view-transitions
description: >
  Implements seamless page transitions and shared-element layout animations in React using the View Transitions API and CSS animations with reduced-motion support. Use this skill when: adding animated screen transitions, tab switches or morphing shared elements in a React app. Do NOT use this skill when: the project is mobile React Native (use building-react-native-interfaces) or only needs GSAP timeline choreography (use engineering-gsap-motion-uis).
---

# Transições de Tela e Shared-Elements em React

Implementa transições visuais fluidas entre rotas e elementos compartilhados (morphing) em React utilizando a View Transitions API nativa e animações CSS aceleradas por GPU, com suporte obrigatório a preferências de movimento reduzido.

## Input/Output Signature
Input:
- transitionType: string # Tipo de transição (page_navigation, tab_switch, shared_element_morph, list_reorder)
- triggerComponentPath: string # Arquivo do componente que dispara ou recebe a transição
- durationMs: number # Duração da animação em milissegundos (default: 300)
- enableReducedMotionFallback: boolean # Se deve prover fade simples ou corte imediato quando solicitado (default: true)
Output:
- viewTransitionImplemented: boolean # Status da implementação da transição
- generatedCssRules: string # Regras CSS de pseudoelementos ::view-transition-old e ::view-transition-new
- modifiedFilesList: array # Arquivos de componente e folha de estilos atualizados
- executionLog: string # Registro dos passos de implementação

## Router and Selection Matrix
| Tipo de Transição | Técnica Recomendada | Grau de Liberdade |
|---|---|---|
| Navegação entre Rotas (App Router) | Invoca `document.startViewTransition` encapsulado em hook customizado | [FRÁGIL] Exige verificação prévia de suporte no navegador (`if (document.startViewTransition)`) |
| Elemento Compartilhado (Shared Element) | Atribui identificador CSS `view-transition-name` exclusivo ao elemento | [FRÁGIL] Proibido duplicar o mesmo nome de transição na mesma tela |
| Abas e Filtros de Lista | Anima transição de posição e opacidade com curvas bezier suaves | [FLEXÍVEL] Aplica timing function de desaceleração suave |
| Preferência de Movimento Reduzido | Desativa animação espacial via `@media (prefers-reduced-motion)` | [FRÁGIL] Obrigatório fornecer transição instantânea ou fade sutil |

## Imperative Execution Workflow
1. Verificar Suporte do Navegador e Fallback [FRÁGIL]:
   - Implemente wrapper defensivo verificando se `document.startViewTransition` existe antes da invocação.
2. Atribuir Nomes de Transição Exclusivos [FRÁGIL]:
   - Configure a propriedade CSS `view-transition-name` estritamente nos elementos que sofrerão morphing compartilhado.
3. Declarar Pseudoelementos de Animação CSS [FRÁGIL]:
   - Estilize `::view-transition-old(name)` e `::view-transition-new(name)` controlando opacidade, transform e duração.
4. Integrar com o Estado Reativo do React [FLEXÍVEL]:
   - Envolva a mutação de estado (ex: `setSelectedTab`) dentro do callback de atualização do `startViewTransition`.
5. Validar Acessibilidade e Queda de Quadros [FRÁGIL]:
   - Teste a página com emulação de movimento reduzido e confirme que a renderização não bloqueia o event loop.

## Execution Checklist
- [ ] Implementar verificação de suporte à View Transitions API com fallback seguro
- [ ] Atribuir identificadores view-transition-name exclusivos sem colisões
- [ ] Definir animações CSS aceleradas por GPU para entrada e saída
- [ ] Vincular atualização de estado React ao callback de transição
- [ ] Validar comportamento com prefers-reduced-motion ativado

## On Failure
- **Gatilho de Erro**: Colisão de view-transition-name com elementos duplicados, flicker de renderização ou travamento de frame.
- **Ação Imediata**: Desativar a transição animada e aplicar atualização de estado convencional direta.
- **Rollback**: Remover identificadores CSS de transição duplicados nos componentes.
- **Fallback**: Substituir por transição CSS de opacidade (fade) tradicional de 150ms.
- **Logs**: Registrar elementos envolvidos na colisão de nomes e exceções lançadas no console do navegador.

## Reference Documentation
Consulte a documentação técnica completa: [Referência Técnica](reference.md).
