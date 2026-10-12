# Referência Arquitetural do Domínio: DEVOPS

## Table of Contents
1. [Visão Geral do Domínio](#visão-geral-do-domínio)
2. [Catálogo de Habilidades e Responsabilidades](#catálogo-de-habilidades-e-responsabilidades)
3. [Padrões de Integração e Roteamento](#padrões-de-integração-e-roteamento)
4. [Diretrizes de Qualidade e Segurança](#diretrizes-de-qualidade-e-segurança)

## Visão Geral do Domínio
O domínio `devops` reúne um conjunto de habilidades altamente especializadas e desacopladas, projetadas segundo os padrões estritos de Agent Skills da Anthropic.
Finalidade: DevOps, CI/CD e Implantação.

## Catálogo de Habilidades e Responsabilidades
| [building-ci-validation-pipelines](./building-ci-validation-pipelines/SKILL.md) | Builds and orchestrates continuous integration pipelines with strict quality gates, static scanners, parallel test suites and coverage reports | `[./building-ci-validation-pipelines/SKILL.md](./building-ci-validation-pipelines/SKILL.md)` |
| [automating-cd-deployments](./automating-cd-deployments/SKILL.md) | Automates continuous delivery flows: provisions staging and production environments, runs post-deploy smoke tests and triggers automatic rollback | `[./automating-cd-deployments/SKILL.md](./automating-cd-deployments/SKILL.md)` |
| [deploying-to-vercel-platform](./deploying-to-vercel-platform/SKILL.md) | Deploys applications and websites to Vercel, including production deployments and preview links, when the user asks to deploy an app, push it live or create a preview deployment | `[./deploying-to-vercel-platform/SKILL.md](./deploying-to-vercel-platform/SKILL.md)` |
| [managing-git-branch-workflows](./managing-git-branch-workflows/SKILL.md) | Manages Git workflows: atomic branches, interactive rebase, splitting tangled commits and rigorous conflict resolution | `[./managing-git-branch-workflows/SKILL.md](./managing-git-branch-workflows/SKILL.md)` |
| [tagging-semantic-releases](./tagging-semantic-releases/SKILL.md) | Calculates the semantic version increment (SemVer), generates release notes and changelog entries, and signs version tags in the repository | `[./tagging-semantic-releases/SKILL.md](./tagging-semantic-releases/SKILL.md)` |
| [synchronizing-cloud-storage](./synchronizing-cloud-storage/SKILL.md) | Synchronizes OmniRoute configuration, provider connections and settings to and from cloud storage, managing cloud worker authentication and remote backup targets | `[./synchronizing-cloud-storage/SKILL.md](./synchronizing-cloud-storage/SKILL.md)` |
| [verifying-prelaunch-readiness](./verifying-prelaunch-readiness/SKILL.md) | Runs an exhaustive pre-launch readiness checklist covering environment variables, secret checks and production integrity before real traffic is routed to a version | `[./verifying-prelaunch-readiness/SKILL.md](./verifying-prelaunch-readiness/SKILL.md)` |
| [orchestrating-staged-rollouts](./orchestrating-staged-rollouts/SKILL.md) | Orchestrates gradual production releases with canary traffic, active monitoring of error metrics and instant rollback triggers | `[./orchestrating-staged-rollouts/SKILL.md](./orchestrating-staged-rollouts/SKILL.md)` |
| [merging-validated-pull-requests](./merging-validated-pull-requests/SKILL.md) | Consumes analyzed pull request plans, implements authorized fixes with contributor credit, validates exact candidates and merges only the owner-selected groups that were explicitly authorized, through the shared gates | `[./merging-validated-pull-requests/SKILL.md](./merging-validated-pull-requests/SKILL.md)` |
| [deploying-with-vercel-tokens](./deploying-with-vercel-tokens/SKILL.md) | Deploys and manages Vercel projects with token-based CLI authentication instead of interactive login, for setup and deployment on machines or pipelines that use access tokens | `[./deploying-with-vercel-tokens/SKILL.md](./deploying-with-vercel-tokens/SKILL.md)` |
| [optimizing-vercel-deployments](./optimizing-vercel-deployments/SKILL.md) | Optimizes the cost and performance of deployed Vercel projects, especially Next.js, SvelteKit, Nuxt and limited Astro apps, by collecting Vercel metrics, usage, project configuration and code scan results | `[./optimizing-vercel-deployments/SKILL.md](./optimizing-vercel-deployments/SKILL.md)` |

## Padrões de Integração e Roteamento
- Cada habilidade opera com assinatura estrita de Input/Output.
- O roteador de domínio (`SKILL.md`) atua como camada de orquestração de 1 nível de profundidade.
- Habilidades com rotinas extensas ou especificações técnicas possuem seus próprios arquivos `reference.md` auxiliares.

## Diretrizes de Qualidade e Segurança
- Todas as execuções devem validar pré-condições antes de realizar qualquer alteração estrutural.
- Em caso de falha, acione a seção `## On Failure` com rollback imediato e logs diagnósticos.
