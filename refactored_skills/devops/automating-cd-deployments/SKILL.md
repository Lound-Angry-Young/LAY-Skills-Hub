---
name: automating-cd-deployments
description: >
  Automates continuous delivery flows: provisions staging and production environments, runs post-deploy smoke tests and triggers automatic rollback. Use this skill when: promoting artifacts through environments or wiring automated deployment and rollback. Do NOT use this skill when: building the CI validation pipeline (use building-ci-validation-pipelines) or releasing a canary to a traffic subset (use orchestrating-staged-rollouts).
---

# Automação de Pipelines de Entrega Contínua (CD)

Orquestra pipelines de implantação contínua (CD) entre ambientes de homologação e produção, executando verificações de fumaça pós-deploy e disparo de reversão automática diante de falhas.

## Input/Output Signature
Input:
- deploymentEnvironment: string # Ambiente alvo da entrega (staging, production)
- artifactVersionTag: string # Tag de versão ou hash do commit do artefato a ser implantado
- runSmokeTests: boolean # Se deve disparar testes automatizados pós-implantação (default: true)
- autoRollbackOnFailure: boolean # Se deve reverter automaticamente em caso de falha nos testes (default: true)
Output:
- deploymentSuccess: boolean # Status da implantação
- activeDeploymentUrl: string # URL ativa do ambiente recém-implantado
- smokeTestResults: object # Resumo dos testes de fumaça executados pós-deploy
- executionLog: string # Registro cronológico do pipeline de entrega

## Router and Selection Matrix
| Ambiente / Estratégia | Ação Recomendada | Grau de Liberdade |
|---|---|---|
| Implantação em Staging | Executa deploy direto e dispara suíte abrangente de fumaça | [FLEXÍVEL] Tolera instabilidades temporárias em dependências externas |
| Implantação em Produção | Executa blue/green ou swap atômico após validação em staging | [FRÁGIL] Exige aprovação de portão de qualidade e testes estritos |
| Falha em Teste de Fumaça | Dispara rollback imediato para a versão anterior comprovadamente estável | [FRÁGIL] Ação de reversão automática incondicional para proteger tráfego |
| Promoção de Artefato | Transfere a mesma imagem ou build testado sem recompilação | [FRÁGIL] Garante paridade absoluta entre staging e produção |

## Imperative Execution Workflow
1. Validar Artefato e Pré-Requisitos do Ambiente [FRÁGIL]:
   - Verifique se a tag de versão `artifactVersionTag` foi aprovada em todos os gates de CI anteriores.
2. Provisionar e Configurar Variáveis de Ambiente [FRÁGIL]:
   - Injete credenciais e configurações seguras correspondentes a `deploymentEnvironment` sem expor segredos.
3. Disparar Comando de Implantação Atômica [FRÁGIL]:
   - Execute o script de implantação da plataforma com estratégia blue/green ou zero-downtime.
4. Executar Testes de Fumaça Pós-Deploy [FRÁGIL]:
   - Realize requisições HTTP nos endpoints vitais de saúde (`/api/health`), rotas críticas e autenticação.
5. Consolidar Estado ou Acionar Reversão [FLEXÍVEL]:
   - Em caso de êxito nos testes, confirme o tráfego na nova versão; se houver falha, dispare o rollback imediato.

## Execution Checklist
- [ ] Validar aprovação prévia do artefato no pipeline de integração contínua
- [ ] Injetar variáveis de ambiente específicas do destino
- [ ] Executar implantação atômica sem tempo de inatividade
- [ ] Disparar bateria de testes de fumaça pós-implantação
- [ ] Confirmar estabilidade ou executar procedimento de rollback

## On Failure
- **Gatilho de Erro**: Falha nos testes de fumaça pós-deploy, erro HTTP 5xx contínuo ou timeout no comando de implantação.
- **Ação Imediata**: Acionar o procedimento de rollback instantâneo para o release imediatamente anterior.
- **Rollback**: Restaurar o ponteiro de tráfego para a versão estável prévia e notificar os mantenedores.
- **Fallback**: Congelar novas implantações no ambiente e manter a versão estável em execução contínua.
- **Logs**: Registrar o log de deploy, falhas detalhadas dos testes de fumaça e métricas de erro registradas.

## Reference Documentation
Consulte a documentação técnica completa: [Referência Técnica](reference.md).
