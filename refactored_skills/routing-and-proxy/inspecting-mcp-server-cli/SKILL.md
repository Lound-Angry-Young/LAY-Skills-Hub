---
name: inspecting-mcp-server-cli
description: >
  Inspects MCP server status from the CLI, listing registered tools and scopes, running tool invocations and managing MCP audit logs. Use this skill when: checking which MCP tools and scopes are registered or auditing MCP calls from the terminal. Do NOT use this skill when: connecting an MCP client to the server (use integrating-omniroute-mcp-server).
---

## Overview

Inspect the MCP server status, list registered tools and scopes, run tool invocations, and manage MCP audit logs from the CLI.

## Quick install

```bash
npm install -g omniroute   # or: npx omniroute
omniroute --version
```

## Subcommands

### `mcp`

**Example:**

```bash
omniroute mcp
```

### `mcp status`

Show MCP server status

**Flags:**

- `--json`

**Example:**

```bash
omniroute mcp status
```

### `mcp restart`

Restart the MCP server

**Example:**

```bash
omniroute mcp restart
```

### `mcp enable`

**Flags:**

- `--transport <transport>`

**Example:**

```bash
omniroute mcp enable
```

### `mcp disable`

**Example:**

```bash
omniroute mcp disable
```

### `mcp call <tool> [argsJson]`

**Flags:**

- `--args <json>`
- `--args-file <path>`
- `--stream`
- `--scope <s>`

**Example:**

```bash
omniroute mcp call <tool> [argsJson]
```

### `mcp scopes`

**Flags:**

- `--tool <name>`

**Example:**

```bash
omniroute mcp scopes
```
