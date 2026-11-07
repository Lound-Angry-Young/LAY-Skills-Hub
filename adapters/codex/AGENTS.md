<!-- LAY-SKILLS:BEGIN -->
## LAY Skills — instruções globais

No primeiro uso de cada projeto, antes de editar, execute o diagnóstico abaixo. Ele consulta primeiro o repositório pai e depois as fontes. O cache evita repetir a rede; `--refresh` força nova consulta. Se indisponível, informe a limitação e siga com o catálogo local.

`"{{PYTHON_EXE}}" "{{LAY_RUNTIME_DIR}}\scripts\skill_hub.py" start --home "{{USER_HOME}}" --project "CAMINHO_DO_PROJETO"`

No PowerShell, prefixe o comando por `&`. Substitua CAMINHO_DO_PROJETO pelo diretório atual; use argumentos separados.

Graphify sempre orienta a navegação: consulte o grafo existente antes de alterações estruturais; valide achados nos arquivos. Se ausente, informe e use inventário local provisório, sem inventar execução do Graphify. Caveman sempre: português direto, uma questão por vez, sem perder precisão, negações ou limitações. Peça contexto apenas quando faltar informação que mude a decisão. Em projeto existente, mostre prioridades e evidências antes de editar. Em projeto novo, ative skills conforme a etapa. Não imponha stack ou estética herdada.

Leia `{{LAY_RUNTIME_DIR}}\skills\lay-orchestrator\SKILL.md` para orquestração e `{{LAY_RUNTIME_DIR}}\docs\GUIA.md` para seleção. Busque por área com `python "{{LAY_RUNTIME_DIR}}\scripts\skill_hub.py" search design`. Não carregue o catálogo inteiro no contexto. As instruções do usuário e do projeto definem o escopo.

Graphify CLI isolada: `{{USER_HOME}}\.lay-skills\tools\graphify\Scripts\graphify.exe`. Use o executável por caminho absoluto quando não estiver no PATH.
<!-- LAY-SKILLS:END -->

<!-- LAY-PIPELINE:BEGIN -->
## Pipeline de cota (Codex)

Perfis:
- `sol` (`gpt-6.1-sol`, high): refatoração pesada, decisões arquiteturais críticas e auditoria profunda.
- `terra` (`gpt-6.1-terra`, medium, padrão): engenharia de componentes, testes (Vitest/Playwright), fixtures e migrações.
- `luna` (`gpt-6-luna`, low): tarefas mecânicas rápidas, formatação, extração simples e checagens pontuais.
- `astra`: apenas sob autorização explícita do usuário.

O sandbox executa `node`, `npm` e `git`. O Python de `AppData\Local\Programs` é bloqueado internamente no sandbox do Codex: execute testes Node/TypeScript aqui, e utilize ambientes com Python nativo quando necessário.
Receba sempre um pacote de tarefa (`task_id`, objetivo, arquivos permitidos, saída exata, critério de parada). Não explore o repositório além dos arquivos estritamente citados no pacote. Ao primeiro aviso de cota: interrompa e relate.
<!-- LAY-PIPELINE:END -->

## Diretrizes Gerais de Engenharia e Qualidade (Codex)

### 1. Engenharia, Escopo e Salvaguardas
- **Mudanças Mínimas:** Modifique estritamente o necessário para atender ao objetivo. Não faça refatorações cosméticas em código alheio ao pedido.
- **Preservação Arquitetural:** Mantenha convenções, dependências, rotas e padrões vigentes no projeto alvo.
- **Isolamento de Fornecedor:** Não invoque nem execute modelos de outros fornecedores. Opere dentro do runtime nativo do Codex.
- **Salvaguardas de Execução:** Solicite confirmação humana explícita antes de comandos destrutivos (remoção de arquivos, resets de git), deploy ou publicação externa.

### 2. Qualidade Visual e Identidade do Projeto (Anti-Slop Universal)
- **Anti-Slop Universal:** Evite padrões genéricos de IA (gradientes roxo/azul padrão, cards flutuantes idênticos, `rounded-2xl` indiscriminado e ausência de hierarquia). Use escala tipográfica intencional, contraste semântico e espaçamento consistente.
- **Acessibilidade e Estados:** Assegure contraste mínimo WCAG AA (4.5:1 texto regular, 3:1 componentes), navegação por teclado (`focus-visible`), estados interativos (`hover`, `active`, `disabled`) e suporte a `prefers-reduced-motion`.
- **Respeito à Identidade:** O design deve obedecer à marca, referências e design system do projeto alvo. Não imponha estética brutalista herdada em projetos de terceiros.

<!-- LAY-MANAGED:END -->
