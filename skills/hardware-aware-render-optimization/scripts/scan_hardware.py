"""
Hardware Profiler para Pipelines Graficos e 3D do Ecossistema LAY.
Escaneia CPU, RAM, GPU, VRAM e capacidades CUDA/OptiX.
"""

import subprocess
import json
import platform
import os
import sys

def get_system_profile():
    profile = {
        "os": platform.system(),
        "os_version": platform.version(),
        "architecture": platform.machine(),
        "cpu": platform.processor(),
        "gpu": None,
        "vram_total_mb": 0,
        "vram_free_mb": 0,
        "driver_version": None,
        "cuda_compute_cap": None,
        "optix_supported": False,
        "tier": "Tier C (CPU / Integrated GPU)"
    }
    
    # 1. Tentar nvidia-smi para GPU NVIDIA
    try:
        query_cmd = [
            "nvidia-smi",
            "--query-gpu=name,memory.total,memory.free,driver_version,compute_cap",
            "--format=csv,noheader,nounits"
        ]
        output = subprocess.check_output(query_cmd, encoding="utf-8").strip()
        if output:
            parts = [p.strip() for p in output.split(",")]
            profile["gpu"] = parts[0]
            profile["vram_total_mb"] = int(parts[1])
            profile["vram_free_mb"] = int(parts[2])
            profile["driver_version"] = parts[3]
            profile["cuda_compute_cap"] = float(parts[4])
            profile["optix_supported"] = profile["cuda_compute_cap"] >= 7.0
            
            # Classificar Tier
            if profile["vram_total_mb"] >= 10000:
                profile["tier"] = "Tier A (Alta Capacidade: 10GB+ VRAM, OptiX / Cycles X 2048 samples)"
            elif profile["vram_total_mb"] >= 6000:
                profile["tier"] = "Tier B (Media-Alta Capacidade: 6GB-8GB VRAM, OptiX 1024 samples)"
            else:
                profile["tier"] = "Tier B-Entry (4GB VRAM, limites de resolucao intermediarios)"
    except Exception as e:
        profile["gpu_error"] = str(e)
        
    return profile

if __name__ == "__main__":
    data = get_system_profile()
    print(json.dumps(data, indent=2))
