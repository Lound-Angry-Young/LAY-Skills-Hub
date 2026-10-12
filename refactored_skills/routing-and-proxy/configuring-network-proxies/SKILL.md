---
name: configuring-network-proxies
description: >
  Configures HTTP, HTTPS and SOCKS proxies for upstream provider requests, with per-provider or global rules, connectivity tests and proxy rotation. Use this skill when: upstream provider traffic must go through a proxy or proxy rotation is needed. Do NOT use this skill when: exposing OmniRoute itself through a tunnel (use tunneling-omniroute-endpoints).
---

## Overview

Configure HTTP/HTTPS/SOCKS proxies for upstream provider requests. Set per-provider or global proxy rules, test connectivity, and manage proxy rotation.

## Authentication

All requests require a valid Bearer token or session cookie. Obtain a token via `POST /api/auth/login` or configure `REQUIRE_API_KEY=false` for local development.

## Endpoints

_No endpoints mapped for this area yet._
## Payloads

See the full OpenAPI specification at `GET /api/openapi/spec` or `docs/openapi.yaml` for detailed request/response schemas.
