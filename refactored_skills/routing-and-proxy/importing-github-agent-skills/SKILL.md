---
name: importing-github-agent-skills
description: >
  Searches, scores, scans and imports agent skills from GitHub repositories that contain SKILL.md, CLAUDE.md, .cursorrules and similar files, checking heuristic relevance and screening for malware or hardcoded secrets before installing. Use this skill when: discovering and importing community agent skills from GitHub. Do NOT use this skill when: distributing already-installed skills to local coding tools (use collecting-cli-agent-skills).
---

## Overview

Search, score, scan, and import agent skills from GitHub repositories that contain SKILL.md, CLAUDE.md, .cursorrules, and similar agent skill files. Discover community skills across many tool and provider categories, evaluate relevance with heuristic scoring, check for malware or hardcoded secrets, and install into Hermes, Claude Code, Gemini CLI, or OpenCode agent directories.

## Authentication

All requests require a valid Bearer token or session cookie. Obtain a token via `POST /api/auth/login` or configure `REQUIRE_API_KEY=false` for local development.

## Endpoints

_No endpoints mapped for this area yet._
## Payloads

See the full OpenAPI specification at `GET /api/openapi/spec` or `docs/openapi.yaml` for detailed request/response schemas.
