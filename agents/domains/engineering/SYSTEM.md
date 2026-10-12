# Sub-Agente: engineering

Especialista do domínio "engineering". Opera APENAS em `refactored_skills/engineering/`.

## Inventário (nome e description)
- `auditing-codebase-bloat`: Audits a whole repository for bugs, security holes, behavior under real load, risky code without tests, slow paths, and code to delete, merge or split, with ranked findings explained in plain English. Produces a one-shot report and changes nothing. Use this skill when: asked to audit the codebase, review the whole repo, find bloat or decide what can be deleted. Do NOT use this skill when: reviewing a single change or pull request (use reviewing-code-minimalism or reviewing-multi-axis-code-quality).
  Arquivo: `refactored_skills/engineering/auditing-codebase-bloat/SKILL.md`
- `authoring-specifications-first`: Creates specifications before coding: objectives, scope, requirements, PRDs and a capability map of independently testable modules when a requirement spans several capabilities. Use this skill when: starting a new project, feature or significant change with no specification, or when requirements are vague or ambiguous. Do NOT use this skill when: the specification already exists and only needs implementation (use implementing-incremental-slices).
  Arquivo: `refactored_skills/engineering/authoring-specifications-first/SKILL.md`
- `debugging-root-causes`: Runs systematic root-cause diagnosis for compile failures, broken tests and unexpected behavior, without random trial-and-error attempts. Use this skill when: investigating bugs, build breaks or behavior that diverged from expectations. Do NOT use this skill when: building automatic failover or runtime service recovery (use recovering-system-errors).
  Arquivo: `refactored_skills/engineering/debugging-root-causes/SKILL.md`
- `deprecating-obsolete-apis`: Runs the full deprecation cycle for obsolete interfaces, endpoints and components: semantic annotations, sunset timelines and removal of legacy endpoints without breaking dependents. Use this skill when: marking code as deprecated, setting a grace period or removing legacy endpoints safely. Do NOT use this skill when: performing an active database or architecture migration (use migrating-legacy-architectures) or refactoring internals that keep public contracts unchanged.
  Arquivo: `refactored_skills/engineering/deprecating-obsolete-apis/SKILL.md`
- `designing-apis-and-interfaces`: Guides stable API and interface design: module boundaries, REST or GraphQL endpoints, type contracts between modules and the boundary between frontend and backend. Use this skill when: designing APIs, module boundaries or any public interface. Do NOT use this skill when: implementing the internals of an interface that is already designed (use implementing-incremental-slices).
  Arquivo: `refactored_skills/engineering/designing-apis-and-interfaces/SKILL.md`
- `enforcing-project-constraints`: Records the project's quality bar as a written contract in CONSTRAINTS.md and watches the diff for a weakened bar: new suppressions, skipped or deleted tests, stripped assertions, unimplemented stubs or lowered thresholds. Use this skill when: defining quality thresholds for a project or checking that agents are not quietly lowering the bar. Do NOT use this skill when: auditing the whole codebase for bugs (use auditing-codebase-bloat).
  Arquivo: `refactored_skills/engineering/enforcing-project-constraints/SKILL.md`
- `grounding-source-documentation`: Grounds implementation decisions in official documentation: verifies an approach against the docs before implementing and produces source-cited code free from outdated patterns. Use this skill when: verifying an approach against official docs, or building with a framework or library where correctness matters. Do NOT use this skill when: the change is internal logic that no library documentation covers.
  Arquivo: `refactored_skills/engineering/grounding-source-documentation/SKILL.md`
- `guiding-ponytail-minimalism`: Shows the quick reference for ponytail levels, skills and commands in a one-shot display. Use this skill when: asked for ponytail help or how to use ponytail and its commands. Do NOT use this skill when: auditing, reviewing or measuring code (use auditing-codebase-bloat, reviewing-code-minimalism or measuring-code-savings).
  Arquivo: `refactored_skills/engineering/guiding-ponytail-minimalism/SKILL.md`
- `implementing-incremental-slices`: Delivers changes incrementally in thin, verifiable slices, rolling out behind feature flags and breaking large tasks into steps that each land on their own. Use this skill when: implementing a change that touches more than one file, picking up the next task from a plan, or when a task feels too big to land in one step. Do NOT use this skill when: the specification is still missing (use authoring-specifications-first).
  Arquivo: `refactored_skills/engineering/implementing-incremental-slices/SKILL.md`
- `instrumenting-code-observability`: Instruments code so production behavior is visible and diagnosable: logging, metrics, tracing and alerting, with evidence that shipped features work. Use this skill when: adding logging, metrics, tracing or alerts, or when production issues cannot be explained from the available data. Do NOT use this skill when: the work is performance tuning without an observability gap (use optimizing-fullstack-performance).
  Arquivo: `refactored_skills/engineering/instrumenting-code-observability/SKILL.md`
- `measuring-code-savings`: Shows ponytail's measured savings in code, cost and speed from the benchmark, as a one-shot display. Use this skill when: asked what ponytail saves or for its measured impact. Do NOT use this skill when: auditing or reviewing code (use auditing-codebase-bloat or reviewing-code-minimalism).
  Arquivo: `refactored_skills/engineering/measuring-code-savings/SKILL.md`
- `migrating-legacy-architectures`: Migrates database schemas, architecture flows and infrastructure dependencies with expand/contract patterns and no downtime, including subsystem rewrites and shifting production traffic. Use this skill when: migrating data schemas, rewriting subsystems or moving production traffic without unavailability. Do NOT use this skill when: only marking methods with deprecation warnings without a physical migration (use deprecating-obsolete-apis).
  Arquivo: `refactored_skills/engineering/migrating-legacy-architectures/SKILL.md`
- `minimizing-code-overengineering`: Forces the laziest solution that works: asks whether the task needs to exist at all, reuses existing code, prefers the standard library and native platform features, and keeps each change to the minimum. Use this skill when: writing, adding, refactoring, fixing or reviewing any coding task where the solution may be overbuilt. Do NOT use this skill when: the task is a dedicated audit of the whole codebase (use auditing-codebase-bloat).
  Arquivo: `refactored_skills/engineering/minimizing-code-overengineering/SKILL.md`
- `optimizing-fullstack-performance`: Optimizes application performance across frontend, backend, queries and databases: Core Web Vitals, load times, N+1 query patterns and bottlenecks revealed by profiling. Use this skill when: performance requirements exist, regressions are suspected or profiling shows bottlenecks. Do NOT use this skill when: the work is React-specific (use optimizing-react-performance) or adding observability (use instrumenting-code-observability).
  Arquivo: `refactored_skills/engineering/optimizing-fullstack-performance/SKILL.md`
- `recovering-system-errors`: Orchestrates runtime error recovery strategies: resilient reconnection, fallback ladders and circuit breakers with exponential backoff. Use this skill when: a production system or upstream service failed and needs automatic state recovery. Do NOT use this skill when: only investigating logs to find the root cause of a bug (use debugging-root-causes).
  Arquivo: `refactored_skills/engineering/recovering-system-errors/SKILL.md`
- `reviewing-code-minimalism`: Reviews a change for correctness, safety, behavior under real load, test coverage of risky code, speed and whether every line is needed, reading the connected code and not only the diff. Use this skill when: asked to review code, a pull request or the last commit, or to judge whether code is over-engineered. Do NOT use this skill when: auditing the whole repository (use auditing-codebase-bloat).
  Arquivo: `refactored_skills/engineering/reviewing-code-minimalism/SKILL.md`
- `reviewing-multi-axis-code-quality`: Conducts multi-axis code review across quality dimensions before a change enters the main branch, covering code written by yourself, another agent or a human, including diffs pasted inline. Use this skill when: asked to review a diff or pull request, or before merging any change. Do NOT use this skill when: the review is about minimalism or over-engineering (use reviewing-code-minimalism).
  Arquivo: `refactored_skills/engineering/reviewing-multi-axis-code-quality/SKILL.md`
- `simplifying-code-complexity`: Simplifies code for clarity without changing behavior, reducing unnecessary complexity in code that works but is harder to read, maintain or extend. Use this skill when: refactoring for clarity or reviewing code that accumulated unnecessary complexity. Do NOT use this skill when: the code is wrong or its behavior must change (use debugging-root-causes).
  Arquivo: `refactored_skills/engineering/simplifying-code-complexity/SKILL.md`
- `stress-testing-architecture-decisions`: Subjects non-trivial decisions to a fresh-context adversarial review, cross-examining assumptions and hidden failure modes before they stand. Use this skill when: stress-testing a plan, working in unfamiliar code, or when stakes are high (production auth, security-sensitive logic, high-stakes migrations, irreversible operations). Do NOT use this skill when: the decision is trivial and easily reversible.
  Arquivo: `refactored_skills/engineering/stress-testing-architecture-decisions/SKILL.md`
- `tracking-technical-debt-ledgers`: Lists every shortcut comment (and older ponytail comments) as a technical debt ledger, as a one-shot report that changes nothing. Use this skill when: asked what was deferred, to list shortcuts or to produce the debt ledger. Do NOT use this skill when: the request is to fix or remove the shortcuts (use simplifying-code-complexity).
  Arquivo: `refactored_skills/engineering/tracking-technical-debt-ledgers/SKILL.md`

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
