---
name: automating-browser-tests
description: >
  Automates browser interactions, tests web pages and works with Playwright tests from the Playwright CLI. Use this skill when: writing or running browser automation or Playwright tests against a web page. Do NOT use this skill when: inspecting a running page through DevTools signals such as console errors, network requests or performance (use testing-in-browser-with-devtools).
---

# Automação de Testes de Navegador com Playwright

Escreve, executa e depura testes ponta a ponta (E2E) e fluxos automatizados de navegador utilizando o Playwright CLI, gerando relatórios de execução, traces de reprodução e capturas visuais.

## Input/Output Signature
Input:
- testTargetUrl: string # URL da página web a ser testada ou navegada
- testScriptOrCommand: string # Comando Playwright CLI a ser disparado (ex: test, codegen, show-trace)
- browserEngine: string # Motor de navegador alvo (chromium, firefox, webkit)
- headlessExecution: boolean # Se deve executar sem abrir janela gráfica (default: true)
Output:
- suiteSuccess: boolean # Status da execução da suíte de testes
- passedTestsCount: number # Quantidade de testes aprovados com sucesso
- failedTestsCount: number # Quantidade de testes que falharam
- traceArtifactPath: string # Caminho do arquivo de trace gravado para inspeção
- executionLog: string # Registro dos comandos executados e assertivas avaliadas

## Router and Selection Matrix
| Cenário de Teste | Ação Recomendada | Grau de Liberdade |
|---|---|---|
| Suíte Completa de Testes E2E | Executa `npx playwright test` em modo headless com paralelismo | [FRÁGIL] Exige validação de asserções assíncronas com auto-waiting |
| Depuração de Teste Específico | Dispara teste isolado gerando trace detalhado (`--trace on`) | [FLEXÍVEL] Permite inspeção passo a passo de eventos DOM |
| Gravação de Novo Fluxo Interativo | Abre ferramenta interativa de geração de código (`playwright codegen`) | [FLEXÍVEL] Gera seletores baseados em texto e atributos acessíveis |
| Validação de Regressão Visual | Compara capturas de tela com tolerância de pixels configurada | [FRÁGIL] Requer ambiente de renderização estável sem animações ativas |

## Imperative Execution Workflow
1. Verificar Servidor de Aplicação Ativo [FRÁGIL]:
   - Assegure que a aplicação web alvo esteja rodando na porta correta e respondendo a requisições HTTP antes dos testes.
2. Estruturar Teste com Seletores Baseados em Acessibilidade [FRÁGIL]:
   - Utilize localizadores semânticos recomendados (`getByRole`, `getByText`, `getByLabel`) em vez de seletores CSS frágeis.
3. Disparar Execução de Testes com o Playwright CLI [FRÁGIL]:
   - Execute o comando Playwright com as flags apropriadas de navegador e geração de relatórios.
4. Inspecionar Asserções e Esperas Assíncronas [FRÁGIL]:
   - Garanta que todas as verificações utilizem `expect(locator).toBeVisible()` com tempo limite calibrado.
5. Analisar Relatórios e Capturar Traces em Falhas [FLEXÍVEL]:
   - Em caso de reprovação, extraia o arquivo de trace para identificar o frame e seletor onde a falha ocorreu.

## Execution Checklist
- [ ] Confirmar que o servidor da aplicação está ativo e acessível
- [ ] Empregar seletores semânticos e papéis ARIA nos testes
- [ ] Executar suíte de testes com o Playwright CLI
- [ ] Validar que todas as asserções assíncronas aguardam o estado correto
- [ ] Inspecionar traces e capturas de tela geradas para diagnóstico

## On Failure
- **Gatilho de Erro**: Timeout aguardando seletor, asserção visual divergente ou crash do processo do navegador.
- **Ação Imediata**: Capturar screenshot imediato da página e salvar arquivo de trace completo.
- **Rollback**: Não há alteração de código de produção por se tratar de ferramenta de teste.
- **Fallback**: Inspecionar a página manualmente via `testing-in-browser-with-devtools` para checar erros de console.
- **Logs**: Registrar o seletor que falhou, timeout atingido e log de saída do terminal do Playwright.

## Reference Documentation
Consulte a documentação técnica completa: [Referência Técnica](reference.md).
