# Graphify — Knowledge Graph Determinístico para Codebases

> **Regra de Ouro da Arquitetura:** Toda análise, planejamento de refatoração ou busca por dependências deve passar pelo Graphify antes de qualquer modificação de código. O grafo fornece uma visão determinística da AST sem custos de vetorização e sem alucinações de LLM.

---

## 1. O que é o Graphify?

O **Graphify** (`graphifyy`) é uma ferramenta que analisa o código-fonte (TypeScript, JavaScript, Python, Rust, Go, etc.), documentos e arquivos de configuração, gerando um **Grafo de Conhecimento** persistente com:
- **Detecção de Comunidades (Algoritmo de Leiden):** Agrupa subsistemas do projeto de forma natural e desacoplada.
- **Identificação de God Nodes:** Descobre automaticamente quais funções, componentes ou módulos concentram a maior quantidade de conexões no sistema.
- **Rastreamento de Menor Caminho (*Shortest Path*):** Mapeia o fluxo exato de dados ou chamadas entre duas pontas do sistema (ex: do `Hero` até `createSuccao`).
- **Visualizador D3 Interativo Standalone:** Gera um arquivo HTML autocontido (`graph.html`) para exploração visual em 2D/3D com busca, filtros por comunidade e inspeção de nós.

---

## 2. Como o Graphify foi Integrado ao Projeto ("Por Fora")

O Graphify é mantido como uma ferramenta **estritamente externa e isolada**. Ele nunca é importado como dependência do frontend (Next.js/React) e não possui rotas no site final.

### Estrutura de Pastas e Arquivos

```
seu-projeto/
├── .graphifyignore               # Ignora diretórios pesados ou irrelevantes
├── tools/
│   └── graphify/                 # Repositório clonado ou Submódulo Git
├── graphify-out/                 # Diretório gerado com os artefatos do grafo
│   ├── graph.json                # Grafo completo com nós, arestas e métricas
│   ├── graph.html                # Visualizador visual interativo standalone
│   ├── GRAPH_REPORT.md           # Relatório textual com comunidades e god nodes
│   └── .graphify_python          # Cache do interpretador Python utilizado
└── skills/
    └── graphify/
        └── SKILL.md              # Instruções operacionais completas para a IA
```

---

## 3. Passo a Passo de Instalação e Configuração em Novo Projeto

### Passo 1: Instalação do Pacote Python

O Graphify pode ser instalado globalmente ou em ambiente virtual:

```bash
# Via pip
pip install graphifyy

# Ou via uv (recomendado para performance)
uv tool install graphifyy
```

### Passo 2: Adicionar como Submódulo Git (Opcional, para versionamento do código-fonte da ferramenta)

```bash
git submodule add https://github.com/Graphify-Labs/graphify.git tools/graphify
```

### Passo 3: Criação do Arquivo `.graphifyignore`

Crie um arquivo `.graphifyignore` na raiz do projeto para evitar que o parser varra pastas de dependências compiladas ou ferramentas auxiliares:

```gitignore
tools/
tools/**
graphify-out/
graphify-out/**
.next/
.next/**
node_modules/
node_modules/**
public/graphify/
public/graphify/**
dist/
build/
coverage/
```

### Passo 4: Isolamento no TypeScript, ESLint e Prettier

Para que o Next.js, o TypeScript e o Linter não tentem compilar ou formatar os arquivos internos do Graphify em `tools/` ou `graphify-out/`:

1. **`tsconfig.json`**:
   ```json
   {
     "exclude": ["node_modules", "tools", "graphify-out"]
   }
   ```

2. **`eslint.config.mjs`**:
   ```javascript
   globalIgnores([
     "tools/**",
     "graphify-out/**",
     ".next/**",
     "node_modules/**"
   ])
   ```

3. **`.prettierignore`**:
   ```
   tools
   graphify-out
   .next
   node_modules
   ```

### Passo 5: Script no `package.json`

Adicione o script padronizado na seção `scripts` do `package.json`:

```json
{
  "scripts": {
    "graphify": "python -m graphify extract . --code-only && python -m graphify cluster-only . && python -m graphify export html"
  }
}
```

---

## 4. Comandos Essenciais para o Agente e Desenvolvedor

### 1. Construir ou Atualizar o Grafo

```bash
# Executa extração, clusterização e exportação do HTML
pnpm graphify

# Ou diretamente via módulo Python:
python -m graphify extract . --code-only
python -m graphify cluster-only .
python -m graphify export html
```

### 2. Responder Dúvidas de Arquitetura (Query)

Em vez de fazer `grep` ou buscar arquivos aleatórios, pergunte ao grafo:

```bash
python -m graphify query "Como os componentes de UI acessam o tema global?"
python -m graphify query "Onde o estado de autenticação é manipulado?"
```

### 3. Encontrar a Rota entre Dois Componentes (Path)

Descubra como dois pontos do sistema se conectam:

```bash
python -m graphify path "Header" "ThemeToggle"
python -m graphify path "PaginaInicial" "BancoDeDados"
```

### 4. Explicar um Nó Central / Símbolo (Explain)

Analisa todas as dependências diretas, quem consome e métricas de centralidade do nó:

```bash
python -m graphify explain "useAuth"
python -m graphify explain "ApiClient"
```

### 5. Abrir o Visualizador Gráfico

Abra o arquivo gerado diretamente no navegador (não precisa de servidor web):
- Caminho: `graphify-out/graph.html`
- Ou utilize a flag `--serve` caso prefira visualização com hot-reload local:
  ```bash
  python -m graphify serve
  ```

---

## 5. Como o Agente de IA Deve Usar o Graphify

1. **Fast-path:** Se `graphify-out/graph.json` existir no projeto, qualquer pergunta técnica de arquitetura deve rodar primeiro um `python -m graphify query "<pergunta>"`.
2. **Impact Analysis:** Antes de renomear ou refatorar uma função crítica, rode `python -m graphify explain "<Simbolo>"` para saber exatamente todos os arquivos que serão afetados.
3. **Pós-refatoração:** Sempre que novos módulos forem adicionados ou rotas criadas, rode `pnpm graphify` para sincronizar o grafo.
