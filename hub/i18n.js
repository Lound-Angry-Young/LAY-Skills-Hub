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
      'ticker.domains': 'DOMÍNIOS',

      // Hero
      'hero.badge': 'Arquitetura modular • evidências determinísticas',
      'hero.title': 'Ecossistema total <span class="destaque-amarelo">de skills de agentes</span><br><span class="destaque-magenta">Pernambuco → mundo</span>',
      'hero.impact': 'Skills construídas com componentes de última geração e alta performance.',
      'hero.intro': 'Hub visual interativo reunindo capacidades especializadas e fontes de referência de elite mundial: orquestração central de agentes (<strong class="nome">lay-orchestrator</strong>, <strong class="nome">Caveman</strong>, <strong class="nome">Graphify</strong>), referências de ponta (<strong class="nome">Addy Osmani</strong>, <strong class="nome">Vercel Labs</strong>, <strong class="nome">Semgrep</strong>, <strong class="nome">Playwright</strong>) e bibliotecas criativas (<strong class="nome">Vanta 3D</strong>, <strong class="nome">React Bits</strong>, <strong class="nome">Lenis Smooth Scroll</strong> e <strong class="nome">Libraries.dev</strong>). Inspecione códigos, copie prompts individuais e gere arquiteturas completas sob medida.',
      'hero.stat_skills': 'skills',
      'hero.stat_sources': 'fontes upstream',
      'hero.stat_specialists': 'especialistas',
      'hero.btn_master_prompt': 'Copiar prompt mestre',
      'hero.btn_install': 'Instalar subagentes',
      'hero.btn_github': 'Repositório GitHub',

      // Especialistas / Esquadrão
      'specialists.kicker': 'ESPECIALISTAS AUTÔNOMOS • CLAUDE CODE & ECOSSISTEMA',
      'specialists.title': 'ESQUADRÃO DE AGENTES',
      'specialists.lead': 'Selecione um agente especialista para inspecionar capacidades ativas, ferramentas, domínio e instruções diretas de ativação.',
      'specialists.subagents_page': 'Página de subagentes',
      'specialists.prompts_to_copy': 'Prompts para copiar',
      'specialists.see_others': 'Ver os outros',
      'specialists.active_badge': 'ATIVO',
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
      'pad.native_eco': 'Ecossistema Nativo LAY®',

      // Catálogo
      'catalog.kicker': 'Catálogo',
      'catalog.title': 'Skills',
      'catalog.search_ph': 'Buscar skill, autor ou fonte',
      'catalog.cat_all': 'TODAS',
      'catalog.cat_general': 'GERAL',
      'catalog.cat_label': 'Categoria',
      'catalog.filters_btn': 'Filtros',
      'catalog.source_label': 'Fonte',
      'catalog.source_all': 'Todas as fontes',
      'catalog.source_default': 'Fonte',
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
      'install.prereq_title': 'Pré-requisitos:',
      'install.prereq_items': 'Git · Python 3.10+ · Claude Code',
      'install.prereq_note': 'Use <code>python</code>. No Windows, se não funcionar, use <code>py -3</code>. Claude Code: CLI no terminal ou app desktop; os subagentes aparecem nas sessões novas.',
      'install.step1_kicker': '01 · INSTALAR',
      'install.step1_title': 'Três comandos',
      'install.step1_desc': 'Execute no terminal, dentro da pasta do repositório clonado.',
      'install.step1_badge': 'Passo 01',
      'install.step1_card_title': 'Clonar com submódulos',
      'install.step1_card_desc': 'Faça uma vez. Se já clonou sem submódulos, rode <code>git submodule update --init --recursive</code>.',
      'install.bash_custom_dir': 'bash · pasta de sua escolha',
      'install.bash_in_repo': 'bash · dentro do repositório',
      'install.btn_copy': 'Copiar',
      'install.step2_badge': 'Passo 02',
      'install.step2_card_title': 'Instalar os subagentes',
      'install.step2_card_desc': 'Instala os arquivos <code>lay-*.md</code> em <code>~/.claude/agents/</code> e grava o índice de roteamento no <code>~/.claude/CLAUDE.md</code>, entre os marcadores <code>LAY-SKILLS</code>. Quer também Codex e Antigravity? Troque <code>claude</code> por <code>all</code>.',
      'install.step3_badge': 'Passo 03',
      'install.step3_card_title': 'Conferir',
      'install.step3_card_desc': 'O <code>doctor</code> confere a instalação e termina com a contagem de entradas verificadas e de problemas. Depois, em uma sessão do Claude Code, rode <code>/agents</code>: os <code>lay-*</code> aparecem na lista.',
      'install.scopes_note': '<strong>Escopos.</strong> O global (passo 02) vale em todos os seus projetos. Os mesmos arquivos ficam versionados em <code>.claude/agents/</code> deste repositório e valem quando o Claude Code abre este repositório. Quando os dois existem, o do projeto prevalece.',
      'install.step2_kicker': '02 · SUBAGENTES',
      'install.step2_title': 'Um por domínio',
      'install.step2_desc': 'Cada um recebe só as ferramentas do seu trabalho. Você pode chamar pelo nome.',
      'install.step3_kicker': '03 · COMO CHAMAR',
      'install.step3_title': 'Automático ou pelo nome',
      'install.step3_desc': 'Você não precisa decorar nada. Escreva o pedido normalmente, ou nomeie o especialista.',
      'install.call_auto_tag': 'Automático',
      'install.call_auto_title': 'O Claude escolhe',
      'install.call_auto_desc1': 'Ele compara seu pedido com a <code>description</code> de cada subagente, que traz os gatilhos <strong>Use quando</strong> e <strong>Não use para</strong>.',
      'install.call_auto_desc2': 'Exemplo: <em>"revise a segurança do login"</em> aciona <code>lay-seguranca</code>.',
      'install.call_explicit_tag': 'Explícito',
      'install.call_explicit_title': 'Você nomeia',
      'install.call_explicit_desc1': 'Quando quiser certeza do especialista, peça pelo nome:',
      'install.call_note': '<strong>Subagente novo não aparece?</strong> Reinicie a sessão. Os perfis são carregados no início da sessão.',
      'install.step4_kicker': '04 · ORQUESTRAÇÃO',
      'install.step4_title': 'Quem decide é a conversa',
      'install.step4_desc': 'A conversa principal escolhe o domínio, delega e junta as respostas. Subagentes não chamam outros subagentes.',
      'install.flow_step1_name': '1 · Pedido',
      'install.flow_step1_desc': 'Você descreve o que quer.',
      'install.flow_step2_name': '2 · Domínio',
      'install.flow_step2_desc': 'A conversa escolhe <strong>um</strong> domínio primário.',
      'install.flow_step3_name': '3 · HANDOFF',
      'install.flow_step3_desc': 'Delega com <code>task</code>, <code>domain</code>, <code>context</code>, <code>constraints</code> e <code>acceptance_criteria</code>.',
      'install.flow_step4_name': '4 · RESULT',
      'install.flow_step4_desc': 'O subagente devolve <code>status</code>, <code>artifacts</code>, <code>summary</code> e <code>open_items</code>.',
      'install.flow_step5_name': '5 · Resposta',
      'install.flow_step5_desc': 'A conversa responde em português direto.',
      'install.rules_1': 'Um domínio primário por pedido. Domínios independentes rodam em paralelo, em lotes de até 5.',
      'install.rules_2': 'Pedido ambíguo: no máximo uma pergunta de clarificação.',
      'install.rules_3': 'Nenhum domínio cobre o pedido: a resposta diz isso e sugere criar uma skill.',
      'install.rules_4': 'Ações externas ou irreversíveis (enviar, publicar, apagar) só com confirmação explícita.',
      'install.step5_kicker': '05 · PROMPTS PARA COPIAR',
      'install.step5_title': 'Cole no Claude Code',
      'install.step5_desc': 'Copie o bloco, cole na sessão do Claude Code e envie. Eles não dependem de nenhum dado pessoal.',
      'install.view_prompt': 'Ver prompt',
      'install.prompt_a_badge': 'Prompt A',
      'install.prompt_a_title': 'Instalar os subagentes',
      'install.prompt_a_desc': 'Use em um computador novo, com o Claude Code aberto na pasta onde quer o clone.',
      'install.prompt_b_badge': 'Prompt B',
      'install.prompt_b_title': 'Atualizar com confirmação',
      'install.prompt_b_desc': 'Consulta primeiro. Só aplica depois que você disser sim.',
      'install.prompt_c_badge': 'Prompt C',
      'install.prompt_c_title': 'Pedir com orquestração',
      'install.prompt_c_desc': 'Substitua o último campo pelo seu pedido. Serve para qualquer projeto com os subagentes instalados.',
      'install.step6_kicker': '06 · ATUALIZAR E REMOVER',
      'install.step6_title': 'Sem surpresas',
      'install.step6_desc': 'A abertura de sessão só consulta. Aplicar é sempre um comando seu.',
      'install.upd_card1_badge': 'Atualizar',
      'install.upd_card1_title': 'Consultar, aplicar, reinstalar',
      'install.upd_card1_desc': 'Consulta: <code>sync --check</code>. Aplica: <code>sync --apply</code>, que só faz fast-forward limpo e preserva suas alterações. Depois, <code>install --agents all</code>.',
      'install.upd_card2_badge': 'Remover',
      'install.upd_card2_title': 'Desinstalar',
      'install.upd_card2_desc': 'Remove os subagentes <code>lay-*</code> que você não editou à mão. Arquivos seus, com outro nome, ficam.',
      'install.step7_kicker': '07 · PROBLEMAS COMUNS',
      'install.step7_title': 'Se algo falhar',
      'install.step7_desc': 'A instalação para quando encontra algo que não pode sobrescrever. Nada é apagado por engano.',
      'install.prob_cause': 'Causa',
      'install.prob_action': 'O que fazer',
      'install.prob1_title': 'Subagente não aparece',
      'install.prob1_cause': 'A sessão foi aberta antes da instalação.',
      'install.prob1_action': 'Reinicie a sessão do Claude Code e rode <code>doctor</code>.',
      'install.prob2_title': 'Mensagem com "Colisão"',
      'install.prob2_cause': 'Já existe um <code>lay-*.md</code> que não é do instalador.',
      'install.prob2_action': 'Renomeie ou remova o seu arquivo e rode a instalação de novo. O arquivo existente é preservado até lá.',
      'install.prob3_title': 'Mensagem com "modificado"',
      'install.prob3_cause': 'Você editou um <code>lay-*.md</code> à mão.',
      'install.prob3_action': 'Guarde sua edição com outro nome, remova o arquivo e reinstale.',
      'install.prob4_title': 'Mensagem com "Fonte modificada"',
      'install.prob4_cause': 'Há alteração rastreada no clone de uma fonte.',
      'install.prob4_action': 'Rode <code>git status</code> no clone e resolva antes de instalar.',
      'install.prob5_title': '<code>python</code> não encontrado',
      'install.prob5_cause': 'Python ausente ou fora do PATH.',
      'install.prob5_action': 'Instale o Python 3.10+. No Windows, use <code>py -3</code>.',
      'install.step8_kicker': '08 · ATRIBUIÇÕES',
      'install.step8_title': 'Fontes originais',
      'install.step8_desc': 'Os subagentes combinam skills nativas LAY e capacidades adaptadas de repositórios públicos.',
      'install.th_subagent': 'Subagente',
      'install.th_domain': 'Domínio',
      'install.th_description': 'Descrição',
      'install.th_access': 'Acesso',
      'install.th_tools': 'Ferramentas',
      'install.show_all_chips': 'Mostrar todas ({0})',
      'install.show_less_chips': 'Mostrar menos',
      'install.only_lay_skills': 'Só skills LAY, sem fonte upstream direta',
      'install.project_no_file': 'Projeto: sem arquivo em .claude/agents/ no último build',
      'install.precedence_note': 'Se os dois existirem, vale o do projeto.',
      'install.no_upstream_sources': 'Nenhuma fonte upstream direta nos subagentes.',
      'install.upstream_sources': 'Fontes upstream dos subagentes',
      'install.open_new_tab': 'abre em nova aba',
      'install.project_label': 'Projeto: ',
      'install.global_label': 'Global: ',
      'install.skill_singular': 'skill',
      'install.skill_plural': 'skills',
      'install.subagents_unavailable': 'Lista de subagentes indisponível. Os comandos e os prompts desta página continuam válidos.',
      'install.prompt_a_text': 'Instale os subagentes LAY deste computador. Siga estes passos e pare se algum falhar:\n\n1. Se o repositório ainda não existir aqui, clone com submódulos:\n   git clone --recurse-submodules https://github.com/Lound-Angry-Young/LAY-Skills-Hub.git\n   Entre na pasta criada.\n2. Rode: python scripts/skill_hub.py install --agents claude\n3. Rode: python scripts/skill_hub.py doctor e me mostre o resultado.\n4. Confirme que a pasta ~/.claude/agents tem os arquivos lay-*.md dos subagentes.\n5. Não rode sync --apply, reset nem nenhum comando que altere o repositório sem me perguntar antes.\n6. Ao final, diga se preciso reiniciar a sessão para os subagentes aparecerem.',
      'install.prompt_b_text': 'Atualize os subagentes LAY deste computador, sem alterar nada sem minha confirmação:\n\n1. Entre na pasta do clone do LAY-Skills-Hub.\n2. Rode: python scripts/skill_hub.py sync --check e me mostre o que mudou.\n3. Só se eu confirmar, rode: python scripts/skill_hub.py sync --apply\n4. Depois rode: python scripts/skill_hub.py install --agents all e python scripts/skill_hub.py doctor.\n5. Diga se preciso reiniciar a sessão.',
      'install.prompt_c_text': 'Use os subagentes LAY para este pedido e siga a orquestração:\n- Escolha um domínio primário e delegue ao subagente correspondente (lay-frontend, lay-qa, lay-seguranca etc.).\n- Subagentes não chamam outros subagentes: você coordena e junta as respostas.\n- Se o pedido for ambíguo, faça no máximo uma pergunta.\n- Antes de qualquer ação externa ou irreversível (enviar, publicar, apagar), peça minha confirmação.\n\nPedido: [descreva aqui]'
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
      'ticker.domains': 'DOMAINS',

      // Hero
      'hero.badge': 'Modular architecture • deterministic evidence',
      'hero.title': 'Complete ecosystem <span class="destaque-amarelo">of agent skills</span><br><span class="destaque-magenta">Pernambuco → world</span>',
      'hero.impact': 'Skills built with next-generation, high-performance components.',
      'hero.intro': 'Interactive visual hub gathering specialized capabilities and world-class reference sources: core agent orchestration (<strong class="nome">lay-orchestrator</strong>, <strong class="nome">Caveman</strong>, <strong class="nome">Graphify</strong>), elite references (<strong class="nome">Addy Osmani</strong>, <strong class="nome">Vercel Labs</strong>, <strong class="nome">Semgrep</strong>, <strong class="nome">Playwright</strong>), and creative libraries (<strong class="nome">Vanta 3D</strong>, <strong class="nome">React Bits</strong>, <strong class="nome">Lenis Smooth Scroll</strong>, and <strong class="nome">Libraries.dev</strong>). Inspect code, copy individual prompts, and generate tailored end-to-end architectures.',
      'hero.stat_skills': 'skills',
      'hero.stat_sources': 'upstream sources',
      'hero.stat_specialists': 'specialists',
      'hero.btn_master_prompt': 'Copy master prompt',
      'hero.btn_install': 'Install subagents',
      'hero.btn_github': 'GitHub Repository',

      // Especialistas / Esquadrão
      'specialists.kicker': 'AUTONOMOUS SPECIALISTS • CLAUDE CODE & ECOSYSTEM',
      'specialists.title': 'AGENT SQUADRON',
      'specialists.lead': 'Select a specialist agent to inspect active capabilities, tools, domain, and direct activation instructions.',
      'specialists.subagents_page': 'Subagents page',
      'specialists.prompts_to_copy': 'Prompts to copy',
      'specialists.see_others': 'See others',
      'specialists.active_badge': 'ACTIVE',
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
      'pad.native_eco': 'LAY® Native Ecosystem',

      // Catálogo
      'catalog.kicker': 'Catalog',
      'catalog.title': 'Skills',
      'catalog.search_ph': 'Search skill, author or source',
      'catalog.cat_all': 'ALL',
      'catalog.cat_general': 'GENERAL',
      'catalog.cat_label': 'Category',
      'catalog.filters_btn': 'Filters',
      'catalog.source_label': 'Source',
      'catalog.source_all': 'All sources',
      'catalog.source_default': 'Source',
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
      'install.prereq_title': 'Prerequisites:',
      'install.prereq_items': 'Git · Python 3.10+ · Claude Code',
      'install.prereq_note': 'Use <code>python</code>. On Windows, if that fails, use <code>py -3</code>. Claude Code: terminal CLI or desktop app; subagents appear in new sessions.',
      'install.step1_kicker': '01 · INSTALL',
      'install.step1_title': 'Three commands',
      'install.step1_desc': 'Run in terminal, inside the cloned repository folder.',
      'install.step1_badge': 'Step 01',
      'install.step1_card_title': 'Clone with submodules',
      'install.step1_card_desc': 'Run once. If already cloned without submodules, run <code>git submodule update --init --recursive</code>.',
      'install.bash_custom_dir': 'bash · directory of your choice',
      'install.bash_in_repo': 'bash · inside repository',
      'install.btn_copy': 'Copy',
      'install.step2_badge': 'Step 02',
      'install.step2_card_title': 'Install subagents',
      'install.step2_card_desc': 'Installs <code>lay-*.md</code> files into <code>~/.claude/agents/</code> and writes the routing index into <code>~/.claude/CLAUDE.md</code> between <code>LAY-SKILLS</code> markers. Want Codex and Antigravity too? Replace <code>claude</code> with <code>all</code>.',
      'install.step3_badge': 'Step 03',
      'install.step3_card_title': 'Verify',
      'install.step3_card_desc': '<code>doctor</code> inspects the installation and reports verified entries and issues. Then, in a Claude Code session, run <code>/agents</code>: the <code>lay-*</code> specialists will appear in the list.',
      'install.scopes_note': '<strong>Scopes.</strong> Global (step 02) applies across all your projects. The same files are versioned in <code>.claude/agents/</code> within this repository and apply when Claude Code opens this repo. When both exist, the project-scoped files take precedence.',
      'install.step2_kicker': '02 · SUBAGENTS',
      'install.step2_title': 'One per domain',
      'install.step2_desc': 'Each specialist receives only the tools needed for its job. You can call by name.',
      'install.step3_kicker': '03 · HOW TO CALL',
      'install.step3_title': 'Automatic or by name',
      'install.step3_desc': 'No memorization required. Write your request naturally, or name the specialist.',
      'install.call_auto_tag': 'Automatic',
      'install.call_auto_title': 'Claude chooses',
      'install.call_auto_desc1': 'It matches your prompt against each subagent <code>description</code>, which specifies <strong>Use when</strong> and <strong>Do not use for</strong> triggers.',
      'install.call_auto_desc2': 'Example: <em>"review login security"</em> activates <code>lay-seguranca</code>.',
      'install.call_explicit_tag': 'Explicit',
      'install.call_explicit_title': 'You name it',
      'install.call_explicit_desc1': 'When you want a specific specialist, request it by name:',
      'install.call_note': '<strong>New subagent not appearing?</strong> Restart your session. Profiles are loaded at session startup.',
      'install.step4_kicker': '04 · ORCHESTRATION',
      'install.step4_title': 'The main conversation decides',
      'install.step4_desc': 'The main conversation picks the domain, delegates, and collects responses. Subagents do not call other subagents.',
      'install.flow_step1_name': '1 · Request',
      'install.flow_step1_desc': 'You describe what you need.',
      'install.flow_step2_name': '2 · Domain',
      'install.flow_step2_desc': 'The conversation chooses <strong>one</strong> primary domain.',
      'install.flow_step3_name': '3 · HANDOFF',
      'install.flow_step3_desc': 'Delegates with <code>task</code>, <code>domain</code>, <code>context</code>, <code>constraints</code>, and <code>acceptance_criteria</code>.',
      'install.flow_step4_name': '4 · RESULT',
      'install.flow_step4_desc': 'The subagent returns <code>status</code>, <code>artifacts</code>, <code>summary</code>, and <code>open_items</code>.',
      'install.flow_step5_name': '5 · Response',
      'install.flow_step5_desc': 'The conversation responds in direct prose.',
      'install.rules_1': 'One primary domain per request. Independent domains run in parallel in batches of up to 5.',
      'install.rules_2': 'Ambiguous request: maximum of one clarifying question.',
      'install.rules_3': 'No domain covers the request: the response states this and suggests creating a skill.',
      'install.rules_4': 'External or irreversible actions (send, publish, delete) require explicit confirmation.',
      'install.step5_kicker': '05 · PROMPTS TO COPY',
      'install.step5_title': 'Paste into Claude Code',
      'install.step5_desc': 'Copy the block, paste into your Claude Code session, and send. They contain no private data.',
      'install.view_prompt': 'View prompt',
      'install.prompt_a_badge': 'Prompt A',
      'install.prompt_a_title': 'Install subagents',
      'install.prompt_a_desc': 'Use on a new machine, with Claude Code opened in the folder where you want to clone.',
      'install.prompt_b_badge': 'Prompt B',
      'install.prompt_b_title': 'Update with confirmation',
      'install.prompt_b_desc': 'Checks first. Only applies changes after your explicit approval.',
      'install.prompt_c_badge': 'Prompt C',
      'install.prompt_c_title': 'Request with orchestration',
      'install.prompt_c_desc': 'Replace the last field with your request. Works for any project with subagents installed.',
      'install.step6_kicker': '06 · UPDATE AND UNINSTALL',
      'install.step6_title': 'No surprises',
      'install.step6_desc': 'Session initialization only checks. Applying is always your command.',
      'install.upd_card1_badge': 'Update',
      'install.upd_card1_title': 'Check, apply, reinstall',
      'install.upd_card1_desc': 'Check: <code>sync --check</code>. Apply: <code>sync --apply</code>, which performs a clean fast-forward preserving your changes. Then run <code>install --agents all</code>.',
      'install.upd_card2_badge': 'Remove',
      'install.upd_card2_title': 'Uninstall',
      'install.upd_card2_desc': 'Removes unedited <code>lay-*</code> subagents. Your custom files under different names are kept untouched.',
      'install.step7_kicker': '07 · COMMON ISSUES',
      'install.step7_title': 'If something fails',
      'install.step7_desc': 'Installation stops when it encounters something it cannot overwrite. Nothing is deleted by mistake.',
      'install.prob_cause': 'Cause',
      'install.prob_action': 'Action',
      'install.prob1_title': 'Subagent does not appear',
      'install.prob1_cause': 'The session was opened before installation.',
      'install.prob1_action': 'Restart your Claude Code session and run <code>doctor</code>.',
      'install.prob2_title': 'Message with "Collision"',
      'install.prob2_cause': 'A non-installer <code>lay-*.md</code> already exists.',
      'install.prob2_action': 'Rename or remove your file and re-run installation. The existing file is preserved until then.',
      'install.prob3_title': 'Message with "modified"',
      'install.prob3_cause': 'You manually edited a <code>lay-*.md</code> file.',
      'install.prob3_action': 'Save your edit under another name, remove the file, and reinstall.',
      'install.prob4_title': 'Message with "Modified source"',
      'install.prob4_cause': 'Tracked changes detected in a source clone.',
      'install.prob4_action': 'Run <code>git status</code> inside the source clone and resolve before installing.',
      'install.prob5_title': '<code>python</code> not found',
      'install.prob5_cause': 'Python is missing or not in system PATH.',
      'install.prob5_action': 'Install Python 3.10+. On Windows, use <code>py -3</code>.',
      'install.step8_kicker': '08 · ATTRIBUTIONS',
      'install.step8_title': 'Original sources',
      'install.step8_desc': 'Subagents combine native LAY skills and adapted capabilities from public reference repositories.',
      'install.th_subagent': 'Subagent',
      'install.th_domain': 'Domain',
      'install.th_description': 'Description',
      'install.th_access': 'Access',
      'install.th_tools': 'Tools',
      'install.show_all_chips': 'Show all ({0})',
      'install.show_less_chips': 'Show less',
      'install.only_lay_skills': 'Only native LAY skills, no direct upstream source',
      'install.project_no_file': 'Project: no file in .claude/agents/ in last build',
      'install.precedence_note': 'When both exist, the project-scoped one takes precedence.',
      'install.no_upstream_sources': 'No direct upstream source in subagents.',
      'install.upstream_sources': 'Subagent upstream sources',
      'install.open_new_tab': 'opens in new tab',
      'install.project_label': 'Project: ',
      'install.global_label': 'Global: ',
      'install.skill_singular': 'skill',
      'install.skill_plural': 'skills',
      'install.subagents_unavailable': 'Subagents list unavailable. Page commands and prompts remain valid.',
      'install.prompt_a_text': 'Install the LAY subagents on this computer. Follow these steps and stop if any fails:\n\n1. If the repository does not exist here yet, clone with submodules:\n   git clone --recurse-submodules https://github.com/Lound-Angry-Young/LAY-Skills-Hub.git\n   Enter the created directory.\n2. Run: python scripts/skill_hub.py install --agents claude\n3. Run: python scripts/skill_hub.py doctor and show me the output.\n4. Confirm that ~/.claude/agents contains the lay-*.md subagent files.\n5. Do not run sync --apply, reset, or any command modifying the repository without asking me first.\n6. At the end, tell me if I need to restart the session for the subagents to appear.',
      'install.prompt_b_text': 'Update the LAY subagents on this computer, without altering anything without my confirmation:\n\n1. Enter the LAY-Skills-Hub clone directory.\n2. Run: python scripts/skill_hub.py sync --check and show me what changed.\n3. Only if I confirm, run: python scripts/skill_hub.py sync --apply\n4. Then run: python scripts/skill_hub.py install --agents all and python scripts/skill_hub.py doctor.\n5. Tell me if I need to restart the session.',
      'install.prompt_c_text': 'Use the LAY subagents for this request and follow orchestration:\n- Choose one primary domain and delegate to the corresponding subagent (lay-frontend, lay-qa, lay-seguranca, etc.).\n- Subagents do not call other subagents: you coordinate and merge the responses.\n- If the request is ambiguous, ask at most one clarifying question.\n- Before any external or irreversible action (send, publish, delete), request my confirmation.\n\nRequest: [describe here]'
    }
  };

  var ROTULOS_CATEGORIA_PT = {
    design: 'DESIGN & UI/UX',
    contexto: 'CONTEXTO & AGENTES',
    engenharia: 'ENGENHARIA',
    testes: 'TESTES & QUALIDADE',
    produto: 'PRODUTO & SPECS',
    seguranca: 'SEGURANÇA & SCAN',
    operacoes: 'OPERAÇÕES & CI/CD',
    midia: 'MÍDIA & IMAGENS',
    pesquisa: 'PESQUISA',
    documentacao: 'DOCUMENTAÇÃO',
    llm: 'ROTEAMENTO & LLM',
    creative3d: '3D & WEBGL SHADERS',
    frontend: 'COMPONENTES & MOTION',
    minimalismo: 'MINIMALISMO & ANTI-SLOP',
    cards: 'CARDS & WIDGETS'
  };

  var ROTULOS_CATEGORIA_EN = {
    design: 'DESIGN & UI/UX',
    contexto: 'CONTEXT & AGENTS',
    engenharia: 'ENGINEERING',
    testes: 'TESTING & QA',
    produto: 'PRODUCT & SPECS',
    seguranca: 'SECURITY & SCAN',
    operacoes: 'DEVOPS & CI/CD',
    midia: 'MEDIA & IMAGES',
    pesquisa: 'RESEARCH',
    documentacao: 'DOCUMENTATION',
    llm: 'ROUTING & LLM',
    creative3d: '3D & WEBGL SHADERS',
    frontend: 'COMPONENTS & MOTION',
    minimalismo: 'MINIMALISM & ANTI-SLOP',
    cards: 'CARDS & WIDGETS'
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

  var AGENTE_GATILHOS = {
    'lay-3d': {
      'en': {
        use_quando: 'the request involves 3D, Blender, shaders, animated backgrounds, or web visual effect libraries.',
        nao_use_para: 'page layout without 3D or WebGL elements.',
        resumo: '3D, Blender, shaders, animated backgrounds & visual FX'
      }
    },
    'lay-banco-de-dados': {
      'en': {
        use_quando: 'the request involves backup, restoration, snapshots, corrupted SQLite recovery, or LLM response caching.',
        nao_use_para: 'application schema modeling or general database queries.',
        resumo: 'backup, restore, snapshots & inference cache'
      }
    },
    'lay-contexto': {
      'en': {
        use_quando: 'the request involves understanding a project via graphs, planning tasks, gathering requirements, saving context, or compressing prompts.',
        nao_use_para: 'writing implementation code.',
        resumo: 'project knowledge graphs, planning & prompt compression'
      }
    },
    'lay-design': {
      'en': {
        use_quando: 'the request involves visual identity, moodboards, mockups, or design references before implementation.',
        nao_use_para: 'writing interface code (use lay-frontend).',
        resumo: 'visual identity, moodboards, mockups & design systems'
      }
    },
    'lay-devops': {
      'en': {
        use_quando: 'the request involves commits, branches, releases, tags, CI/CD pipelines, deployments, or launches.',
        nao_use_para: 'writing tests or feature functionality code.',
        resumo: 'commits, branches, CI/CD, releases & deployments'
      }
    },
    'lay-documentacao': {
      'en': {
        use_quando: 'the request involves reviewing prose, writing style audits, architectural decision records (ADRs), or text polishing for publication.',
        nao_use_para: 'code comments or inline API references.',
        resumo: 'writing guidelines, ADRs & prose polishing'
      }
    },
    'lay-engenharia': {
      'en': {
        use_quando: 'the request involves architecture, code review, root-cause debugging, refactoring, migrations, or application performance.',
        nao_use_para: 'visual UI (use lay-frontend) or CI/CD delivery (use lay-devops).',
        resumo: 'architecture, code review, debugging & refactoring'
      }
    },
    'lay-frontend': {
      'en': {
        use_quando: 'the request involves creating or reviewing UI screens, components, landing pages, layouts, or interface animations.',
        nao_use_para: 'backend, APIs, or infrastructure.',
        resumo: 'React, Next.js, accessible UI & animations'
      }
    },
    'lay-omniroute': {
      'en': {
        use_quando: 'the request involves OmniRoute, model routing, providers, combos, call costs, spending limits, or OmniRoute server configuration.',
        nao_use_para: 'application code not using OmniRoute.',
        resumo: 'OpenAI inference, model routing, combos & proxies'
      }
    },
    'lay-qa': {
      'en': {
        use_quando: 'the request involves testing, test coverage, CI failures, pre-merge validation, animated component compliance, or model benchmarks.',
        nao_use_para: 'implementing features without a testing focus.',
        resumo: 'TDD, browser automation, Playwright & QA gates'
      }
    },
    'lay-seguranca': {
      'en': {
        use_quando: 'the request involves vulnerabilities, security audits, secrets, authentication, API keys, or security scanning.',
        nao_use_para: 'implementing features without a security focus. This profile only reads and analyzes; it does not edit files.',
        resumo: 'vulnerability audits, Semgrep SAST & CVE scanning'
      }
    }
  };

  var NOTAS_PERFIL_I18N = {
    'lay-seguranca': {
      'pt-BR': 'Não edita arquivos, por instrução do perfil. Tem Bash.',
      'en': 'Does not edit files, per profile instruction. Has Bash.'
    },
    'lay-design': {
      'pt-BR': 'Não escreve código de interface. Para isso, use lay-frontend.',
      'en': 'Does not write interface code. Use lay-frontend instead.'
    }
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
    if (currentLocale === 'pt-BR' && ROTULOS_CATEGORIA_PT[catId]) {
      return ROTULOS_CATEGORIA_PT[catId];
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

  function gatilhosAgente(nome, useQuandoPt, naoUseParaPt, resumoPt) {
    if (currentLocale === 'en' && AGENTE_GATILHOS[nome] && AGENTE_GATILHOS[nome].en) {
      return AGENTE_GATILHOS[nome].en;
    }
    return {
      use_quando: useQuandoPt,
      nao_use_para: naoUseParaPt,
      resumo: resumoPt || useQuandoPt
    };
  }

  function notaPerfil(nome, fallback) {
    var item = NOTAS_PERFIL_I18N[nome];
    if (item && item[currentLocale]) return item[currentLocale];
    return fallback || '';
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
        e.preventDefault();
        e.stopPropagation();
        var lang = opt.getAttribute('data-lang');
        if (lang) {
          setLocale(lang);
          closePopover();
          btn.focus();
        }
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
    gatilhosAgente: gatilhosAgente,
    notaPerfil: notaPerfil,
    ROTULOS_CATEGORIA_PT: ROTULOS_CATEGORIA_PT,
    ROTULOS_CATEGORIA_EN: ROTULOS_CATEGORIA_EN,
    ACESSO_LABELS: ACESSO_LABELS
  };

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initLanguageSelector);
  } else {
    initLanguageSelector();
  }
})(typeof window !== 'undefined' ? window : this);
