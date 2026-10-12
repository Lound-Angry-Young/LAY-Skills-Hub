# Referência Arquitetural do Domínio: DOCUMENTATION

## Table of Contents
1. [Visão Geral do Domínio](#visão-geral-do-domínio)
2. [Catálogo de Habilidades e Responsabilidades](#catálogo-de-habilidades-e-responsabilidades)
3. [Padrões de Integração e Roteamento](#padrões-de-integração-e-roteamento)
4. [Diretrizes de Qualidade e Segurança](#diretrizes-de-qualidade-e-segurança)

## Visão Geral do Domínio
O domínio `documentation` reúne um conjunto de habilidades altamente especializadas e desacopladas, projetadas segundo os padrões estritos de Agent Skills da Anthropic.
Finalidade: Documentação Técnica e Prose Engineering.

## Catálogo de Habilidades e Responsabilidades
| [polishing-user-facing-prose](./polishing-user-facing-prose/SKILL.md) | Cleans and finalizes authorized natural-language text for readers by auditing invisible Unicode and rewriting prose while keeping facts, meaning and the writer voice | `[./polishing-user-facing-prose/SKILL.md](./polishing-user-facing-prose/SKILL.md)` |
| [documenting-architecture-decisions](./documenting-architecture-decisions/SKILL.md) | Records architecture decisions as ADRs and documents the reasoning behind design choices, public API changes and shipped features for future engineers and agents | `[./documenting-architecture-decisions/SKILL.md](./documenting-architecture-decisions/SKILL.md)` |
| [stripping-ai-provenance-marks](./stripping-ai-provenance-marks/SKILL.md) | Removes multi-vendor AI provenance marks from text and files: invisible Unicode, statistical text watermarks through rewriting, and C2PA, EXIF, XMP and container metadata on images and documents | `[./stripping-ai-provenance-marks/SKILL.md](./stripping-ai-provenance-marks/SKILL.md)` |
| [auditing-writing-guidelines](./auditing-writing-guidelines/SKILL.md) | Reviews docs and prose for Writing Guidelines compliance, checking style, voice and tone against the writing handbook | `[./auditing-writing-guidelines/SKILL.md](./auditing-writing-guidelines/SKILL.md)` |

## Padrões de Integração e Roteamento
- Cada habilidade opera com assinatura estrita de Input/Output.
- O roteador de domínio (`SKILL.md`) atua como camada de orquestração de 1 nível de profundidade.
- Habilidades com rotinas extensas ou especificações técnicas possuem seus próprios arquivos `reference.md` auxiliares.

## Diretrizes de Qualidade e Segurança
- Todas as execuções devem validar pré-condições antes de realizar qualquer alteração estrutural.
- Em caso de falha, acione a seção `## On Failure` com rollback imediato e logs diagnósticos.
