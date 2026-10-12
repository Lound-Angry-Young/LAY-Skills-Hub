---
name: chatting-via-omniroute-cli
description: >
  Sends chat completions, streams responses and starts an interactive REPL session from the OmniRoute CLI, with combo routing and system prompt configuration across all providers. Use this skill when: testing a model or combo interactively or sending a one-off chat request from the terminal. Do NOT use this skill when: integrating an application through the HTTP inference API (use executing-omniroute-inference).
---

## Overview

Send chat completions, stream responses, and start an interactive REPL session from the CLI. Supports all OmniRoute providers, combo routing, and system prompt configuration.

## Quick install

```bash
npm install -g omniroute   # or: npx omniroute
omniroute --version
```

## Subcommands

### `chat [prompt]`

**Flags:**

- `--file <path>`
- `--stdin`
- `-s, --system <prompt>`
- `-m, --model <id>`
- `--max-tokens <n>`
- `--temperature <t>`
- `--top-p <p>`
- `--reasoning-effort <level>`
- `--thinking-budget <tokens>`
- `--combo <name>`
- `--responses-api`
- `--stream`
- `--no-history`

**Example:**

```bash
omniroute chat [prompt]
```

### `repl`

**Flags:**

- `-m, --model <id>`
- `--combo <name>`
- `-s, --system <prompt>`
- `--resume <session>`

**Example:**

```bash
omniroute repl
```

### `stream [prompt]`

**Flags:**

- `--file <path>`
- `--stdin`
- `-m, --model <id>`
- `-s, --system <prompt>`
- `--combo <name>`
- `--max-tokens <n>`
- `--responses-api`
- `--raw`
- `--debug`
- `--save <path>`

**Example:**

```bash
omniroute stream [prompt]
```
