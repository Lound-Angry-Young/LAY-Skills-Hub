---
name: installing-blender-headless
description: >
  Detects hardware accelerators (GPU, CUDA, OptiX) and silently installs Blender without human intervention via winget. Use this skill when: the Blender executable is missing or needs automated installation. Do NOT use this skill when: Blender is already installed and only needs MCP configuration (use configuring-blender-mcp-server).
---

# Instalação Headless do Blender via Winget

Detecta aceleradores de hardware e instala o Blender de forma silenciosa e autônoma através do Windows Package Manager (winget), configurando variáveis de ambiente e caminhos de execução.

## Input/Output Signature
Input:
- packageId: string # Identificador do pacote winget (default: BlenderFoundation.Blender)
- installScope: string # Escopo da instalação (user ou machine)
- silentMode: boolean # Se deve executar sem prompts gráficos ou interação (default: true)
Output:
- isInstalled: boolean # Indica se a instalação foi finalizada com sucesso
- detectedBlenderPath: string # Caminho absoluto do executável instalado
- installedVersion: string # Versão identificada do Blender
- executionLog: string # Log detalhado da saída do instalador winget

## Router and Selection Matrix
| Condição / Ambiente | Ação Recomendada | Grau de Liberdade |
|---|---|---|
| Instalação Padrão Windows 10/11 | Executa `winget install` com flags silenciosas e acordos aceitos | [FRÁGIL] Exige flags `--silent` e `--accept-source-agreements` |
| Blender Já Instalado | Detecta caminho existente e pula o download de pacotes | [FRÁGIL] Evita sobrescrita de versões funcionais |
| Falha de Permissão de Sistema | Tenta instalação com escopo `--scope user` | [FLEXÍVEL] Contorna necessidade de elevação de privilégios |
| Caminho Ausente no PATH | Localiza instalação em `Program Files` e retorna caminho absoluto | [FLEXÍVEL] Procura caminhos comuns sem quebrar o fluxo |

## Imperative Execution Workflow
1. Verificar se o Blender Já Está Instalado [FRÁGIL]:
   - Inspecione o `PATH` do sistema e pastas padrão (`C:\Program Files\Blender Foundation\Blender *`) buscando `blender.exe`.
2. Preparar Comando Silencioso do Winget [FRÁGIL]:
   - Monte o comando com as flags obrigatórias:
     `winget install --id BlenderFoundation.Blender -e --silent --accept-package-agreements --accept-source-agreements`.
3. Executar Processo de Instalação [FRÁGIL]:
   - Dispare o comando monitorando código de retorno e capturando saída do instalador.
4. Localizar Binário Instalado e Registrar Versão [FRÁGIL]:
   - Execute `blender.exe --version` utilizando o caminho recém-instalado para confirmar funcionamento.
5. Disponibilizar Caminho para Configuração MCP [FLEXÍVEL]:
   - Retorne o caminho absoluto do executável pronto para vinculação com `configuring-blender-mcp-server`.

## Execution Checklist
- [ ] Checar presença prévia do executável no sistema
- [ ] Montar comando winget com todas as flags de instalação autônoma
- [ ] Executar instalação e monitorar código de saída
- [ ] Validar execução com comando `blender --version`
- [ ] Registrar caminho do executável para uso dos agentes 3D

## On Failure
- **Gatilho de Erro**: Falha no download do pacote, winget indisponível, código de erro do instalador ou falha de rede.
- **Ação Imediata**: Interromper o processo de instalação e registrar o código de saída emitido pelo winget.
- **Rollback**: Desinstalar arquivos residuais parciais se o instalador tiver abortado no meio do processo.
- **Fallback**: Informar o usuário e sugerir instalação manual a partir do instalador oficial ou uso de versão portable em zip.
- **Logs**: Registrar log de erro do winget localizado em `%LOCALAPPDATA%\Packages\Microsoft.DesktopAppInstaller_*\LocalState\DiagOutputDir`.

## Reference Documentation
Consulte a documentação técnica completa: [Referência Técnica](reference.md).
