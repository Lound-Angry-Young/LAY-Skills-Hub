---
name: routing-database-skills
description: >
  Routes database backup, restore and cache requests to the matching skill: CLI and OmniRoute server backups, snapshot restores and inference cache management. Use this skill when: deciding which backup, restore or cache skill applies. Do NOT use this skill when: the task is schema design or application queries.
---

## Domain Skills Catalog
| Skill | Finalidade Primária | Link Direto |
|---|---|---|
| [backing-up-cli-data](./backing-up-cli-data/SKILL.md) | Creates incremental snapshots of local SQLite databases and state data from the OmniRoute CLI, archiving them and syncing to remote storage on demand or on a schedule | `./backing-up-cli-data/SKILL.md` |
| [backing-up-omniroute-databases](./backing-up-omniroute-databases/SKILL.md) | Manages the backup lifecycle of OmniRoute server databases: SQLite snapshots, schema export and cloud uploads of tables and configuration | `./backing-up-omniroute-databases/SKILL.md` |
| [managing-inference-cache](./managing-inference-cache/SKILL.md) | Manages the LLM response cache: views cache statistics, clears entries, configures TTL policies and tunes semantic-similarity thresholds | `./managing-inference-cache/SKILL.md` |
| [restoring-cli-snapshots](./restoring-cli-snapshots/SKILL.md) | Restores backup files and database snapshots into the local CLI runtime, with a pre-restore integrity check and a safety rollback | `./restoring-cli-snapshots/SKILL.md` |
| [restoring-omniroute-databases](./restoring-omniroute-databases/SKILL.md) | Restores OmniRoute server databases safely, validating schema, reindexing and restoring transactionally under a concurrency lock | `./restoring-omniroute-databases/SKILL.md` |
