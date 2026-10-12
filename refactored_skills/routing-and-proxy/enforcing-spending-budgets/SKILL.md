---
name: enforcing-spending-budgets
description: >
  Configures spending limits, token quotas and rate-limit policies per API key or globally, inspects current consumption and enforces cost controls across providers. Use this skill when: capping spend, tokens or request rates for a key or the whole deployment. Do NOT use this skill when: only reading usage history (use analyzing-usage-call-logs) or managing the keys themselves (use managing-api-keys).
---

## Overview

Configure spending limits, token quotas, and rate-limit policies per API key or globally. Inspect current consumption and enforce cost controls across providers.

## Authentication

All requests require a valid Bearer token or session cookie. Obtain a token via `POST /api/auth/login` or configure `REQUIRE_API_KEY=false` for local development.

## Endpoints

### GET /api/rate-limit

Get rate limit configuration

```bash
curl https://localhost:20128/api/rate-limit \
  -H "Authorization: Bearer $OMNIROUTE_TOKEN"
```

### POST /api/rate-limit

Update rate limit configuration

```bash
curl -X POST https://localhost:20128/api/rate-limit \
  -H "Authorization: Bearer $OMNIROUTE_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{}'
```

## Payloads

See the full OpenAPI specification at `GET /api/openapi/spec` or `docs/openapi.yaml` for detailed request/response schemas.
