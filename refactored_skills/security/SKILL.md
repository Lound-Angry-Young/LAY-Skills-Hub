---
name: routing-security-skills
description: >
  Routes security requests to the matching security skill: code security review, Semgrep static scans, dependency and CVE scanning, LLM application security, API key and session authentication, and access policy audits. Use this skill when: deciding which security skill applies to a request. Do NOT use this skill when: the task is purely functional testing with no security focus.
---

## Domain Skills Catalog
| Skill | Finalidade Primária | Link Direto |
|---|---|---|
| [auditing-access-policies](./auditing-access-policies/SKILL.md) | Audits access policies and activity from the OmniRoute CLI: inspects audit logs, telemetry and request history, filtering by event type, user or time range for compliance reviews | `./auditing-access-policies/SKILL.md` |
| [auditing-code-security](./auditing-code-security/SKILL.md) | Applies secure-coding guidelines when writing or reviewing code, flagging vulnerabilities such as injection, broken authentication and unsafe file, database, network, cryptography or infrastructure configuration | `./auditing-code-security/SKILL.md` |
| [authenticating-api-sessions](./authenticating-api-sessions/SKILL.md) | Manages API key authentication and session tokens for the OmniRoute API: sends Bearer tokens, obtains session cookies and configures login requirements | `./authenticating-api-sessions/SKILL.md` |
| [hardening-application-security](./hardening-application-security/SKILL.md) | Hardens code against vulnerabilities by checking input handlers, authentication, data storage, external integrations, dependency risk and OWASP Top Ten exposure | `./hardening-application-security/SKILL.md` |
| [managing-api-keys](./managing-api-keys/SKILL.md) | Creates, lists, rotates and revokes OmniRoute API keys, controlling per-key scopes, spending limits, expiration and model allowlists | `./managing-api-keys/SKILL.md` |
| [managing-cli-keys](./managing-cli-keys/SKILL.md) | Creates, lists, rotates and revokes OmniRoute API keys from the CLI, manages OAuth flows for provider authentication and inspects key scopes and expiration | `./managing-cli-keys/SKILL.md` |
| [scanning-code-with-semgrep](./scanning-code-with-semgrep/SKILL.md) | Runs Semgrep static analysis scans and writes custom YAML detection rules across 30+ languages to find security vulnerabilities and bug patterns | `./scanning-code-with-semgrep/SKILL.md` |
| [scanning-dependency-vulnerabilities](./scanning-dependency-vulnerabilities/SKILL.md) | Scans a repository for dependency vulnerabilities, CVEs, license compliance problems, insecure code patterns and OWASP Top 10 risks | `./scanning-dependency-vulnerabilities/SKILL.md` |
| [securing-llm-applications](./securing-llm-applications/SKILL.md) | Applies the OWASP Top 10 for LLM 2025 security guidelines to LLM applications, covering prompt injection, RAG pipelines, and tool-using or agentic systems | `./securing-llm-applications/SKILL.md` |
