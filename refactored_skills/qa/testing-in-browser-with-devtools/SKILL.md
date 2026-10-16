---
name: testing-in-browser-with-devtools
description: >
  Tests in real browsers through Chrome DevTools MCP: inspects the DOM, captures console errors, analyzes network requests, profiles performance and verifies visual output with runtime data. Use this skill when: building or debugging anything that runs in a browser. Do NOT use this skill when: only writing Playwright test code without runtime inspection (use automating-browser-tests).
---

# Inspeção e Testes no Navegador com Chrome DevTools MCP

Inspeciona e testa páginas web em navegadores reais utilizando o Chrome DevTools MCP: captura erros de console em tempo real, analisa cascata de requisições de rede, audita layout visual e diagnostica gargalos de runtime.

## Input/Output Signature
Input:
- pageTargetUrl: string # URL da página web a ser inspecionada no navegador
- inspectionActions: array # Ações a realizar (capture_console, inspect_dom, analyze_network, take_screenshot)
- targetDomSelector: string # Seletor CSS do elemento foco para inspeção de layout e propriedades
Output:
- inspectionSuccess: boolean # Status da conexão e inspeção
- capturedConsoleErrors: array # Lista de exceções, avisos e mensagens de erro do console
- networkRequestsSummary: object # Relação de requisições de rede, códigos HTTP e tempos de resposta
- layoutAuditVerdict: string # Parecer sobre alinhamento visual, overflow e acessibilidade básica

## Router and Selection Matrix
| Sinal a Inspecionar | Ação Recomendada | Grau de Liberdade |
|---|---|---|
| Erros e Avisos de Console | Captura streams de logs em busca de exceções não tratadas e erros de hidratação | [FRÁGIL] Qualquer erro não tratado no console indica defeito a ser corrigido |
| Tráfego de Rede e APIs | Monitora requisições AJAX/Fetch, códigos de resposta HTTP 4xx/5xx e payloads | [FRÁGIL] Exige verificação estrita de falhas de endpoints de dados |
| Problemas de Layout e Overflow | Inspeciona caixas de elementos, barras de rolagem indesejadas e clipping | [FLEXÍVEL] Examina propriedades computadas de estilo no DOM |
| Verificação Visual Renderizada | Tira screenshot da página ou componente e valida contra o design pretendido | [FLEXÍVEL] Confirma ausência de artefatos visuais ou saltos de layout |

## Imperative Execution Workflow
1. Abrir ou Conectar à Página Alvo via DevTools MCP [FRÁGIL]:
   - Conecte o cliente MCP ao navegador Chrome e navegue até `pageTargetUrl` aguardando o carregamento completo do DOM.
2. Inspecionar e Capturar Mensagens do Console [FRÁGIL]:
   - Filtre erros de JavaScript, avisos de React e mensagens de segurança que ocorreram durante o carregamento da página.
3. Analisar Cascata de Requisições de Rede [FLEXÍVEL]:
   - Verifique que todos os ativos estáticos e endpoints de API responderam com status 200/304 sem falhas de conexão.
4. Auditar Elementos DOM e Estilos Computados [FLEXÍVEL]:
   - Inspecione dimensões de caixas, propriedades de padding, flex/grid e confirme ausência de rolagem horizontal espúria.
5. Capturar Evidência Visual da Renderização [FRÁGIL]:
   - Gere captura de tela do estado renderizado para comprovar o funcionamento e alinhamento visual da interface.

## Execution Checklist
- [ ] Estabelecer conexão com o navegador Chrome via DevTools MCP
- [ ] Navegar para a página alvo e monitorar carregamento
- [ ] Capturar e auditar erros e avisos do console do navegador
- [ ] Inspecionar requisições de rede e verificar respostas das APIs
- [ ] Registrar captura visual da interface renderizada

## On Failure
- **Gatilho de Erro**: Exceção não tratada no console da página, falha em requisição de API essencial ou travamento do renderizador.
- **Ação Imediata**: Capturar o stack trace completo do console e o estado atual do DOM.
- **Rollback**: Não aplicável; a ferramenta atua em modo de inspeção sem mutações de código.
- **Fallback**: Abrir a ferramenta de desenvolvimento local para inspeção manual interativa.
- **Logs**: Registrar linha e arquivo de origem da exceção JavaScript e resposta da requisição de rede que falhou.

## Reference Documentation
Consulte a documentação técnica completa: [Referência Técnica](reference.md).
