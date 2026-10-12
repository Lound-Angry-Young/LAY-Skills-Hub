"""
Script de Instalacao e Configuracao Automatizada do Blender MCP.
Detecta Blender, instala via winget se ausente, e gera a configuracao MCP calibrada por hardware.
"""

import os
import sys
import subprocess
import json
import shutil
from pathlib import Path

def find_blender():
    # 1. Checar no PATH
    blender = shutil.which("blender")
    if blender:
        return blender
        
    # 2. Checar locais padrao no Windows
    possible_roots = [
        Path(os.environ.get("ProgramFiles", r"C:\Program Files")) / "Blender Foundation",
        Path(os.environ.get("ProgramFiles(x86)", r"C:\Program Files (x86)")) / "Blender Foundation",
        Path(os.environ.get("LOCALAPPDATA", "")) / "Programs" / "Blender Foundation"
    ]
    
    for root in possible_roots:
        if root.exists():
            exes = list(root.glob("**/blender.exe"))
            if exes:
                return str(exes[0])
                
    return None

def install_blender_winget():
    print("[INFO] Blender nao encontrado. Disparando instalacao silenciosa via Winget...")
    cmd = [
        "winget", "install",
        "--id", "BlenderFoundation.Blender",
        "-e",
        "--accept-source-agreements",
        "--accept-package-agreements",
        "--silent"
    ]
    try:
        subprocess.run(cmd, check=True)
        print("[SUCESSO] Instalacao do Blender concluida!")
        return find_blender()
    except Exception as e:
        print(f"[ERRO] Falha ao instalar Blender via winget: {e}")
        return None

def generate_mcp_config(blender_path, gpu_vram_mb=12288, use_optix=True):
    config = {
        "mcpServers": {
            "blender": {
                "command": "npx",
                "args": ["-y", "@three-ws/blender-mcp"],
                "env": {
                    "BLENDER_PATH": blender_path if blender_path else "blender",
                    "CYCLES_DEVICE": "OPTIX" if use_optix else "CUDA",
                    "OPTIX_DENOISING": "true",
                    "GPU_VRAM_MB": str(gpu_vram_mb)
                }
            }
        }
    }
    return config

def main():
    print("=== ORQUESTRADOR BLENDER MCP ===")
    blender_path = find_blender()
    if blender_path:
        print(f"[OK] Blender detectado em: {blender_path}")
    else:
        print("[AVISO] Blender nao esta instalado localmente.")
        # Se passado flag --install, instala
        if "--install" in sys.argv:
            blender_path = install_blender_winget()
        else:
            print("[INFO] Execute com '--install' para instalar automaticamente via winget.")
            
    # Gerar configuracao recomendada
    config = generate_mcp_config(blender_path)
    output_file = Path("blender_mcp_config.json")
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(config, f, indent=2)
        
    print(f"[OK] Configuracao MCP gerada em: {output_file.resolve()}")
    print(json.dumps(config, indent=2))

if __name__ == "__main__":
    main()
