# Diretrizes Gerais de Agente — [NOME DO PROJETO]

> **REGRA DE OURO (GRAPHIFY):** Tudo o que a IA for planejar, executar ou analisar DEVE passar pelo Graphify. Este é o fluxo oficial e o melhor caminho para o projeto.
>
> **REGRA OBRIGATÓRIA:** Toda alteração de código, nova geração ou mudança arquitetural deve ser registrada neste arquivo de contexto para manter o projeto atualizado.

---

## 1. Visão Geral e Princípios Fundamentais

- **Projeto:** [Nome do Projeto]
- **Missão:** [Descrever o propósito central do projeto]
- **Filosofia de Código:**
  - **Zero Dependências Supérfluas:** Modularidade e controle estrito do bundle.
  - **Acessibilidade e Desempenho:** Contraste WCAG AA, suporte a `prefers-reduced-motion`.
  - **Qualidade Contínua:** Cobertura de testes unitários e E2E com asserção real de interface no DOM.

---

## 2. A Regra de Ouro: Fluxo Oficial com Graphify

Antes de qualquer implementação ou refatoração, consulte o Graphify:

```bash
# Perguntas de fluxo
python -m graphify query "Onde os dados do usuário são processados?"

# Conexão entre módulos
python -m graphify path "ComponenteA" "ComponenteB"

# Inspeção de nós centrais
python -m graphify explain "NomeDoModulo"

# Atualização pós-alterações
pnpm graphify
```

---

## 3. Stack Tecnológica e Dependências

| Camada | Ferramenta | Versão | Função no Projeto |
| :--- | :--- | :--- | :--- |
| **Framework Web** | Next.js (App Router) | `^16.0` | Renderização, rotas e otimização de fontes |
| **UI Library** | React & React-DOM | `^19.0` | Componentes funcionais e hooks |
| **Linguagem** | TypeScript | `^5.0` | Tipagem estrita (`strict: true`) |
| **Testes Unitários** | Vitest & Testing Library | `^5.0` / `^16.0` | Testes de unidade e componentes |
| **Testes E2E** | Playwright | `^1.40` | Testes de fumaça multi-device |
| **Qualidade & Lint** | ESLint & Prettier | `^9.0` / `^3.0` | Padrões de código e formatação |
| **Knowledge Graph** | Graphify (`graphifyy`) | Recente | Parsing AST e grafo determinístico |

---

## 4. Estrutura de Diretórios Recomendada

```
projeto/
├── AGENTS.md                 # Regras gerais para todos os agentes
├── CLAUDE.md                 # Contexto de operação para Claude Code
├── agent.md                  # Este arquivo mestre
├── .graphifyignore          # Exclusões do Graphify
├── skills/                  # Skills operacionais da IA
│   ├── README.md
│   ├── graphify/SKILL.md
│   ├── quality/SKILL.md
│   ├── taste/SKILL.md
│   ├── impeccable/SKILL.md
│   ├── ui-ux-pro/SKILL.md
│   └── caveman/SKILL.md
├── tools/                   # Ferramentas externas isoladas (submódulos)
│   └── graphify/
├── graphify-out/            # Artefatos locais gerados pelo Graphify
├── src/
│   ├── app/                 # Páginas e rotas (App Router)
│   ├── components/          # Componentes reutilizáveis
│   ├── lib/                 # Utilitários, hooks e store
│   ├── locales/             # Arquivos de internacionalização (i18n)
│   └── styles/
│       └── tokens.css       # Design Tokens oficiais
└── e2e/                     # Testes ponta a ponta Playwright
```

---

## 5. Histórico e Registro de Alterações Arquiteturais

| Data | Agente / Autor | Descrição da Alteração |
| :--- | :--- | :--- |
| YYYY-MM-DD | Nome / Agente | Inicialização do repositório base com esteira de testes e Graphify. |
