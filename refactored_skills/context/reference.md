# Referência Arquitetural do Domínio: CONTEXT

## Table of Contents
1. [Visão Geral do Domínio](#visão-geral-do-domínio)
2. [Catálogo de Habilidades e Responsabilidades](#catálogo-de-habilidades-e-responsabilidades)
3. [Padrões de Integração e Roteamento](#padrões-de-integração-e-roteamento)
4. [Diretrizes de Qualidade e Segurança](#diretrizes-de-qualidade-e-segurança)

## Visão Geral do Domínio
O domínio `context` reúne um conjunto de habilidades altamente especializadas e desacopladas, projetadas segundo os padrões estritos de Agent Skills da Anthropic.
Finalidade: Engenharia de Contexto e Comunicação de Agentes.

## Catálogo de Habilidades e Responsabilidades
| [compressing-agent-messages](./compressing-agent-messages/SKILL.md) | Ultra-compressed communication mode that cuts output tokens while keeping technical accuracy, with lite, full, ultra and wenyan levels | `[./compressing-agent-messages/SKILL.md](./compressing-agent-messages/SKILL.md)` |
| [testing-cli-prompt-compression](./testing-cli-prompt-compression/SKILL.md) | Configures and tests prompt compression from the CLI: manages RTK filters and Caveman rules, stacked compression modes, and previews compression output with real prompts | `[./testing-cli-prompt-compression/SKILL.md](./testing-cli-prompt-compression/SKILL.md)` |
| [managing-cli-context-pipelines](./managing-cli-context-pipelines/SKILL.md) | Manages context engineering configurations, RTK filter sets and conversation sessions from the CLI, applying context-relay settings and inspecting active context pipelines | `[./managing-cli-context-pipelines/SKILL.md](./managing-cli-context-pipelines/SKILL.md)` |
| [engineering-agent-context](./engineering-agent-context/SKILL.md) | Optimizes agent context setup: starting new sessions, recovering from degraded output, switching between tasks and configuring rules files and context for a project | `[./engineering-agent-context/SKILL.md](./engineering-agent-context/SKILL.md)` |
| [architecting-generative-ai-apps](./architecting-generative-ai-apps/SKILL.md) | Researches implementation patterns for a generative-AI feature by comparing a relevant open-source example: architecture, provider boundaries, costs and tests before adapting any code | `[./architecting-generative-ai-apps/SKILL.md](./architecting-generative-ai-apps/SKILL.md)` |
| [generating-knowledge-graphs](./generating-knowledge-graphs/SKILL.md) | Answers questions about a codebase, its architecture, file relationships or project content by building and querying a persistent knowledge graph with graphify over code, docs, papers, images and videos, treating graphify-out/ as the first source when it exists | `[./generating-knowledge-graphs/SKILL.md](./generating-knowledge-graphs/SKILL.md)` |
| [refining-raw-product-ideas](./refining-raw-product-ideas/SKILL.md) | Refines raw ideas into sharp, actionable concepts through divergent and convergent thinking, stress-testing assumptions and expanding options before converging on one | `[./refining-raw-product-ideas/SKILL.md](./refining-raw-product-ideas/SKILL.md)` |
| [interviewing-user-requirements](./interviewing-user-requirements/SKILL.md) | Extracts what the user actually wants through a one-question-at-a-time interview until intent is about 95% clear, when a request is underspecified or the user asks to be interviewed or challenged | `[./interviewing-user-requirements/SKILL.md](./interviewing-user-requirements/SKILL.md)` |
| [orchestrating-lay-ecosystem-skills](./orchestrating-lay-ecosystem-skills/SKILL.md) | Coordinates the LAY skill repertoire: initial diagnosis of new and existing projects, installation and updates of the catalog, and selection of capabilities by area for design, engineering, security and audit | `[./orchestrating-lay-ecosystem-skills/SKILL.md](./orchestrating-lay-ecosystem-skills/SKILL.md)` |
| [configuring-prompt-compression](./configuring-prompt-compression/SKILL.md) | Configures RTK (command output), Caveman (prose) and stacked compression modes, managing language packs and custom rules, and testing prompt compression that reduces tokens by 60-90% | `[./configuring-prompt-compression/SKILL.md](./configuring-prompt-compression/SKILL.md)` |
| [optimizing-rtk-prompt-contexts](./optimizing-rtk-prompt-contexts/SKILL.md) | Configures RTK filters, context engineering rules and context relay settings, testing compression with real prompt samples and managing context transformation pipelines | `[./optimizing-rtk-prompt-contexts/SKILL.md](./optimizing-rtk-prompt-contexts/SKILL.md)` |
| [breaking-down-task-plans](./breaking-down-task-plans/SKILL.md) | Breaks a spec or clear requirements into ordered, implementable tasks, estimating scope and identifying work that can run in parallel when a task is too large to start | `[./breaking-down-task-plans/SKILL.md](./breaking-down-task-plans/SKILL.md)` |
| [discovering-and-invoking-skills](./discovering-and-invoking-skills/SKILL.md) | Discovers and invokes agent skills: the meta-skill that decides which skill or workflow applies when a session starts or a new piece of work begins | `[./discovering-and-invoking-skills/SKILL.md](./discovering-and-invoking-skills/SKILL.md)` |

## Padrões de Integração e Roteamento
- Cada habilidade opera com assinatura estrita de Input/Output.
- O roteador de domínio (`SKILL.md`) atua como camada de orquestração de 1 nível de profundidade.
- Habilidades com rotinas extensas ou especificações técnicas possuem seus próprios arquivos `reference.md` auxiliares.

## Diretrizes de Qualidade e Segurança
- Todas as execuções devem validar pré-condições antes de realizar qualquer alteração estrutural.
- Em caso de falha, acione a seção `## On Failure` com rollback imediato e logs diagnósticos.
