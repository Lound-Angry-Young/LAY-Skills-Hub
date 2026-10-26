## Table of Contents
1. [Visão Geral do Skills CLI](#visão-geral-do-skills-cli)
2. [Comandos Principais e Opções](#comandos-principais-e-opções)
3. [Categorias Frequentes de Busca](#categorias-frequentes-de-busca)
4. [Critérios de Avaliação e Segurança](#critérios-de-avaliação-e-segurança)

## Visão Geral do Skills CLI

O Skills CLI (`npx skills` ou `skills` instalado globalmente via npm) é o gerenciador de pacotes para o ecossistema aberto de habilidades de agentes (open agent skills ecosystem). Ele permite descobrir, instalar, atualizar e criar instruções reutilizáveis para agentes como Claude Code, Cursor, OpenCode, Codex e outros. O catálogo e ranking de habilidades é mantido publicamente em https://skills.sh.

## Comandos Principais e Opções

| Comando | Descrição | Exemplo de Uso |
|---|---|---|
| `npx skills find [query]` | Pesquisa habilidades por palavra-chave ou interativamente | `npx skills find react performance` |
| `npx skills find [query] --owner <owner>` | Pesquisa restringindo ao autor/organização | `npx skills find --owner vercel-labs` |
| `npx skills add <pacote>` | Instala uma skill para agentes no projeto ou globalmente | `npx skills add vercel-labs/agent-skills -g -y` |
| `npx skills add <pacote> --skill <nome>` | Instala uma skill específica de um repositório | `npx skills add vercel-labs/agent-skills --skill web-design-guidelines` |
| `npx skills list` | Lista as habilidades atualmente instaladas | `npx skills list` |
| `npx skills check` | Verifica atualizações disponíveis para as skills instaladas | `npx skills check` |
| `npx skills update [skills...]` | Atualiza todas ou habilidades específicas instaladas | `npx skills update` |
| `npx skills remove [skills...]` | Remove habilidades instaladas | `npx skills remove vercel-labs/agent-skills` |
| `npx skills init [name]` | Inicializa um template para criação de nova skill | `npx skills init my-custom-skill` |
| `npx skills use <source>@<skill>` | Executa uma skill pontual sem gravá-la permanentemente | `npx skills use vercel-labs/agent-skills@react-best-practices` |

## Categorias Frequentes de Busca

| Categoria | Termos Sugeridos de Busca | Fontes Recomendadas |
|---|---|---|
| Desenvolvimento Web Frontend | `react`, `nextjs`, `typescript`, `tailwind`, `view-transitions` | `vercel-labs/agent-skills` |
| Qualidade e Testes | `testing`, `playwright`, `jest`, `e2e`, `accessibility` | `microsoft/playwright-cli`, `anthropics/skills` |
| DevOps e Implantação | `deploy`, `docker`, `kubernetes`, `ci-cd`, `actions` | `vercel-labs/agent-skills` |
| Documentação e ADRs | `docs`, `readme`, `changelog`, `adrs`, `api-docs` | `addyosmani/agent-skills` |
| Revisão de Código | `review`, `refactor`, `clean-code`, `code-quality` | `addyosmani/agent-skills` |
| Design e Interfaces | `ui`, `ux`, `design-system`, `taste`, `stitch` | `leonxlnx/taste-skill`, `voltagent/awesome-design-md` |

## Critérios de Avaliação e Segurança

Ao avaliar skills comunitárias antes de recomendar ou instalar:
1. **Contagem de Instalações:** Priorize habilidades com mais de 1.000 instalações no leaderboard de `skills.sh`.
2. **Reputação da Organização:** Dê preferência a repositórios mantidos por organizações e autores de referência (`vercel-labs`, `anthropics`, `microsoft`).
3. **Estrelas do Repositório GitHub:** Verifique se o repositório upstream possui estrelas e atividade recente.
4. **Inspeção de Instruções:** Certifique-se de que o arquivo `SKILL.md` não solicita execução cega de scripts binários ou download de arquivos arbitrários desconhecidos.
