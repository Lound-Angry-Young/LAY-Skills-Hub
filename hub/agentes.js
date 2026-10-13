// LAY SKILLS HUB - AGENTES GERADOS (11 ESPECIALISTAS)
window.LAY_AGENTES = [
  {
    "nome": "lay-3d",
    "dominio": "creative-3d",
    "categoria": "DESIGN & UI/UX",
    "descricao": "Especialista em 3D e efeitos gráficos: calibração de hardware para renderização, Blender (instalação e MCP), fundos Vanta, efeitos WebGL e bibliotecas criativas da web. Use quando: o pedido envolver 3D, Blender, shaders, fundos animados ou bibliotecas de efeitos visuais. Não use para: layout de página sem elemento 3D ou WebGL.",
    "ferramentas": [
      "Read",
      "Grep",
      "Glob",
      "Bash",
      "Edit",
      "Write"
    ],
    "use_quando": "o pedido envolver 3D, Blender, shaders, fundos animados ou bibliotecas de efeitos visuais",
    "nao_use_para": "layout de página sem elemento 3D ou WebGL.",
    "nao_use_para_completo": "layout de página sem elemento 3D ou WebGL.",
    "resumo": "o pedido envolver 3D, Blender, shaders, fundos animados ou bibliotecas de efeitos visuais",
    "acesso": "Edita e roda comandos",
    "skills_ativas": 6,
    "skills": [
      "calibrating-hardware-rendering",
      "configuring-blender-mcp-server",
      "installing-blender-headless",
      "integrating-creative-web-toolkits",
      "rendering-vanta-backgrounds",
      "selecting-creative-libraries"
    ],
    "fontes_upstream": [
      {
        "id": "tengbao--vanta",
        "titulo": "Vanta.js 3D WebGL Backgrounds",
        "autor": "Tengbao",
        "url": "https://github.com/tengbao/vanta"
      },
      {
        "id": "Jakubantalik--Libraries.dev",
        "titulo": "Libraries.dev Creative Hub",
        "autor": "Jakub Antalik",
        "url": "https://github.com/Jakubantalik/Libraries.dev"
      }
    ],
    "subagente_em": "Claude Code",
    "clientes_com_skills": [
      "Claude Code",
      "Codex",
      "Antigravity"
    ],
    "configurado": {
      "projeto": true,
      "projeto_caminho": ".claude/agents/lay-3d.md",
      "global_caminho": "~/.claude/agents/lay-3d.md"
    }
  },
  {
    "nome": "lay-banco-de-dados",
    "dominio": "database",
    "categoria": "OPERAÇÕES & CI/CD",
    "descricao": "Especialista em banco de dados: backup e restauração de bancos SQLite do OmniRoute e da CLI, snapshots e cache de inferência. Use quando: o pedido envolver backup, restauração, snapshot, banco corrompido ou cache de respostas do LLM. Não use para: modelagem de schema ou consultas de aplicação.",
    "ferramentas": [
      "Read",
      "Grep",
      "Glob",
      "Bash",
      "Edit",
      "Write"
    ],
    "use_quando": "o pedido envolver backup, restauração, snapshot, banco corrompido ou cache de respostas do LLM",
    "nao_use_para": "modelagem de schema ou consultas de aplicação.",
    "nao_use_para_completo": "modelagem de schema ou consultas de aplicação.",
    "resumo": "o pedido envolver backup, restauração, snapshot, banco corrompido ou cache de respostas do LLM",
    "acesso": "Edita e roda comandos",
    "skills_ativas": 5,
    "skills": [
      "backing-up-cli-data",
      "backing-up-omniroute-databases",
      "managing-inference-cache",
      "restoring-cli-snapshots",
      "restoring-omniroute-databases"
    ],
    "fontes_upstream": [],
    "subagente_em": "Claude Code",
    "clientes_com_skills": [
      "Claude Code",
      "Codex",
      "Antigravity"
    ],
    "configurado": {
      "projeto": true,
      "projeto_caminho": ".claude/agents/lay-banco-de-dados.md",
      "global_caminho": "~/.claude/agents/lay-banco-de-dados.md"
    }
  },
  {
    "nome": "lay-contexto",
    "dominio": "context",
    "categoria": "CONTEXTO & AGENTES",
    "descricao": "Especialista em contexto e planejamento: descoberta de skills, engenharia de contexto, compressão de prompts e mensagens, pipelines de contexto RTK, grafos de conhecimento do projeto, entrevista de requisitos, quebra de tarefas e refinamento de ideias. Use quando: o pedido envolver entender um projeto por grafo, planejar tarefas, levantar requisitos, economizar contexto ou comprimir prompts. Não use para: escrever código de funcionalidade.",
    "ferramentas": [
      "Read",
      "Grep",
      "Glob",
      "Bash",
      "Edit",
      "Write"
    ],
    "use_quando": "o pedido envolver entender um projeto por grafo, planejar tarefas, levantar requisitos, economizar contexto ou comprimir prompts",
    "nao_use_para": "escrever código de funcionalidade.",
    "nao_use_para_completo": "escrever código de funcionalidade.",
    "resumo": "o pedido envolver entender um projeto por grafo, planejar tarefas, levantar requisitos, economizar",
    "acesso": "Edita e roda comandos",
    "skills_ativas": 13,
    "skills": [
      "architecting-generative-ai-apps",
      "breaking-down-task-plans",
      "compressing-agent-messages",
      "configuring-prompt-compression",
      "discovering-and-invoking-skills",
      "engineering-agent-context",
      "generating-knowledge-graphs",
      "interviewing-user-requirements",
      "managing-cli-context-pipelines",
      "optimizing-rtk-prompt-contexts",
      "orchestrating-lay-ecosystem-skills",
      "refining-raw-product-ideas",
      "testing-cli-prompt-compression"
    ],
    "fontes_upstream": [],
    "subagente_em": "Claude Code",
    "clientes_com_skills": [
      "Claude Code",
      "Codex",
      "Antigravity"
    ],
    "configurado": {
      "projeto": true,
      "projeto_caminho": ".claude/agents/lay-contexto.md",
      "global_caminho": "~/.claude/agents/lay-contexto.md"
    }
  },
  {
    "nome": "lay-design",
    "dominio": "design",
    "categoria": "DESIGN & UI/UX",
    "descricao": "Especialista em design visual: geração de brandkit, mockups de telas de celular e web, referências de seções de site e consulta de sistemas de design. Use quando: o pedido envolver identidade visual, moodboard, mockups ou referências de design antes de implementar. Não use para: escrever código de interface (use lay-frontend).",
    "ferramentas": [
      "Read",
      "Grep",
      "Glob",
      "Edit",
      "Write"
    ],
    "use_quando": "o pedido envolver identidade visual, moodboard, mockups ou referências de design antes de implementar",
    "nao_use_para": "escrever código de interface (use lay-frontend).",
    "nao_use_para_completo": "escrever código de interface (use lay-frontend).",
    "resumo": "o pedido envolver identidade visual, moodboard, mockups ou referências de design antes",
    "acesso": "Edita, sem comandos",
    "skills_ativas": 4,
    "skills": [
      "consulting-design-references",
      "generating-brandkit-identities",
      "generating-mobile-ui-mockups",
      "generating-web-ui-references"
    ],
    "fontes_upstream": [
      {
        "id": "voltagent--awesome-design-md",
        "titulo": "Awesome Design MD",
        "autor": "VoltAgent",
        "url": "https://github.com/voltagent/awesome-design-md"
      }
    ],
    "subagente_em": "Claude Code",
    "clientes_com_skills": [
      "Claude Code",
      "Codex",
      "Antigravity"
    ],
    "configurado": {
      "projeto": true,
      "projeto_caminho": ".claude/agents/lay-design.md",
      "global_caminho": "~/.claude/agents/lay-design.md"
    }
  },
  {
    "nome": "lay-devops",
    "dominio": "devops",
    "categoria": "OPERAÇÕES & CI/CD",
    "descricao": "Especialista em entrega: convenções de commit, fluxo de branches e rebase, pipelines de CI, deploy contínuo, deploy na Vercel, rollouts graduais, prontidão de lançamento, releases semânticas e sincronização de dados em nuvem. Use quando: o pedido envolver commits, branches, releases, tags, pipelines de CI/CD, deploy ou lançamento. Não use para: escrever testes ou código de funcionalidade.",
    "ferramentas": [
      "Read",
      "Grep",
      "Glob",
      "Bash",
      "Edit",
      "Write"
    ],
    "use_quando": "o pedido envolver commits, branches, releases, tags, pipelines de CI/CD, deploy ou lançamento",
    "nao_use_para": "escrever testes ou código de funcionalidade.",
    "nao_use_para_completo": "escrever testes ou código de funcionalidade.",
    "resumo": "o pedido envolver commits, branches, releases, tags, pipelines de CI/CD, deploy ou lançamento",
    "acesso": "Edita e roda comandos",
    "skills_ativas": 12,
    "skills": [
      "authoring-conventional-commits",
      "automating-cd-deployments",
      "building-ci-validation-pipelines",
      "deploying-to-vercel-platform",
      "deploying-with-vercel-tokens",
      "managing-git-branch-workflows",
      "merging-validated-pull-requests",
      "optimizing-vercel-deployments",
      "orchestrating-staged-rollouts",
      "synchronizing-cloud-storage",
      "tagging-semantic-releases",
      "verifying-prelaunch-readiness"
    ],
    "fontes_upstream": [],
    "subagente_em": "Claude Code",
    "clientes_com_skills": [
      "Claude Code",
      "Codex",
      "Antigravity"
    ],
    "configurado": {
      "projeto": true,
      "projeto_caminho": ".claude/agents/lay-devops.md",
      "global_caminho": "~/.claude/agents/lay-devops.md"
    }
  },
  {
    "nome": "lay-documentacao",
    "dominio": "documentation",
    "categoria": "DOCUMENTAÇÃO",
    "descricao": "Especialista em documentação e escrita: auditoria de estilo de escrita, ADRs e registro de decisões de arquitetura, polimento de texto para leitores e remoção de marcas de proveniência de IA. Use quando: o pedido envolver revisar um texto, documentar uma decisão de arquitetura ou limpar prosa para publicação. Não use para: comentários de código ou referência de API.",
    "ferramentas": [
      "Read",
      "Grep",
      "Glob",
      "Edit",
      "Write"
    ],
    "use_quando": "o pedido envolver revisar um texto, documentar uma decisão de arquitetura ou limpar prosa para publicação",
    "nao_use_para": "comentários de código ou referência de API.",
    "nao_use_para_completo": "comentários de código ou referência de API.",
    "resumo": "o pedido envolver revisar um texto, documentar uma decisão de arquitetura ou limpar prosa",
    "acesso": "Edita, sem comandos",
    "skills_ativas": 4,
    "skills": [
      "auditing-writing-guidelines",
      "documenting-architecture-decisions",
      "polishing-user-facing-prose",
      "stripping-ai-provenance-marks"
    ],
    "fontes_upstream": [],
    "subagente_em": "Claude Code",
    "clientes_com_skills": [
      "Claude Code",
      "Codex",
      "Antigravity"
    ],
    "configurado": {
      "projeto": true,
      "projeto_caminho": ".claude/agents/lay-documentacao.md",
      "global_caminho": "~/.claude/agents/lay-documentacao.md"
    }
  },
  {
    "nome": "lay-engenharia",
    "dominio": "engineering",
    "categoria": "ENGENHARIA",
    "descricao": "Especialista em engenharia de software: desenho de APIs e interfaces, especificações, implementação incremental, code review, depuração de causa raiz, recuperação de erros, migrações, deprecações, performance full-stack, observabilidade e restrições de qualidade. Use quando: o pedido envolver arquitetura, revisão de código, depuração, refatoração, migração ou performance de aplicação. Não use para: UI visual (use lay-frontend) ou entrega e CI/CD (use lay-devops).",
    "ferramentas": [
      "Read",
      "Grep",
      "Glob",
      "Bash",
      "Edit",
      "Write"
    ],
    "use_quando": "o pedido envolver arquitetura, revisão de código, depuração, refatoração, migração ou performance de aplicação",
    "nao_use_para": "UI visual (use lay-frontend) ou entrega e CI/CD (use lay-devops).",
    "nao_use_para_completo": "UI visual (use lay-frontend) ou entrega e CI/CD (use lay-devops).",
    "resumo": "o pedido envolver arquitetura, revisão de código, depuração, refatoração, migração ou performance",
    "acesso": "Edita e roda comandos",
    "skills_ativas": 20,
    "skills": [
      "auditing-codebase-bloat",
      "authoring-specifications-first",
      "debugging-root-causes",
      "deprecating-obsolete-apis",
      "designing-apis-and-interfaces",
      "enforcing-project-constraints",
      "grounding-source-documentation",
      "guiding-ponytail-minimalism",
      "implementing-incremental-slices",
      "instrumenting-code-observability",
      "measuring-code-savings",
      "migrating-legacy-architectures",
      "minimizing-code-overengineering",
      "optimizing-fullstack-performance",
      "recovering-system-errors",
      "reviewing-code-minimalism",
      "reviewing-multi-axis-code-quality",
      "simplifying-code-complexity",
      "stress-testing-architecture-decisions",
      "tracking-technical-debt-ledgers"
    ],
    "fontes_upstream": [],
    "subagente_em": "Claude Code",
    "clientes_com_skills": [
      "Claude Code",
      "Codex",
      "Antigravity"
    ],
    "configurado": {
      "projeto": true,
      "projeto_caminho": ".claude/agents/lay-engenharia.md",
      "global_caminho": "~/.claude/agents/lay-engenharia.md"
    }
  },
  {
    "nome": "lay-frontend",
    "dominio": "frontend",
    "categoria": "DESIGN & UI/UX",
    "descricao": "Especialista em frontend de produção: interfaces React e Next.js, componentes acessíveis, animações (GSAP, Lenis, view transitions, react-bits), componentes animados dos registros Pixel-Perfect e Componentry (escolha por custo, instalação e esclarecimento de requisitos antes de gerar telas), direção visual anti-slop, responsividade e redesign de sites existentes. Use quando: o pedido envolver criar ou revisar telas, componentes, landing pages, layout ou animação de interface. Não use para: backend, APIs ou infraestrutura.",
    "ferramentas": [
      "Read",
      "Grep",
      "Glob",
      "Bash",
      "Edit",
      "Write"
    ],
    "use_quando": "o pedido envolver criar ou revisar telas, componentes, landing pages, layout ou animação de interface",
    "nao_use_para": "backend, APIs ou infraestrutura.",
    "nao_use_para_completo": "backend, APIs ou infraestrutura.",
    "resumo": "o pedido envolver criar ou revisar telas, componentes, landing pages, layout ou animação",
    "acesso": "Edita e roda comandos",
    "skills_ativas": 22,
    "skills": [
      "animating-react-bits-components",
      "animating-react-view-transitions",
      "applying-legacy-design-taste",
      "architecting-react-composition",
      "auditing-web-design-guidelines",
      "authoring-stitch-design-systems",
      "building-react-native-interfaces",
      "clarifying-screen-requirements",
      "converting-images-to-code",
      "crafting-high-end-visuals",
      "designing-industrial-brutalist-interfaces",
      "designing-minimalist-interfaces",
      "elevating-frontend-taste",
      "enforcing-full-code-output",
      "engineering-frontend-interfaces",
      "engineering-gsap-motion-uis",
      "governing-anti-slop-aesthetics",
      "integrating-external-ui-components",
      "optimizing-react-performance",
      "orchestrating-smooth-scroll",
      "redesigning-legacy-interfaces",
      "selecting-animated-ui-components"
    ],
    "fontes_upstream": [
      {
        "id": "DavidHDev--react-bits",
        "titulo": "React Bits UI FX",
        "autor": "David H. Dev",
        "url": "https://github.com/DavidHDev/react-bits"
      },
      {
        "id": "darkroomengineering--lenis",
        "titulo": "Lenis Smooth Scroll",
        "autor": "Darkroom Engineering",
        "url": "https://github.com/darkroomengineering/lenis"
      }
    ],
    "subagente_em": "Claude Code",
    "clientes_com_skills": [
      "Claude Code",
      "Codex",
      "Antigravity"
    ],
    "configurado": {
      "projeto": true,
      "projeto_caminho": ".claude/agents/lay-frontend.md",
      "global_caminho": "~/.claude/agents/lay-frontend.md"
    }
  },
  {
    "nome": "lay-omniroute",
    "dominio": "routing-and-proxy",
    "categoria": "OPERAÇÕES & CI/CD",
    "descricao": "Especialista no OmniRoute (CLI e API): inferência compatível com OpenAI, providers, combos de roteamento, proxies de rede, custos e uso, limites de gasto, resiliência, MCP, A2A, webhooks, túneis e catálogo de modelos. Use quando: o pedido envolver OmniRoute, roteamento entre modelos, providers, combos, custo por chamada, limites de gasto ou configuração do servidor OmniRoute. Não use para: código de aplicação que não usa OmniRoute.",
    "ferramentas": [
      "Read",
      "Grep",
      "Glob",
      "Bash",
      "Edit",
      "Write"
    ],
    "use_quando": "o pedido envolver OmniRoute, roteamento entre modelos, providers, combos, custo por chamada, limites de gasto ou configuração do servidor OmniRoute",
    "nao_use_para": "código de aplicação que não usa OmniRoute.",
    "nao_use_para_completo": "código de aplicação que não usa OmniRoute.",
    "resumo": "o pedido envolver OmniRoute, roteamento entre modelos, providers, combos, custo por chamada, limites",
    "acesso": "Edita e roda comandos",
    "skills_ativas": 32,
    "skills": [
      "analyzing-usage-call-logs",
      "chatting-via-omniroute-cli",
      "checking-omniroute-server-health",
      "collecting-cli-agent-skills",
      "configuring-codex-cli-proxy",
      "configuring-network-proxies",
      "configuring-omniroute-cli-setup",
      "configuring-omniroute-settings",
      "coordinating-omniroute-a2a",
      "enforcing-spending-budgets",
      "executing-omniroute-inference",
      "handling-omniroute-webhooks",
      "importing-github-agent-skills",
      "inspecting-mcp-server-cli",
      "inspecting-resilience-circuits",
      "inspecting-spending-costs-cli",
      "integrating-omniroute-mcp-server",
      "interacting-with-a2a-cli",
      "invoking-cli-tool-plugins",
      "managing-embedded-service-versions",
      "managing-omni-skills-and-memory",
      "managing-omniroute-providers",
      "managing-omniroute-server-daemon",
      "managing-providers-via-cli",
      "managing-routing-combos-cli",
      "managing-tunnels-via-cli",
      "monitoring-omniroute-resilience",
      "querying-models-via-cli",
      "querying-omniroute-models",
      "routing-omniroute-combos",
      "submitting-batch-inference-jobs",
      "tunneling-omniroute-endpoints"
    ],
    "fontes_upstream": [],
    "subagente_em": "Claude Code",
    "clientes_com_skills": [
      "Claude Code",
      "Codex",
      "Antigravity"
    ],
    "configurado": {
      "projeto": true,
      "projeto_caminho": ".claude/agents/lay-omniroute.md",
      "global_caminho": "~/.claude/agents/lay-omniroute.md"
    }
  },
  {
    "nome": "lay-qa",
    "dominio": "qa",
    "categoria": "TESTES & QUALIDADE",
    "descricao": "Especialista em qualidade e testes: TDD, automação de browser e Playwright, inspeção com DevTools, conformidade de componentes animados (imports, movimento reduzido, WebGL por rota, licença), benchmarks de modelos, varredura de qualidade do código, gates de release e reparo de CI e de pull requests. Use quando: o pedido envolver testes, cobertura, falhas de CI, validação antes de merge, conferência de componente animado ou benchmarks. Não use para: implementar funcionalidades sem foco em teste.",
    "ferramentas": [
      "Read",
      "Grep",
      "Glob",
      "Bash",
      "Edit",
      "Write"
    ],
    "use_quando": "o pedido envolver testes, cobertura, falhas de CI, validação antes de merge, conferência de componente animado ou benchmarks",
    "nao_use_para": "implementar funcionalidades sem foco em teste.",
    "nao_use_para_completo": "implementar funcionalidades sem foco em teste.",
    "resumo": "o pedido envolver testes, cobertura, falhas de CI, validação antes de merge, conferência",
    "acesso": "Edita e roda comandos",
    "skills_ativas": 9,
    "skills": [
      "automating-browser-tests",
      "driving-test-driven-development",
      "enforcing-green-pull-requests",
      "evaluating-model-benchmarks",
      "scanning-codebase-quality",
      "sweeping-failing-ci-builds",
      "testing-in-browser-with-devtools",
      "validating-green-release-gates",
      "verifying-animated-component-compliance"
    ],
    "fontes_upstream": [],
    "subagente_em": "Claude Code",
    "clientes_com_skills": [
      "Claude Code",
      "Codex",
      "Antigravity"
    ],
    "configurado": {
      "projeto": true,
      "projeto_caminho": ".claude/agents/lay-qa.md",
      "global_caminho": "~/.claude/agents/lay-qa.md"
    }
  },
  {
    "nome": "lay-seguranca",
    "dominio": "security",
    "categoria": "SEGURANÇA & SCAN",
    "descricao": "Especialista em segurança: auditoria de código, hardening de aplicações, Semgrep, varredura de dependências e CVEs, chaves e sessões de API, segurança de aplicações com LLM e políticas de acesso. Use quando: o pedido envolver vulnerabilidades, auditoria, segredos, autenticação, chaves de API ou varredura de segurança. Não use para: implementar funcionalidades sem foco em segurança. Este perfil só lê e analisa; não edita arquivos.",
    "ferramentas": [
      "Read",
      "Grep",
      "Glob",
      "Bash"
    ],
    "use_quando": "o pedido envolver vulnerabilidades, auditoria, segredos, autenticação, chaves de API ou varredura de segurança",
    "nao_use_para": "implementar funcionalidades sem foco em segurança. Este perfil só lê e analisa; não edita arquivos.",
    "nao_use_para_completo": "implementar funcionalidades sem foco em segurança. Este perfil só lê e analisa; não edita arquivos.",
    "resumo": "o pedido envolver vulnerabilidades, auditoria, segredos, autenticação, chaves de API ou varredura",
    "acesso": "Não edita · tem Bash",
    "skills_ativas": 9,
    "skills": [
      "auditing-access-policies",
      "auditing-code-security",
      "authenticating-api-sessions",
      "hardening-application-security",
      "managing-api-keys",
      "managing-cli-keys",
      "scanning-code-with-semgrep",
      "scanning-dependency-vulnerabilities",
      "securing-llm-applications"
    ],
    "fontes_upstream": [],
    "subagente_em": "Claude Code",
    "clientes_com_skills": [
      "Claude Code",
      "Codex",
      "Antigravity"
    ],
    "configurado": {
      "projeto": true,
      "projeto_caminho": ".claude/agents/lay-seguranca.md",
      "global_caminho": "~/.claude/agents/lay-seguranca.md"
    }
  }
];
