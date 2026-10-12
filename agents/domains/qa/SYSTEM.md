# Sub-Agente: qa

Especialista do domínio "qa". Opera APENAS em `refactored_skills/qa/`.

## Inventário (nome e description)
- `automating-browser-tests`: Automates browser interactions, tests web pages and works with Playwright tests from the Playwright CLI. Use this skill when: writing or running browser automation or Playwright tests against a web page. Do NOT use this skill when: inspecting a running page through DevTools signals such as console errors, network requests or performance (use testing-in-browser-with-devtools).
  Arquivo: `refactored_skills/qa/automating-browser-tests/SKILL.md`
- `driving-test-driven-development`: Drives development with tests in a red-green-refactor loop when implementing logic, fixing a bug or changing behavior, to prove that the code works. Use this skill when: implementing any logic, fixing any bug or changing existing behavior. Do NOT use this skill when: the work is a browser-level check of a running page (use testing-in-browser-with-devtools) or a codebase quality scan (use scanning-codebase-quality).
  Arquivo: `refactored_skills/qa/driving-test-driven-development/SKILL.md`
- `enforcing-green-pull-requests`: Inspects and prepares the selected pull request queue against its exact current base, repairs authorized defects with contributor credit and reports full versus partial validation. Use this skill when: a maintainer pre-greens selected pull requests before merge. Do NOT use this skill when: merging (use merging-validated-pull-requests) or sweeping failing CI on the base branch (use sweeping-failing-ci-builds).
  Arquivo: `refactored_skills/qa/enforcing-green-pull-requests/SKILL.md`
- `evaluating-model-benchmarks`: Creates and runs evaluation suites, watches live benchmark progress, views scorecards, compares model performance and integrates eval runs with CI workflows from the CLI. Use this skill when: benchmarking or comparing models through evaluation suites. Do NOT use this skill when: only checking that a model is reachable or configured (use querying-models-via-cli).
  Arquivo: `refactored_skills/qa/evaluating-model-benchmarks/SKILL.md`
- `running-playwright-dev-tools`: Runs development workflows for the playwright-cli repository, such as rolling dependencies, releasing and other repository maintenance tasks. Use this skill when: maintaining the playwright-cli repository itself. Do NOT use this skill when: writing browser tests for an application (use automating-browser-tests).
  Arquivo: `refactored_skills/qa/running-playwright-dev-tools/SKILL.md`
- `scanning-codebase-quality`: Runs a scoped, read-only quality scan that reports exact-candidate evidence, failures and frozen debt, for ad-hoc gate sweeps or release preparation. Use this skill when: an ad-hoc quality gate sweep or release preparation needs a read-only scan. Do NOT use this skill when: full release acceptance is required (a static scan is not enough; use validating-green-release-gates) or the task is to repair failing builds (use sweeping-failing-ci-builds).
  Arquivo: `refactored_skills/qa/scanning-codebase-quality/SKILL.md`
- `sweeping-failing-ci-builds`: Repairs confirmed CI failures base-first, then prepares the affected pull requests one at a time with exact-candidate evidence. Use this skill when: asked to sweep red builds or restore the pull request queue. Do NOT use this skill when: merging or closing pull requests, weakening tests or changing CI configuration, or running a read-only scan (use scanning-codebase-quality).
  Arquivo: `refactored_skills/qa/sweeping-failing-ci-builds/SKILL.md`
- `testing-in-browser-with-devtools`: Tests in real browsers through Chrome DevTools MCP: inspects the DOM, captures console errors, analyzes network requests, profiles performance and verifies visual output with runtime data. Use this skill when: building or debugging anything that runs in a browser. Do NOT use this skill when: only writing Playwright test code without runtime inspection (use automating-browser-tests).
  Arquivo: `refactored_skills/qa/testing-in-browser-with-devtools/SKILL.md`
- `validating-green-release-gates`: Runs or inspects the local Release-Green observer for an exact base or combined pull request candidate, separating hard failures, advisory drift and incomplete evidence. Use this skill when: a maintainer runs a preflight on a release candidate. Do NOT use this skill when: full CI acceptance is required (a separate requirement) or for an ad-hoc read-only scan (use scanning-codebase-quality).
  Arquivo: `refactored_skills/qa/validating-green-release-gates/SKILL.md`

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
