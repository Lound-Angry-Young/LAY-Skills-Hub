---
name: configuring-network-proxies
description: >
  Configures HTTP, HTTPS and SOCKS proxies for upstream provider requests, with per-provider or global rules, connectivity tests and proxy rotation. Use this skill when: upstream provider traffic must go through a proxy or proxy rotation is needed. Do NOT use this skill when: exposing OmniRoute itself through a tunnel (use tunneling-omniroute-endpoints).
---

# Configuração de Proxies de Rede para Provedores Upstream

Configura e gerencia proxies HTTP, HTTPS e SOCKS5 para roteamento de tráfego de saída do OmniRoute para provedores de IA, suportando regras globais ou por provedor, rotação de IPs e testes de conectividade.

## Input/Output Signature
Input:
- proxyProtocolAndUrl: string # URL completa do proxy (ex: http://proxy.corp:8080 ou socks5://127.0.0.1:1080)
- targetProviderScope: string # Provedor específico ou 'global' para todas as requisições
- bypassDomainsList: array # Lista de domínios ou faixas IP que não devem passar pelo proxy
- enableProxyRotation: boolean # Se deve alternar entre múltiplos proxies cadastrados (default: false)
Output:
- proxyConfigStatus: string # Estado da configuração (configured, tested, failed)
- connectivityTestResult: object # Latência e código de status do teste de conexão com o provedor
- activeProxyUrl: string # URL mascarada do proxy ativo
- executionLog: string # Registro dos passos de validação de rede

## Router and Selection Matrix
| Tipo de Proxy / Escopo | Procedimento Recomendado | Grau de Liberdade |
|---|---|---|
| Proxy Corporativo HTTP/HTTPS | Injeta variáveis de ambiente padrão ou configura rota via settings | [FRÁGIL] Exige validação de certificados CA corporativos se aplicável |
| Proxy Seguro SOCKS5 | Utiliza transporte SOCKS5 com suporte a resolução DNS remota | [FRÁGIL] Garante ausência de vazamento de DNS (DNS leak) |
| Roteamento Exclusivo por Provedor | Vincula proxy apenas às requisições direcionadas a um provedor específico | [FLEXÍVEL] Permite que outros provedores utilizem conexão direta |
| Rotação de Proxies em Pool | Alterna endpoints de proxy para contornar bloqueios regionais ou rate limits | [FLEXÍVEL] Aplica algoritmo round-robin ou menor latência |

## Imperative Execution Workflow
1. Validar Formato e Sintaxe da URL do Proxy [FRÁGIL]:
   - Verifique protocolo suportado (`http`, `https`, `socks5`), host, porta e credenciais embutidas.
2. Injetar Regras de Bypass e Exceções Locais [FRÁGIL]:
   - Garanta que `localhost`, `127.0.0.1` e serviços de infraestrutura local não sejam roteados pelo proxy.
3. Testar Conectividade com o Provedor Upstream [FRÁGIL]:
   - Dispare requisição de probe HTTP HEAD através do proxy para o endpoint da API do provedor alvo.
4. Aplicar e Persistir Configuração de Rede [FRÁGIL]:
   - Atualize os parâmetros de conexão do OmniRoute vinculando o proxy ao escopo selecionado.
5. Monitorar Latência Adicional e Estabilidade [FLEXÍVEL]:
   - Avalie o overhead de latência introduzido pelo salto de proxy e registre no painel de observabilidade.

## Execution Checklist
- [ ] Validar sintaxe da URL do proxy e autenticação necessária
- [ ] Configurar domínios de bypass local para evitar interceptação de serviços internos
- [ ] Executar teste de handshake e conectividade com a API de destino
- [ ] Persistir configuração de proxy no escopo pretendido
- [ ] Medir e documentar o impacto na latência média das requisições

## On Failure
- **Gatilho de Erro**: Timeout de conexão com o proxy, erro 407 (Proxy Authentication Required) ou falha de resolução DNS.
- **Ação Imediata**: Desativar o proxy imediatamente para restabelecer conectividade direta de emergência.
- **Rollback**: Restaurar as configurações de rede anteriores sem proxy.
- **Fallback**: Comutar para rota direta ou tentar proxy secundário do pool cadastrado.
- **Logs**: Registrar endereço do proxy mascarado, código de erro retornado e latência observada na falha.
