## Table of Contents
- [1. Protocolo Universal de Escaneamento de Hardware](#1-protocolo-universal-de-escaneamento-de-hardware)
- [2. Matriz de Calibração por Nível de Hardware (Tiers)](#2-matriz-de-calibração-por-nível-de-hardware-tiers)
- [3. O Prompt Universal de Diagnóstico e Calibração](#3-o-prompt-universal-de-diagnóstico-e-calibração)

## 1. Protocolo Universal de Escaneamento de Hardware

Antes de rodar qualquer pipeline de computação gráfica pesada, o agente deve executar ou solicitar o escaneamento do sistema.

### Script de Escaneamento Rápido em PowerShell / CMD:
```powershell
# Coleta de especificações completas de GPU, CPU e Memória
Get-CimInstance Win32_VideoController | Select-Object Name, AdapterRAM, DriverVersion
Get-CimInstance Win32_Processor | Select-Object Name, NumberOfCores, NumberOfLogicalProcessors
Get-CimInstance Win32_PhysicalMemory | Measure-Object -Property Capacity -Sum | Select-Object @{N="TotalRAM_GB"; E={[math]::Round($_.Sum / 1GB, 2)}}

# Se houver GPU NVIDIA, coletar especificações de CUDA e VRAM exatas via nvidia-smi:
if (Get-Command nvidia-smi -ErrorAction SilentlyContinue) {
    nvidia-smi --query-gpu=name,memory.total,memory.free,driver_version,compute_cap --format=csv,noheader
}
```

### Script de Diagnóstico Python Automatizado (`scan_hardware.py`):
```python
import subprocess
import json
import platform
import os

def scan_system():
    info = {
        "os": platform.system(),
        "os_version": platform.version(),
        "cpu": platform.processor(),
        "gpu": None,
        "vram_mb": 0,
        "cuda_compute_cap": None,
        "driver_version": None,
        "optix_capable": False
    }
    try:
        res = subprocess.check_output(
            ["nvidia-smi", "--query-gpu=name,memory.total,driver_version,compute_cap", "--format=csv,noheader,nounits"],
            encoding="utf-8"
        ).strip().split(",")
        info["gpu"] = res[0].strip()
        info["vram_mb"] = int(res[1].strip())
        info["driver_version"] = res[2].strip()
        info["cuda_compute_cap"] = float(res[3].strip())
        # OptiX requer Compute Capability >= 5.0 (RTX começa em 7.5 Turing e 8.6 Ampere)
        info["optix_capable"] = info["cuda_compute_cap"] >= 7.0
    except Exception as e:
        info["gpu_scan_fallback"] = str(e)
    return info

if __name__ == "__main__":
    profile = scan_system()
    print(json.dumps(profile, indent=2))
```

---

## 2. Matriz de Calibração por Nível de Hardware (Tiers)

Com base no hardware detectado, o pipeline calibra os parâmetros:

### Nível A: Estação com NVIDIA RTX (Ampere/Ada) — Exemplo: RTX 3060 12GB VRAM
- **Perfil de Capacidade:** 12GB de VRAM GDDR6 dedicados, núcleos RT de 2ª geração, Tensor cores, Compute Capability 8.6.
- **Diretriz de Qualidade Máxima:** O buffer de 12GB permite trabalhar com cenas complexas e bakes de alta fidelidade sem paginação no disco.
- **Configuração do Blender Cycles:**
  - `compute_device_type = 'OPTIX'`
  - `samples = 1024` a `2048` para render final de cada frame.
  - `use_denoising = True`, `denoiser = 'OPTIX'` (denoising temporal para animações, eliminando ruído entre quadros sem borrar detalhes finos).
  - Resolução de Render Bruto: 2160x2160 (4K quadrado) para manter nitidez impecável de chanfros e reflexos.
- **Configuração de Exportação Web:**
  - Transcodificação via FFmpeg com `libvpx-vp9` ou `hevc_nvenc`:
    - Resolução final: 1080x1080 (downsampling supersampled do 4K bruto gera anti-aliasing natural).
    - Canal alfa transparente ativo (`pix_fmt yuva420p`).
    - `crf = 18` e `b:v 0` (qualidade visual idêntica ao master original pesando menos de 3.5 MB).

### Nível B: Estação com GPU Mid/Entry (4GB a 8GB VRAM) — Exemplo: RTX 3050 / GTX 1660
- **Perfil de Capacidade:** 4GB a 8GB VRAM.
- **Ajustes de Segurança:**
  - `samples = 512` com OptiX/OpenImageDenoise.
  - Resolução de render bruto limitada a 1440x1440.
  - Monitoramento estrito de pico de VRAM para evitar estouro de CUDA Out of Memory (OOM).

### Nível C: Sem GPU Dedicada ou GPU Integrada (Intel Iris / AMD Radeon Graphics)
- **Perfil de Capacidade:** Memória compartilhada do sistema.
- **Estratégia:** Fuga total de render offline em Cycles; migração direta para otimização de geometria em tempo real no navegador via WebGL / Three.js com malha Draco de 5.73 MB.

---

## 3. O Prompt Universal de Diagnóstico e Calibração

Utilize este prompt no início de qualquer tarefa de render ou geração local para que o agente inspecione a máquina e adapte o código:

```markdown
[ATIVAR SKILL: `hardware-aware-render-optimization`]

Você é o Arquiteto de Performance e Renderização Gráfica do projeto.
Antes de gerar o script de renderização ou executar pipelines 3D locais, execute o diagnóstico de hardware do sistema:

1. ETAPA DE DIAGNÓSTICO:
   - Identifique a GPU instalada, VRAM dedicada disponível, núcleos lógicos de CPU e suporte a aceleração por hardware (CUDA/OptiX).
   - Se for o computador do operador com a NVIDIA RTX 3060 (12GB VRAM), calibre para a Capacidade Nível A.

2. METAS INEGOCIÁVEIS:
   - Qualidade Máxima Local: Não economize no processamento local. Use iluminação física real (Cycles OptiX), bakes PBR de alta resolução e amostragem densa para eliminar ruídos ou artefatos.
   - Entrega Web Otimizada: A saída gerada deve ser comprimida com fidelidade visual impecável para rodar suave na internet a 60fps (vídeo WebM com alfa < 3.5 MB ou malha 3D Draco < 6 MB).

3. ENTREGA:
   - Forneça o relatório conciso do perfil detectado.
   - Apresente o script final calibrado especificamente para as peças e memória da estação.
```
