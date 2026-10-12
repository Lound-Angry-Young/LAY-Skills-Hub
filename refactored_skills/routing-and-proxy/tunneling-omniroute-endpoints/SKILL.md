---
name: tunneling-omniroute-endpoints
description: >
  Creates and manages secure tunnels (ngrok, Cloudflare Tunnel, custom) to expose OmniRoute to the internet or share access with remote agents and CI pipelines. Use this skill when: making an OmniRoute endpoint reachable from outside the machine through the API. Do NOT use this skill when: only proxying upstream provider traffic (use configuring-network-proxies).
---

## Overview

Create and manage secure tunnels (ngrok, Cloudflare Tunnel, custom) to expose OmniRoute to the internet or share access with remote agents and CI pipelines.

## Authentication

All requests require a valid Bearer token or session cookie. Obtain a token via `POST /api/auth/login` or configure `REQUIRE_API_KEY=false` for local development.

## Endpoints

_No endpoints mapped for this area yet._
## Payloads

See the full OpenAPI specification at `GET /api/openapi/spec` or `docs/openapi.yaml` for detailed request/response schemas.
