---
name: backing-up-omniroute-databases
description: >
  Manages the backup lifecycle of OmniRoute server databases: SQLite snapshots, schema export and cloud uploads of tables and configuration. Use this skill when: triggering manual or automated backups of OmniRoute tables and settings. Do NOT use this skill when: backing up local CLI data (use backing-up-cli-data) or restoring a server after a failure (use restoring-omniroute-databases).
---

## Overview

Trigger system backups, restore from backup files, and manage the SQLite database lifecycle. Supports export, import, and incremental snapshot strategies.

## Authentication

All requests require a valid Bearer token or session cookie. Obtain a token via `POST /api/auth/login` or configure `REQUIRE_API_KEY=false` for local development.

## Endpoints

### GET /api/system/env/repair

GET system › env › repair

```bash
curl https://localhost:20128/api/system/env/repair \
  -H "Authorization: Bearer $OMNIROUTE_TOKEN"
```

### POST /api/system/env/repair

POST system › env › repair

```bash
curl -X POST https://localhost:20128/api/system/env/repair \
  -H "Authorization: Bearer $OMNIROUTE_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{}'
```

### GET /api/system/version

GET system › version

```bash
curl https://localhost:20128/api/system/version \
  -H "Authorization: Bearer $OMNIROUTE_TOKEN"
```

### POST /api/system/version

POST system › version

```bash
curl -X POST https://localhost:20128/api/system/version \
  -H "Authorization: Bearer $OMNIROUTE_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{}'
```

## Payloads

See the full OpenAPI specification at `GET /api/openapi/spec` or `docs/openapi.yaml` for detailed request/response schemas.
