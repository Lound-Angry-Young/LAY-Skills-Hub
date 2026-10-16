---
name: configuring-blender-mcp-server
description: >
  Configures, calibrates and connects the Blender MCP (Model Context Protocol) server for agent-driven scene orchestration and hardware-calibrated rendering. Use this skill when: Blender is already installed and an agent must connect to it over MCP. Do NOT use this skill when: Blender is not installed (use installing-blender-headless) or only the hardware must be diagnosed (use calibrating-hardware-rendering).
---

# Configuração do Servidor Blender MCP

Configura e inicializa o servidor MCP (Model Context Protocol) para orquestração remota do Blender por agentes de IA, estabelecendo transporte seguro, mapeamento de portas e scripts de inicialização.

## Input/Output Signature
Input:
- blenderExecutablePath: string # Caminho absoluto do binário executável do Blender
- transportType: string # Tipo de transporte do servidor MCP (stdio ou sse)
- listenPort: number # Porta de escuta para transporte SSE (default: 8181)
- hardwareTier: string # Nível de hardware para calibração inicial da sessão (Tier 1 a 4)
Output:
- serverStatus: string # Estado final do serviço (running, configured, failed)
- connectionEndpoint: string # URI de conexão para o cliente MCP (ex: http://localhost:8181/sse)
- supportedToolCount: number # Quantidade de ferramentas 3D registradas pelo servidor
- serverPid: number # Identificador de processo do Blender MCP iniciado

## Router and Selection Matrix
| Ambiente / Transporte | Ação Recomendada | Grau de Liberdade |
|---|---|---|
| Cliente IDE Local (Antigravity/Cursor) | Configura transporte stdio via script Python embutido no Blender | [FRÁGIL] Exige flags `--background` e caminho absoluto do script |
| Agente Remoto ou Multi-Sessão | Configura servidor SSE com escuta em porta dedicada e loop de eventos | [FRÁGIL] Requer vinculação à interface de rede correta |
| Inicialização em Modo Headless | Executa Blender em segundo plano sem carregar interface gráfica | [FRÁGIL] Obrigatório uso da flag `-b` para economizar memória |
| Verificação de Conectividade | Testa handshake MCP e lista ferramentas 3D registradas | [FLEXÍVEL] Permite timeout configurável para inicialização |

## Imperative Execution Workflow
1. Validar Presença do Binário do Blender [FRÁGIL]:
   - Verifique a existência do executável do Blender no caminho fornecido ou em `C:\Program Files\Blender Foundation`.
2. Preparar Script do Servidor MCP [FRÁGIL]:
   - Confirme a presença dos módulos Python necessários (`mcp`, `bpy`) e configure o arquivo de inicialização do servidor.
3. Configurar Parâmetros de Transporte e Rede [FRÁGIL]:
   - Defina o método de comunicação (`stdio` para processo filho direto ou `sse` com `listenPort`).
4. Disparar Inicialização do Processo em Segundo Plano [FRÁGIL]:
   - Inicie o Blender com `blender.exe -b --python-expr "..."` capturando stdout e identificador de processo (PID).
5. Validar Handshake e Ferramentas Disponíveis [FLEXÍVEL]:
   - Envie requisição de inicialização MCP e confirme o retorno das ferramentas de manipulação de malha, luz e render.

## Execution Checklist
- [ ] Confirmar existência do executável do Blender
- [ ] Validar script do servidor MCP e dependências Python
- [ ] Configurar transporte de comunicação (stdio ou SSE)
- [ ] Iniciar processo do Blender em modo headless (-b)
- [ ] Realizar teste de handshake e listar ferramentas 3D

## On Failure
- **Gatilho de Erro**: Falha ao localizar o binário do Blender, porta já ocupada ou erro de importação de módulos no Python interno.
- **Ação Imediata**: Encerrar processos zumbis do Blender e liberar portas de rede.
- **Rollback**: Restaurar configurações anteriores do cliente MCP para o servidor antigo.
- **Fallback**: Se o binário do Blender estiver ausente, invocar automaticamente `installing-blender-headless`.
- **Logs**: Registrar linha de comando completa disparada, log de inicialização do Blender e stderr capturado.

## Reference Documentation
Consulte a documentação técnica completa: [Referência Técnica](reference.md).
