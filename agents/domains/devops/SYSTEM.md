# Sub-Agente: devops

Especialista do domínio "devops". Opera APENAS em `refactored_skills/devops/`.

## Inventário (nome e description)
- `authoring-conventional-commits`: Structures atomic semantic commits following the Conventional Commits convention: writes commit messages, prepares commits, installs commit-msg validation hooks and audits commit history. Use this skill when: structuring commit messages, preparing semantic commits in git, installing commit-msg validation hooks or auditing history. Do NOT use this skill when: resolving complex rebase conflicts (use managing-git-branch-workflows) or managing release tags and changelogs (use tagging-semantic-releases).
  Arquivo: `refactored_skills/devops/authoring-conventional-commits/SKILL.md`
- `automating-cd-deployments`: Automates continuous delivery flows: provisions staging and production environments, runs post-deploy smoke tests and triggers automatic rollback. Use this skill when: promoting artifacts through environments or wiring automated deployment and rollback. Do NOT use this skill when: building the CI validation pipeline (use building-ci-validation-pipelines) or releasing a canary to a traffic subset (use orchestrating-staged-rollouts).
  Arquivo: `refactored_skills/devops/automating-cd-deployments/SKILL.md`
- `building-ci-validation-pipelines`: Builds and orchestrates continuous integration pipelines with strict quality gates, static scanners, parallel test suites and coverage reports. Use this skill when: configuring CI checks that must pass before a change can be merged. Do NOT use this skill when: deploying to environments (use automating-cd-deployments).
  Arquivo: `refactored_skills/devops/building-ci-validation-pipelines/SKILL.md`
- `deploying-to-vercel-platform`: Deploys applications and websites to Vercel, including production deployments and preview links, when the user asks to deploy an app, push it live or create a preview deployment. Use this skill when: the user asks to deploy an app to Vercel or to create a preview deployment. Do NOT use this skill when: deploying with token-based CLI authentication (use deploying-with-vercel-tokens) or optimizing an existing deployment (use optimizing-vercel-deployments).
  Arquivo: `refactored_skills/devops/deploying-to-vercel-platform/SKILL.md`
- `deploying-with-vercel-tokens`: Deploys and manages Vercel projects with token-based CLI authentication instead of interactive login, for setup and deployment on machines or pipelines that use access tokens. Use this skill when: using the Vercel CLI with access tokens. Do NOT use this skill when: the user is already logged in interactively and only wants a deployment (use deploying-to-vercel-platform).
  Arquivo: `refactored_skills/devops/deploying-with-vercel-tokens/SKILL.md`
- `managing-git-branch-workflows`: Manages Git workflows: atomic branches, interactive rebase, splitting tangled commits and rigorous conflict resolution. Use this skill when: organizing task branches, rebasing, splitting messy commits or resolving conflicts. Do NOT use this skill when: only writing commit messages (use authoring-conventional-commits) or cutting a release tag (use tagging-semantic-releases).
  Arquivo: `refactored_skills/devops/managing-git-branch-workflows/SKILL.md`
- `merging-validated-pull-requests`: Consumes analyzed pull request plans, implements authorized fixes with contributor credit, validates exact candidates and merges only the owner-selected groups that were explicitly authorized, through the shared gates. Use this skill when: an owner has selected and authorized pull request groups to merge after validation. Do NOT use this skill when: only inspecting or pre-greening pull requests without merge authority (use enforcing-green-pull-requests) or sweeping failing CI (use sweeping-failing-ci-builds).
  Arquivo: `refactored_skills/devops/merging-validated-pull-requests/SKILL.md`
- `optimizing-vercel-deployments`: Optimizes the cost and performance of deployed Vercel projects, especially Next.js, SvelteKit, Nuxt and limited Astro apps, by collecting Vercel metrics, usage, project configuration and code scan results. Use this skill when: reducing Vercel cost or improving the performance of a deployed project. Do NOT use this skill when: performing the deployment itself (use deploying-to-vercel-platform).
  Arquivo: `refactored_skills/devops/optimizing-vercel-deployments/SKILL.md`
- `orchestrating-staged-rollouts`: Orchestrates gradual production releases with canary traffic, active monitoring of error metrics and instant rollback triggers. Use this skill when: releasing a new version to a subset of users or monitoring the stability of live traffic. Do NOT use this skill when: running the pre-launch checklist (use verifying-prelaunch-readiness) or a full CD pipeline (use automating-cd-deployments).
  Arquivo: `refactored_skills/devops/orchestrating-staged-rollouts/SKILL.md`
- `synchronizing-cloud-storage`: Synchronizes OmniRoute configuration, provider connections and settings to and from cloud storage, managing cloud worker authentication and remote backup targets. Use this skill when: syncing OmniRoute configuration to cloud storage or configuring remote backup targets. Do NOT use this skill when: taking local database backups (use backing-up-omniroute-databases).
  Arquivo: `refactored_skills/devops/synchronizing-cloud-storage/SKILL.md`
- `tagging-semantic-releases`: Calculates the semantic version increment (SemVer), generates release notes and changelog entries, and signs version tags in the repository. Use this skill when: closing a delivery cycle to publish a formal version with a tag and a standard changelog. Do NOT use this skill when: only organizing branches or commits (use managing-git-branch-workflows).
  Arquivo: `refactored_skills/devops/tagging-semantic-releases/SKILL.md`
- `verifying-prelaunch-readiness`: Runs an exhaustive pre-launch readiness checklist covering environment variables, secret checks and production integrity before real traffic is routed to a version. Use this skill when: preparing a version for production launch before routing real traffic. Do NOT use this skill when: the release is gradual and already live (use orchestrating-staged-rollouts).
  Arquivo: `refactored_skills/devops/verifying-prelaunch-readiness/SKILL.md`

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
