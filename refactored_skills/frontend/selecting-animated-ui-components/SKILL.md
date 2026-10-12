---
name: selecting-animated-ui-components
description: >
  Selects an animated UI component from the Pixel-Perfect and Componentry registries for a screen need, ranking options by rendering cost tier, reduced-motion handling, client-component requirements, touch fallback and missing local files. Use this skill when: choosing a text effect, button, image reveal, gallery or carousel, scroll section, cursor effect, background, card, 3D element, SVG or logo, navigation dock or page block from those two registries. Do NOT use this skill when: the component is a plain React component without animation, a react-bits component (use animating-react-bits-components), a route transition (use animating-react-view-transitions), a smooth-scroll setup (use orchestrating-smooth-scroll), or the requirements are still unknown (use clarifying-screen-requirements first).
---

# Selecionando componentes animados

Escolha o componente pela necessidade da tela e depois pelo custo. Cada item do catálogo, com domínio, tier, flags e a coluna "Instalar antes", está em [reference.md](reference.md).

Esta skill não baixa nada. O catálogo é uma tabela local, lida sem rede. Só depois da escolha, o código é baixado, pela skill [integrating-external-ui-components](../integrating-external-ui-components/SKILL.md), e só o item e o que ele precisa.

## Antes de escolher

Não escolha com base em suposição. Se faltar um destes fatos, pare e use [clarifying-screen-requirements](../clarifying-screen-requirements/SKILL.md):
- objetivo do bloco e ação principal;
- dispositivo principal (celular, desktop ou ambos);
- stack do projeto (Next.js App Router, Vite ou outra);
- tolerância a movimento (sóbria, moderada ou expressiva).

## O que escolher

Os itens abaixo foram conferidos no catálogo. A coluna "Atenção" diz o que adicionar antes de publicar.

| Necessidade | Escolha primeiro | Alternativa | Atenção |
|---|---|---|---|
| Brilho contínuo em texto | `text-gradient` (T1, CSS) | `flipping-word-swap` (T2) | `text-gradient` não tem transição nem keyframes no código. `flipping-word-swap` trata movimento reduzido e toque |
| Entrada de título ao carregar | `kinetic-text-reveal` (T2, trata movimento reduzido) | `text-reveal` (T2) | `text-reveal` não trata movimento reduzido: adicionar |
| Botão de ação | `antinomy-button` (T2, trata movimento reduzido; exemplo de referência) | `premium-button` ou `metal-button` (T1, CSS) | `premium-button` e `metal-button` têm transição CSS e não tratam movimento reduzido: adicionar `@media (prefers-reduced-motion: reduce)` |
| Galeria ou carrossel | `cylinder-carousel` (T2, trata movimento reduzido e toque) | `orbit-card-stack` (T2, trata movimento reduzido) | `orbit-card-stack` não tem toque: adicionar fallback |
| Card com destaque no hover | `hover-transition` (T1, trata movimento reduzido e toque) | `tilt-card-glare` (T2) | `tilt-card-glare` não tem toque e precisa de verificação de diretiva |
| Revelação de imagem ao rolar | `directional-mask-reveal` (T2) | `wave-mask-reveal` (T2) | Os dois não tratam movimento reduzido: adicionar |
| Seção fixa com scroll | `sticky-scroll-cards` (T2, trata movimento reduzido) | `scroll-tilted-grid` (T2, trata movimento reduzido) | Sem atenção de diretiva: os dois já têm "use client" |
| Efeito que segue o cursor | `pixel-canvas` (T2, trata toque) | `magnet-lines` (T2) | `pixel-canvas` não trata movimento reduzido. `magnet-lines` não tem toque nem movimento reduzido |
| Menu ou dock | `magnetic-dock` (T2, trata movimento reduzido) | navegação sem animação | Não tem toque: adicionar fallback |
| Logo ou ícone animado | `svg-1` (T2, sem diretiva) | `signature` (T2) | `svg-1` e `signature` não tratam movimento reduzido: adicionar |
| Borda ou moldura decorativa | `border-1` (T1, sem diretiva) | `star-border` (T1) | Não tratam movimento reduzido. A descrição de `star-border` fala em cantos animados, mas o código não tem transição nem keyframes: confirme no navegador antes de prometer o efeito |
| Seção de preços | `pricing-02` (T1, trata movimento reduzido) | `pricing-01` (T1) | `pricing-01` não trata movimento reduzido |
| Hero completo | `gradient-hero-01` (T1, sem diretiva) | `hero-geometric` (T3) | `gradient-hero-01` não trata movimento reduzido. `hero-geometric` é WebGL: no máximo um por tela |
| Fundo de hero | T2 de canvas ou CSS (ver domínio fundos-animados no catálogo) | T3 só com pedido explícito | T3 usa a GPU a cada quadro |

Quando nenhum item servir, diga que o catálogo não tem o efeito e proponha CSS próprio ou um componente novo. Não invente nome de item.

## Como escolher

Aplique nesta ordem e pare na primeira decisão clara:
1. Dá para resolver só com CSS ou SVG? Escolha T1.
2. O tier cabe no orçamento da tela (seção seguinte)?
3. "Mov. reduzido" é "sim"? Se for "não", a escolha só vale com a checagem adicionada pela skill de integração.
4. "Use client" é "sim" ou "verificar"? A tela precisa de um limite de componente cliente.
5. "Toque" é "não"? O item depende de ponteiro. Adicione fallback antes de publicar.
6. "Faltam" tem entradas? Os arquivos faltantes entram no plano de instalação.
7. Bibliotecas com licença própria (GSAP, Three.js, lil-gui, Framer Motion, Motion)? Registre a nota de licença.
8. Só então compare com a direção visual pedida. A direção visual vem do usuário, não do catálogo.

## Orçamento de desempenho

O orçamento é regra deste hub, não medição. Meça no navegador antes de fechar a escolha em página crítica.
- **T1:** sem limite prático de quantidade. Cuide do layout e do reflow.
- **T2:** anime só `transform` e `opacity`. Como sugestão, mantenha no máximo três efeitos T2 ativos ao mesmo tempo, e pause os que estão fora da tela.
- **T3:** no máximo um por tela. Carregue com import dinâmico (no Next.js, com `ssr: false`) e pause com IntersectionObserver e aba oculta.
- **Depuração:** remova `lil-gui` antes de publicar. Há 17 itens com essa dependência.
- **Estado final:** todo efeito precisa de um estado final estático, usado com movimento reduzido.

## Checklist

- [ ] Necessidade e dispositivo confirmados
- [ ] Solução T1 avaliada antes de T2 e T3
- [ ] Tier cabe no orçamento da tela
- [ ] Movimento reduzido verificado ou planejado
- [ ] "Use client" identificado
- [ ] Fallback de toque para efeitos de ponteiro
- [ ] Arquivos faltantes listados
- [ ] Nota de licença registrada

## Manutenção

O catálogo é gerado por `scripts/gerar_catalogo_componentes.py`, que lê os registros ao vivo, sem clonar repositórios. Regenere quando quiser atualizar. A origem e a data de cada leitura ficam na seção 5 do catálogo. Na instalação, o CLI baixa a versão atual do registro, que pode ser mais nova que o catálogo.
