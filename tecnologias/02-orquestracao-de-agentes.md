# Orquestração e Governança de Agentes de IA

> **Propósito:** Definir o padrão de orquestração, regras comportamentais inegociáveis e hierarquia de contexto para que múltiplos agentes de IA (Antigravity, Claude Code, Codex, Cursor, etc.) operem com máxima precisão, sem alucinações e com rastreabilidade total.

---

## 1. Arquitetura de Arquivos de Contexto

Para que os agentes entendam o projeto sem necessidade de re-explicar regras a cada prompt, adota-se uma **arquitetura em 4 camadas de contexto**:

```
seu-projeto/
├── AGENTS.md             # Camada 1: Regras universais de ambiente e Golden Rules
├── CLAUDE.md             # Camada 2: Diretrizes operacionais e Changelog contínuo
├── agent.md              # Camada 3: Arquitetura completa, Stack, God Nodes e Decisões
├── claude-agent.md       # Camada 4: Diretrizes especializadas e boas práticas de runtime
└── skills/               # Camada Operacional: Habilidades executáveis sob demanda
    ├── README.md         # Catálogo de skills
    ├── [skill-name]/
    │   └── SKILL.md      # Instrução executável com frontmatter YAML
```

---

## 2. As Regras de Ouro Inegociáveis

### Regra de Ouro 1: Análise Determinística via Graphify
- **Proibição:** O agente não deve fazer buscas cegas por texto (`grep` indiscriminado) ou presumir relações entre arquivos.
- **Obrigação:** Toda análise arquitetural, refatoração de símbolos ou mapeamento de dependências deve ser consultada via Graphify (`python -m graphify query/path/explain`).

### Regra de Ouro 2: Verificação de UI Anti-Negligência
> Essa regra surgiu para eliminar o padrão preguiçoso de agentes onde o teste unitário passa no terminal, mas a interface do usuário continua quebrada ou estática.

1. **Proibição de testes superficiais:**
   - É **estritamente proibido** aprovar uma funcionalidade de UI avaliando apenas variáveis internas, `localStorage`, `sessionStorage`, estados de componentes ou chamadas de mock.
2. **Obrigatoriedade de asserção visual no DOM real:**
   - Todo teste unitário (Vitest + React Testing Library) ou E2E (Playwright) deve obrigatoriamente validar a mutação de nós de texto visíveis aos olhos do usuário final (ex: elementos de texto trocando no DOM).
3. **Verificação bidirecional:**
   - Em alternâncias de estado (ex: seletor de idiomas `PT-BR ↔ EN`, som `ON ↔ OFF`, tema `Light ↔ Dark`), deve-se testar a ida e a volta completa para garantir que o ciclo de reatividade não quebra ao retornar ao estado inicial.

### Regra de Ouro 3: Registro Contínuo no Changelog
- Toda e qualquer alteração de código, adição de biblioteca, ajuste de layout ou decisão arquitetural deve ser registrada no histórico em tabela nos arquivos de contexto (`CLAUDE.md` e `agent.md`).
- Formato:
  ```markdown
  | Data | Autor | Resumo da Alteração |
  | :--- | :---- | :------------------ |
  | YYYY-MM-DD | Agente / Nome | Descrição técnica com componentes e arquivos afetados |
  ```

---

## 3. Estrutura do Sistema de Skills

O diretório `skills/` padroniza ações repetitivas e diretrizes especializadas. Cada skill é auto-contida em sua respectiva subpasta:

```
skills/
├── README.md
├── graphify/SKILL.md      # Navegação do grafo de dependências e queries AST
├── quality/SKILL.md       # Roteiro de qualidade e checagem de sanidade (test/lint/build)
├── taste/SKILL.md         # Diretrizes de design anti-slop e personalidade visual
├── impeccable/SKILL.md    # Auditoria de craft, contraste e acessibilidade WCAG
├── ui-ux-pro/SKILL.md     # Ergonomia de UI, padrões interativos e mobile-first
└── caveman/SKILL.md       # Modo ultra-comprimido para economia de 65-75% de tokens
```

### Formato Padrão de um `SKILL.md`

Todo arquivo de skill deve começar com **frontmatter YAML**:

```yaml
---
name: nome-da-skill
description: "Descrição clara e concisa indicando quando e por que o agente deve usar esta habilidade."
---

# Nome da Skill

Contexto, diretrizes e comandos operacionais...
```

---

## 4. Pipeline de Sanidade Pré-Conclusão

Nenhuma tarefa pode ser considerada concluída pelo agente sem a execução e aprovação do pipeline de sanidade em cascata:

```bash
# 1. Testes Unitários de Componentes e Funções
pnpm test

# 2. Checagem Estática de Tipos (TypeScript + Rotas)
pnpm typecheck

# 3. Linter Estrito (0 erros e 0 warnings)
pnpm lint

# 4. Verificação de Formatação de Código
pnpm format:check

# 5. Build Estático de Produção
pnpm build

# 6. Testes End-to-End contra o Build Real
pnpm test:e2e
```
