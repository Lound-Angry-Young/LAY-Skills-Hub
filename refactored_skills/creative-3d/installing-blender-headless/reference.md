## Table of Contents
- [1. Resposta Técnica: O Blender Precisa Estar Instalado Primeiro?](#1-resposta-técnica-o-blender-precisa-estar-instalado-primeiro)
- [2. Protocolo de Detecção e Instalação do Blender](#2-protocolo-de-detecção-e-instalação-do-blender)
- [3. Seleção do Servidor Blender MCP](#3-seleção-do-servidor-blender-mcp)
- [4. Configuração do Servidor MCP Calibrada por Hardware](#4-configuração-do-servidor-mcp-calibrada-por-hardware)
- [5. Script Automatizado de Instalação e Configuração (`setup_blender_mcp.py`)](#5-script-automatizado-de-instalação-e-configuração-setup_blender_mcppy)
- [6. O Prompt Universal para IA (Configuração Autônoma)](#6-o-prompt-universal-para-ia-configuração-autônoma)

Esta skill orienta a detecção de ambiente, instalação automatizada do Blender no Windows e configuração do servidor MCP (*Model Context Protocol*) para permitir que assistentes de IA (Claude, Codex, Antigravity) executem renderizações, conversões de formato e inspeções de cenas 3D diretamente na estação de trabalho local.

---

## 1. Resposta Técnica: O Blender Precisa Estar Instalado Primeiro?

**SIM, para a execução dos renders e comandos 3D.**
- O servidor MCP atua como uma ponte de comunicação em protocolo aberto (JSON-RPC) entre o LLM e a engine gráfica. Ele **não embute o binário do Blender** (que pesa ~500 MB). Ele invoca o executável local `blender.exe` em segundo plano (*headless mode*: `blender -b -P ...`).
- **Ordem de Execução:**
  1. A configuração do MCP no cliente de IA (Claude Desktop, Antigravity, Cursor) **pode** ser escrita antes.
  2. Porém, qualquer chamada de ferramenta 3D falhará até que o `blender.exe` esteja acessível no sistema.
  3. Portanto, o protocolo desta skill executa a **instalação silenciosa e não assistida do Blender via Winget** caso o binário não seja encontrado.

---

## 2. Protocolo de Detecção e Instalação do Blender

### Etapa 1: Verificação de Instalação Existente (PowerShell)
```powershell
# 1. Checar se 'blender' esta no PATH ou no diretorio padrao do Windows
$blenderPath = (Get-Command blender -ErrorAction SilentlyContinue).Source
if (-not $blenderPath) {
    $defaultPaths = Get-ChildItem "C:\Program Files\Blender Foundation" -Recurse -Filter "blender.exe" -ErrorAction SilentlyContinue
    if ($defaultPaths) {
        $blenderPath = $defaultPaths[0].FullName
    }
}

if ($blenderPath) {
    Write-Host "Blender detectado em: $blenderPath"
} else {
    Write-Host "Blender nao encontrado. Instalando automaticamente via Winget..."
    winget install --id BlenderFoundation.Blender -e --accept-source-agreements --accept-package-agreements --silent
}
```

---

## 3. Seleção do Servidor Blender MCP

O ecossistema open-source possui duas soluções consolidadas para headless Blender via MCP:

1. **`@three-ws/blender-mcp` (Recomendado para Pipelines Web & Headless):**
   - Roda via `npx -y @three-ws/blender-mcp`.
   - Recursos: Conversão de formatos (GLB, FBX, OBJ, USDZ), decimação de malhas, inspeção geométrica, renderização de previews e execução de scripts `bpy` com retorno inline.
   - Não exige manter o Blender com interface gráfica aberta.

2. **`blender-mcp-enhanced` (Recomendado para Sessões Interativas):**
   - Comunicação via socket TCP com addon em sessão viva do Blender.

---

## 4. Configuração do Servidor MCP Calibrada por Hardware

Adicione o seguinte bloco ao arquivo de configuração de MCP (ex: `claude_desktop_config.json` ou arquivo de settings do ambiente):

```json
{
  "mcpServers": {
    "blender": {
      "command": "npx",
      "args": [
        "-y",
        "@three-ws/blender-mcp"
      ],
      "env": {
        "BLENDER_PATH": "C:\\Program Files\\Blender Foundation\\Blender 4.5\\blender.exe",
        "CYCLES_DEVICE": "OPTIX",
        "OPTIX_DENOISING": "true",
        "GPU_VRAM_MB": "12288"
      }
    }
  }
}
```

> **Calibração de Hardware (Ex: RTX 3060 12GB):**  
> As variáveis `CYCLES_DEVICE=OPTIX` e `GPU_VRAM_MB=12288` orientam os scripts executados via MCP a alocarem a VRAM GDDR6 máxima disponível para amostragem densa sem estouro de memória.

---

## 5. Script Automatizado de Instalação e Configuração (`setup_blender_mcp.py`)

Localizado em `scripts/setup_blender_mcp.py` dentro desta skill, o script:
1. Escaneia o sistema à procura do `blender.exe`.
2. Se ausente, dispara a instalação oficial não assistida via `winget`.
3. Valida a presença do Node.js/npx para o servidor MCP.
4. Gera e salva o arquivo de configuração de MCP calibrado com a GPU da máquina.

---

## 6. O Prompt Universal para IA (Configuração Autônoma)

Utilize este prompt para que uma IA configure o Blender MCP autonomamente na máquina:

```markdown
[ATIVAR SKILLS: `blender-mcp-setup-and-automation`, `hardware-aware-render-optimization`]

Você é o Engenheiro de Infraestrutura e Ferramentas 3D do projeto.
Sua missão é verificar, instalar e configurar o servidor Blender MCP de forma totalmente funcional:

1. VERIFICAÇÃO DO BLENDER:
   - Verifique se o Blender está instalado localmente. Se não estiver, execute a instalação silenciosa via Winget (`winget install --id BlenderFoundation.Blender -e --silent`).
   - Obtenha o caminho absoluto do executável `blender.exe`.

2. DIAGNÓSTICO DE HARDWARE:
   - Identifique a GPU local (se for a RTX 3060 12GB de Douglas, ative aceleração OptiX e 12GB de VRAM).

3. INSTALAÇÃO E CONFIGURAÇÃO DO MCP:
   - Configure o servidor `@three-ws/blender-mcp` no arquivo de configuração de MCP do ambiente.
   - Configure as variáveis de ambiente com o caminho exato do Blender e motor OptiX.

4. TESTE DE VERIFICAÇÃO:
   - Execute um teste rápido de chamada MCP para inspecionar um arquivo 3D (`assets/lady_justice_web.glb`), confirmando que a ponte entre a IA e o Blender está 100% operacional.

Apresente o resultado das verificações e o status de prontidão da ponte MCP.
```
