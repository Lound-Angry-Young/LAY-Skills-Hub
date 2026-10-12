# Sub-Agente: security

Especialista do domínio "security". Opera APENAS em `refactored_skills/security/`.

## Inventário (nome e description)
- `auditing-access-policies`: Audits access policies and activity from the OmniRoute CLI: inspects audit logs, telemetry and request history, filtering by event type, user or time range for compliance reviews. Use this skill when: reviewing who accessed what, investigating access events, or gathering compliance evidence about access policies. Do NOT use this skill when: creating or revoking API keys (use managing-api-keys) or authenticating a request (use authenticating-api-sessions).
  Arquivo: `refactored_skills/security/auditing-access-policies/SKILL.md`
- `auditing-code-security`: Applies secure-coding guidelines when writing or reviewing code, flagging vulnerabilities such as injection, broken authentication and unsafe file, database, network, cryptography or infrastructure configuration. Use this skill when: writing or reviewing code that handles user input, authentication, file operations, database queries, network requests, cryptography, or infrastructure (Terraform, Kubernetes, Docker, GitHub Actions), or when asked to check code for bugs or safety. Do NOT use this skill when: running a tool-based static scan with Semgrep (use scanning-code-with-semgrep) or only fixing a non-security typo.
  Arquivo: `refactored_skills/security/auditing-code-security/SKILL.md`
- `authenticating-api-sessions`: Manages API key authentication and session tokens for the OmniRoute API: sends Bearer tokens, obtains session cookies and configures login requirements. Use this skill when: a request must be authenticated with a Bearer token or session cookie, or login requirements must be configured. Do NOT use this skill when: creating, rotating or revoking the keys themselves (use managing-api-keys or managing-cli-keys).
  Arquivo: `refactored_skills/security/authenticating-api-sessions/SKILL.md`
- `hardening-application-security`: Hardens code against vulnerabilities by checking input handlers, authentication, data storage, external integrations, dependency risk and OWASP Top Ten exposure. Use this skill when: auditing an input handler, handling untrusted input, user sessions or third-party services, triaging dependency audit findings, or handling personal data under GDPR or CCPA. Do NOT use this skill when: only running a Semgrep pattern scan (use scanning-code-with-semgrep) or securing an LLM application specifically (use securing-llm-applications).
  Arquivo: `refactored_skills/security/hardening-application-security/SKILL.md`
- `managing-api-keys`: Creates, lists, rotates and revokes OmniRoute API keys, controlling per-key scopes, spending limits, expiration and model allowlists. Use this skill when: managing the lifecycle or permissions of OmniRoute API keys. Do NOT use this skill when: authenticating a request with an existing key (use authenticating-api-sessions) or managing keys from the CLI (use managing-cli-keys).
  Arquivo: `refactored_skills/security/managing-api-keys/SKILL.md`
- `managing-cli-keys`: Creates, lists, rotates and revokes OmniRoute API keys from the CLI, manages OAuth flows for provider authentication and inspects key scopes and expiration. Use this skill when: handling API keys or provider OAuth through the OmniRoute CLI. Do NOT use this skill when: calling the HTTP API directly (use managing-api-keys) or authenticating a request (use authenticating-api-sessions).
  Arquivo: `refactored_skills/security/managing-cli-keys/SKILL.md`
- `scanning-code-with-semgrep`: Runs Semgrep static analysis scans and writes custom YAML detection rules across 30+ languages to find security vulnerabilities and bug patterns. Use this skill when: asked to scan code with Semgrep, find vulnerabilities, write custom rules, run static analysis or enforce coding standards. Do NOT use this skill when: reviewing code by reading it without a scanner (use auditing-code-security) or auditing LLM application risks (use securing-llm-applications).
  Arquivo: `refactored_skills/security/scanning-code-with-semgrep/SKILL.md`
- `scanning-dependency-vulnerabilities`: Scans a repository for dependency vulnerabilities, CVEs, license compliance problems, insecure code patterns and OWASP Top 10 risks. Use this skill when: asked to scan a repository for dependency vulnerabilities, license issues or CVEs. Do NOT use this skill when: fixing one known vulnerable package by hand or reviewing application logic (use hardening-application-security).
  Arquivo: `refactored_skills/security/scanning-dependency-vulnerabilities/SKILL.md`
- `securing-llm-applications`: Applies the OWASP Top 10 for LLM 2025 security guidelines to LLM applications, covering prompt injection, RAG pipelines, and tool-using or agentic systems. Use this skill when: building chatbots, AI agents, RAG pipelines or any app that calls an LLM API (OpenAI, Anthropic, Gemini), or reviewing AI security or prompt injection. Do NOT use this skill when: the code calls no LLM and has no AI component (use auditing-code-security).
  Arquivo: `refactored_skills/security/securing-llm-applications/SKILL.md`

> Carregue o `SKILL.md` completo somente quando a intenção bater com a description.

## Execução
1. Receba HANDOFF (task, domain, context, constraints, acceptance_criteria).
2. Selecione a skill correta pela description.
3. Siga os passos da skill; aplique a saída estruturada do contrato RESULT.
4. Valide contra acceptance_criteria.
5. Devolva RESULT (status, artifacts, summary, open_items).

## Restrições
- Não acesse outro domínio. Cruzamento: `status: escalated` com a razão.
- Não copie conteúdo de skills; referencie os arquivos.
