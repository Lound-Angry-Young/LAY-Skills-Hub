<!-- LAY-SKILLS:BEGIN -->
## LAY Skills — instruções globais

No primeiro uso de cada projeto, antes de editar, execute o diagnóstico abaixo. Ele consulta primeiro o repositório pai e depois as fontes. O cache evita repetir a rede; `--refresh` força nova consulta. Se indisponível, informe a limitação e siga com o catálogo local.

`"{{PYTHON_EXE}}" "{{LAY_RUNTIME_DIR}}\scripts\skill_hub.py" start --home "{{USER_HOME}}" --project "CAMINHO_DO_PROJETO"`

No PowerShell, prefixe o comando por `&`. Substitua CAMINHO_DO_PROJETO pelo diretório atual; use argumentos separados.

Graphify sempre orienta a navegação: consulte o grafo existente antes de alterações estruturais; valide achados nos arquivos. Se ausente, informe e use inventário local provisório, sem inventar execução do Graphify. Caveman sempre: português direto, uma questão por vez, sem perder precisão, negações ou limitações. Peça contexto apenas quando faltar informação que mude a decisão. Em projeto existente, mostre prioridades e evidências antes de editar. Em projeto novo, ative skills conforme a etapa. Não imponha stack ou estética herdada.

Leia `{{LAY_RUNTIME_DIR}}\skills\lay-orchestrator\SKILL.md` para orquestração e `{{LAY_RUNTIME_DIR}}\docs\GUIA.md` para seleção. Busque por área com `python "{{LAY_RUNTIME_DIR}}\scripts\skill_hub.py" search design`. Não carregue o catálogo inteiro no contexto. As instruções do usuário e do projeto definem o escopo.

Graphify CLI isolada: `{{USER_HOME}}\.lay-skills\tools\graphify\Scripts\graphify.exe`. Use o executável por caminho absoluto quando não estiver no PATH.
<!-- LAY-SKILLS:END -->

## Diretrizes Gerais de Engenharia e Qualidade (Antigravity)

### 1. Engenharia, Escopo e Neutralidade
- **Mudanças Mínimas:** Modifique estritamente o necessário para atender ao objetivo. Não faça refatorações cosméticas em código alheio ao pedido.
- **Preservação Arquitetural:** Mantenha convenções, dependências, rotas e padrões vigentes no projeto.
- **Neutralidade de Fornecedor:** Utilize exclusivamente recursos e modelos nativos do Antigravity (família Gemini). É vedado convocar APIs ou modelos de outros fornecedores (Anthropic, OpenAI) sem autorização expressa.
- **Salvaguardas de Execução:** Solicite confirmação humana explícita antes de comandos destrutivos (remoção de arquivos, resets de git), deploy ou publicação externa. *(Nota: Esta é uma diretriz de conduta do agente; os controles técnicos de execução dependem da configuração de permissões da IDE).*

### 2. Qualidade Visual e Identidade do Projeto
- **Anti-Slop Universal:** Evite padrões genéricos de IA (gradientes roxo/azul padrão, cards flutuantes idênticos, `rounded-2xl` indiscriminado e falta de hierarquia). Use escala tipográfica intencional, contraste semântico e espaçamento consistente.
- **Acessibilidade e Estados:** Assegure contraste mínimo WCAG AA (4.5:1 texto regular, 3:1 componentes), navegação por teclado (`focus-visible`), estados interativos (`hover`, `active`, `disabled`) e suporte a `prefers-reduced-motion`.
- **Respeito à Identidade:** O design deve obedecer à marca, referências e design system do projeto alvo. Não imponha a estética brutalista ou cores da marca LAY em projetos de terceiros.

### 3. Ativação Proporcional de Skills (Progressive Disclosure)
- **Telas Novas e Redesigns:** Ao planejar ou criar telas e componentes visuais substanciais, consulte a skill pertinente (`elevating-frontend-taste` para direção visual/tipografia, `governing-anti-slop-aesthetics` para revisão anti-clichê, ou `engineering-frontend-interfaces` para arquitetura de componentes).
- **Ajustes Pontuais:** Em correções de bugs, pequenas alterações de estilo ou ajustes em componentes existentes, não carregue skills completas desnecessariamente; aplique diretamente os princípios de consistência, contraste e acessibilidade.
- **Procedimentos nas Skills:** Regras globais guardam apenas princípios inegociáveis. Guias passo a passo, matrizes e referências detalhadas permanecem dentro dos arquivos de skill.
- **Extensibilidade e Novas Skills:** Consulte `{{LAY_RUNTIME_DIR}}\docs\EXTENSIBILIDADE.md` para adicionar, integrar ou regenerar skills e subagentes nativos do Antigravity.

<!-- LAY-MANAGED:END -->
