# Referência Arquitetural do Domínio: DESIGN

## Table of Contents
1. [Visão Geral do Domínio](#visão-geral-do-domínio)
2. [Catálogo de Habilidades e Responsabilidades](#catálogo-de-habilidades-e-responsabilidades)
3. [Padrões de Integração e Roteamento](#padrões-de-integração-e-roteamento)
4. [Diretrizes de Qualidade e Segurança](#diretrizes-de-qualidade-e-segurança)

## Visão Geral do Domínio
O domínio `design` reúne um conjunto de habilidades altamente especializadas e desacopladas, projetadas segundo os padrões estritos de Agent Skills da Anthropic.
Finalidade: Design Visual, Brandkits e Mockups.

## Catálogo de Habilidades e Responsabilidades
| [generating-brandkit-identities](./generating-brandkit-identities/SKILL.md) | Generates premium brand-kit image boards for brand guidelines, logo systems, identity decks and visual-world presentations, with intentional logo concepting, sparse typography, symbolic meaning and art-directed imagery | `[./generating-brandkit-identities/SKILL.md](./generating-brandkit-identities/SKILL.md)` |
| [consulting-design-references](./consulting-design-references/SKILL.md) | Selects a product-specific visual direction from the awesome-design-md collection and compares design systems before an interface is implemented, consulting source designs selectively while preserving the project's brand | `[./consulting-design-references/SKILL.md](./consulting-design-references/SKILL.md)` |
| [generating-mobile-ui-mockups](./generating-mobile-ui-mockups/SKILL.md) | Generates premium, app-native mobile screen concepts and flows for iOS, Android and cross-platform products, shown inside a phone mockup with clean hierarchy, readable text and consistent multi-screen styling | `[./generating-mobile-ui-mockups/SKILL.md](./generating-mobile-ui-mockups/SKILL.md)` |
| [generating-web-ui-references](./generating-web-ui-references/SKILL.md) | Generates premium, conversion-aware website design reference images, producing one separate horizontal image per page section with varied composition, CTAs and hero scales under one consistent palette so developers can recreate the page | `[./generating-web-ui-references/SKILL.md](./generating-web-ui-references/SKILL.md)` |

## Padrões de Integração e Roteamento
- Cada habilidade opera com assinatura estrita de Input/Output.
- O roteador de domínio (`SKILL.md`) atua como camada de orquestração de 1 nível de profundidade.
- Habilidades com rotinas extensas ou especificações técnicas possuem seus próprios arquivos `reference.md` auxiliares.

## Diretrizes de Qualidade e Segurança
- Todas as execuções devem validar pré-condições antes de realizar qualquer alteração estrutural.
- Em caso de falha, acione a seção `## On Failure` com rollback imediato e logs diagnósticos.
