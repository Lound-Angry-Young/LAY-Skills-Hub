# Instalação e operação

Para aplicar este hub a um novo projeto depois da instalação global, siga o [passo a passo de integração](INTEGRAR-NOVO-PROJETO.md).

Requisitos para o hub: Git, Python 3.10+ e acesso às fontes GitHub durante clone/atualização. O orquestrador usa só a biblioteca padrão Python. A instalação padrão prepara Graphify em um ambiente Python isolado no hub. Outros runtimes descritos pelas fontes (Semgrep, Playwright, OmniRoute etc.) têm dependências próprias e são preparados quando a tarefa exigir.

## Um comando no Windows

```powershell
git clone --recurse-submodules https://github.com/Lound-Angry-Young/SKILLS-E-CONFIGS-PARA-NOVOS-PROJETOS.git
cd SKILLS-E-CONFIGS-PARA-NOVOS-PROJETOS
./install.ps1
```

Se o repositório já foi clonado, `git submodule update --init --recursive` traz as fontes fixadas. Em macOS/Linux, execute `./install.sh` depois do clone recursivo. O comando `install` cria entradas globais com prefixo `lay-*` em `~/.agents/skills`, `~/.claude/skills`, `~/.gemini/config/skills` (Antigravity IDE) e `~/.gemini/antigravity-cli/skills` (CLI); preserva outras skills e insere um bloco delimitado nas instruções globais. O conteúdo integral fica em `~/.lay-skills/bundles/<fonte>/<SHA>/`; o runtime e os guias ficam em `~/.lay-skills/runtime/`. A CLI Graphify isolada fica em `~/.lay-skills/tools/graphify/Scripts/graphify.exe` no Windows ou `bin/graphify` em POSIX. Use `install --skip-tools` para preparar apenas skills sem dependências Python extras. O clone pode ser movido depois da instalação; para atualizações automáticas ele precisa continuar disponível ou ser reinstalado a partir do novo clone.

```powershell
python scripts/skill_hub.py install --agents all
python scripts/skill_hub.py doctor
python scripts/skill_hub.py search design
python scripts/skill_hub.py scan
python scripts/skill_hub.py start --project 'C:\caminho\do\projeto'
python scripts/skill_hub.py start --project 'C:\caminho\do\projeto' --refresh
python scripts/skill_hub.py start --project 'C:\caminho\do\projeto' --offline
python scripts/skill_hub.py sync --check
python scripts/skill_hub.py sync --apply
python scripts/skill_hub.py uninstall
```

`--home` permite instalar/testar em outro diretório de usuário. `sync` consulta **primeiro** o repositório pai, depois as fontes, e só aplica fast-forward limpo. Alterações locais não são descartadas. `--check` não altera revisões; `--apply` atualiza commits de fontes e catálogo. `start`, e o hook de início de sessão, só consulta: roda `sync --check` na primeira vez por projeto, registra o resultado e apresenta prioridades para código existente. Nunca altera arquivos do repositório. `--refresh` força nova consulta; `--offline` usa o inventário instalado e sinaliza ausência de verificação. Os relatórios `.state/` são locais e ignorados pelo Git.

Desinstalar remove apenas wrappers gerenciados cujo hash não mudou. Bundles e backups permanecem em `~/.lay-skills/` para recuperação. Arquivos pré-existentes com o mesmo nome são preservados e a instalação para com mensagem de colisão. Reinstalações repetidas atualizam entradas gerenciadas sem duplicar blocos globais.

## Abertura inicial nos agentes

Os arquivos globais curtos orientam Codex, Claude e Antigravity a executar `start` no primeiro uso do projeto. O instalador pode configurar hooks nativos quando estes são compatíveis e sem sobrescrever hooks existentes. No Codex, hooks de usuário precisam de confiança explícita em `/hooks` para executarem; enquanto isso, o arquivo `AGENTS.md` continua como instrução de fallback. Em Claude, `SessionStart` pode reler skills na sessão; em Antigravity, o evento equivalente é `PreInvocation` no primeiro ciclo. Uma atualização iniciada depois que o cliente carregou o catálogo pode exigir nova sessão ou recarregamento para expor novos IDs. Consulte [documentação Codex](https://learn.chatgpt.com/docs/hooks), [Claude](https://code.claude.com/docs/en/hooks) e [Antigravity](https://antigravity.google/docs/hooks).

## Regra de atualização de fontes

1. **Consulta:** automática no início de sessão, por projeto (`start` roda `sync --check`). Não altera nenhum arquivo.
2. **Aplicação:** explícita, com `python scripts/skill_hub.py sync --apply` no repositório do hub. Só fast-forward limpo; alterações locais são preservadas.
3. **Commit:** cada fonte atualizada vira um commit `chore(upstream): atualizar <fonte> para <sha7>`. O registro vai num commit próprio: `chore(registry): atualizar registro das fontes`.
4. **Reflexo nos agentes:** depois, `python scripts/skill_hub.py install --agents all`.
