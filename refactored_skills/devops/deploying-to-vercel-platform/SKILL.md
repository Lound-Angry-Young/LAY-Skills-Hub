---
name: deploying-to-vercel-platform
description: >
  Deploys applications and websites to Vercel, including production deployments and preview links, when the user asks to deploy an app, push it live or create a preview deployment. Use this skill when: the user asks to deploy an app to Vercel or to create a preview deployment. Do NOT use this skill when: deploying with token-based CLI authentication (use deploying-with-vercel-tokens) or optimizing an existing deployment (use optimizing-vercel-deployments).
---

# Deploy to Vercel

Deploy any project to Vercel. **Always deploy as preview** (not production) unless the user explicitly asks for production.

The goal is to get the user into the best long-term setup: their project linked to Vercel with git-push deploys. Every method below tries to move the user closer to that state.

## Sections
- Step 1: Gather Project State
- Step 2: Choose a Deploy Method
- Agent-Specific Notes
- Output
- Troubleshooting

## Reference Documentation
Consulte a documentação técnica completa: [Referência Técnica](reference.md).
