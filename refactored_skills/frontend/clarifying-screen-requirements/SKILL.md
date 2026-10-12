---
name: clarifying-screen-requirements
description: >
  Asks targeted questions before a screen, landing page, section or animated component is generated, to capture the real goal, primary device, stack, visual direction, motion tolerance, performance budget and content status, so the output does not rest on silent assumptions. Use this skill when: a request asks to create or generate a screen, page, section or component and at least one critical fact is missing. Do NOT use this skill when: the user already gave the critical facts, the task is a bug fix or a code review, or the question is product discovery (use interviewing-user-requirements).
---

# Esclarecendo requisitos de tela

Antes de gerar uma tela, confirme os fatos abaixo. Não gere com premissa silenciosa. Premissa aceita pelo usuário pode ser usada, desde que apareça no resumo.

## Fatos críticos (bloqueiam a geração)

1. **Objetivo e ação principal.** O que a tela faz e qual ação o usuário deve tomar. Ex.: comprar, agendar, entender o produto.
2. **Dispositivo principal.** Celular, desktop ou os dois, com a proporção se souber.
3. **Stack.** Framework e estrutura do projeto. Descubra antes de perguntar: leia `package.json`, `components.json` e `next.config.*`. Pergunte só o que o projeto não mostra.
4. **Tolerância a movimento.** Sóbria, moderada ou expressiva. Define quais itens do catálogo cabem.
5. **Direção visual.** Cores, tipografia ou referência já definidas. Se não houver, a direção é decidida com o usuário, não pelo catálogo.

## Fatos secundários (podem virar premissa, marcada como tal)

6. **Orçamento de desempenho.** O público usa aparelhos modestos ou conexão lenta? Sem resposta, a premissa é aparelho intermediário, registrada no resumo.
7. **Conteúdo.** Textos e imagens reais ou placeholder.
8. **Acessibilidade.** Premissa padrão do hub: WCAG AA. Registre a premissa.
9. **Modo escuro.** Exigido ou não.

## Protocolo

1. Leia o pedido e o projeto antes de perguntar. Responda sozinho o que o projeto já mostra.
2. Liste os fatos críticos que faltam, em ordem de bloqueio.
3. Faça uma pergunta por vez, a de maior bloqueio. Use AskUserQuestion com 2 a 4 opções objetivas quando couber, mais "Outro".
4. Quando a resposta destravar as seguintes, siga para a próxima. Pare quando os fatos críticos estiverem completos.
5. Se o usuário responder "você decide", registre a premissa no resumo, marcada como premissa, e siga.
6. Antes de gerar, mostre um resumo curto com as decisões e as premissas. Gere depois.

## Quando não há ferramenta de pergunta

Um subagente sem AskUserQuestion não gera arquivos. Devolva no RESULT `status: awaiting-answers` com as perguntas em ordem de bloqueio. A conversa principal faz as perguntas e reenvia o contexto no HANDOFF.

## Erros comuns

- Perguntar o que o projeto já responde, como a stack ou as cores existentes. Leia antes.
- Mandar uma lista de dez perguntas. Uma por vez, a de maior bloqueio.
- Gerar com premissa não registrada. O usuário não sabe o que foi decidido por ele.
