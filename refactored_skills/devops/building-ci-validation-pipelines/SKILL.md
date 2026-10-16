---
name: building-ci-validation-pipelines
description: >
  Builds and orchestrates continuous integration pipelines with strict quality gates, static scanners, parallel test suites and coverage reports. Use this skill when: configuring CI checks that must pass before a change can be merged. Do NOT use this skill when: deploying to environments (use automating-cd-deployments).
---

# Construção de Pipelines de Integração Contínua (CI)

Projeta e configura pipelines de integração contínua (CI) com portões estritos de qualidade: checagem de tipos, linters, testes automatizados paralelos, varredura de vulnerabilidades e cobertura mínima.

## Input/Output Signature
Input:
- ciPlatform: string # Plataforma de CI alvo (github_actions, gitlab_ci, local_runner)
- workflowFilePath: string # Caminho do arquivo de definição do pipeline (ex: .github/workflows/ci.yml)
- requiredQualityGates: array # Portões obrigatórios (typecheck, lint, unit_tests, security_scan, coverage)
- minCoverageThreshold: number # Percentual mínimo obrigatório de cobertura de testes (default: 80)
Output:
- pipelineConfigValid: boolean # Indica se o arquivo de workflow está sintaticamente válido
- configuredJobs: array # Lista de jobs e matrizes de execução configuradas
- qualityGateSummary: object # Relação de regras bloqueantes que barram o merge
- executionLog: string # Registro da validação estrutural do arquivo de workflow

## Router and Selection Matrix
| Tipo de Repositório / Matriz | Estrutura de Jobs Recomendada | Grau de Liberdade |
|---|---|---|
| Monorepo / Multi-Package | Jobs isolados com filtros de caminho (`paths`) e cache compartilhado | [FLEXÍVEL] Otimiza tempo de execução rodando apenas módulos alterados |
| Aplicação TypeScript / Node | Jobs paralelos: `lint` + `typecheck` -> `test` -> `build` | [FRÁGIL] Exige lockfile imutável (`npm ci` ou `pnpm install --frozen-lockfile`) |
| Suíte com Testes E2E Pesados | Isola testes de integração em job desacoplado com artefatos de vídeo/log | [FLEXÍVEL] Executa após sucesso dos testes unitários rápidos |
| Varredura de Segurança SAST | Integração de Semgrep e auditoria de pacotes bloqueante | [FRÁGIL] Qualquer vulnerabilidade de severidade alta barra o pipeline |

## Imperative Execution Workflow
1. Definir Gatilhos de Disparo do Pipeline [FRÁGIL]:
   - Configure o evento de ativação para `pull_request` e `push` direcionados às branches principais (`main`, `master`).
2. Configurar Cache de Dependências e Determinismo [FRÁGIL]:
   - Utilize comandos com checagem estrita de integridade de lockfile e ative cache de dependências do gerenciador.
3. Paralelizar Validações Estáticas [FLEXÍVEL]:
   - Execute linters, checadores de tipos (`tsc --noEmit`) e validadores de commits em jobs simultâneos.
4. Estruturar Matriz de Testes e Cobertura [FRÁGIL]:
   - Dispare suítes de teste com geração de relatório LCOV e validação da métrica mínima de cobertura.
5. Configurar Portão Bloqueante de Merge [FRÁGIL]:
   - Estabeleça que todos os jobs obrigatórios devem emitir status verde antes que a branch possa ser integrada.

## Execution Checklist
- [ ] Definir gatilhos para pull requests e pushes na branch principal
- [ ] Configurar instalação determinística de dependências com lockfile congelado
- [ ] Configurar jobs paralelos de lint, typecheck e testes
- [ ] Estabelecer limite mínimo bloqueante de cobertura de testes
- [ ] Validar sintaxe do arquivo de workflow contra o esquema da plataforma

## On Failure
- **Gatilho de Erro**: Falha em qualquer job obrigatório do pipeline, violação de cobertura ou erro de sintaxe no arquivo de workflow.
- **Ação Imediata**: Bloquear a aprovação da pull request e emitir anotações com o ponto exato da quebra.
- **Rollback**: Não há alteração de código em produção; a branch pull request permanece bloqueada até correção.
- **Fallback**: Permitir reexecução manual apenas para falhas transitórias de infraestrutura (flaky network).
- **Logs**: Exibir os logs de erro do job que falhou com links diretos para as linhas reprovadas.

## Reference Documentation
Consulte a documentação técnica completa: [Referência Técnica](reference.md).
