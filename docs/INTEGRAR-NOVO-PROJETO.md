# Integrar o LAY Skills Hub em um projeto novo

As skills são instaladas **globalmente uma vez por máquina**. Cada projeto recebe apenas contexto próprio; não copie `upstream/`, bundles ou todo o catálogo de skills para dentro dele. O hub seleciona capacidades quando a tarefa pede. Hyperframes está fora do catálogo.

## 1. Preparar a máquina uma vez

Requisitos: Git, Python 3.10+ e acesso ao GitHub no clone. A instalação preserva skills e regras pessoais existentes; uma colisão de nome interrompe o processo para revisão. Consulte [operação](OPERACAO.md) para detalhes e limites.

Windows (PowerShell):

```powershell
git clone --recurse-submodules https://github.com/Lound-Angry-Young/LAY-Skills-Hub.git
cd LAY-Skills-Hub
./install.ps1
python scripts/skill_hub.py doctor
```

macOS/Linux:

```sh
git clone --recurse-submodules https://github.com/Lound-Angry-Young/LAY-Skills-Hub.git
cd LAY-Skills-Hub
./install.sh
python3 scripts/skill_hub.py doctor
```

`install` coloca adaptadores nas pastas globais de Codex, Claude Code e Antigravity. Os arquivos integrais de cada fonte ficam em `~/.lay-skills/bundles/`; os guias e o runtime ficam em `~/.lay-skills/runtime/`. Graphify é preparado em ambiente isolado. Outros executáveis citados por skills são instalados apenas quando o projeto realmente precisar deles. Se já existe um clone sem submódulos, execute `git submodule update --init --recursive` antes de instalar.

## 2. Criar o contexto mínimo do projeto

Crie o diretório do projeto e, dentro dele, um `AGENTS.md` curto. Use [`templates/AGENTS.template.md`](../templates/AGENTS.template.md) como base. Preencha **objetivo**, **público**, **ação principal**, **stack/restrições** e **como verificar o resultado**. Se ainda não há decisão de stack ou visual, registre isso em vez de copiar exemplos antigos. Só acrescente [`CLAUDE.md`](../templates/CLAUDE.template.md) e [`GEMINI.md`](../templates/GEMINI.template.md) se esses clientes precisarem de instruções locais adicionais. Para trabalho visual, preencha apenas os campos pertinentes de [`DESIGN.template.md`](../templates/DESIGN.template.md).

Exemplo de `AGENTS.md` enxuto:

```md
# Projeto

- Objetivo: permitir que [público] realize [ação principal].
- Contexto e restrições: [domínio, dados, plataforma, stack decidida ou em aberto].
- Conclusão verificável: [comportamento observável e teste/checagem relevante].

Use o LAY Skills Hub global. No primeiro uso, execute `start` para verificar o repositório pai antes das fontes. Consulte Graphify quando houver grafo; se não houver, identifique o mapa local como provisório. Comunique-se de forma direta (Caveman). Busque e leia somente as skills necessárias para a etapa atual. Preserve as decisões e convenções deste projeto.
```

O agente deve seguir primeiro o pedido atual e as instruções locais aplicáveis. O modelo acima orienta, sem impor framework, estética ou dependências.

## 3. Iniciar o projeto no hub

Na primeira sessão, abra o agente **dentro do diretório do projeto**. Os hooks globais podem acionar `start`; execute-o manualmente quando não houver evidência de que rodou. No Codex, hooks de usuário só executam depois de habilitados em `/hooks`.

Windows (PowerShell; substitua o caminho do projeto):

```powershell
python "$HOME\.lay-skills\runtime\scripts\skill_hub.py" start --home "$HOME" --project "C:\caminho\do\projeto"
```

macOS/Linux:

```sh
python3 "$HOME/.lay-skills/runtime/scripts/skill_hub.py" start --project "/caminho/do/projeto"
```

`start` verifica primeiro este repositório pai, depois as fontes. A primeira verificação bem-sucedida é registrada por projeto; `--refresh` força nova consulta e `--offline` usa o catálogo instalado, deixando claro que a rede não foi consultada. ✅ aparece apenas quando uma atualização foi aplicada e verificada. Se houver código, leia a tabela de prioridades e evidências antes de editar. Se for um diretório novo, defina o problema e ative skills conforme a etapa.

## 4. Escolher por etapa, sem despejar o catálogo no contexto

Use `search` no runtime instalado, por exemplo:

```powershell
python "$HOME/.lay-skills/runtime/scripts/skill_hub.py" search design
```

No PowerShell, se `$HOME` não apontar para o perfil esperado, use o caminho absoluto de `~/.lay-skills/runtime/scripts/skill_hub.py`. Em macOS/Linux, troque `python` por `python3`. `search` retorna IDs reais; abra o `SKILL.md` original indicado pelo adaptador e só suas referências pertinentes. Consulte [guia](GUIA.md), [dicionário](DICIONARIO.md) e [catálogo](CATALOGO.md) quando precisar.

| Momento | Pergunta prática | Repertório inicial |
|---|---|---|
| Descoberta | Quem precisa fazer o quê? | `interview-me`, `idea-refine` |
| Planejamento | Qual é a menor entrega verificável? | `spec-driven-development`, `planning-and-task-breakdown` |
| Design | Qual hierarquia e linguagem visual servem à intenção? | `elevating-frontend-taste`, `frontend-ui-engineering`, `consulting-design-references` |
| Implementação | Que mudança resolve o próximo problema? | `incremental-implementation`, skills da stack escolhida |
| Segurança | Onde entram dados, identidade, segredos e permissões? | `code-security`, `scanning-dependency-vulnerabilities`, `semgrep` quando executável estiver disponível |
| Validação | O fluxo e o resultado visível funcionam? | `quality`, `automating-browser-tests`, `web-design-guidelines` quando pertinentes |
| Entrega | Como operar e observar o que foi construído? | `ci-cd-and-automation`, `observability-and-instrumentation` |

Graphify orienta a leitura de dependências durante o trabalho; Caveman mantém respostas curtas e precisas. Skills adicionais entram quando há uma lacuna concreta. Para design, sintetize referências em critérios próprios, conforme [DESIGN.md](DESIGN.md). Runtimes externos, credenciais e serviços citados por uma skill não são concedidos automaticamente pela instalação.

## Pedido inicial reutilizável para o agente

```text
Estamos começando um projeto em [diretório]. Objetivo: [resultado]. Público: [quem]. Ação principal: [o que deve conseguir fazer]. Restrições já decididas: [lista ou “nenhuma”]. Critério de conclusão: [comportamento verificável].

Leia o AGENTS.md local e o LAY Skills Hub global. Execute o diagnóstico inicial se ainda não foi registrado. Use Graphify com evidência ou informe que está usando mapa local provisório. Trate uma decisão por vez, faça perguntas diretas apenas quando a resposta mudar a solução e selecione skills por etapa. Antes de implementar, apresente o próximo passo e a skill principal. Preserve as decisões deste projeto.
```

Se o projeto ganhar código antes da primeira abertura com o hub, trate-o como **projeto existente**: mostre prioridades, evidências e próxima ação antes da edição. O [guia](GUIA.md) descreve essa triagem.
