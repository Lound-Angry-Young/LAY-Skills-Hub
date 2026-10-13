# Guia de seleção

Comece pelo pedido concreto. Escolha uma skill principal e especialistas apenas quando cobrirem uma lacuna real. Use `python scripts/skill_hub.py search <termo>` para ver IDs e descrições; o [catálogo](CATALOGO.md) contém o arquivo original de cada entrada. Abra o `SKILL.md` original escolhido e as referências necessárias, sem carregar a coleção inteira.

| Trabalho | Comece por | Acrescente quando houver motivo |
|---|---|---|
| Entender código, dependências, impacto | `generating-knowledge-graphs` e `lay-orchestrator` | `context-engineering`, `ponytail-audit` |
| Descobrir intenção e definir escopo | `interview-me`, `idea-refine` | `planning-and-task-breakdown`, `spec-driven-development` |
| Interface e identidade | `taste-skill`, `frontend-ui-engineering` | `consulting-design-references`, `brandkit`, `web-design-guidelines`, `impeccable`, `ui-ux-pro` |
| Animação, 3D WebGL e rolagem suave | `rendering-vanta-backgrounds`, `animating-react-bits-components` | `orchestrating-smooth-scroll`, `selecting-creative-libraries`, `taste` |
| Componente animado dos registros Pixel-Perfect ou Componentry | `selecting-animated-ui-components` (catálogo e critérios) | `integrating-external-ui-components`, `clarifying-screen-requirements` antes de gerar tela, `verifying-animated-component-compliance` para conferir |
| Acessibilidade e acabamento | `impeccable`, `web-design-guidelines` | `playwright-cli` para validar o fluxo visível |
| Implementar e revisar código | `incremental-implementation`, `code-review-and-quality` | `react-best-practices`, `composition-patterns`, `api-and-interface-design` conforme stack |
| Testes e automação do browser | `quality`, `test-driven-development` | `playwright-cli`, `browser-testing-with-devtools` |
| Segurança e auditoria | `code-security`, `security-scan` | `semgrep`, `llm-security`, `security-and-hardening` |
| Operação e entrega | `ci-cd-and-automation`, `shipping-and-launch` | `observability-and-instrumentation`, `deploy-to-vercel` se plataforma for Vercel |
| Modelos, agentes e roteamento | `omni-*`, `cli-*` do OmniRoute | `architecting-generative-ai-apps` para padrões de implementação quando cabível |
| Imagens e mídia de projeto | `imagegen-frontend-web`, `imagegen-frontend-mobile` | `watermarks-remover` apenas para mídia autorizada |
| Comunicação e custo de contexto | `compressing-agent-messages`, `using-agent-skills` | `context-engineering`, `omni-compression` conforme ambiente |

O nome na tabela é termo de busca; o **ID global** é prefixado por origem para evitar colisões. Exemplo: `python scripts/skill_hub.py search playwright`. Consulte o [dicionário](DICIONARIO.md) para função e limite de cada fonte.

## Projeto existente

Antes de editar, levante objetivo, stack, Git, arquivos relevantes, testes disponíveis e estado de Graphify. Mostre uma tabela curta com **prioridade, evidência, próxima ação e skill**. Uma ausência detectada é evidência; uma vulnerabilidade suposta não é. Execute o trabalho autorizado após a triagem. Use scans e testes proporcionais, sem alterar o projeto só para completar uma lista.

## Projeto novo

Defina objetivo, usuário, tarefa principal e restrições de stack/marca/acessibilidade. Pergunte diretamente quando uma resposta mudar a solução. Acione planejamento na definição, design na exploração, engenharia na implementação, segurança nos pontos de entrada/dados e testes na validação. Não instale todas as dependências das fontes por precaução.

Graphify e Caveman são transversais; a [política](POLITICAS.md) especifica como aplicá-los sem alegações não verificadas. As regras visuais de uma skill só entram quando combinam com intenção e identidade do produto. Use o [guia de design](DESIGN.md) para sintetizar decisões.
