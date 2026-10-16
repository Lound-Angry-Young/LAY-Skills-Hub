---
name: scanning-code-with-semgrep
description: >
  Runs Semgrep static analysis scans and writes custom YAML detection rules across 30+ languages to find security vulnerabilities and bug patterns. Use this skill when: asked to scan code with Semgrep, find vulnerabilities, write custom rules, run static analysis or enforce coding standards. Do NOT use this skill when: reviewing code by reading it without a scanner (use auditing-code-security) or auditing LLM application risks (use securing-llm-applications).
---

# Scanning Code with Semgrep

Executa análises estáticas avançadas com Semgrep e desenvolve regras customizadas em YAML para detecção de vulnerabilidades de segurança, anti-patterns e violações arquiteturais em mais de 30 linguagens de programação.

## Input/Output Signature

- **Inputs**:
  - `scanTargetDirectory: string` - Diretório ou arquivo raiz a ser submetido à varredura estática.
  - `rulesetConfiguration: "p/security-audit" | "p/owasp-top-ten" | "p/default" | "local_rules"` - Configuração de regras a ser aplicada.
  - `customRuleFilePath?: string` - Caminho para arquivo YAML contendo regras personalizadas para a varredura.
  - `reportOutputFormat: "json" | "text" | "sarif"` - Formato de saída para o relatório de resultados.
- **Outputs**:
  - `detectedIssues: SemgrepVulnerabilityItem[]` - Lista estruturada de achados contendo arquivo, linha, severidade e CWE.
  - `sarifExportFilePath?: string` - Caminho para o artefato SARIF gerado para ingestão em pipelines de CI/CD.
  - `findingsSummaryCount: { critical: number, high: number, medium: number, low: number }` - Contagem de vulnerabilidades por severidade.

## Router and Selection Matrix

| Condição de Ativação | Skill Alternativa | Racional de Roteamento |
| :--- | :--- | :--- |
| Revisar código manualmente sem ferramenta de scanner automatizado | `auditing-code-security` | Análise manual exploratória pertence à auditoria de segurança de código. |
| Auditar riscos de segurança específicos em aplicações LLM / RAG | `securing-llm-applications` | Taxonomia de segurança em IA generativa pertence a securing-llm-applications. |
| Identificar vulnerabilidades e CVEs em dependências de terceiros | `scanning-dependency-vulnerabilities` | Escaneamento de pacotes e lockfiles pertence à análise de dependências. |

## Imperative Execution Workflow

1. Verificar Disponibilidade do Semgrep no Ambiente [FRÁGIL]:
   - Execute `semgrep --version` para validar se a CLI do Semgrep está instalada e operacional.
2. Definir Configuração de Regras e Filtros de Exclusão [FLEXÍVEL]:
   - Selecione o ruleset adequado ao objetivo: `--config p/security-audit` para varredura de segurança, `--config p/owasp-top-ten` para conformidade web, ou `--config <customRuleFilePath>` para regras de projeto.
   - Configure exclusão de pastas não pertinentes: `--exclude "node_modules" --exclude "dist" --exclude ".git" --exclude "tests"`.
3. Executar Varredura Estática nos Alvos [FRÁGIL]:
   - Execute o comando: `semgrep scan --config <rulesetConfiguration> --<reportOutputFormat> --output semgrep_report.<reportOutputFormat> <scanTargetDirectory>`.
4. Triar Achados e Distinguir Vulnerabilidades Reais [FLEXÍVEL]:
   - Avalie cada ocorrência em relação ao contexto da aplicação; descarte falsos positivos demonstráveis documentando supressões justificadas (`nosemgrep`).
5. Gerar Relatório e Consolidar Ações Corretivas [FRÁGIL]:
   - Estruture os achados de severidade Crítica e Alta com indicações exatas de refatoração para mitigação imediata.

## Execution Checklist

- [ ] Validar execução do binário semgrep no ambiente
- [ ] Escolher o ruleset adequado (security-audit, owasp-top-ten ou regra customizada)
- [ ] Excluir pastas compiladas, caches e bibliotecas de terceiros do scan
- [ ] Exportar resultado em formato estruturado (JSON ou SARIF)
- [ ] Auditar achados críticos e propor remediações defensivas

## On Failure

- **Gatilho de Erro**: Falha de sintaxe em regra YAML customizada, estouro de memória em repositório excessivo ou erro no binário semgrep.
- **Ação Imediata**: Interromper o scan e inspecionar a saída de erro da CLI.
- **Rollback**: N/A (operação de análise estática estritamente somente leitura).
- **Fallback**: Executar scan particionado por subpastas ou aplicar regras pré-selecionadas menores.
- **Logs**: Registrar comando de invocação, arquivos com erro de parsing e saída de stderr do Semgrep.

## Reference Documentation
Consulte a documentação técnica completa: [Referência Técnica](reference.md)
