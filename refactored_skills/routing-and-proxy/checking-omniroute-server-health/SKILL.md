---
name: checking-omniroute-server-health
description: >
  Checks OmniRoute server health, component status and live metrics from the CLI, including a real-time watch of circuit breakers and provider status. Use this skill when: verifying the server is up, inspecting component status or watching live provider health. Do NOT use this skill when: inspecting cost or usage history (use analyzing-usage-call-logs) or tuning circuit thresholds (use inspecting-resilience-circuits).
---

## Overview

Check server health, component status, and live metrics from the CLI. Run `health`, `health components`, and `health watch` for a real-time dashboard of circuit breakers and provider status.

## Quick install

```bash
npm install -g omniroute   # or: npx omniroute
omniroute --version
```

## Subcommands

### `doctor`

**Flags:**

- `--no-liveness`
- `--host <host>`
- `--liveness-url <url>`

**Example:**

```bash
omniroute doctor
```

### `health`

**Flags:**

- `-v, --verbose`
- `--json`
- `--alerts-only`

**Example:**

```bash
omniroute health
```

### `health components`

List health components and their status

**Flags:**

- `--alerts-only`

**Example:**

```bash
omniroute health components
```

### `health watch`

Live dashboard — refresh every N seconds

**Flags:**

- `--interval <s>`

**Example:**

```bash
omniroute health watch
```

### `status`

Show OmniRoute status dashboard

**Flags:**

- `-v, --verbose`

**Example:**

```bash
omniroute status
```
