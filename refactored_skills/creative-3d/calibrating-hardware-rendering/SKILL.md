---
name: calibrating-hardware-rendering
description: >
  Diagnoses local hardware (GPU, VRAM, CPU cores, RAM, CUDA and OptiX support) to calibrate 3D rendering, texture baking and web asset compression automatically. Use this skill when: choosing render quality or bake settings for the local machine. Do NOT use this skill when: installing Blender (use installing-blender-headless) or configuring the MCP server (use configuring-blender-mcp-server).
---

# Hardware-Aware Render Optimization — Calibração por Maquinário Local

Esta skill estabelece a rotina de diagnóstico de peças e arquitetura de hardware da estação de trabalho local, adaptando dinamicamente os parâmetros de processamento gráfico pesado (Blender Cycles, PyTorch, bakes de textura PBR, exportação de vídeo com canal alfa e compressão 3D) para extrair a **qualidade visual máxima absoluta** sem estourar limites de memória (VRAM) e mantendo a entrega web leve (< 5 MB).

---

## Sections
- 1. Protocolo Universal de Escaneamento de Hardware
- 2. Matriz de Calibração por Nível de Hardware (Tiers)
- 3. O Prompt Universal de Diagnóstico e Calibração

## Reference Documentation
Consulte a documentação técnica completa: [Referência Técnica](reference.md).
