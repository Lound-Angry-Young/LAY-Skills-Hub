# LAY Skills Hub

Base de skills, subagentes e um site estático para agentes de IA que usam Claude Code, OpenAI Codex ou Google Antigravity. Serve a quem configura esses agentes e quer instruções reutilizáveis por domínio, em vez de repetir as mesmas regras em cada projeto.

Números do repositório:

- 136 skills públicas, em 11 domínios.
- 11 subagentes para o Claude Code, um por domínio.
- 17 fontes upstream, incluídas como submódulos.
- 357 itens no catálogo de referência de componentes animados (300 do Pixel-Perfect e 57 do Componentry). Os agentes consultam o catálogo. Os componentes não ficam instalados no hub.

## Como funciona

O repositório tem três camadas.

### 1. Skills por domínio

Cada skill é uma pasta em `refactored_skills/<domínio>/<nome>/`, com um `SKILL.md` que descreve o que ela faz, quando usá-la e os passos. Algumas têm um `reference.md` com material de apoio. Os 11 domínios são `routing-and-proxy`, `frontend`, `engineering`, `context`, `devops`, `qa`, `security`, `creative-3d`, `documentation`, `design` e `database`. Cada domínio tem um `SKILL.md` de entrada na própria pasta.

A skill de orquestração fica em `skills/lay-orchestrator/SKILL.md`.

### 2. Catálogo e subagentes gerados

- `catalog/skills.json` é o catálogo das skills. `docs/CATALOGO.md` é gerado por `python scripts/skill_hub.py catalog`.
- `agents/perfis.json` define os 11 subagentes. `scripts/build_agents.py` gera cada um em `.claude/agents/`.
- `python scripts/nova_skill.py regenerar` valida as skills e regenera catálogo, hub e subagentes. Se a validação falhar, nada é regenerado.

### 3. Site estático

`index.html` (dashboard) lê `hub/data.js`, `hub/totais.js` e `hub/agentes.js`; `instalacao.html` (guia dos subagentes) lê `hub/totais.js` e `hub/agentes.js`. `scripts/build_hub.py` gera os quatro arquivos de `hub/`:

- `hub/data.js` (`window.LAY_SKILLS`): metadados das skills, sem o conteúdo.
- `hub/conteudo.js` (`window.LAY_CONTEUDO`): conteúdo completo das skills, separado de `data.js`. Cada skill tem `content` (uma linha do markdown por item do array, para leitura direta no editor) e `prompt`. `index.html` o carrega só ao abrir uma skill.
- `hub/agentes.js` (`window.LAY_AGENTES`): dados dos especialistas, lidos por `index.html` e `instalacao.html`.
- `hub/totais.js` (`window.LAY_TOTAIS`): contagens.

O workflow `.github/workflows/deploy-pages.yml` publica a raiz do repositório no GitHub Pages a cada push na `main`. Ele também pode ser disparado manualmente. Endereços:

- Dashboard: https://lound-angry-young.github.io/LAY-Skills-Hub/
- Guia dos subagentes: https://lound-angry-young.github.io/LAY-Skills-Hub/instalacao.html

Em um fork, ative o Pages em Settings > Pages, com a fonte "GitHub Actions".

## Instalação e uso

### Dashboard local

Abra `index.html` no navegador.

### Clonar com as fontes

```bash
git clone --recurse-submodules https://github.com/Lound-Angry-Young/LAY-Skills-Hub.git
cd LAY-Skills-Hub
```

Se o clone foi feito sem submódulos:

```bash
git submodule update --init --recursive
```

### Instalar nos agentes

```bash
python scripts/skill_hub.py install --agents all
python scripts/skill_hub.py doctor
```

`install --agents all` instala as skills para Codex, Antigravity e Claude Code. Para o Claude Code, grava os 11 subagentes em `~/.claude/agents/`. Para um cliente só, troque `all` pelo nome do cliente: `python scripts/skill_hub.py install --agents claude` (ou `codex`, ou `antigravity`). `doctor` confere a instalação.

Os scripts `install.ps1` (Windows) e `install.sh` (Linux e macOS) executam `install` e `doctor` do mesmo instalador:

```powershell
powershell -ExecutionPolicy Bypass -File ".\install.ps1"
```

```bash
bash ./install.sh
```

Atualizar e remover:

```bash
python scripts/skill_hub.py sync --check   # consulta as fontes
python scripts/skill_hub.py sync --apply   # aplica as atualizações
python scripts/skill_hub.py uninstall      # remove o que o instalador registrou
```

### Adicionar skills

```bash
python scripts/nova_skill.py dominios
python scripts/nova_skill.py nova <nome> --dominio <dominio> --descricao "<texto>" --corpo corpo.md
python scripts/nova_skill.py lote <pasta>
python scripts/nova_skill.py regenerar
```

- `dominios` lista os domínios, as skills e o subagente de cada um.
- `nova` cria uma skill no padrão. `lote` adiciona uma pasta `<dominio>/<nome>/SKILL.md`.
- Formato, skills privadas e exemplos estão em [docs/ADICIONAR_SKILLS.md](docs/ADICIONAR_SKILLS.md).

## Subagentes

O hub traz 11 subagentes para o Claude Code, um por domínio. Cada perfil tem uma `description` com os gatilhos "Use quando" e "Não use para". É ela que o Claude usa para decidir quando delegar. Também dá para pedir um especialista pelo nome. Subagentes não chamam outros subagentes: o roteamento fica na conversa principal.

| Subagente | Domínio | Use quando (resumo) | Ferramentas |
| :--- | :--- | :--- | :--- |
| `lay-omniroute` | routing-and-proxy | roteamento entre modelos, providers, combos, custos e limites de gasto no OmniRoute | completo |
| `lay-frontend` | frontend | criar ou revisar telas, componentes, landing pages, layout e animação de interface | completo |
| `lay-engenharia` | engineering | arquitetura, revisão de código, depuração, refatoração, migração e performance | completo |
| `lay-contexto` | context | grafo do projeto, planejamento, requisitos e compressão de contexto ou de prompts | completo |
| `lay-devops` | devops | commits, branches, releases, CI/CD, deploy e lançamento | completo |
| `lay-qa` | qa | testes, cobertura, falhas de CI, validação antes de merge e conferência de componente animado | completo |
| `lay-seguranca` | security | vulnerabilidades, auditoria, segredos, autenticação e chaves de API | sem Edit e Write |
| `lay-3d` | creative-3d | 3D, Blender, shaders, fundos animados e WebGL | completo |
| `lay-documentacao` | documentation | revisão de texto, ADRs e prosa para publicação | sem Bash |
| `lay-design` | design | identidade visual, moodboard, mockups e referências antes de implementar | sem Bash |
| `lay-banco-de-dados` | database | backup, restauração, snapshots e cache de respostas do LLM | completo |

Ferramentas: "completo" são Read, Grep, Glob, Bash, Edit e Write. "sem Edit e Write" são Read, Grep, Glob e Bash, e o `lay-seguranca` só lê e analisa. "sem Bash" são Read, Grep, Glob, Edit e Write.

Onde ficam:

- Global, em `~/.claude/agents/`: vale para todos os projetos.
- Projeto, em `.claude/agents/`: versionado neste repositório. Quando os dois existem, vale o do projeto.

As regras de roteamento estão em [CLAUDE.md](CLAUDE.md). O contrato de handoff está em [agents/wiring/HANDOFF.md](agents/wiring/HANDOFF.md) e o índice em [agents/README.md](agents/README.md). O guia com prompts prontos está em [instalacao.html](https://lound-angry-young.github.io/LAY-Skills-Hub/instalacao.html).

## Skills de componentes animados

Novidade desta versão. Estas skills escolhem, instalam e conferem componentes animados dos registros Pixel-Perfect e Componentry. Os componentes não fazem parte deste repositório. Os agentes consultam o catálogo de referência, e a instalação baixa só o item escolhido, pela URL do registro.

| Skill | Domínio | O que faz |
| :--- | :--- | :--- |
| [`selecting-animated-ui-components`](refactored_skills/frontend/selecting-animated-ui-components/SKILL.md) | frontend | Escolhe um componente pela necessidade e pelo custo: T1 (CSS e DOM), T2 (biblioteca de animação ou canvas 2D) e T3 (WebGL). Não baixa nada. |
| [`integrating-external-ui-components`](refactored_skills/frontend/integrating-external-ui-components/SKILL.md) | frontend | Instala o item escolhido sob demanda, pelo CLI do shadcn, e prepara utils, tipos e pacotes faltantes. |
| [`clarifying-screen-requirements`](refactored_skills/frontend/clarifying-screen-requirements/SKILL.md) | frontend | Faz perguntas antes de gerar uma tela, para não decidir por suposição. |
| [`verifying-animated-component-compliance`](refactored_skills/qa/verifying-animated-component-compliance/SKILL.md) | qa | Confere imports, "use client", movimento reduzido, WebGL por rota, toque, lil-gui, licença e tsc. Só lê e não altera arquivos. |

### Catálogo e gerador

O catálogo de referência é [`refactored_skills/frontend/selecting-animated-ui-components/reference.md`](refactored_skills/frontend/selecting-animated-ui-components/reference.md). Ele tem 357 itens: 300 do Pixel-Perfect e 57 do Componentry, lidos ao vivo em 2026-10-12 (seção 5 do arquivo). A instalação baixa a versão atual do registro, que pode ser mais nova que o catálogo.

O gerador é `scripts/gerar_catalogo_componentes.py`:

```bash
python scripts/gerar_catalogo_componentes.py
python scripts/gerar_catalogo_componentes.py --pixel-perfect <clone-local>
python scripts/gerar_catalogo_componentes.py --componentry <clone-local>
```

Sem argumentos, lê os registros publicados ao vivo. Com `--pixel-perfect` ou `--componentry`, lê um clone local, sem rede. Os clones não são submódulos do hub. `--site <arquivo.js>` grava um arquivo de dados opcional, que o site atual não usa. Sem essa opção, nenhum arquivo do site é gravado.

### Fluxo

1. Se faltar objetivo, dispositivo, stack, tolerância a movimento ou direção visual, `clarifying-screen-requirements` faz as perguntas antes de gerar a tela, uma por vez.
2. `selecting-animated-ui-components` escolhe o item. Quando CSS ou SVG resolvem, escolha T1. T3 (WebGL) fica para pedido explícito, porque renderiza na GPU a cada quadro. Se nenhum item servir, a skill diz isso e propõe CSS próprio ou um componente novo.
3. `integrating-external-ui-components` instala o item com o CLI do shadcn, sempre com `-y`:

   ```bash
   npx shadcn@latest add https://www.pixel-perfect.space/r/<nome>.json -y
   npx shadcn@latest add https://componentry.dev/r/<nome>.json -y
   ```

   A instalação exige `components.json` na raiz do projeto. Sem ele, a skill para e aguarda confirmação. Ela não sobrescreve arquivo existente e não roda `shadcn init` sem confirmação. Nunca clona repositório e nunca baixa o catálogo inteiro.
4. `verifying-animated-component-compliance` confere os arquivos criados e relata. Não corrige nada.

### Regras de uso

- No máximo um componente WebGL (T3) por tela. A verificação conta por rota.
- Movimento reduzido: todo efeito tem um estado final estático, que aparece quando o usuário pede movimento reduzido. Use `useReducedMotion` (Framer Motion), `gsap.matchMedia()` (GSAP) ou `window.matchMedia("(prefers-reduced-motion: reduce)")`.
- Toque: efeito que depende de ponteiro (`mousemove`, `pointermove`, `mouseenter`) precisa de caminho para toque. Desative a animação em `(hover: none)` e mostre o estado final.
- "use client": no Next.js App Router, o arquivo que usa hook ou evento começa com `"use client"` na primeira linha. Se um arquivo de servidor importar o componente, mova o uso para um componente cliente.
- lil-gui: é um painel de depuração. Antes de publicar, remova a importação e os controles, mantenha os valores padrão como constantes e rode `npm uninstall lil-gui`. São 17 itens do catálogo que importam lil-gui.
- Licença: mantenha o aviso MIT do arquivo copiado quando o original tiver cabeçalho. Registre a nota de cada biblioteca usada (GSAP, Three.js, Framer Motion ou Motion) em `THIRD_PARTY_NOTICES` ou no README do projeto.
- GSAP: o README do Componentry alerta que `image-trail` e `layered-stack` exigem atenção à licença do GSAP. Confira a licença na fonte antes de usar esses itens.
- Antes de publicar, `npx tsc --noEmit` e o build do projeto precisam passar.

## Manutenção e validação

```bash
python scripts/nova_skill.py regenerar
python scripts/validate_skills.py
python -m unittest discover -s tests -p "test_*.py"
python scripts/gerar_catalogo_componentes.py
```

- `nova_skill.py regenerar` valida as skills e regenera catálogo, hub e subagentes. Se a validação falhar, nada é regenerado. Rode depois de adicionar ou alterar skills.
- `validate_skills.py` valida as skills em `refactored_skills/`.
- `unittest` roda os testes da pasta `tests/`.
- `gerar_catalogo_componentes.py` regenera o catálogo de componentes. Depois, confira a origem e a data na seção 5 de `reference.md` e rode `validate_skills.py`.

### Atualização das fontes

A regra completa está em [docs/OPERACAO.md](docs/OPERACAO.md). Em resumo: a consulta é automática no início da sessão e não altera arquivos; a aplicação é explícita, com `python scripts/skill_hub.py sync --apply`, e só faz fast-forward limpo, sem descartar alterações locais; cada fonte atualizada vira um commit `chore(upstream): atualizar <fonte> para <sha7>`; depois, `python scripts/skill_hub.py install --agents all` reflete a mudança nos agentes.

## Créditos

### Fontes upstream

O hub usa 17 fontes upstream. Os repositórios estão em `upstream/`, como submódulos (ver `.gitmodules`). As licenças são as de cada repositório. Este README não resume os termos delas.

| Repositório | Autor |
| :--- | :--- |
| [addyosmani/agent-skills](https://github.com/addyosmani/agent-skills) | Addy Osmani |
| [vercel-labs/agent-skills](https://github.com/vercel-labs/agent-skills) | Vercel Labs |
| [Leonxlnx/taste-skill](https://github.com/Leonxlnx/taste-skill) | @Leonxlnx |
| [semgrep/skills](https://github.com/semgrep/skills) | Semgrep Team |
| [microsoft/playwright-cli](https://github.com/microsoft/playwright-cli) | Microsoft |
| [Ray0907/security-scan](https://github.com/Ray0907/security-scan) | Ray0907 |
| [DietrichGebert/ponytail](https://github.com/DietrichGebert/ponytail) | Dietrich Gebert |
| [safishamsi/graphify](https://github.com/safishamsi/graphify) | Safi Shamsi |
| [guillaumemeyer/watermarks-remover](https://github.com/guillaumemeyer/watermarks-remover) | Guillaume Meyer |
| [diegosouzapw/OmniRoute](https://github.com/diegosouzapw/OmniRoute) | Diego Souza |
| [Anil-matcha/open-generative-ai](https://github.com/Anil-matcha/open-generative-ai) | Anil Matcha |
| [voltagent/awesome-design-md](https://github.com/voltagent/awesome-design-md) | VoltAgent |
| [latent-spaces/brag](https://github.com/latent-spaces/brag) | Latent Spaces |
| [tengbao/vanta](https://github.com/tengbao/vanta) | Tengbao |
| [DavidHDev/react-bits](https://github.com/DavidHDev/react-bits) | David H. Dev |
| [darkroomengineering/lenis](https://github.com/darkroomengineering/lenis) | Darkroom Engineering |
| [Jakubantalik/Libraries.dev](https://github.com/Jakubantalik/Libraries.dev) | Jakub Antalik |

### Outras atribuições

- Caveman: Julius Brussee (@JuliusBrussee), licença MIT. Repositório: https://github.com/JuliusBrussee/caveman

### Componentes de referência

- Pixel-Perfect
  - Site: https://www.pixel-perfect.space/
  - Repositório: https://github.com/vansh-nagar/Pixel-Perfect
  - Licença MIT. Autor: Vansh Nagar.
- Componentry
  - Site: https://componentry.dev/
  - Repositório: https://github.com/harshjdhv/componentry
  - Licença MIT. Autor: Harsh Jadhav.
  - Ressalva do próprio README do Componentry: `image-trail` e `layered-stack` exigem atenção à licença do GSAP. Este README não afirma termos da GSAP.

Esses componentes não fazem parte deste repositório. Os clones usados para gerar o catálogo ficam fora do hub, e cada item é baixado só quando escolhido.

### Referências do fundo

O fundo halftone do site é inspirado em duas referências visuais. O fundo não copia código delas:

- `currency-sky-background`, do Pixel-Perfect.
- `dither-gradient`, do Componentry.

### Planejamento

Planejamento do projeto: Georges. Perfil: https://github.com/GeorgesBallister
