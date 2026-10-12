---
name: managing-tunnels-via-cli
description: >
  Starts and stops tunnel connections (ngrok, Cloudflare, custom) from the CLI, inspects active tunnel URLs, configures authentication and tests external reachability. Use this skill when: opening or checking a tunnel from the terminal. Do NOT use this skill when: creating tunnels through the API (use tunneling-omniroute-endpoints).
---

## Overview

Start and stop tunnel connections (ngrok, Cloudflare, custom) from the CLI. Inspect active tunnel URLs, configure authentication, and test external reachability.

## Quick install

```bash
npm install -g omniroute   # or: npx omniroute
omniroute --version
```

## Subcommands

### `tunnel`

**Example:**

```bash
omniroute tunnel
```

### `tunnel list`

**Flags:**

- `--json`

**Example:**

```bash
omniroute tunnel list
```

### `tunnel create [type]`

**Example:**

```bash
omniroute tunnel create [type]
```

### `tunnel stop <type>`

**Flags:**

- `--yes`

**Example:**

```bash
omniroute tunnel stop <type>
```

### `tunnel status <type>`

**Flags:**

- `--json`

**Example:**

```bash
omniroute tunnel status <type>
```

### `tunnel logs <type>`

**Flags:**

- `--tail <n>`

**Example:**

```bash
omniroute tunnel logs <type>
```

### `tunnel info <type>`

**Flags:**

- `--json`

**Example:**

```bash
omniroute tunnel info <type>
```

### `tunnel rotate <type>`

**Flags:**

- `--yes`

**Example:**

```bash
omniroute tunnel rotate <type>
```
