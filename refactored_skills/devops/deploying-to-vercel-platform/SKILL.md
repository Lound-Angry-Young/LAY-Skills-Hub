---
name: deploying-to-vercel-platform
description: >
  Deploys applications to the Vercel platform: inspects project configuration, framework preset and build output, runs production or preview deployments, and verifies URL reachability. Use this skill when: deploying a project to Vercel. Do NOT use this skill when: using token-based authentication on a remote CI machine (use deploying-with-vercel-tokens) or optimizing costs of an already-deployed project (use optimizing-vercel-deployments).
---

# Implantação de Aplicações na Plataforma Vercel

Executa e gerencia implantações de projetos na plataforma Vercel (Next.js, Remix, Astro, SvelteKit, Vite), validando configurações de build, ambientes de preview/produção e acessibilidade das rotas públicas.

## Input/Output Signature
Input:
- projectRootPath: string # Caminho raiz do projeto contendo o código e dependências
- targetEnvironment: string # Ambiente de destino (preview ou production)
- vercelConfigPath: string # Caminho opcional do arquivo vercel.json de configuração
Output:
- deploymentSuccess: boolean # Status da operação de implantação
- deploymentUrl: string # URL pública atribuída pela Vercel ao deployment
- inspectedFramework: string # Framework detectado automaticamente pelo build
- deploymentDurationSeconds: number # Duração total do processo de compilação e deploy

## Router and Selection Matrix
| Tipo de Implantação | Ação Recomendada | Grau de Liberdade |
|---|---|---|
| Implantação de Produção | Executa `vercel --prod` com apontamento imediato para o domínio principal | [FRÁGIL] Exige validação prévia de testes e ausência de erros de build |
| Implantação de Prévia (Preview) | Executa `vercel` gerando URL temporária e imutável de verificação | [FLEXÍVEL] Ideal para validação visual e testes de aceitação |
| Configurações Especiais de Rota | Aplica regras de cabeçalho, reescrita e redirecionamento via `vercel.json` | [FRÁGIL] Requer sintaxe estrita para evitar loops de redirecionamento |
| Verificação de Conectividade | Testa retorno HTTP 200 na URL gerada antes de confirmar o deploy | [FRÁGIL] Confirmação obrigatória de disponibilidade pública |

## Imperative Execution Workflow
1. Inspecionar Estado do Projeto e Dependências [FRÁGIL]:
   - Verifique a presença de `package.json`, scripts de build e garanta que o projeto compila localmente sem erros.
2. Identificar Framework e Configuração de Saída [FLEXÍVEL]:
   - Analise `vercel.json` se existente e confirme se o preset do framework está alinhado com a versão em uso.
3. Disparar Comando de Implantação na Vercel [FRÁGIL]:
   - Execute o comando da CLI da Vercel para o ambiente selecionado (`vercel` para preview ou `vercel --prod`).
4. Monitorar Logs de Compilação Remota [FLEXÍVEL]:
   - Acompanhe o streaming de logs da Vercel até a finalização do job e geração da URL pública.
5. Validar Disponibilidade Pública da URL [FRÁGIL]:
   - Dispare requisição HTTP GET na `deploymentUrl` confirmando resposta com código de sucesso 200.

## Execution Checklist
- [ ] Confirmar que o build de produção local passa sem erros
- [ ] Validar arquivo de configuração vercel.json se existente
- [ ] Executar comando de implantação para o ambiente correto
- [ ] Capturar a URL final atribuída ao deployment
- [ ] Testar requisição HTTP na URL pública confirmando código 200

## On Failure
- **Gatilho de Erro**: Falha no build remoto na Vercel, estouro de tempo limite de compilação ou URL retornando 5xx.
- **Ação Imediata**: Interromper o processo e consultar o painel de logs de compilação remota.
- **Rollback**: A Vercel mantém o deployment anterior ativo caso o novo build falhe; nenhuma ação manual de rollback é necessária.
- **Fallback**: Inspecionar os logs de build em busca de variáveis de ambiente faltantes ou módulos incompatíveis.
- **Logs**: Registrar o identificador de deployment da Vercel e o trecho final do log onde ocorreu o erro.

## Reference Documentation
Consulte a documentação técnica completa: [Referência Técnica](reference.md).
