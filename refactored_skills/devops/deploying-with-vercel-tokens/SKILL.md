---
name: deploying-with-vercel-tokens
description: >
  Deploys and manages Vercel projects with token-based CLI authentication instead of interactive login, for setup and deployment on machines or pipelines that use access tokens. Use this skill when: using the Vercel CLI with access tokens. Do NOT use this skill when: the user is already logged in interactively and only wants a deployment (use deploying-to-vercel-platform).
---

# Implantação Automatizada na Vercel via Tokens de Acesso

Executa implantações e operações administrativas na Vercel sem interface gráfica ou login interativo, utilizando tokens de acesso seguro (`VERCEL_TOKEN`, `VERCEL_ORG_ID`, `VERCEL_PROJECT_ID`) em pipelines de automação.

## Input/Output Signature
Input:
- projectRootPath: string # Caminho do repositório a ser implantado
- targetEnvironment: string # Ambiente de destino (production ou preview)
- vercelTokenEnvVarName: string # Nome da variável que contém o token de acesso (default: VERCEL_TOKEN)
- teamScopeId: string # ID opcional do time ou organização proprietária do projeto
Output:
- deploymentSuccess: boolean # Status da operação de implantação via token
- deploymentUrl: string # URL pública gerada para a implantação
- authenticatedUser: string # Identificador da conta autenticada pelo token
- executionLog: string # Registro dos comandos executados com credenciais mascaradas

## Router and Selection Matrix
| Ambiente de Execução | Estratégia de Autenticação | Grau de Liberdade |
|---|---|---|
| Runner de CI/CD (GitHub/GitLab) | Injeta variáveis via secrets do pipeline e passa flags `--token` | [FRÁGIL] Proibido imprimir ou registrar o valor do token em logs |
| Script Local Automatizado | Lê token de arquivo `.env` seguro ou variável de ambiente da sessão | [FRÁGIL] Exige máscara estrita em qualquer saída do terminal |
| Projetos em Organizações (Teams) | Adiciona obrigatoriamente a flag `--scope <teamScopeId>` | [FRÁGIL] Falha se o projeto pertencer a um time e o escopo for omitido |
| Validação de Escopo e Permissões | Executa `vercel whoami --token ...` antes de disparar o deploy | [FLEXÍVEL] Previne falhas de permissão no meio do upload |

## Imperative Execution Workflow
1. Verificar Presença e Validade do Token de Acesso [FRÁGIL]:
   - Confirme a existência da variável `VERCEL_TOKEN` no ambiente e valide o formato de credencial.
2. Validar Identidade e Escopo da Conta [FRÁGIL]:
   - Dispare `vercel whoami --token $VERCEL_TOKEN` para confirmar autenticação e permissões da credencial.
3. Vincular Projeto com Identificadores de Time e Projeto [FRÁGIL]:
   - Garanta que as variáveis `VERCEL_ORG_ID` e `VERCEL_PROJECT_ID` estejam configuradas ou injete flags correspondentes.
4. Disparar Implantação em Modo Não-Interativo [FRÁGIL]:
   - Execute `vercel --token $VERCEL_TOKEN --yes` adicionando `--prod` se o destino for produção.
5. Validar Conclusão e Mascarar Saídas [FRÁGIL]:
   - Capture a URL de saída garantindo que nenhum token de acesso apareça na transcrição ou nos logs de saída.

## Execution Checklist
- [ ] Confirmar existência da variável com o token da Vercel
- [ ] Validar identidade da conta via comando whoami
- [ ] Verificar configuração do escopo de time e ID do projeto
- [ ] Executar deploy não-interativo com flag --yes
- [ ] Assegurar que os tokens de autenticação permaneçam mascarados nos logs

## On Failure
- **Gatilho de Erro**: Token de acesso inválido ou expirado, falta de permissão no time/projeto ou erro no build remoto.
- **Ação Imediata**: Abortar o pipeline imediatamente e alertar sobre a falha de autenticação.
- **Rollback**: A versão em produção anterior permanece intacta; nenhum estado inconsistente é promovido.
- **Fallback**: Solicitar a renovação ou regeneração do token de acesso no painel de segurança da Vercel.
- **Logs**: Registrar o código de status HTTP do erro sem expor nenhum caractere do token em texto claro.

## Reference Documentation
Consulte a documentação técnica completa: [Referência Técnica](reference.md).
