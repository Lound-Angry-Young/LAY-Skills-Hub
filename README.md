<div align="center">

# ⚡ LAY Skills Hub

**Base de habilidades, subagentes e regras para agentes de IA**

Google Antigravity · OpenAI Codex · Claude Code

![Stars](https://img.shields.io/github/stars/Lound-Angry-Young/LAY-Skills-Hub?style=for-the-badge&logo=github&color=fff201&labelColor=060709)
![Release](https://img.shields.io/badge/release-v1.0.0-blue?style=for-the-badge&logo=git)
![Skills](https://img.shields.io/badge/skills-136%20online-00f0ff?style=for-the-badge&logo=probot)
![Agents](https://img.shields.io/badge/agents-Antigravity%20%7C%20Codex%20%7C%20Claude-fff201?style=for-the-badge)
![License](https://img.shields.io/badge/license-MIT-green?style=for-the-badge)
![GitHub Pages](https://img.shields.io/badge/pages-ready-brightgreen?style=for-the-badge&logo=github)

<br>

<a href="https://lound-angry-young.github.io/LAY-Skills-Hub/">
  <img src="docs/assets/screenshots/01-hero.png" alt="Hub de skills LAY: hero com 136 skills, 17 fontes upstream e 11 subagentes" width="100%">
</a>

<br><br>

[**🌐 Dashboard**](https://lound-angry-young.github.io/LAY-Skills-Hub/) &nbsp;·&nbsp;
[**📘 Guia dos subagentes**](https://lound-angry-young.github.io/LAY-Skills-Hub/instalacao.html) &nbsp;·&nbsp;
[**⬇️ Instalação**](#-instalação) &nbsp;·&nbsp;
[**🤖 Subagentes**](#-subagentes-para-claude-code)

</div>

---

## 📑 Sumário

- [Visão geral](#-visão-geral)
- [Galeria](#-galeria)
- [Subagentes para Claude Code](#-subagentes-para-claude-code)
- [Componentes animados](#-componentes-animados)
- [Adicionar skills](#-adicionar-skills)
- [Instalação](#-instalação)
- [Taxonomia das 136 habilidades](#-taxonomia-das-136-habilidades)
- [Publicação no GitHub Pages](#-publicação-no-github-pages)
- [Créditos](#-créditos)
- [Mídia](#-mídia)

---

## 🎯 Visão geral

O **LAY Skills Hub** abastece assistentes de código e agentes autônomos (**Google Antigravity**, **OpenAI Codex** e **Claude Code**) com **136 habilidades** e diretrizes técnicas, além de **11 subagentes** especialistas para o Claude Code.

Em vez de respostas genéricas, o hub injeta na camada de contexto dos agentes contratos de arquitetura, metodologia de testes (TDD), regras de segurança (OWASP Top 10), bibliotecas criativas contemporâneas e componentes animados de referência.

| | |
| :--- | :--- |
| 🧠 **136 skills homologadas** | Curadoria de práticas da indústria: Addy Osmani, Vercel Labs, Semgrep e Microsoft Playwright. |
| 🤖 **11 subagentes** | Um especialista por domínio para o Claude Code, instalado globalmente ou versionado no projeto. |
| 🎛️ **Dashboard visual** | Interface estática (`index.html`), pronta para uso local ou no GitHub Pages. |
| 🧾 **Prompts sob medida** | Monte uma seleção de skills e copie o plano de projeto formatado com um clique. |
| 🧭 **Contexto e grafos** | Diagnóstico inicial com `lay-orchestrator`, grafos com **Graphify** e comunicação concisa com **Caveman**. |
| 🎬 **Stack criativa** | Suporte a **Vanta 3D**, **React Bits**, **Lenis Smooth Scroll**, **Libraries.dev** e 357 componentes animados de referência. |

---

## 🖼️ Galeria

Capturas do site atual, tiradas em Chrome headless a 1440×900 (2x) e, no celular, a 390×844 (2x).

<table>
  <tr>
    <td align="center" width="50%">
      <img src="docs/assets/screenshots/01-hero.png" alt="Hero do dashboard com métricas" width="100%"><br>
      <sub><b>Dashboard</b>: hero, métricas e atalhos do hub</sub>
    </td>
    <td align="center" width="50%">
      <img src="docs/assets/screenshots/03-catalogo.png" alt="Catálogo com busca, filtros por categoria e cards" width="100%"><br>
      <sub><b>Catálogo</b>: busca, filtros por categoria e cards com ações</sub>
    </td>
  </tr>
  <tr>
    <td align="center" width="50%">
      <img src="docs/assets/screenshots/04-detalhe-skill.png" alt="Janela com a especificação de uma skill" width="100%"><br>
      <sub><b>Especificação</b>: o <code>SKILL.md</code> completo, com a fonte</sub>
    </td>
    <td align="center" width="50%">
      <img src="docs/assets/screenshots/05-prompt-mestre.png" alt="Janela do prompt mestre" width="100%"><br>
      <sub><b>Prompt mestre</b>: inicialização pronta para qualquer projeto novo</sub>
    </td>
  </tr>
  <tr>
    <td align="center" width="50%">
      <img src="docs/assets/screenshots/06-planejador.png" alt="Planejador com as skills selecionadas" width="100%"><br>
      <sub><b>Planejador</b>: só as skills selecionadas entram no prompt</sub>
    </td>
    <td align="center" width="50%">
      <img src="docs/assets/screenshots/07-celular.png" alt="Dashboard no celular" width="60%"><br>
      <sub><b>Celular</b>: o dashboard funciona sem rolagem horizontal</sub>
    </td>
  </tr>
</table>

### 🤖 Subagentes e guia de instalação

<table>
  <tr>
    <td align="center" colspan="2">
      <img src="docs/assets/screenshots/02-especialistas.png" alt="Seção de escolha pelo domínio, com os subagentes" width="100%"><br>
      <sub><b>Escolha pelo domínio</b>: os subagentes do Claude Code, um por domínio</sub>
    </td>
  </tr>
  <tr>
    <td align="center" colspan="2">
      <img src="docs/assets/screenshots/08-guia-subagentes.png" alt="Guia de instalação dos subagentes em três passos" width="100%"><br>
      <sub><b>Guia de instalação</b>: instalar, conferir e usar os subagentes</sub>
    </td>
  </tr>
</table>

---

## 🤖 Subagentes para Claude Code

O hub traz **11 subagentes** para o Claude Code, um especialista por domínio. Cada um recebe as skills do seu domínio e só as ferramentas que o trabalho exige. A conversa principal escolhe o especialista, delega a tarefa e junta a resposta. **Subagentes não chamam outros subagentes.**

| Subagente | Domínio | Use quando | Ferramentas |
| :--- | :--- | :--- | :--- |
| `lay-omniroute` | routing-and-proxy | roteamento entre modelos, providers, combos, custos e limites de gasto | leitura, edição e comandos |
| `lay-frontend` | frontend | telas, componentes, landing pages, layout e animação de interface | leitura, edição e comandos |
| `lay-engenharia` | engineering | arquitetura, revisão de código, depuração, refatoração, migração e performance | leitura, edição e comandos |
| `lay-contexto` | context | grafo do projeto, planejamento, requisitos, economia de contexto e compressão de prompts | leitura, edição e comandos |
| `lay-devops` | devops | commits, branches, releases, tags, CI/CD e deploy | leitura, edição e comandos |
| `lay-qa` | qa | testes, cobertura, falhas de CI, validação antes de merge e conferência de componente animado | leitura, edição e comandos |
| `lay-seguranca` | security | vulnerabilidades, auditoria, segredos, autenticação e chaves de API | leitura e comandos, sem edição |
| `lay-3d` | creative-3d | 3D, Blender, shaders, fundos animados e bibliotecas de efeitos visuais | leitura, edição e comandos |
| `lay-documentacao` | documentation | revisão de texto, ADRs e prosa para publicação | sem comandos (sem Bash) |
| `lay-design` | design | identidade visual, moodboard, mockups e referências de design | sem comandos (sem Bash) |
| `lay-banco-de-dados` | database | backup, restauração, snapshots e cache de respostas do LLM | leitura, edição e comandos |

### Como chamar

- **Automático:** escreva o pedido normalmente. O Claude escolhe o subagente pela `description`, que traz os gatilhos "Use quando" e "Não use para".
- **Pelo nome:** `use o subagente lay-qa para cobrir o checkout com testes`.
- Subagente novo não aparece? Reinicie a sessão: os perfis são carregados no início.

### Onde ficam

- **Global**, em `~/.claude/agents/`: vale em todos os seus projetos.
- **Projeto**, em [`.claude/agents/`](.claude/agents/): versionado neste repositório. Quando os dois existem, o do projeto prevalece.

### Orquestração

As regras de roteamento estão na seção "Orquestração de subagentes" do [`CLAUDE.md`](CLAUDE.md). O contrato de handoff está em [`agents/wiring/HANDOFF.md`](agents/wiring/HANDOFF.md) e o índice em [`agents/README.md`](agents/README.md).

📘 **Guia completo, com prompts para copiar:** [instalação e uso dos subagentes](https://lound-angry-young.github.io/LAY-Skills-Hub/instalacao.html).

---

## 🧩 Componentes animados

Os registros **Pixel-Perfect** e **Componentry** somam **357 componentes animados** de referência: 300 do Pixel-Perfect e 57 do Componentry. Os agentes consultam o catálogo em [`refactored_skills/frontend/selecting-animated-ui-components/reference.md`](refactored_skills/frontend/selecting-animated-ui-components/reference.md).

Nada é instalado no hub. Cada componente é baixado só quando escolhido, pela skill `integrating-external-ui-components`, e conferido depois por `verifying-animated-component-compliance`. A seleção considera custo de renderização, movimento reduzido, componentes cliente e alternativa para toque.

```bash
python scripts/gerar_catalogo_componentes.py    # lê os registros ao vivo e atualiza o catálogo de referência
```

As licenças e ressalvas de cada registro estão em [Créditos](#-créditos).

---

## ➕ Adicionar skills

Uma skill ou um lote inteiro entra no padrão com um comando. O gerador confere o formato, atualiza os roteadores do domínio e regenera catálogo, dashboard e subagentes. Se algo estiver fora do padrão, nada é gravado.

```bash
python scripts/nova_skill.py dominios                      # domínios, skills e subagente de cada um
python scripts/nova_skill.py nova <nome> --dominio <dominio> --descricao "<texto>" --corpo corpo.md
python scripts/nova_skill.py lote <pasta>                  # pasta <dominio>/<nome>/SKILL.md, tudo ou nada
python scripts/nova_skill.py regenerar
```

📘 Passo a passo, formato e skills privadas: [docs/ADICIONAR_SKILLS.md](docs/ADICIONAR_SKILLS.md).

---

## ⬇️ Instalação

<details open>
<summary><b>Opção 1: dashboard local, sem instalar nada</b></summary>

Dê um duplo clique em [`index.html`](index.html), ou rode no PowerShell:

```powershell
Start-Process "index.html"
```

</details>

<details open>
<summary><b>Opção 2: clonar com as fontes (submódulos)</b></summary>

```bash
git clone --recurse-submodules https://github.com/Lound-Angry-Young/LAY-Skills-Hub.git
cd LAY-Skills-Hub
```

Já clonou sem submódulos? Rode `git submodule update --init --recursive`.

</details>

<details open>
<summary><b>Opção 3: instalar nos agentes</b></summary>

Distribui as skills para os perfis globais do **Google Antigravity**, **OpenAI Codex** e **Claude Code**, incluindo os 11 subagentes.

| Sistema | Comando |
| :--- | :--- |
| Windows (PowerShell) | `powershell -ExecutionPolicy Bypass -File ".\install.ps1"` |
| Linux / macOS | `bash "./install.sh"` |
| Só Claude Code | `python scripts/skill_hub.py install --agents claude` |
| Conferir a instalação | `python scripts/skill_hub.py doctor` |

Atualizar e remover:

```bash
python scripts/skill_hub.py sync --check     # consulta as fontes, não altera nada
python scripts/skill_hub.py sync --apply     # aplica atualizações (explícito)
python scripts/skill_hub.py install --agents all
python scripts/skill_hub.py uninstall
```

<details>
<summary>Regra de atualização das fontes</summary>

1. **Consulta:** automática no início de sessão, por projeto. Não altera nenhum arquivo.
2. **Aplicação:** explícita, com `sync --apply`. Só fast-forward limpo; alterações locais são preservadas.
3. **Commit:** cada fonte atualizada vira um commit `chore(upstream): atualizar <fonte> para <sha7>`.
4. **Reflexo nos agentes:** depois, `install --agents all`.

</details>

</details>

---

## 🏛️ Taxonomia das 136 habilidades

| Domínio | Fontes & Destaques | Capacidades Chave |
| :--- | :--- | :--- |
| **Engenharia & Arquitetura** | Addy Osmani (`agent-skills`), Vercel Labs | TDD rigoroso, interfaces estáveis, simplificação de código, refatoração segura, composition patterns. |
| **Segurança & Auditoria** | Semgrep (`skills`), Ray0907 (`security-scan`) | Análise estática (SAST), regras OWASP Top 10, proteção contra prompt injection em LLMs (OWASP Top 10 for LLM 2025). |
| **Interface & Design** | Vercel Labs, Leon Lin (`taste-skill`), Voltagent | Diretrizes de acessibilidade WCAG AA, design systems de referência, transições nativas (`ViewTransition`), microinterações. |
| **Criatividade & 3D WebGL** | Darkroom Engineering, Tengbao, DavidHDev, Jakub Antalik | Rolagem inercial (**Lenis**), fundos 3D reativos (**Vanta.js**), componentes animados (**React Bits**), catálogo **Libraries.dev**. |
| **Qualidade & E2E** | Microsoft Playwright CLI, Dietrich Gebert (`ponytail`) | Automação e inspeção de navegadores reais via CLI, auditoria de código redundante (YAGNI). |
| **Contexto & Orquestração** | `lay-orchestrator`, Julius Brussee (`caveman`), Safi Shamsi (`graphify`) | Diagnóstico inicial de projetos, grafos persistentes de arquitetura, modo conciso de comunicação direta. |

---

## 🌐 Publicação no GitHub Pages

O repositório já está pronto para o **GitHub Pages**: há o arquivo [`.nojekyll`](.nojekyll) na raiz e o workflow [`.github/workflows/deploy-pages.yml`](.github/workflows/deploy-pages.yml).

<details>
<summary>Como ativar em um fork ou repositório seu</summary>

1. Acesse **Settings** > **Pages** no GitHub.
2. Em **Build and deployment**, selecione **GitHub Actions** (ou **Deploy from a branch** > `main` / `/ (root)`).
3. O dashboard ficará em `https://<seu-usuario>.github.io/<seu-repositorio>/`.

</details>

---

## 📜 Créditos

### Fontes upstream

O hub usa 17 fontes upstream. Os repositórios estão em `upstream/`, como submódulos (ver `.gitmodules`). As licenças são as de cada repositório. Este README não resume os termos delas. Skills LAY derivadas trazem, no próprio `SKILL.md`, a linha de atribuição com a fonte e a licença.

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

---

## 📂 Mídia

Capturas usadas neste README, em `docs/assets/screenshots/`:

| Arquivo | Conteúdo |
| :--- | :--- |
| [`01-hero.png`](docs/assets/screenshots/01-hero.png) | Hero do dashboard, com métricas (1440×900 @2x) |
| [`02-especialistas.png`](docs/assets/screenshots/02-especialistas.png) | Escolha pelo domínio, com os subagentes |
| [`03-catalogo.png`](docs/assets/screenshots/03-catalogo.png) | Catálogo com busca, filtros e cards |
| [`04-detalhe-skill.png`](docs/assets/screenshots/04-detalhe-skill.png) | Janela de especificação de skill |
| [`05-prompt-mestre.png`](docs/assets/screenshots/05-prompt-mestre.png) | Janela do prompt mestre |
| [`06-planejador.png`](docs/assets/screenshots/06-planejador.png) | Planejador sob medida |
| [`07-celular.png`](docs/assets/screenshots/07-celular.png) | Dashboard no celular (390×844 @2x) |
| [`08-guia-subagentes.png`](docs/assets/screenshots/08-guia-subagentes.png) | Guia de instalação dos subagentes |

---

<div align="center">

Desenvolvido para máxima performance e autonomia de agentes de IA • Padrão de Engenharia de Elite

</div>
