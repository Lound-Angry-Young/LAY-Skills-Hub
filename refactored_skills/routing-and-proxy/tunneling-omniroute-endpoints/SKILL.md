---
name: tunneling-omniroute-endpoints
description: >
  Creates and manages secure tunnels (ngrok, Cloudflare Tunnel, custom) to expose OmniRoute to the internet or share access with remote agents and CI pipelines. Use this skill when: making an OmniRoute endpoint reachable from outside the machine through the API. Do NOT use this skill when: only proxying upstream provider traffic (use configuring-network-proxies).
---

# Túneis Seguros para Exposição de Endpoints OmniRoute

Cria, monitora e gerencia túneis seguros (Cloudflare Tunnel, ngrok, Tailscale Funnel) para expor instâncias locais do OmniRoute à internet ou conectar agentes remotos e pipelines de CI/CD externos com autenticação.

## Input/Output Signature
Input:
- tunnelProviderType: string # Provedor de túnel pretendido (cloudflare, ngrok, tailscale, custom)
- localServerPort: number # Porta local do OmniRoute a ser tunelada (default: 20128)
- requireTunnelAuth: boolean # Se deve exigir token de autenticação em todas as conexões externas (default: true)
Output:
- tunnelActiveStatus: string # Estado do túnel (active, establishing, stopped, error)
- publicTunnelUrl: string # URL pública e segura gerada pelo provedor de túnel
- tunnelProcessPid: number # Identificador de processo do túnel em execução
- executionLog: string # Registro dos comandos de abertura e encerramento do túnel

## Router and Selection Matrix
| Provedor de Túnel | Procedimento Recomendado | Grau de Liberdade |
|---|---|---|
| Cloudflare Tunnel (Gratuito e Rápido) | Utiliza binário `cloudflared` criando túnel temporário rápido | [FRÁGIL] Exige presença do binário e portas de rede liberadas |
| ngrok (Com Domínio Personalizado) | Inicia túnel ngrok com token de autenticação e domínio reservado | [FRÁGIL] Requer variável NGROK_AUTHTOKEN configurada |
| Tailscale Funnel | Utiliza a rede privada da malha Tailscale para acesso autenticado entre nós | [FLEXÍVEL] Ideal para comunicação entre servidores confiáveis |
| Encerramento de Túnel | Interrompe o processo e fecha o tráfego externo imediatamente | [FRÁGIL] Garante corte imediato de exposição pública |

## Imperative Execution Workflow
1. Validar Presença do Binário do Provedor de Túnel [FRÁGIL]:
   - Verifique a acessibilidade do binário correspondente (`cloudflared`, `ngrok` ou `tailscale`) no ambiente local.
2. Inspecionar Servidor Local e Bloqueio de Segurança [FRÁGIL]:
   - Confirme que o servidor OmniRoute está ativo localmente e que chaves de autenticação estão ativadas para rotas públicas.
3. Disparar Inicialização do Processo de Túnel [FRÁGIL]:
   - Inicie o túnel vinculando a porta local `localServerPort` e capturando a URL pública emitida no stdout.
4. Validar Conectividade Externa via Probe HTTP [FRÁGIL]:
   - Dispare requisição de teste para a `publicTunnelUrl` confirmando alcance de rede externo sem bloqueios de firewall.
5. Disponibilizar URL para Agentes e Monitorar Sessão [FLEXÍVEL]:
   - Exporte a URL pública para uso como `OMNIROUTE_BASE_URL` em pipelines ou agentes externos autorizados.

## Execution Checklist
- [ ] Verificar presença do executável do túnel no sistema
- [ ] Garantir que o OmniRoute local está ativo e protegido por autenticação
- [ ] Iniciar o túnel seguro na porta local correta
- [ ] Capturar e testar a URL pública gerada
- [ ] Monitorar a conexão e fechar o túnel ao término da atividade

## On Failure
- **Gatilho de Erro**: Falha ao iniciar binário do túnel, token de autenticação inválido ou porta local fechada.
- **Ação Imediata**: Encerrar processos zumbis do túnel e verificar o log de erro do terminal.
- **Rollback**: Fechar qualquer conexão parcial de túnel aberta para evitar exposição desprotegida.
- **Fallback**: Alternar para provedor de túnel secundário (ex: de Cloudflare para ngrok) ou usar VPN dedicada.
- **Logs**: Registrar provedor de túnel selecionado, código de saída e erro emitido no stdout/stderr.
