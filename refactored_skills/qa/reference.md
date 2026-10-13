# Referência Arquitetural do Domínio: QA

## Table of Contents
1. [Visão Geral do Domínio](#visão-geral-do-domínio)
2. [Catálogo de Habilidades e Responsabilidades](#catálogo-de-habilidades-e-responsabilidades)
3. [Padrões de Integração e Roteamento](#padrões-de-integração-e-roteamento)
4. [Diretrizes de Qualidade e Segurança](#diretrizes-de-qualidade-e-segurança)

## Visão Geral do Domínio
O domínio `qa` reúne um conjunto de habilidades altamente especializadas e desacopladas, projetadas segundo os padrões estritos de Agent Skills da Anthropic.
Finalidade: Garantia de Qualidade e Testes.

## Catálogo de Habilidades e Responsabilidades
| [testing-in-browser-with-devtools](./testing-in-browser-with-devtools/SKILL.md) | Tests in real browsers through Chrome DevTools MCP: inspects the DOM, captures console errors, analyzes network requests, profiles performance and verifies visual output with runtime data | `[./testing-in-browser-with-devtools/SKILL.md](./testing-in-browser-with-devtools/SKILL.md)` |
| [evaluating-model-benchmarks](./evaluating-model-benchmarks/SKILL.md) | Creates and runs evaluation suites, watches live benchmark progress, views scorecards, compares model performance and integrates eval runs with CI workflows from the CLI | `[./evaluating-model-benchmarks/SKILL.md](./evaluating-model-benchmarks/SKILL.md)` |
| [automating-browser-tests](./automating-browser-tests/SKILL.md) | Automates browser interactions, tests web pages and works with Playwright tests from the Playwright CLI | `[./automating-browser-tests/SKILL.md](./automating-browser-tests/SKILL.md)` |
| [enforcing-green-pull-requests](./enforcing-green-pull-requests/SKILL.md) | Inspects and prepares the selected pull request queue against its exact current base, repairs authorized defects with contributor credit and reports full versus partial validation | `[./enforcing-green-pull-requests/SKILL.md](./enforcing-green-pull-requests/SKILL.md)` |
| [scanning-codebase-quality](./scanning-codebase-quality/SKILL.md) | Runs a scoped, read-only quality scan that reports exact-candidate evidence, failures and frozen debt, for ad-hoc gate sweeps or release preparation | `[./scanning-codebase-quality/SKILL.md](./scanning-codebase-quality/SKILL.md)` |
| [sweeping-failing-ci-builds](./sweeping-failing-ci-builds/SKILL.md) | Repairs confirmed CI failures base-first, then prepares the affected pull requests one at a time with exact-candidate evidence | `[./sweeping-failing-ci-builds/SKILL.md](./sweeping-failing-ci-builds/SKILL.md)` |
| [validating-green-release-gates](./validating-green-release-gates/SKILL.md) | Runs or inspects the local Release-Green observer for an exact base or combined pull request candidate, separating hard failures, advisory drift and incomplete evidence | `[./validating-green-release-gates/SKILL.md](./validating-green-release-gates/SKILL.md)` |
| [driving-test-driven-development](./driving-test-driven-development/SKILL.md) | Drives development with tests in a red-green-refactor loop when implementing logic, fixing a bug or changing behavior, to prove that the code works | `[./driving-test-driven-development/SKILL.md](./driving-test-driven-development/SKILL.md)` |
| [verifying-animated-component-compliance](./verifying-animated-component-compliance/SKILL.md) | Verifies a copied or generated animated UI component against the project rules: local imports resolved, use client where hooks are used, reduced-motion handling present, at most one WebGL component per route, touch fallback for pointer-only effects, debug controls removed, license notice kept, and the project type-checks and builds | `[./verifying-animated-component-compliance/SKILL.md](./verifying-animated-component-compliance/SKILL.md)` |

## Padrões de Integração e Roteamento
- Cada habilidade opera com assinatura estrita de Input/Output.
- O roteador de domínio (`SKILL.md`) atua como camada de orquestração de 1 nível de profundidade.
- Habilidades com rotinas extensas ou especificações técnicas possuem seus próprios arquivos `reference.md` auxiliares.

## Diretrizes de Qualidade e Segurança
- Todas as execuções devem validar pré-condições antes de realizar qualquer alteração estrutural.
- Em caso de falha, acione a seção `## On Failure` com rollback imediato e logs diagnósticos.
