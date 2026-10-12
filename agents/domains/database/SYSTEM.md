# Sub-Agente: database

Especialista do domínio "database". Opera APENAS em `refactored_skills/database/`.

## Inventário (nome e description)
- `backing-up-cli-data`: Creates incremental snapshots of local SQLite databases and state data from the OmniRoute CLI, archiving them and syncing to remote storage on demand or on a schedule. Use this skill when: making one-off or scheduled backups of CLI databases and configuration. Do NOT use this skill when: backing up the OmniRoute server databases (use backing-up-omniroute-databases) or restoring a snapshot (use restoring-cli-snapshots).
  Arquivo: `refactored_skills/database/backing-up-cli-data/SKILL.md`
- `backing-up-omniroute-databases`: Manages the backup lifecycle of OmniRoute server databases: SQLite snapshots, schema export and cloud uploads of tables and configuration. Use this skill when: triggering manual or automated backups of OmniRoute tables and settings. Do NOT use this skill when: backing up local CLI data (use backing-up-cli-data) or restoring a server after a failure (use restoring-omniroute-databases).
  Arquivo: `refactored_skills/database/backing-up-omniroute-databases/SKILL.md`
- `managing-inference-cache`: Manages the LLM response cache: views cache statistics, clears entries, configures TTL policies and tunes semantic-similarity thresholds. Use this skill when: inspecting or tuning LLM response caching. Do NOT use this skill when: configuring prompt compression (use configuring-prompt-compression) or managing database backups (use backing-up-omniroute-databases).
  Arquivo: `refactored_skills/database/managing-inference-cache/SKILL.md`
- `restoring-cli-snapshots`: Restores backup files and database snapshots into the local CLI runtime, with a pre-restore integrity check and a safety rollback. Use this skill when: recovering CLI databases after corruption or syncing an instance from an archived snapshot. Do NOT use this skill when: creating backups (use backing-up-cli-data) or restoring the OmniRoute server (use restoring-omniroute-databases).
  Arquivo: `refactored_skills/database/restoring-cli-snapshots/SKILL.md`
- `restoring-omniroute-databases`: Restores OmniRoute server databases safely, validating schema, reindexing and restoring transactionally under a concurrency lock. Use this skill when: restoring the OmniRoute server after a failure or during an instance migration. Do NOT use this skill when: restoring CLI snapshots (use restoring-cli-snapshots) or taking backups (use backing-up-omniroute-databases).
  Arquivo: `refactored_skills/database/restoring-omniroute-databases/SKILL.md`

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
