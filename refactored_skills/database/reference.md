# Referência Arquitetural do Domínio: DATABASE

## Table of Contents
1. [Visão Geral do Domínio](#visão-geral-do-domínio)
2. [Catálogo de Habilidades e Responsabilidades](#catálogo-de-habilidades-e-responsabilidades)
3. [Padrões de Integração e Roteamento](#padrões-de-integração-e-roteamento)
4. [Diretrizes de Qualidade e Segurança](#diretrizes-de-qualidade-e-segurança)

## Visão Geral do Domínio
O domínio `database` reúne um conjunto de habilidades altamente especializadas e desacopladas, projetadas segundo os padrões estritos de Agent Skills da Anthropic.
Finalidade: Banco de Dados, Backups e Cache.

## Catálogo de Habilidades e Responsabilidades
| [backing-up-cli-data](./backing-up-cli-data/SKILL.md) | Creates incremental snapshots of local SQLite databases and state data from the OmniRoute CLI, archiving them and syncing to remote storage on demand or on a schedule | `[./backing-up-cli-data/SKILL.md](./backing-up-cli-data/SKILL.md)` |
| [restoring-cli-snapshots](./restoring-cli-snapshots/SKILL.md) | Restores backup files and database snapshots into the local CLI runtime, with a pre-restore integrity check and a safety rollback | `[./restoring-cli-snapshots/SKILL.md](./restoring-cli-snapshots/SKILL.md)` |
| [managing-inference-cache](./managing-inference-cache/SKILL.md) | Manages the LLM response cache: views cache statistics, clears entries, configures TTL policies and tunes semantic-similarity thresholds | `[./managing-inference-cache/SKILL.md](./managing-inference-cache/SKILL.md)` |
| [backing-up-omniroute-databases](./backing-up-omniroute-databases/SKILL.md) | Manages the backup lifecycle of OmniRoute server databases: SQLite snapshots, schema export and cloud uploads of tables and configuration | `[./backing-up-omniroute-databases/SKILL.md](./backing-up-omniroute-databases/SKILL.md)` |
| [restoring-omniroute-databases](./restoring-omniroute-databases/SKILL.md) | Restores OmniRoute server databases safely, validating schema, reindexing and restoring transactionally under a concurrency lock | `[./restoring-omniroute-databases/SKILL.md](./restoring-omniroute-databases/SKILL.md)` |

## Padrões de Integração e Roteamento
- Cada habilidade opera com assinatura estrita de Input/Output.
- O roteador de domínio (`SKILL.md`) atua como camada de orquestração de 1 nível de profundidade.
- Habilidades com rotinas extensas ou especificações técnicas possuem seus próprios arquivos `reference.md` auxiliares.

## Diretrizes de Qualidade e Segurança
- Todas as execuções devem validar pré-condições antes de realizar qualquer alteração estrutural.
- Em caso de falha, acione a seção `## On Failure` com rollback imediato e logs diagnósticos.
