---
name: hardening-application-security
description: >
  Hardens code against vulnerabilities by checking input handlers, authentication, data storage, external integrations, dependency risk and OWASP Top Ten exposure. Use this skill when: auditing an input handler, handling untrusted input, user storage, authentication, data boundaries, or hardening code against common vulnerability classes. Do NOT use this skill when: fixing a single known vulnerable dependency package (use scanning-dependency-vulnerabilities) or reviewing general non-security logic.
---

# Hardening Application Security

Aplica práticas rigorosas de segurança defensiva em código de aplicação contra o OWASP Top 10 e vetores comuns de ataque. Trata toda entrada externa como hostil, implementa arquitetura de três camadas de fronteira, parametriza interações com bancos e sistemas, e protege dados sensíveis e credenciais.

## Input/Output Signature

- **Inputs**:
  - `sourceModulePath: string` - Caminho para o arquivo ou módulo sob análise de endurecimento de segurança.
  - `threatBoundaryLevel: "public_api" | "internal_service" | "agent_tool" | "frontend_ui"` - Nível de exposição da fronteira.
  - `dataClassification: "public" | "internal" | "pii" | "secrets"` - Sensibilidade dos dados manipulados pelo código.
- **Outputs**:
  - `detectedVulnerabilities: SecurityFinding[]` - Lista de vulnerabilidades identificadas com arquivo, linha, severidade e CWE.
  - `remediatedCodeSnippet: string` - Código refatorado com defesas em profundidade e validação fail-closed.
  - `appliedHardeningControls: string[]` - Controles de segurança aplicados (sanitização, parametrização, hashing, autorização).

## Router and Selection Matrix

| Condição de Ativação | Skill Alternativa | Racional de Roteamento |
| :--- | :--- | :--- |
| Escanear dependências de pacotes em busca de CVEs conhecidos | `scanning-dependency-vulnerabilities` | Vulnerabilidades de terceiros em lockfiles requerem análise de SBOM/CVE. |
| Auditar vulnerabilidades em aplicações baseadas em LLM e RAG | `securing-llm-applications` | Prompt injection e envenenamento de RAG possuem taxonomias OWASP LLM próprias. |
| Executar varredura estática de código com regras customizadas Semgrep | `scanning-code-with-semgrep` | Varredura automatizada com scanners AST pertence à automação Semgrep. |

## Imperative Execution Workflow

1. Mapear Modelo de Ameaças e Vetores de Entrada [FRÁGIL]:
   - Identifique todas as fontes de dados externos: parâmetros de rota, corpos JSON, headers, uploads de arquivo e webhooks.
   - Determine o nível de impacto caso a fronteira seja violada (vazamento de dados, execução remota de código, bypass de autenticação).
2. Implementar Validação Sintática Rígida de Borda (Tier 1) [FRÁGIL]:
   - Use validadores declarativos rígidos (ex.: Zod, Pydantic) com rejeição explícita de campos adicionais (strip/forbid).
   - Rejeite qualquer entrada que não corresponda ao tipo, tamanho, formato e regex especificados (fail-closed).
3. Aplicar Sanitização Semântica e Neutralização de Injeções (Tier 2) [FRÁGIL]:
   - Parametrize todas as consultas SQL, NoSQL ou chamadas de ORM; proíba concatenação ou interpolação de strings em queries.
   - Aplique escaping contextual para dados renderizados em HTML/DOM para neutralizar XSS.
   - Sanitize caminhos de arquivo para impedir ataques de Directory Traversal (`../`).
4. Endurecer Controles de Autorização e Gerenciamento de Sessão (Tier 3) [FLEXÍVEL]:
   - Garanta verificações de autorização baseadas em objeto (prevenção de BOLA/IDOR), checando se o ator autenticado possui propriedade sobre o registro.
   - Aplique rate limiting em endpoints sensíveis (login, recuperação de senha, operações de escrita em massa).
5. Proteger Armazenamento de Segredos e Dados Sensíveis [FRÁGIL]:
   - Elimine senhas ou chaves gravadas em código; utilize variáveis de ambiente ou secret vaults.
   - Aplique hash criptograficamente seguro (Argon2id ou bcrypt com fator de custo calibrado) para senhas.
   - Mascare dados pessoais (PII) e tokens antes de emitir registros para logs.

## Execution Checklist

- [ ] Validar e tipar estritamente toda entrada externa com rejeição fail-closed
- [ ] Parametrizar todas as queries e comandos sem interpolação de strings
- [ ] Validar propriedade de recurso em cada operação (prevenção de BOLA/IDOR)
- [ ] Configurar cabeçalhos defensivos (CSP, HSTS, X-Content-Type-Options)
- [ ] Garantir ausência total de segredos em código, repositório e registros de log

## On Failure

- **Gatilho de Erro**: Identificação de vulnerabilidade crítica (RCE, SQLi, Auth Bypass) durante a auditoria de código.
- **Ação Imediata**: Bloquear o fluxo de release ou marcar o componente como inseguro até que a correção seja aplicada.
- **Rollback**: Reverter qualquer alteração que reduza ou contorne controles de segurança pré-existentes.
- **Fallback**: Implementar camada de barreira paliativa (WAF rule ou desativação temporária do endpoint vulnerável).
- **Logs**: Registrar detalhe da falha, linha de código afetada e classificação CWE sem expor payloads exploráveis.

## Reference Documentation
Consulte a documentação técnica completa: [Referência Técnica](reference.md)
