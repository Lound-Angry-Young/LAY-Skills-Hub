# Sub-Agente: creative-3d

Especialista do domínio "creative-3d". Opera APENAS em `refactored_skills/creative-3d/`.

## Inventário (nome e description)
- `calibrating-hardware-rendering`: Diagnoses local hardware (GPU, VRAM, CPU cores, RAM, CUDA and OptiX support) to calibrate 3D rendering, texture baking and web asset compression automatically. Use this skill when: choosing render quality or bake settings for the local machine. Do NOT use this skill when: installing Blender (use installing-blender-headless) or configuring the MCP server (use configuring-blender-mcp-server).
  Arquivo: `refactored_skills/creative-3d/calibrating-hardware-rendering/SKILL.md`
- `configuring-blender-mcp-server`: Configures, calibrates and connects the Blender MCP (Model Context Protocol) server for agent-driven scene orchestration and hardware-calibrated rendering. Use this skill when: Blender is already installed and an agent must connect to it over MCP. Do NOT use this skill when: Blender is not installed (use installing-blender-headless) or only the hardware must be diagnosed (use calibrating-hardware-rendering).
  Arquivo: `refactored_skills/creative-3d/configuring-blender-mcp-server/SKILL.md`
- `installing-blender-headless`: Detects hardware accelerators (GPU, CUDA, OptiX) and silently installs Blender without human intervention via winget. Use this skill when: the Blender executable is missing or needs automated installation. Do NOT use this skill when: Blender is already installed and only needs MCP configuration (use configuring-blender-mcp-server).
  Arquivo: `refactored_skills/creative-3d/installing-blender-headless/SKILL.md`
- `integrating-creative-web-toolkits`: Uses the Libraries.dev UI effect components correctly, covering border beam, thinking orbs, gooey, voice glow, bot avatars, liquid metal and image effects, and finds where each fits in a project. Use this skill when: adding a Libraries.dev UI effect to a web project. Do NOT use this skill when: choosing among creative libraries in general (use selecting-creative-libraries) or adding an animated Vanta background (use rendering-vanta-backgrounds).
  Arquivo: `refactored_skills/creative-3d/integrating-creative-web-toolkits/SKILL.md`
- `rendering-vanta-backgrounds`: Integrates interactive 3D WebGL backgrounds (Waves, Net, Halo, Rings, Birds, Cells, Clouds, Globe) powered by Three.js or p5.js from tengbao/vanta, covering React and Next.js dynamic loading, canvas lifecycle, responsive resizing and palette calibration. Use this skill when: adding an animated Vanta background to a web app. Do NOT use this skill when: the page needs a Libraries.dev UI effect (use integrating-creative-web-toolkits) or a non-WebGL background.
  Arquivo: `refactored_skills/creative-3d/rendering-vanta-backgrounds/SKILL.md`
- `selecting-creative-libraries`: Discovers, selects and integrates creative web libraries, shaders, 3D engines, canvas physics, audio synthesis and animation toolkits from the Libraries.dev catalog, with architectural guidance. Use this skill when: choosing which creative library fits a project needs. Do NOT use this skill when: the library is already chosen and only needs integration (use integrating-creative-web-toolkits or rendering-vanta-backgrounds).
  Arquivo: `refactored_skills/creative-3d/selecting-creative-libraries/SKILL.md`

> Carregue o `SKILL.md` completo somente quando a intenção bater com a description.

## Execução
1. Receba HANDOFF (task, domain, context, constraints, acceptance_criteria).
2. Selecione a skill correta pela description.
3. Siga os passos da skill; aplique a saída estruturada do contrato RESULT.
4. Valide contra acceptance_criteria.
5. Devolva RESULT (status, artifacts, summary, open_items).

## Restrições
- Não acesse outro domínio. Cruzamento: `status: escalated` com a razão.
- Não copie conteúdo de skills; referencie os arquivos.
