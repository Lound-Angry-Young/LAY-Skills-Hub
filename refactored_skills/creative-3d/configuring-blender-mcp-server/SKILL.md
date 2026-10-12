---
name: configuring-blender-mcp-server
description: >
  Configures, calibrates and connects the Blender MCP (Model Context Protocol) server for agent-driven scene orchestration and hardware-calibrated rendering. Use this skill when: Blender is already installed and an agent must connect to it over MCP. Do NOT use this skill when: Blender is not installed (use installing-blender-headless) or only the hardware must be diagnosed (use calibrating-hardware-rendering).
---

# Blender MCP Setup & Automation — Orquestração de MCP 3D Local

Esta skill orienta a detecção de ambiente, instalação automatizada do Blender no Windows e configuração do servidor MCP (*Model Context Protocol*) para permitir que assistentes de IA (Claude, Codex, Antigravity) executem renderizações, conversões de formato e inspeções de cenas 3D diretamente na estação de trabalho local.

---

## Sections
- 1. Resposta Técnica: O Blender Precisa Estar Instalado Primeiro?
- 2. Protocolo de Detecção e Instalação do Blender
- 3. Seleção do Servidor Blender MCP
- 4. Configuração do Servidor MCP Calibrada por Hardware
- 5. Script Automatizado de Instalação e Configuração (`setup_blender_mcp.py`)
- 6. O Prompt Universal para IA (Configuração Autônoma)

## Reference Documentation
Consulte a documentação técnica completa: [Referência Técnica](reference.md).
