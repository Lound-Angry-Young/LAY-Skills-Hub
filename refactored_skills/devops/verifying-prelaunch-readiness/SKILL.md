---
name: verifying-prelaunch-readiness
description: >
  Runs an exhaustive pre-launch readiness checklist covering environment variables, secret checks and production integrity before real traffic is routed to a version. Use this skill when: preparing a version for production launch before routing real traffic. Do NOT use this skill when: the release is gradual and already live (use orchestrating-staged-rollouts).
---

# Verificação de Prontidão para Lançamento (Pre-Launch)

Executa lista exaustiva de verificação pré-lançamento antes do direcionamento de tráfego real para um novo release: integridade de variáveis de ambiente, proteção contra vazamento de segredos, migrações de banco e observabilidade.

## Input/Output Signature
Input:
- targetReleaseVersion: string # Identificador da versão candidata a lançamento
- targetProductionUrl: string # URL de produção onde o release será ativado
- requiredChecksList: array # Verificações obrigatórias (secrets, env_vars, migrations, health, dns, sentry)
Output:
- readinessScorePercent: number # Percentual de conformidade da verificação
- isLaunchApproved: boolean # Status formal de aprovação para início de tráfego
- failedChecksDetails: array # Relação detalhada de itens reprovados com severidade
- auditReportPath: string # Caminho do relatório de auditoria pre-launch gerado

## Router and Selection Matrix
| Categoria de Checagem | Critério de Aprovação | Grau de Liberdade |
|---|---|---|
| Proteção de Segredos e Chaves | Nenhum token real, chave privada ou senha presente em repositório ou build | [FRÁGIL] Qualquer segredo detectado em texto claro veta o lançamento |
| Variáveis de Ambiente | Todas as variáveis obrigatórias declaradas e validadas contra schema | [FRÁGIL] Variável ausente ou com valor padrão de desenvolvimento veta |
| Migrações de Banco de Dados | Esquemas atualizados com suporte a retrocompatibilidade (expand/contract) | [FRÁGIL] Migração bloqueante sem teste prévio veta o lançamento |
| Monitoramento e Alertas | Rastreamento de erros ativo e rota de health-check respondendo 200 | [FLEXÍVEL] Valida conectividade de sondas de liveness e readiness |

## Imperative Execution Workflow
1. Varrer Código contra Vazamento de Credenciais [FRÁGIL]:
   - Execute varredura estrita com ferramentas SAST e regex buscando tokens de API, chaves privadas e senhas embutidas.
2. Validar Existência de Todas as Variáveis de Ambiente [FRÁGIL]:
   - Confronte o arquivo `.env.example` com o conjunto de variáveis injetadas no ambiente de produção.
3. Auditar Status de Migrações de Banco de Dados [FRÁGIL]:
   - Confirme que todas as migrações necessárias foram aplicadas sem bloqueios de tabela ou incompatibilidades.
4. Testar Endpoint de Saúde e Conectividade de Dependências [FRÁGIL]:
   - Dispare requisições para os endpoints de diagnóstico e verifique conexão com bancos e serviços externos.
5. Emitir Parecer Formal de Prontidão [FLEXÍVEL]:
   - Compile o relatório com todas as checagens e aprove o lançamento somente se 100% dos requisitos críticos passarem.

## Execution Checklist
- [ ] Varrer artefatos e código contra vazamento de credenciais
- [ ] Confirmar preenchimento e validade de todas as variáveis de ambiente
- [ ] Validar status das migrações de banco de dados
- [ ] Confirmar funcionamento dos endpoints de health-check e telemetria
- [ ] Emitir relatório formal com aprovação ou veto de lançamento

## On Failure
- **Gatilho de Erro**: Qualquer segredo exposto em build, variável de ambiente faltante ou falha de conectividade com banco.
- **Ação Imediata**: Vetar formalmente o início do roteamento de tráfego para a versão candidata.
- **Rollback**: Não há alteração de tráfego; a versão anterior permanece operando normalmente em produção.
- **Fallback**: Notificar os mantenedores com a lista exata dos itens reprovados para saneamento imediato.
- **Logs**: Registrar relatório de auditoria detalhado indicando as linhas e configurações que reprovaram o checklist.

## Reference Documentation
Consulte a documentação técnica completa: [Referência Técnica](reference.md).
