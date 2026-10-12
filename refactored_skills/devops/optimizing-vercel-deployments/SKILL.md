---
name: optimizing-vercel-deployments
description: >
  Optimizes the cost and performance of deployed Vercel projects, especially Next.js, SvelteKit, Nuxt and limited Astro apps, by collecting Vercel metrics, usage, project configuration and code scan results. Use this skill when: reducing Vercel cost or improving the performance of a deployed project. Do NOT use this skill when: performing the deployment itself (use deploying-to-vercel-platform).
---

# Vercel Optimize

Run an observability-first Vercel optimization audit. Do not inspect source files until `signals.json` exists and a deterministic gate points to a route, file, or project setting.

Core doctrine: read [references/doctrine.md](references/doctrine.md) if any rule is unclear.

- Metrics first. Recommendations start from Vercel production signals, not repo-wide grep.
- Deterministic gates. `scripts/gate-investigations.mjs` decides what deserves investigation.
- Candidate-bound scope. Read only files named by a candidate or a route-local import chain.
- Version-aware citations. Use only `references/docs-library.json`; invalid or version-mismatched citations are stripped.
- Customer copy. Read [references/voice.md](references/voice.md) before writing report text or chat output.

## Sections
- Prerequisites
- Framework Support
- Run Directory
- Pipeline
- Recommendation Rules
- Scanner Rules
- Final Customer Terms
- Failure Copy

## Reference Documentation
Consulte a documentação técnica completa: [Referência Técnica](reference.md).
