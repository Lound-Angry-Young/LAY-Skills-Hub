---
name: finding-agent-skills
description: >
  Discovers, searches, evaluates and installs agent skills from the open ecosystem and skills.sh registry using the Skills CLI. Use this skill when: searching for community skills to solve a task, finding installable skills from skills.sh, or installing skills with npx skills. Do NOT use this skill when: selecting among already-installed LAY skills (use discovering-and-invoking-skills) or importing raw GitHub repos into OmniRoute (use importing-github-agent-skills).
---

# Localizando e Instalando Agent Skills do Ecossistema

Descobre, avalia a reputação e instala pacotes de agent skills do ecossistema aberto (`skills.sh`, GitHub) usando a interface de linha de comando oficial `npx skills` (ou o binário global `skills`).

## Input/Output Signature
Input:
- taskQuery: string # Termo de busca, domínio ou funcionalidade procurada (ex: 'react testing', 'deploy', 'changelog')
- ownerFilter: string # Filtro opcional por organização ou usuário GitHub (ex: 'vercel-labs', 'anthropics')
- targetScope: string # Escopo da instalação: 'global' (-g) ou 'local' no projeto (default: 'global')
Output:
- success: boolean # Se a busca ou instalação foi completada com êxito
- candidateSkills: array # Lista de pacotes identificados com métricas de adoção e reputação
- installationCommand: string # Linha de comando pronta para instalação (ex: 'npx skills add <source>@<skill> -g -y')
- executionLog: string # Registro dos comandos executados e diagnósticos obtidos

## Router and Selection Matrix
| Necessidade / Situação | Ação Recomendada | Grau de Liberdade |
|---|---|---|
| Consulta a Habilidades Consolidadas | Consulta o leaderboard de `skills.sh` para stacks populares | [FLEXÍVEL] Prioriza skills com >1K instalações de autores oficiais |
| Busca por Palavra-Chave no Terminal | Dispara `npx skills find <termo>` | [FRÁGIL] Aplica filtros `--owner` quando a organização for conhecida |
| Auditoria de Reputação e Segurança | Inspeciona contagem de instalações, autor e estrelas no GitHub | [FRÁGIL] Bloqueia recomendação de pacotes sem histórico ou suspeitos |
| Instalação de Skill Selecionada | Executa `npx skills add <pacote> -g -y` no ambiente | [FRÁGIL] Garante sinalizador `-g` e não-interativo `-y` |
| Habilidade Inexistente no Registro | Orienta implementação direta ou scaffolding com `npx skills init` | [FLEXÍVEL] Progride sem interromper a demanda do usuário |

## Imperative Execution Workflow
1. Mapear Requisitos e Termos de Descoberta [FLEXÍVEL]:
   - Identifique o domínio técnico e as palavras-chave da funcionalidade desejada pelo usuário (ex: testes, animação, integração).
2. Consultar Fontes e Leaderboard de Alta Adoção [FLEXÍVEL]:
   - Antes de consultas amplas, verifique pacotes consolidados em `skills.sh` de organizações oficiais (`vercel-labs`, `anthropics`, `microsoft`).
3. Disparar Busca Interativa ou Direta [FRÁGIL]:
   - Execute no terminal: `npx skills find <termo>` (opcionalmente `--owner <org>`).
4. Triar Reputação e Critérios de Segurança [FRÁGIL]:
   - Valide se a skill possui métricas confiáveis (preferencialmente >1.000 instalações, repositório ativo e sem comandos destrutivos).
5. Apresentar Opções e Instalar sob Autorização [FRÁGIL]:
   - Exiba o nome da skill, descrição, total de instalações e link de consulta. Caso autorizado, execute `npx skills add <owner/repo@skill> -g -y`.

## Execution Checklist
- [ ] Extrair palavras-chave e domínio da demanda do usuário
- [ ] Checar se há skill equivalente no leaderboard oficial
- [ ] Executar busca no ecossistema com `npx skills find`
- [ ] Validar reputação, contagem de downloads e segurança
- [ ] Apresentar opções fundamentadas e instalar com `npx skills add`

## On Failure
- **Gatilho de Erro**: Falha de rede, timeout do npx, ausência de correspondências ou erro no comando `skills add`.
- **Ação Imediata**: Interromper o processo de instalação e inspecionar a saída de erro do CLI.
- **Rollback**: Remover pastas ou symlinks corrompidos criados durante a tentativa de instalação.
- **Fallback**: Comunicar a ausência da skill, oferecendo resolução direta com capacidades nativas ou sugerir criação via `npx skills init`.
- **Logs**: Registrar termo pesquisado, lista de pacotes avaliados e o stack trace ou código de saída do CLI.

## Reference Documentation
Consulte a documentação técnica e tabela de comandos: [Referência do Skills CLI](reference.md).
