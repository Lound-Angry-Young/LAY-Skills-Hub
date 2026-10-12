# Referência Arquitetural do Domínio: SECURITY

## Table of Contents
1. [Visão Geral do Domínio](#visão-geral-do-domínio)
2. [Catálogo de Habilidades e Responsabilidades](#catálogo-de-habilidades-e-responsabilidades)
3. [Padrões de Integração e Roteamento](#padrões-de-integração-e-roteamento)
4. [Diretrizes de Qualidade e Segurança](#diretrizes-de-qualidade-e-segurança)

## Visão Geral do Domínio
O domínio `security` reúne um conjunto de habilidades altamente especializadas e desacopladas, projetadas segundo os padrões estritos de Agent Skills da Anthropic.
Finalidade: Segurança e Proteção de Aplicações.

## Catálogo de Habilidades e Responsabilidades
| [managing-cli-keys](./managing-cli-keys/SKILL.md) | Creates, lists, rotates and revokes OmniRoute API keys from the CLI, manages OAuth flows for provider authentication and inspects key scopes and expiration | `[./managing-cli-keys/SKILL.md](./managing-cli-keys/SKILL.md)` |
| [auditing-access-policies](./auditing-access-policies/SKILL.md) | Audits access policies and activity from the OmniRoute CLI: inspects audit logs, telemetry and request history, filtering by event type, user or time range for compliance reviews | `[./auditing-access-policies/SKILL.md](./auditing-access-policies/SKILL.md)` |
| [auditing-code-security](./auditing-code-security/SKILL.md) | Applies secure-coding guidelines when writing or reviewing code, flagging vulnerabilities such as injection, broken authentication and unsafe file, database, network, cryptography or infrastructure configuration | `[./auditing-code-security/SKILL.md](./auditing-code-security/SKILL.md)` |
| [securing-llm-applications](./securing-llm-applications/SKILL.md) | Applies the OWASP Top 10 for LLM 2025 security guidelines to LLM applications, covering prompt injection, RAG pipelines, and tool-using or agentic systems | `[./securing-llm-applications/SKILL.md](./securing-llm-applications/SKILL.md)` |
| [managing-api-keys](./managing-api-keys/SKILL.md) | Creates, lists, rotates and revokes OmniRoute API keys, controlling per-key scopes, spending limits, expiration and model allowlists | `[./managing-api-keys/SKILL.md](./managing-api-keys/SKILL.md)` |
| [authenticating-api-sessions](./authenticating-api-sessions/SKILL.md) | Manages API key authentication and session tokens for the OmniRoute API: sends Bearer tokens, obtains session cookies and configures login requirements | `[./authenticating-api-sessions/SKILL.md](./authenticating-api-sessions/SKILL.md)` |
| [scanning-dependency-vulnerabilities](./scanning-dependency-vulnerabilities/SKILL.md) | Scans a repository for dependency vulnerabilities, CVEs, license compliance problems, insecure code patterns and OWASP Top 10 risks | `[./scanning-dependency-vulnerabilities/SKILL.md](./scanning-dependency-vulnerabilities/SKILL.md)` |
| [hardening-application-security](./hardening-application-security/SKILL.md) | Hardens code against vulnerabilities by checking input handlers, authentication, data storage, external integrations, dependency risk and OWASP Top Ten exposure | `[./hardening-application-security/SKILL.md](./hardening-application-security/SKILL.md)` |
| [scanning-code-with-semgrep](./scanning-code-with-semgrep/SKILL.md) | Runs Semgrep static analysis scans and writes custom YAML detection rules across 30+ languages to find security vulnerabilities and bug patterns | `[./scanning-code-with-semgrep/SKILL.md](./scanning-code-with-semgrep/SKILL.md)` |

## Padrões de Integração e Roteamento
- Cada habilidade opera com assinatura estrita de Input/Output.
- O roteador de domínio (`SKILL.md`) atua como camada de orquestração de 1 nível de profundidade.
- Habilidades com rotinas extensas ou especificações técnicas possuem seus próprios arquivos `reference.md` auxiliares.

## Diretrizes de Qualidade e Segurança
- Todas as execuções devem validar pré-condições antes de realizar qualquer alteração estrutural.
- Em caso de falha, acione a seção `## On Failure` com rollback imediato e logs diagnósticos.
