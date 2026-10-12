# Referência Arquitetural do Domínio: CREATIVE-3D

## Table of Contents
1. [Visão Geral do Domínio](#visão-geral-do-domínio)
2. [Catálogo de Habilidades e Responsabilidades](#catálogo-de-habilidades-e-responsabilidades)
3. [Padrões de Integração e Roteamento](#padrões-de-integração-e-roteamento)
4. [Diretrizes de Qualidade e Segurança](#diretrizes-de-qualidade-e-segurança)

## Visão Geral do Domínio
O domínio `creative-3d` reúne um conjunto de habilidades altamente especializadas e desacopladas, projetadas segundo os padrões estritos de Agent Skills da Anthropic.
Finalidade: Gráficos 3D, Shaders e Computação Visual Criativa.

## Catálogo de Habilidades e Responsabilidades
| [installing-blender-headless](./installing-blender-headless/SKILL.md) | Detects hardware accelerators (GPU, CUDA, OptiX) and silently installs Blender without human intervention via winget | `[./installing-blender-headless/SKILL.md](./installing-blender-headless/SKILL.md)` |
| [configuring-blender-mcp-server](./configuring-blender-mcp-server/SKILL.md) | Configures, calibrates and connects the Blender MCP (Model Context Protocol) server for agent-driven scene orchestration and hardware-calibrated rendering | `[./configuring-blender-mcp-server/SKILL.md](./configuring-blender-mcp-server/SKILL.md)` |
| [selecting-creative-libraries](./selecting-creative-libraries/SKILL.md) | Discovers, selects and integrates creative web libraries, shaders, 3D engines, canvas physics, audio synthesis and animation toolkits from the Libraries.dev catalog, with architectural guidance | `[./selecting-creative-libraries/SKILL.md](./selecting-creative-libraries/SKILL.md)` |
| [calibrating-hardware-rendering](./calibrating-hardware-rendering/SKILL.md) | Diagnoses local hardware (GPU, VRAM, CPU cores, RAM, CUDA and OptiX support) to calibrate 3D rendering, texture baking and web asset compression automatically | `[./calibrating-hardware-rendering/SKILL.md](./calibrating-hardware-rendering/SKILL.md)` |
| [integrating-creative-web-toolkits](./integrating-creative-web-toolkits/SKILL.md) | Uses the Libraries.dev UI effect components correctly, covering border beam, thinking orbs, gooey, voice glow, bot avatars, liquid metal and image effects, and finds where each fits in a project | `[./integrating-creative-web-toolkits/SKILL.md](./integrating-creative-web-toolkits/SKILL.md)` |
| [rendering-vanta-backgrounds](./rendering-vanta-backgrounds/SKILL.md) | Integrates interactive 3D WebGL backgrounds (Waves, Net, Halo, Rings, Birds, Cells, Clouds, Globe) powered by Three.js or p5.js from tengbao/vanta, covering React and Next.js dynamic loading, canvas lifecycle, responsive resizing and palette calibration | `[./rendering-vanta-backgrounds/SKILL.md](./rendering-vanta-backgrounds/SKILL.md)` |

## Padrões de Integração e Roteamento
- Cada habilidade opera com assinatura estrita de Input/Output.
- O roteador de domínio (`SKILL.md`) atua como camada de orquestração de 1 nível de profundidade.
- Habilidades com rotinas extensas ou especificações técnicas possuem seus próprios arquivos `reference.md` auxiliares.

## Diretrizes de Qualidade e Segurança
- Todas as execuções devem validar pré-condições antes de realizar qualquer alteração estrutural.
- Em caso de falha, acione a seção `## On Failure` com rollback imediato e logs diagnósticos.
