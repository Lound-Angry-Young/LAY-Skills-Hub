---
name: collecting-cli-agent-skills
description: >
  Detects installed CLI coding tools (Claude Code, Codex, Cursor, Copilot, Cline and more), searches GitHub for matching agent skills and installs them into the detected tools through OmniRoute's built-in APIs. Use this skill when: distributing agent skills to the coding tools installed on the machine. Do NOT use this skill when: only importing skills from GitHub without tool detection (use importing-github-agent-skills).
---

# Descoberta e Distribuição de Skills para Ferramentas CLI

Detecta ferramentas e clientes de programação instalados na máquina local (Claude Code, Codex, Cursor, Copilot, Cline) e distribui automaticamente agent skills compativeis através do OmniRoute.

## Input/Output Signature
Input:
- targetToolClientsList: array # Ferramentas alvo para distribuição (claude, codex, cursor, all_detected)
- searchKeywords: array # Termos para busca de skills compatíveis (ex: react, testing, security)
- overwriteExisting: boolean # Se deve atualizar skills já existentes nos destinos (default: false)
Output:
- detectedClients: array # Ferramentas CLI encontradas no ambiente local
- installedSkillsSummary: object # Relação de skills distribuídas por ferramenta
- failedInstallations: array # Lista de eventuais falhas com motivo da rejeição
- executionLog: string # Registro dos comandos de detecção e cópia executados

## Router and Selection Matrix
| Ferramenta Detectada | Diretório de Instalação Alvo | Grau de Liberdade |
|---|---|---|
| Claude Code | `.claude/skills/` (projeto) ou `~/.claude/skills/` (global) | [FRÁGIL] Exige validação de frontmatter YAML compatível |
| Codex CLI | `~/.codex/skills/` ou diretório de perfil configurado | [FRÁGIL] Requer arquivo de configuração válido |
| Cursor IDE / Cline | `.cursor/rules/` ou `.cline/skills/` conforme convenção | [FLEXÍVEL] Mapeia arquivos de regras e prompts de sistema |
| Todas as Ferramentas | Dispara sincronização em lote para todas as ferramentas encontradas | [FLEXÍVEL] Executa distribuição idempotente sem sobrescrita destrutiva |

## Imperative Execution Workflow
1. Escanear o Ambiente por Clientes Instalados [FRÁGIL]:
   - Verifique a presença de binários e diretórios de configuração de Claude Code, Codex, Cursor e Cline.
2. Listar Skills Disponíveis no Hub Local [FLEXÍVEL]:
   - Consulte o catálogo de skills prontas para distribuição em `refactored_skills` ou cache do OmniRoute.
3. Filtrar Skills pelo Escopo da Ferramenta [FLEXÍVEL]:
   - Mapeie quais habilidades são adequadas para cada assistente com base nas ferramentas que ele suporta.
4. Executar Cópia e Registro nos Diretórios Alvo [FRÁGIL]:
   - Transfira as pastas de skills para os locais de descoberta dos clientes preservando nomes e metadados.
5. Validar Descoberta nos Clientes de Destino [FLEXÍVEL]:
   - Confirme que os arquivos estão legíveis e acessíveis para o runtime das ferramentas de codificação.

## Execution Checklist
- [ ] Escanear ferramentas de codificação ativas no sistema
- [ ] Selecionar skills compatíveis no catálogo
- [ ] Copiar arquivos para os diretórios de configuração de cada cliente
- [ ] Manter integridade de frontmatter e arquivos de referência
- [ ] Confirmar o sucesso da instalação em cada ferramenta

## On Failure
- **Gatilho de Erro**: Falha de permissão no diretório global, cliente desconhecido ou formato de skill inválido.
- **Ação Imediata**: Interromper a cópia para a ferramenta afetada e registrar a falha.
- **Rollback**: Remover pastas parciais copiadas na ferramenta que apresentou erro.
- **Fallback**: Disponibilizar o comando de instalação manual via CLI (`omniroute skills install`).
- **Logs**: Registrar cliente com erro, caminho do diretório inacessível e código de exceção.

## Reference Documentation
Consulte a documentação técnica completa: [Referência Técnica](reference.md).
