---
name: importing-github-agent-skills
description: >
  Searches, scores, scans and imports agent skills from GitHub repositories that contain SKILL.md, CLAUDE.md, .cursorrules and similar files, checking heuristic relevance and screening for malware or hardcoded secrets before installing. Use this skill when: discovering and importing community agent skills from GitHub. Do NOT use this skill when: distributing already-installed skills to local coding tools (use collecting-cli-agent-skills).
---

# Importação e Varredura de Skills do GitHub

Pesquisa, pontua e importa agent skills de repositórios comunitários do GitHub contendo `SKILL.md`, `CLAUDE.md` ou `.cursorrules`, executando varredura heurística de relevância e triagem de segurança contra segredos ou código malicioso.

## Input/Output Signature
Input:
- githubRepoUrlOrQuery: string # URL do repositório GitHub ou termo de busca para descoberta
- targetSkillDomain: string # Domínio pretendido para categorização no hub local
- runSecurityScanBeforeInstall: boolean # Se deve executar análise SAST antes de gravar arquivos (default: true)
Output:
- importSuccess: boolean # Status da importação da skill
- importedSkillName: string # Nome normalizado em gerúndio atribuído à skill importada
- securityAuditFindings: array # Lista de achados de segurança ou confirmação de conformidade
- destinationLocalPath: string # Caminho no repositório onde a skill foi armazenada

## Router and Selection Matrix
| Origem da Skill | Procedimento de Importação | Grau de Liberdade |
|---|---|---|
| Repositório com SKILL.md Padronizado | Clona temporariamente, valida frontmatter YAML e importa mantendo licença | [FRÁGIL] Exige preservação de avisos de direitos autorais e licença original |
| Repositório com Prompt Solto (.cursorrules/CLAUDE.md) | Converte as regras em estrutura canônica de skill com gatilhos explícitos | [FLEXÍVEL] Formula descrição em 3ª pessoa e limites de uso |
| Skill com Risco de Segurança Detectado | Bloqueia a importação caso detecte execuções arbitrárias de shell suspeitas | [FRÁGIL] Tolerância zero para scripts de download de binários não confiáveis |
| Importação em Lote de Repositório Curado | Extrai subpastas de skills individuais e registra fontes em `registry/sources.json` | [FLEXÍVEL] Mantém integridade do catálogo local de fontes |

## Imperative Execution Workflow
1. Inspecionar Conteúdo Remoto no Repositório GitHub [FRÁGIL]:
   - Baixe ou clone o repositório em diretório temporário isolado sem executar nenhum script contido nele.
2. Executar Varredura de Segurança e Segredos [FRÁGIL]:
   - Varrer arquivos buscando tokens de API gravados, links maliciosos e comandos de terminal destrutivos.
3. Normalizar Nome e Frontmatter Conforme o Padrão [FRÁGIL]:
   - Assegure que o nome esteja em gerúndio (`action-verb-ing`) e a descrição contenha `Use this skill when:` e `Do NOT use this skill when:`.
4. Adequar Estrutura do Corpo do Documento [FLEXÍVEL]:
   - Se o corpo exceder 100 linhas, extraia referências extensas para documentos auxiliares iniciando com `## Table of Contents`.
5. Gravar Arquivos no Domínio e Atualizar Catálogo [FRÁGIL]:
   - Salve a skill em `refactored_skills/<dominio>/<skill-name>/` e valide com `scripts/validate_skills.py`.

## Execution Checklist
- [ ] Inspecionar repositório remoto sem executar código arbitrário
- [ ] Conduzir varredura de segurança contra segredos e scripts maliciosos
- [ ] Normalizar metadados para padrão estrito de Agent Skills
- [ ] Preservar aviso de atribuição e licença original do autor
- [ ] Validar a skill importada com o validador oficial do projeto

## On Failure
- **Gatilho de Erro**: Detecção de código malicioso, ausência de instruções úteis, quebra de regras de frontmatter ou falha de git clone.
- **Ação Imediata**: Abortar a importação e purgar o diretório temporário de download.
- **Rollback**: Remover qualquer pasta parcial criada em `refactored_skills/`.
- **Fallback**: Solicitar revisão manual do repositório pelo desenvolvedor antes de tentar nova importação.
- **Logs**: Registrar URL do repositório, problema de segurança detectado e resultado da análise estática.
