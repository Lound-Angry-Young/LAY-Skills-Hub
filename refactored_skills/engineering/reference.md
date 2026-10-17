# Referência Arquitetural do Domínio: ENGINEERING

## Table of Contents
1. [Visão Geral do Domínio](#visão-geral-do-domínio)
2. [Catálogo de Habilidades e Responsabilidades](#catálogo-de-habilidades-e-responsabilidades)
3. [Padrões de Integração e Roteamento](#padrões-de-integração-e-roteamento)
4. [Diretrizes de Qualidade e Segurança](#diretrizes-de-qualidade-e-segurança)

## Visão Geral do Domínio
O domínio `engineering` reúne um conjunto de habilidades altamente especializadas e desacopladas, projetadas segundo os padrões estritos de Agent Skills da Anthropic.
Finalidade: Engenharia de Software e Arquitetura.

## Catálogo de Habilidades e Responsabilidades
| [designing-apis-and-interfaces](./designing-apis-and-interfaces/SKILL.md) | Guides stable API and interface design: module boundaries, REST or GraphQL endpoints, type contracts between modules and the boundary between frontend and backend | `[./designing-apis-and-interfaces/SKILL.md](./designing-apis-and-interfaces/SKILL.md)` |
| [reviewing-multi-axis-code-quality](./reviewing-multi-axis-code-quality/SKILL.md) | Conducts multi-axis code review across quality dimensions before a change enters the main branch, covering code written by yourself, another agent or a human, including diffs pasted inline | `[./reviewing-multi-axis-code-quality/SKILL.md](./reviewing-multi-axis-code-quality/SKILL.md)` |
| [simplifying-code-complexity](./simplifying-code-complexity/SKILL.md) | Simplifies code for clarity without changing behavior, reducing unnecessary complexity in code that works but is harder to read, maintain or extend | `[./simplifying-code-complexity/SKILL.md](./simplifying-code-complexity/SKILL.md)` |
| [enforcing-project-constraints](./enforcing-project-constraints/SKILL.md) | Records the project's quality bar as a written contract in CONSTRAINTS.md and watches the diff for a weakened bar: new suppressions, skipped or deleted tests, stripped assertions, unimplemented stubs or lowered thresholds | `[./enforcing-project-constraints/SKILL.md](./enforcing-project-constraints/SKILL.md)` |
| [debugging-root-causes](./debugging-root-causes/SKILL.md) | Runs systematic root-cause diagnosis for compile failures, broken tests and unexpected behavior, without random trial-and-error attempts | `[./debugging-root-causes/SKILL.md](./debugging-root-causes/SKILL.md)` |
| [recovering-system-errors](./recovering-system-errors/SKILL.md) | Orchestrates runtime error recovery strategies: resilient reconnection, fallback ladders and circuit breakers with exponential backoff | `[./recovering-system-errors/SKILL.md](./recovering-system-errors/SKILL.md)` |
| [deprecating-obsolete-apis](./deprecating-obsolete-apis/SKILL.md) | Runs the full deprecation cycle for obsolete interfaces, endpoints and components: semantic annotations, sunset timelines and removal of legacy endpoints without breaking dependents | `[./deprecating-obsolete-apis/SKILL.md](./deprecating-obsolete-apis/SKILL.md)` |
| [migrating-legacy-architectures](./migrating-legacy-architectures/SKILL.md) | Migrates database schemas, architecture flows and infrastructure dependencies with expand/contract patterns and no downtime, including subsystem rewrites and shifting production traffic | `[./migrating-legacy-architectures/SKILL.md](./migrating-legacy-architectures/SKILL.md)` |
| [stress-testing-architecture-decisions](./stress-testing-architecture-decisions/SKILL.md) | Subjects non-trivial decisions to a fresh-context adversarial review, cross-examining assumptions and hidden failure modes before they stand | `[./stress-testing-architecture-decisions/SKILL.md](./stress-testing-architecture-decisions/SKILL.md)` |
| [implementing-incremental-slices](./implementing-incremental-slices/SKILL.md) | Delivers changes incrementally in thin, verifiable slices, rolling out behind feature flags and breaking large tasks into steps that each land on their own | `[./implementing-incremental-slices/SKILL.md](./implementing-incremental-slices/SKILL.md)` |
| [instrumenting-code-observability](./instrumenting-code-observability/SKILL.md) | Instruments code so production behavior is visible and diagnosable: logging, metrics, tracing and alerting, with evidence that shipped features work | `[./instrumenting-code-observability/SKILL.md](./instrumenting-code-observability/SKILL.md)` |
| [optimizing-fullstack-performance](./optimizing-fullstack-performance/SKILL.md) | Optimizes application performance across frontend, backend, queries and databases: Core Web Vitals, load times, N+1 query patterns and bottlenecks revealed by profiling | `[./optimizing-fullstack-performance/SKILL.md](./optimizing-fullstack-performance/SKILL.md)` |
| [minimizing-code-overengineering](./minimizing-code-overengineering/SKILL.md) | Forces the laziest solution that works: asks whether the task needs to exist at all, reuses existing code, prefers the standard library and native platform features, and keeps each change to the minimum | `[./minimizing-code-overengineering/SKILL.md](./minimizing-code-overengineering/SKILL.md)` |
| [auditing-codebase-bloat](./auditing-codebase-bloat/SKILL.md) | Audits a whole repository for bugs, security holes, behavior under real load, risky code without tests, slow paths, and code to delete, merge or split, with ranked findings explained in plain English | `[./auditing-codebase-bloat/SKILL.md](./auditing-codebase-bloat/SKILL.md)` |
| [tracking-technical-debt-ledgers](./tracking-technical-debt-ledgers/SKILL.md) | Lists every shortcut comment (and older ponytail comments) as a technical debt ledger, as a one-shot report that changes nothing | `[./tracking-technical-debt-ledgers/SKILL.md](./tracking-technical-debt-ledgers/SKILL.md)` |
| [measuring-code-savings](./measuring-code-savings/SKILL.md) | Shows ponytail's measured savings in code, cost and speed from the benchmark, as a one-shot display | `[./measuring-code-savings/SKILL.md](./measuring-code-savings/SKILL.md)` |
| [guiding-ponytail-minimalism](./guiding-ponytail-minimalism/SKILL.md) | Shows the quick reference for ponytail levels, skills and commands in a one-shot display | `[./guiding-ponytail-minimalism/SKILL.md](./guiding-ponytail-minimalism/SKILL.md)` |
| [reviewing-code-minimalism](./reviewing-code-minimalism/SKILL.md) | Reviews a change for correctness, safety, behavior under real load, test coverage of risky code, speed and whether every line is needed, reading the connected code and not only the diff | `[./reviewing-code-minimalism/SKILL.md](./reviewing-code-minimalism/SKILL.md)` |
| [grounding-source-documentation](./grounding-source-documentation/SKILL.md) | Grounds implementation decisions in official documentation: verifies an approach against the docs before implementing and produces source-cited code free from outdated patterns | `[./grounding-source-documentation/SKILL.md](./grounding-source-documentation/SKILL.md)` |
| [authoring-specifications-first](./authoring-specifications-first/SKILL.md) | Creates specifications before coding: objectives, scope, requirements, PRDs and a capability map of independently testable modules when a requirement spans several capabilities | `[./authoring-specifications-first/SKILL.md](./authoring-specifications-first/SKILL.md)` |

## Padrões de Integração e Roteamento
- Cada habilidade opera com assinatura estrita de Input/Output.
- O roteador de domínio (`SKILL.md`) atua como camada de orquestração de 1 nível de profundidade.
- Habilidades com rotinas extensas ou especificações técnicas possuem seus próprios arquivos `reference.md` auxiliares.

## Diretrizes de Qualidade e Segurança
- Todas as execuções devem validar pré-condições antes de realizar qualquer alteração estrutural.
- Em caso de falha, acione a seção `## On Failure` com rollback imediato e logs diagnósticos.
