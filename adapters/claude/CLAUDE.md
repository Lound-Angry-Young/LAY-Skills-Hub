<!-- LAY-SKILLS:BEGIN -->
## LAY Skills — instruções globais

No primeiro uso de cada projeto, antes de editar, execute o diagnóstico abaixo. Ele consulta primeiro o repositório pai e depois as fontes. O cache evita repetir a rede; `--refresh` força nova consulta. Se indisponível, informe a limitação e siga com o catálogo local.

`"{{PYTHON_EXE}}" "{{LAY_RUNTIME_DIR}}\scripts\skill_hub.py" start --home "{{USER_HOME}}" --project "CAMINHO_DO_PROJETO"`

No PowerShell, prefixe o comando por `&`. Substitua CAMINHO_DO_PROJETO pelo diretório atual; use argumentos separados.

Graphify sempre orienta a navegação: consulte o grafo existente antes de alterações estruturais; valide achados nos arquivos. Se ausente, informe e use inventário local provisório, sem inventar execução do Graphify. Caveman sempre: português direto, uma questão por vez, sem perder precisão, negações ou limitações. Peça contexto apenas quando faltar informação que mude a decisão. Em projeto existente, mostre prioridades e evidências antes de editar. Em projeto novo, ative skills conforme a etapa. Não imponha stack ou estética herdada.

Leia `{{LAY_RUNTIME_DIR}}\skills\lay-orchestrator\SKILL.md` para orquestração e `{{LAY_RUNTIME_DIR}}\docs\GUIA.md` para seleção. Busque por área com `python "{{LAY_RUNTIME_DIR}}\scripts\skill_hub.py" search design`. Não carregue o catálogo inteiro no contexto. As instruções do usuário e do projeto definem o escopo.

## Subagentes LAY (Claude Code)

Subagentes globais em ~/.claude/agents. Escolha pelo domínio do pedido e delegue. Subagentes não chamam outros subagentes: o roteamento é desta conversa.

- routing-and-proxy: `lay-omniroute`
- frontend: `lay-frontend`
- engineering: `lay-engenharia`
- context: `lay-contexto`
- devops: `lay-devops`
- qa: `lay-qa`
- security: `lay-seguranca`
- creative-3d: `lay-3d`
- documentation: `lay-documentacao`
- design: `lay-design`
- database: `lay-banco-de-dados`

Graphify CLI isolada: `{{USER_HOME}}\.lay-skills\tools\graphify\Scripts\graphify.exe`. Use o executável por caminho absoluto quando não estiver no PATH.
<!-- LAY-SKILLS:END -->

## Preservação de Cota e Eficiência de Tokens (Regra Global Claude Code)
1. **Modelo Padrão Obrigatório**: Claude Code opera por padrão em **`Sonnet`** (`claude-sonnet-5-5`). O uso de `Opus` (`claude-opus-5-5`) é **estritamente proibido** para loops autônomos, execução contínua de ferramentas, edição de código ordinária ou leitura de logs. O Opus só é liberado sob solicitação explícita do usuário para validação arquitetural crítica.
2. **Compactação Obrigatória (`/compact`)**:
   - Execute `/compact` sempre que mudar de tarefa, fechar um ciclo de prompt ou quando a sessão ultrapassar 30 tool calls.
   - Nunca continue acumulando contexto em sessões longas (>50k tokens) sem compactar, pois isso reduz drasticamente o teto de mensagens da janela de 5 horas.
3. **Delegação de Tarefas Mecânicas**:
   - Inventários, renomeação em massa, busca por regex, extração de dados e checagens repetitivas de arquivos DEVEM ser delegados ao Antigravity (`Gemini 3.8 Flash`) via CLI `agy` ou executados via `Haiku`.
4. **Controle Estrito de Subagentes**:
   - Não dispare subagentes em segundo plano para tarefas simples que podem ser resolvidas com um script rápido local. Evite acumular subagentes paralelos consumindo cota simultânea.
   - Teto de concorrência: 1 orquestrador + no máximo 2 workers de alta capacidade + 3 workers rápidos, só em tarefas independentes. Todo subagente recebe um pacote de tarefa (`task_id`, objetivo, arquivos permitidos, saída exata, critério de parada), nunca o histórico.
   - **Respeito ao Modelo Declarado do Especialista:** Ao invocar a ferramenta `Agent`, NUNCA passe o parâmetro `model` de forma automática. Deixe o parâmetro `model` ausente para que o Claude Code utilize o modelo padrão definido no frontmatter YAML do especialista (`lay-frontend` em Sonnet, `lay-documentacao` em Haiku, etc.). Não propague o modelo da sessão principal (ex: Haiku via settings.json) para o subagente.
   - **Substituição Autorizada (Override):** Transmita o parâmetro `model` na chamada `Agent` exclusivamente quando o usuário solicitar expressamente (ex: *"use haiku para lay-frontend"*).
   - **Natureza Comportamental:** Esta instrução é comportamental no prompt do orquestrador; a ferramenta `Agent` não possui trava técnica no runtime contra preenchimento do parâmetro.
5. **Sessão curta (auditoria de 2026-10-31)**: janela de 200k, nunca a variante de 1M. Uma etapa do `TASKS.md` por sessão; ao fechar, handoff de até uma página e sessão nova. `/compact` é contingência dentro da tarefa, não licença para sessão infinita. Alerta: contexto acima de ~150k, ou mais de 5 subagentes vivos.
6. **Opus só como árbitro**: pelo subagente `lay-arbitro-opus` (1 turno, contexto novo, pacote ≤ 15k tokens). Nunca na thread principal. Todo agente `lay-*` tem `model:` explícito (Sonnet ou Haiku).
7. **Script antes de LLM**: inventário, hash, recorte, renomeação e contagem rodam em script local. Codex (Sol/Terra/Luna) e Antigravity (Flash high/medium/low) conforme `docs/nossa-cultura/00-visao-geral-e-arquitetura/PIPELINE-ORQUESTRACAO.md` do projeto Nossa Cultura. Primeiro aviso de cota: parar, registrar, seguir só com o local.

<!-- LAY-MANAGED:END -->
