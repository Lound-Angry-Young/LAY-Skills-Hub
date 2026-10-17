// =============================================================================
// LAY® SKILLS HUB — INTERNATIONALIZATION (i18n) & AUDIO ENGINE
// Inspirado na arquitetura do Portifolio-LAY (DECISIONS #32 e #61).
// Compatível 100% com GitHub Pages, navegação estática e modo offline.
// =============================================================================
(function (global) {
  'use strict';

  var LOCALE_KEY = 'lay:locale';
  var DEFAULT_LOCALE = 'pt-BR';
  var SUPPORTED_LOCALES = ['pt-BR', 'en'];

  var TRANSLATIONS = {
    'pt-BR': {
      // Top Ticker & Header
      'lang.title': 'IDIOMA / LANGUAGE',
      'header.sub': 'Repertório central de capacidades & regras para agentes',
      'header.skills_label': 'skills',
      'header.skip_link': 'Ir para o conteúdo',
      'ticker.items': 'skills no catálogo',
      'ticker.specialists': 'subagentes por domínio',
      'ticker.sources': 'fontes upstream',
      'ticker.clients': 'Antigravity • Codex • Claude Code',
      'ticker.creative': 'Vanta 3D • React Bits • Lenis Smooth Scroll • Libraries.dev',

      // Hero
      'hero.badge': 'Arquitetura modular • evidências determinísticas',
      'hero.title': 'Ecossistema total <span class="destaque-amarelo">de skills de agentes</span> <span class="destaque-magenta">Pernambuco → mundo</span>',
      'hero.impact': 'Skills construídas com componentes de última geração e alta performance.',
      'hero.intro': 'Hub visual interativo reunindo capacidades especializadas e fontes de referência de elite mundial: orquestração central de agentes (<strong class="nome">lay-orchestrator</strong>, <strong class="nome">Caveman</strong>, <strong class="nome">Graphify</strong>), referências de ponta (<strong class="nome">Addy Osmani</strong>, <strong class="nome">Vercel Labs</strong>, <strong class="nome">Semgrep</strong>, <strong class="nome">Playwright</strong>) e bibliotecas criativas (<strong class="nome">Vanta 3D</strong>, <strong class="nome">React Bits</strong>, <strong class="nome">Lenis Smooth Scroll</strong> e <strong class="nome">Libraries.dev</strong>). Inspecione códigos, copie prompts individuais e gere arquiteturas completas sob medida.',
      'hero.stat_skills': 'skills',
      'hero.stat_sources': 'fontes upstream',
      'hero.stat_specialists': 'especialistas',
      'hero.btn_master_prompt': 'Copiar prompt mestre',
      'hero.btn_install': 'Instalar subagentes',
      'hero.btn_github': 'Repositório GitHub',

      // Especialistas
      'specialists.kicker': 'ESPECIALISTAS AUTÔNOMOS • CLAUDE CODE & ECOSSISTEMA',
      'specialists.title': 'Subagentes do Claude Code',
      'specialists.lead': '18 especialistas pré-configurados com ferramentas restritas, gatilhos de ativação estritos e skills mapeadas. Selecione um especialista no grid para ver suas fontes, capacidades e o comando direto de ativação.',
      'specialists.subagents_page': 'Página de subagentes',
      'specialists.prompts_to_copy': 'Prompts para copiar',
      'specialists.see_others': 'Ver os outros',
      'pad.copy_cmd': 'Copiar Instrução de Ativação',
      'pad.how_install': 'Como Instalar',
      'pad.mission_title': 'Missão e Gatilhos de Decisão',
      'pad.use_when': 'USE QUANDO',
      'pad.dont_use': 'NÃO USE PARA',
      'pad.tools_title': 'Ferramentas Habilitadas',
      'pad.skills_title': 'Skills Ativas no Domínio',
      'pad.skills_hint': 'Clique para inspecionar',
      'pad.sources_title': 'Fontes e Provedores Upstream',
      'pad.config_title': 'Configuração e Arquivos',
      'pad.project': 'Projeto',
      'pad.global': 'Global',
      'pad.active_skill_singular': 'SKILL ATIVA',
      'pad.active_skill_plural': 'SKILLS ATIVAS',

      // Catálogo
      'catalog.kicker': 'Catálogo',
      'catalog.title': 'Skills',
      'catalog.search_ph': 'Buscar skill, autor ou fonte',
      'catalog.cat_all': 'TODAS',
      'catalog.cat_label': 'Categoria',
      'catalog.filters_btn': 'Filtros',
      'catalog.source_label': 'Fonte',
      'catalog.source_all': 'Todas as fontes',
      'catalog.order_label': 'Ordenação',
      'catalog.order_default': 'Ordem padrão',
      'catalog.order_name': 'Nome (A–Z)',
      'catalog.order_category': 'Categoria',
      'catalog.btn_build_plan': 'Montar plano',
      'catalog.view_grid': 'Grade',
      'catalog.view_table': 'Tabela',
      'catalog.displaying': 'Exibindo {0} de {1} skills',
      'catalog.no_results': 'Nenhuma skill encontrada para os critérios atuais',
      'catalog.empty_msg': 'Nenhuma skill encontrada. Tente outro termo ou limpe os filtros.',
      'catalog.btn_more': 'Mostrar mais',
      'catalog.btn_all': 'Mostrar tudo',
      'catalog.btn_prompt': 'Prompt',
      'catalog.btn_detail': 'Detalhe',
      'catalog.btn_plan': 'Plano',
      'catalog.btn_plan_active': '✓ Plano',

      // Barra de Plano & Modais
      'plan.in_plan': 'no plano',
      'plan.skills_in_plan': 'skills no plano',
      'plan.btn_generate_prompt': 'Gerar prompt',
      'plan.btn_clear': 'Limpar',
      'plan.btn_copy': 'Copiar prompt sob medida',
      'modal.close': 'Fechar',
      'modal.skill_title': 'Inspeção de skill',
      'modal.source_repo': 'Repositório fonte',
      'modal.copy_skill_prompt': 'Copiar prompt desta skill',
      'modal.master_title': 'Prompt mestre geral: base para novos projetos',
      'modal.master_intro': 'Copie este prompt e cole no seu agente (Google Antigravity, OpenAI Codex ou Claude Code) ao iniciar qualquer projeto. Ele amarra o hub local, as práticas de engenharia de software, o diagnóstico Graphify e a árvore de skills.',
      'modal.plan_title': 'Planejador sob medida de novo projeto',
      'modal.plan_intro': 'Prompt gerado com base nas skills selecionadas para o seu projeto. Sem seleção, usa as primeiras skills do catálogo.',
      'modal.loading': 'Carregando…',
      'modal.load_error': 'Não foi possível carregar o conteúdo completo desta skill.',

      // Toasts
      'toast.master_copied': 'Prompt mestre copiado! Cole no seu chat do Claude Code ou Antigravity.',
      'toast.prompt_copied': 'Prompt de [{0}] copiado!',
      'toast.plan_copied': 'Plano sob medida copiado!',
      'toast.agent_copied': 'Instrução de ativação do {0} copiada!',
      'toast.copy_error': 'Não foi possível copiar',
      'toast.copied': 'Copiado',

      // Rodapé
      'footer.title': 'LAY® SKILLS HUB — PERNAMBUCO PARA O MUNDO',
      'footer.sub': 'Engenharia de precisão para agentes de inteligência artificial.',
      'footer.copy': 'Lound Angry Young® • Todos os direitos reservados.',
      'footer.subagents': 'Instalação dos subagentes',
      'footer.github': 'Repositório GitHub',
      'footer.upstream_sources': 'Fontes upstream',

      // Página de instalação (instalacao.html)
      'install.back_to_catalog': '← Catálogo',
      'install.ticker': 'INSTALAR python scripts/skill_hub.py install --agents claude',
      'install.kicker': 'CLAUDE CODE • SUBAGENTES',
      'install.title': 'SUBAGENTES LAY<br><span class="destaque">INSTALE EM 3 PASSOS</span>',
      'install.lead': 'Três comandos instalam os subagentes. Depois, confira com o doctor e com /agents.',
      'install.btn_install_cmd': 'COMANDOS DE INSTALAÇÃO',
      'install.btn_prompts': 'PROMPTS PARA COPIAR',
      'install.btn_github': 'REPOSITÓRIO GITHUB',
      'install.stat_subagents': 'subagentes',
      'install.stat_skills': 'skills',
      'install.stat_scopes': 'escopos',
      'install.step1_kicker': '01 · INSTALAR',
      'install.step1_title': 'Três comandos',
      'install.step1_desc': 'Execute no terminal, dentro da pasta do repositório clonado.',
      'install.step2_kicker': '02 · SUBAGENTES',
      'install.step2_title': 'Um por domínio',
      'install.step2_desc': 'Cada um recebe só as ferramentas do seu trabalho. Você pode chamar pelo nome.',
      'install.step3_kicker': '03 · COMO CHAMAR',
      'install.step3_title': 'Automático ou pelo nome',
      'install.step3_desc': 'Você não precisa decorar nada. Escreva o pedido normalmente, ou nomeie o especialista.',
      'install.step4_kicker': '04 · ORQUESTRAÇÃO',
      'install.step4_title': 'Quem decide é a conversa',
      'install.step4_desc': 'A conversa principal escolhe o domínio, delega e junta as respostas. Subagentes não chamam outros subagentes.',
      'install.step5_kicker': '05 · PROMPTS PARA COPIAR',
      'install.step5_title': 'Cole no Claude Code',
      'install.step5_desc': 'Copie o bloco, cole na sessão do Claude Code e envie. Eles não dependem de nenhum dado pessoal.',
      'install.step6_kicker': '06 · ATUALIZAR E REMOVER',
      'install.step6_title': 'Sem surpresas',
      'install.step6_desc': 'A abertura de sessão só consulta. Aplicar é sempre um comando seu.',
      'install.step7_kicker': '07 · PROBLEMAS COMUNS',
      'install.step7_title': 'Se algo falhar',
      'install.step7_desc': 'A instalação para quando encontra algo que não pode sobrescrever. Nada é apagado por engano.',
      'install.step8_kicker': '08 · ATRIBUIÇÕES',
      'install.step8_title': 'Fontes originais',
      'install.step8_desc': 'Os subagentes combinam skills nativas LAY e capacidades adaptadas de repositórios públicos.',
      'install.th_subagent': 'Subagente',
      'install.th_domain': 'Domínio',
      'install.th_description': 'Descrição',
      'install.th_access': 'Acesso',
      'install.th_tools': 'Ferramentas'
    },
    'en': {
      // Top Ticker & Header
      'lang.title': 'IDIOMA / LANGUAGE',
      'header.sub': 'Central repository of capabilities & rules for agents',
      'header.skills_label': 'skills',
      'header.skip_link': 'Skip to content',
      'ticker.items': 'skills in catalog',
      'ticker.specialists': 'domain subagents',
      'ticker.sources': 'upstream sources',
      'ticker.clients': 'Antigravity • Codex • Claude Code',
      'ticker.creative': 'Vanta 3D • React Bits • Lenis Smooth Scroll • Libraries.dev',

      // Hero
      'hero.badge': 'Modular architecture • deterministic evidence',
      'hero.title': 'Complete ecosystem <span class="destaque-amarelo">of agent skills</span> <span class="destaque-magenta">Pernambuco → world</span>',
      'hero.impact': 'Skills built with next-generation, high-performance components.',
      'hero.intro': 'Interactive visual hub gathering specialized capabilities and world-class reference sources: core agent orchestration (<strong class="nome">lay-orchestrator</strong>, <strong class="nome">Caveman</strong>, <strong class="nome">Graphify</strong>), elite references (<strong class="nome">Addy Osmani</strong>, <strong class="nome">Vercel Labs</strong>, <strong class="nome">Semgrep</strong>, <strong class="nome">Playwright</strong>), and creative libraries (<strong class="nome">Vanta 3D</strong>, <strong class="nome">React Bits</strong>, <strong class="nome">Lenis Smooth Scroll</strong>, and <strong class="nome">Libraries.dev</strong>). Inspect code, copy individual prompts, and generate tailored end-to-end architectures.',
      'hero.stat_skills': 'skills',
      'hero.stat_sources': 'upstream sources',
      'hero.stat_specialists': 'specialists',
      'hero.btn_master_prompt': 'Copy master prompt',
      'hero.btn_install': 'Install subagents',
      'hero.btn_github': 'GitHub Repository',

      // Especialistas
      'specialists.kicker': 'AUTONOMOUS SPECIALISTS • CLAUDE CODE & ECOSYSTEM',
      'specialists.title': 'Claude Code Subagents',
      'specialists.lead': '18 preconfigured specialists with restricted tools, strict activation triggers, and mapped skills. Select a specialist in the grid to view its sources, capabilities, and direct activation command.',
      'specialists.subagents_page': 'Subagents page',
      'specialists.prompts_to_copy': 'Prompts to copy',
      'specialists.see_others': 'See others',
      'pad.copy_cmd': 'Copy Activation Prompt',
      'pad.how_install': 'How to Install',
      'pad.mission_title': 'Mission & Decision Triggers',
      'pad.use_when': 'USE WHEN',
      'pad.dont_use': 'DO NOT USE FOR',
      'pad.tools_title': 'Enabled Tools',
      'pad.skills_title': 'Active Domain Skills',
      'pad.skills_hint': 'Click to inspect',
      'pad.sources_title': 'Upstream Sources & Providers',
      'pad.config_title': 'Configuration & Files',
      'pad.project': 'Project',
      'pad.global': 'Global',
      'pad.active_skill_singular': 'ACTIVE SKILL',
      'pad.active_skill_plural': 'ACTIVE SKILLS',

      // Catálogo
      'catalog.kicker': 'Catalog',
      'catalog.title': 'Skills',
      'catalog.search_ph': 'Search skill, author or source',
      'catalog.cat_all': 'ALL',
      'catalog.cat_label': 'Category',
      'catalog.filters_btn': 'Filters',
      'catalog.source_label': 'Source',
      'catalog.source_all': 'All sources',
      'catalog.order_label': 'Sorting',
      'catalog.order_default': 'Default order',
      'catalog.order_name': 'Name (A–Z)',
      'catalog.order_category': 'Category',
      'catalog.btn_build_plan': 'Build plan',
      'catalog.view_grid': 'Grid',
      'catalog.view_table': 'Table',
      'catalog.displaying': 'Displaying {0} of {1} skills',
      'catalog.no_results': 'No skills found for current criteria',
      'catalog.empty_msg': 'No skills found. Try another search or clear filters.',
      'catalog.btn_more': 'Show more',
      'catalog.btn_all': 'Show all',
      'catalog.btn_prompt': 'Prompt',
      'catalog.btn_detail': 'Detail',
      'catalog.btn_plan': 'Plan',
      'catalog.btn_plan_active': '✓ Plan',

      // Barra de Plano & Modais
      'plan.in_plan': 'in plan',
      'plan.skills_in_plan': 'skills in plan',
      'plan.btn_generate_prompt': 'Generate prompt',
      'plan.btn_clear': 'Clear',
      'plan.btn_copy': 'Copy custom prompt',
      'modal.close': 'Close',
      'modal.skill_title': 'Skill Inspection',
      'modal.source_repo': 'Source repository',
      'modal.copy_skill_prompt': 'Copy prompt for this skill',
      'modal.master_title': 'Master Project Prompt: Foundation for New Projects',
      'modal.master_intro': 'Copy this prompt and paste it into your agent (Google Antigravity, OpenAI Codex, or Claude Code) when starting any project. It connects the local hub, software engineering practices, Graphify diagnostics, and the skill tree.',
      'modal.plan_title': 'Custom Project Planner',
      'modal.plan_intro': 'Prompt generated based on the selected skills for your project. Without selection, uses the first skills in the catalog.',
      'modal.loading': 'Loading…',
      'modal.load_error': 'Could not load the full content of this skill.',

      // Toasts
      'toast.master_copied': 'Master prompt copied! Paste into Claude Code or Antigravity.',
      'toast.prompt_copied': 'Prompt for [{0}] copied!',
      'toast.plan_copied': 'Tailored plan copied!',
      'toast.agent_copied': 'Activation prompt for {0} copied!',
      'toast.copy_error': 'Could not copy',
      'toast.copied': 'Copied',

      // Rodapé
      'footer.title': 'LAY® SKILLS HUB — PERNAMBUCO TO THE WORLD',
      'footer.sub': 'Precision engineering for artificial intelligence agents.',
      'footer.copy': 'Lound Angry Young® • All rights reserved.',
      'footer.subagents': 'Subagents installation',
      'footer.github': 'GitHub Repository',
      'footer.upstream_sources': 'Upstream sources',

      // Página de instalação (instalacao.html)
      'install.back_to_catalog': '← Catalog',
      'install.ticker': 'INSTALL python scripts/skill_hub.py install --agents claude',
      'install.kicker': 'CLAUDE CODE • SUBAGENTS',
      'install.title': 'LAY SUBAGENTS<br><span class="destaque">INSTALL IN 3 STEPS</span>',
      'install.lead': 'Three commands install the subagents. Then, verify with doctor and /agents.',
      'install.btn_install_cmd': 'INSTALLATION COMMANDS',
      'install.btn_prompts': 'PROMPTS TO COPY',
      'install.btn_github': 'GITHUB REPOSITORY',
      'install.stat_subagents': 'subagents',
      'install.stat_skills': 'skills',
      'install.stat_scopes': 'scopes',
      'install.step1_kicker': '01 · INSTALL',
      'install.step1_title': 'Three commands',
      'install.step1_desc': 'Run in terminal, inside the cloned repository folder.',
      'install.step2_kicker': '02 · SUBAGENTS',
      'install.step2_title': 'One per domain',
      'install.step2_desc': 'Each specialist receives only the tools needed for its job. You can call by name.',
      'install.step3_kicker': '03 · HOW TO CALL',
      'install.step3_title': 'Automatic or by name',
      'install.step3_desc': 'No memorization required. Write your request naturally, or name the specialist.',
      'install.step4_kicker': '04 · ORCHESTRATION',
      'install.step4_title': 'The main conversation decides',
      'install.step4_desc': 'The main conversation picks the domain, delegates, and collects responses. Subagents do not call other subagents.',
      'install.step5_kicker': '05 · PROMPTS TO COPY',
      'install.step5_title': 'Paste into Claude Code',
      'install.step5_desc': 'Copy the block, paste into your Claude Code session, and send. They contain no private data.',
      'install.step6_kicker': '06 · UPDATE AND UNINSTALL',
      'install.step6_title': 'No surprises',
      'install.step6_desc': 'Session initialization only checks. Applying is always your command.',
      'install.step7_kicker': '07 · COMMON ISSUES',
      'install.step7_title': 'If something fails',
      'install.step7_desc': 'Installation stops when it encounters something it cannot overwrite. Nothing is deleted by mistake.',
      'install.step8_kicker': '08 · ATTRIBUTIONS',
      'install.step8_title': 'Original sources',
      'install.step8_desc': 'Subagents combine native LAY skills and adapted capabilities from public reference repositories.',
      'install.th_subagent': 'Subagent',
      'install.th_domain': 'Domain',
      'install.th_description': 'Description',
      'install.th_access': 'Access',
      'install.th_tools': 'Tools'
    }
  };

  var ROTULOS_CATEGORIA_EN = {
    design: 'DESIGN & UI/UX',
    engenharia: 'ENGINEERING',
    testes: 'TESTING & QA',
    seguranca: 'SECURITY & SCAN',
    llm: 'ROUTING & LLM',
    creative3d: '3D & WEBGL SHADER',
    frontend: 'COMPONENTS & MOTION',
    contexto: 'ANALYSIS & GRAPHS',
    minimalismo: 'MINIMALISM & ANTI-SLOP',
    devops: 'DEVOPS & RELEASE',
    cards: 'CARDS & WIDGETS',
    operacoes: 'DEVOPS & CI/CD',
    documentacao: 'DOCUMENTATION'
  };

  var ACESSO_LABELS = {
    'pt-BR': {
      'Edita e roda comandos': 'Edita e roda comandos',
      'Edita, sem comandos': 'Edita, sem comandos',
      'Não edita · tem Bash': 'Não edita · tem Bash',
      'Só leitura': 'Só leitura'
    },
    'en': {
      'Edita e roda comandos': 'Edits & runs commands',
      'Edita, sem comandos': 'Edits, no commands',
      'Não edita · tem Bash': 'No edit · has Bash',
      'Só leitura': 'Read-only'
    }
  };

  var AGENTE_SUBTITULOS = {
    'lay-design': { 'pt-BR': 'Identidade Visual & Mockups', 'en': 'Visual Identity & Mockups' },
    'lay-frontend': { 'pt-BR': 'Interfaces Web & Microinterações', 'en': 'Web Interfaces & Microinteractions' },
    'lay-3d': { 'pt-BR': 'Blender, WebGL & Shaders', 'en': 'Blender, WebGL & Shaders' },
    'lay-contexto': { 'pt-BR': 'Grafos, Planejamento & Prompts', 'en': 'Graphs, Planning & Prompts' },
    'lay-engenharia': { 'pt-BR': 'Arquitetura, APIs & Causa-Raiz', 'en': 'Architecture, APIs & Root-Cause' },
    'lay-omniroute': { 'pt-BR': 'Roteamento LLM, Combos & Proxy', 'en': 'LLM Routing, Combos & Proxy' },
    'lay-devops': { 'pt-BR': 'CI/CD, Deploy & Releases', 'en': 'CI/CD, Deploy & Releases' },
    'lay-qa': { 'pt-BR': 'TDD, DevTools & Playwright', 'en': 'TDD, DevTools & Playwright' },
    'lay-seguranca': { 'pt-BR': 'Hardening, Semgrep & CVEs', 'en': 'Hardening, Semgrep & CVEs' },
    'lay-banco-de-dados': { 'pt-BR': 'SQLite, Snapshots & Cache', 'en': 'SQLite, Snapshots & Cache' },
    'lay-documentacao': { 'pt-BR': 'ADRs, Estilo & Limpeza Editorial', 'en': 'ADRs, Style & Editorial Cleanup' }
  };

  var lastBlip = 0;
  function playBlip() {
    try {
      var Ctor = window.AudioContext || window.webkitAudioContext;
      if (!Ctor) return;
      var ctx = window._layAudioCtx || (window._layAudioCtx = new Ctor());
      if (ctx.state === 'suspended') { ctx.resume(); }
      var now = performance.now();
      if (now - lastBlip < 80) return;
      lastBlip = now;
      var t = ctx.currentTime;
      var o = ctx.createOscillator();
      var g = ctx.createGain();
      o.type = 'square';
      o.frequency.setValueAtTime(880, t);
      o.frequency.exponentialRampToValueAtTime(440, t + 0.06);
      g.gain.setValueAtTime(0.04, t);
      g.gain.exponentialRampToValueAtTime(0.0001, t + 0.07);
      o.connect(g);
      g.connect(ctx.destination);
      o.start(t);
      o.stop(t + 0.08);
    } catch (e) {
      /* WebAudio indisponível */
    }
  }

  function readInitialLocale() {
    try {
      var params = new URLSearchParams(window.location.search);
      var q = params.get('lang');
      if (q === 'pt-BR' || q === 'en') {
        localStorage.setItem(LOCALE_KEY, q);
        return q;
      }
      var saved = localStorage.getItem(LOCALE_KEY);
      if (saved === 'pt-BR' || saved === 'en') return saved;
    } catch (e) {}
    return DEFAULT_LOCALE;
  }

  var currentLocale = readInitialLocale();

  function getLocale() {
    return currentLocale;
  }

  function t(key, fallback) {
    var dict = TRANSLATIONS[currentLocale] || TRANSLATIONS[DEFAULT_LOCALE];
    return (dict && dict[key]) || fallback || key;
  }

  function rotuloCategoria(catId, fallback) {
    if (currentLocale === 'en' && ROTULOS_CATEGORIA_EN[catId]) {
      return ROTULOS_CATEGORIA_EN[catId];
    }
    return fallback || catId;
  }

  function traduzirAcesso(acesso) {
    var dict = ACESSO_LABELS[currentLocale] || ACESSO_LABELS[DEFAULT_LOCALE];
    return (dict && dict[acesso]) || acesso;
  }

  function subtituloAgente(nome, dominio) {
    var item = AGENTE_SUBTITULOS[nome];
    if (item && item[currentLocale]) return item[currentLocale];
    return dominio;
  }

  function setLocale(locale, skipSound) {
    if (SUPPORTED_LOCALES.indexOf(locale) === -1) return;
    currentLocale = locale;
    try {
      localStorage.setItem(LOCALE_KEY, locale);
    } catch (e) {}
    document.documentElement.lang = locale;

    if (!skipSound) playBlip();

    // Atualiza elementos estáticos marcados com data-i18n
    document.querySelectorAll('[data-i18n]').forEach(function (el) {
      var key = el.getAttribute('data-i18n');
      var val = t(key);
      if (val) {
        if (val.indexOf('<') !== -1) {
          el.innerHTML = val;
        } else {
          el.textContent = val;
        }
      }
    });

    // Atualiza placeholders
    document.querySelectorAll('[data-i18n-ph]').forEach(function (el) {
      var key = el.getAttribute('data-i18n-ph');
      var val = t(key);
      if (val) el.setAttribute('placeholder', val);
    });

    // Atualiza titles
    document.querySelectorAll('[data-i18n-title]').forEach(function (el) {
      var key = el.getAttribute('data-i18n-title');
      var val = t(key);
      if (val) el.setAttribute('title', val);
    });

    // Atualiza labels de acesso
    document.querySelectorAll('[data-i18n-access]').forEach(function (el) {
      var key = el.getAttribute('data-i18n-access');
      el.textContent = traduzirAcesso(key);
    });

    // Atualiza o estado visual das opções do seletor
    document.querySelectorAll('.lang-option').forEach(function (btn) {
      var lang = btn.getAttribute('data-lang');
      var isActive = lang === currentLocale;
      btn.setAttribute('data-active', isActive ? 'true' : 'false');
      btn.setAttribute('aria-selected', isActive ? 'true' : 'false');
      var check = btn.querySelector('.lang-check');
      if (check) check.style.display = isActive ? 'inline' : 'none';
    });

    // Dispara evento para controladores da página
    try {
      window.dispatchEvent(new CustomEvent('lay:localechange', { detail: { locale: locale } }));
    } catch (e) {}
  }

  function initLanguageSelector() {
    var wrap = document.getElementById('lang-wrap');
    var btn = document.getElementById('lang-btn');
    var popover = document.getElementById('lang-popover');
    var closeBtn = document.getElementById('lang-close-btn');
    if (!wrap || !btn || !popover) return;

    function openPopover() {
      popover.hidden = false;
      btn.setAttribute('aria-expanded', 'true');
      playBlip();
    }

    function closePopover() {
      popover.hidden = true;
      btn.setAttribute('aria-expanded', 'false');
    }

    btn.addEventListener('click', function (e) {
      e.stopPropagation();
      if (popover.hidden) openPopover();
      else closePopover();
    });

    if (closeBtn) {
      closeBtn.addEventListener('click', function (e) {
        e.stopPropagation();
        closePopover();
        btn.focus();
      });
    }

    wrap.querySelectorAll('.lang-option').forEach(function (opt) {
      opt.addEventListener('click', function (e) {
        e.stopPropagation();
        var lang = opt.getAttribute('data-lang');
        setLocale(lang);
        closePopover();
        btn.focus();
      });
    });

    document.addEventListener('mousedown', function (e) {
      if (!popover.hidden && !wrap.contains(e.target)) {
        closePopover();
      }
    });

    wrap.addEventListener('keydown', function (e) {
      if (e.key === 'Escape') {
        e.preventDefault();
        closePopover();
        btn.focus();
      }
    });

    // Define locale inicial
    setLocale(currentLocale, true);
  }

  global.LAY_I18N = {
    getLocale: getLocale,
    setLocale: setLocale,
    t: t,
    playBlip: playBlip,
    init: initLanguageSelector,
    rotuloCategoria: rotuloCategoria,
    traduzirAcesso: traduzirAcesso,
    subtituloAgente: subtituloAgente,
    ROTULOS_CATEGORIA_EN: ROTULOS_CATEGORIA_EN,
    ACESSO_LABELS: ACESSO_LABELS
  };

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initLanguageSelector);
  } else {
    initLanguageSelector();
  }
})(typeof window !== 'undefined' ? window : this);
