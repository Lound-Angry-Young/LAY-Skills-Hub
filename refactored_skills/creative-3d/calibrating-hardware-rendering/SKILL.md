---
name: calibrating-hardware-rendering
description: >
  Diagnoses local hardware (GPU, VRAM, CPU cores, RAM, CUDA and OptiX support) to calibrate 3D rendering, texture baking and web asset compression automatically. Use this skill when: choosing render quality or bake settings for the local machine. Do NOT use this skill when: installing Blender (use installing-blender-headless) or configuring the MCP server (use configuring-blender-mcp-server).
---

# Calibração de Renderização e Hardware 3D

Diagnostica a capacidade computacional da máquina local (GPU, VRAM, núcleos de CPU, suporte a CUDA e OptiX) para determinar automaticamente o perfil de renderização, bake de texturas e compressão de malhas 3D.

## Input/Output Signature
Input:
- targetEngine: string # Motor de renderização alvo (cycles, eevee, webgl, threejs)
- assetComplexity: string # Complexidade geométrica da cena (lowpoly, midpoly, cinematic)
- outputResolution: string # Resolução pretendida (1080p, 1440p, 4k)
Output:
- hardwareTier: string # Nível de hardware classificado (Tier 1 a Tier 4)
- recommendedSamples: number # Número ideal de amostras para o motor Cycles/Eevee
- bakeResolution: number # Resolução calculada para bake de texturas (1024, 2048, 4096)
- deviceBackend: string # Backend de computação selecionado (OPTIX, CUDA, HIP, CPU)
- hardwareDiagnostics: object # Especificações detectadas de VRAM, GPU e núcleos de CPU

## Router and Selection Matrix
| Hardware Detectado / Tier | Perfil de Calibração | Grau de Liberdade |
|---|---|---|
| Tier 1: Integrada / Sem GPU Dedicada | Modo Leve: Eevee / WebGL LowPoly, 32-64 samples, bake 1024px | [FRÁGIL] Força limites estritos para evitar congelamento do sistema |
| Tier 2: GPU Dedicada 4-6GB (GTX/RTX entrada) | Modo Equilibrado: OptiX/CUDA, 128 samples, denoise ativado, bake 2048px | [FLEXÍVEL] Balanceia tempo de bake e fidelidade de normais |
| Tier 3: GPU RTX 8-12GB VRAM | Modo Produção: OptiX acelerado, 256-512 samples, bake 4096px | [FLEXÍVEL] Permite renderização de volumetria e reflexos complexos |
| Tier 4: Workstation / 16GB+ VRAM | Modo Ultra: OptiX completo, 1024+ samples, displacement e multires | [FLEXÍVEL] Habilita fidelidade fotorrealista e subdivisão profunda |

## Imperative Execution Workflow
1. Escanear Hardware e Aceleradores Disponíveis [FRÁGIL]:
   - Execute diagnósticos locais via PowerShell/WMI ou CLI do Blender para detectar modelo de GPU, VRAM dedicada e suporte a OptiX/CUDA.
2. Classificar Máquina no Tier Correspondente [FRÁGIL]:
   - Enquadre o hardware na matriz de Tiers (1 a 4) com base na memória de vídeo disponível e número de núcleos de CPU.
3. Calcular Parâmetros Ideais de Renderização [FLEXÍVEL]:
   - Determine resolução de texturas, contagem de samples de Cycles, ativador de OpenImageDenoise e limites de subdivisão.
4. Gerar Script ou Configuração de Render [FRÁGIL]:
   - Exporte o bloco de configuração Python para o Blender configurando `bpy.context.preferences.addons['cycles'].preferences.compute_device_type`.
5. Validar Estabilidade com Teste Curto [FLEXÍVEL]:
   - Dispare renderização de 1 frame de teste em baixa resolução para confirmar ausência de out-of-memory (OOM) na GPU.

## Execution Checklist
- [ ] Escanear especificações de GPU, VRAM e núcleos disponíveis
- [ ] Classificar a máquina no Tier de hardware apropriado
- [ ] Definir backend ideal (OptiX, CUDA ou CPU fallback)
- [ ] Configurar contagem de samples e resolução de texturas
- [ ] Validar estabilidade da cena com frame de teste

## On Failure
- **Gatilho de Erro**: Falha de alocação de VRAM (CUDA/OptiX Out of Memory), timeout de renderização ou driver incompatível.
- **Ação Imediata**: Cancelar o processo de renderização imediatamente para liberar a memória da GPU.
- **Rollback**: Reverter configurações para o Tier imediatamente inferior ou chavear temporariamente para renderização via CPU.
- **Fallback**: Comutar motor de Cycles para Eevee Next ou reduzir textura de 4K para 2K/1K.
- **Logs**: Registrar VRAM solicitada, VRAM livre no momento da queda e código de exceção do driver.

## Reference Documentation
Consulte a documentação técnica completa: [Referência Técnica](reference.md).
