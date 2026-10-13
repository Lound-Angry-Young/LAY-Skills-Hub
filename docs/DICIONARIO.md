# Dicionário de fontes e usos

O repositório guarda **13 fontes completas** em submódulos Git: 12 URLs únicas restantes do pedido (Taste foi citado duas vezes com maiúsculas diferentes) e Graphify como dependência da skill já presente. Hyperframes foi excluído. O [registro](../registry/sources.json) guarda URL, commit, versão e caminhos; o [catálogo gerado](CATALOGO.md) lista apenas skills reais. Uma fonte sem `SKILL.md` público permanece referência documental e não ganha entrada global artificial.

| Fonte | Área e melhor uso | Limite prático |
|---|---|---|
| [addyosmani/agent-skills](https://github.com/addyosmani/agent-skills) | Repertório geral: descoberta, especificação, implementação, testes, revisão, entrega | Selecione um método por etapa; etapas não são rituais obrigatórios. |
| [semgrep/skills](https://github.com/semgrep/skills) | Revisão de segurança de código e LLM com regras e evidência | A skill orienta; a ferramenta Semgrep requer runtime/configuração próprios. |
| [Ray0907/security-scan](https://github.com/Ray0907/security-scan) | Triagem e auditoria orientada a segurança | Resultados precisam de validação; não equivale a certificação. |
| [guillaumemeyer/watermarks-remover](https://github.com/guillaumemeyer/watermarks-remover) | Edição de imagens e workflows de marca d’água | Use somente com direitos e escopo autorizados; modelo/dependências podem faltar. |
| [DietrichGebert/ponytail](https://github.com/DietrichGebert/ponytail) | Dívida técnica, revisão, ganho e auditoria | Algumas cópias `.openclaw` espelham entradas; o repositório integral permanece. |
| [diegosouzapw/OmniRoute](https://github.com/diegosouzapw/OmniRoute) | Roteamento de modelos, orçamento, chaves, MCP, observabilidade e CLI | Configurar serviços/credenciais é tarefa separada; não abra proxy só por instalar o catálogo. |
| [latent-spaces/brag](https://github.com/latent-spaces/brag) | Skill de vídeo de lançamento | Fonte preservada por constar no pedido; entrada global suspensa porque exige Hyperframes, removido. |
| [leonxlnx/taste-skill](https://github.com/leonxlnx/taste-skill) | Direções de design, identidade, interfaces e imagem de referência | Escolha uma direção para o produto; não imponha visual “anti-slop” como estética única. |
| [vercel-labs/agent-skills](https://github.com/vercel-labs/agent-skills) | React, composição, performance, interface e deploy Vercel | Regras de React/Vercel são condicionais à stack. |
| [voltagent/awesome-design-md](https://github.com/voltagent/awesome-design-md) | Biblioteca de sistemas visuais e referências de design | Sem `SKILL.md` público; a skill local `consulting-design-references` seleciona exemplos sem copiar uma marca. |
| [microsoft/playwright-cli](https://github.com/microsoft/playwright-cli) | Automação de browser e verificação de fluxo | A CLI e os navegadores exigem instalação/configuração próprias. |
| [anil-matcha/open-generative-ai](https://github.com/anil-matcha/open-generative-ai) | Repertório e projetos de IA generativa | Sem `SKILL.md` público; a skill local `architecting-generative-ai-apps` pesquisa exemplos. Aplicativos não se tornam serviços após copiar arquivos. |
| [Graphify-Labs/graphify](https://github.com/Graphify-Labs/graphify) | Fonte completa do Graphify, com runtime e referências | Para executar, prefira a variante atual da fonte; o instalador aponta a skill `generating-knowledge-graphs` para o bundle dela. |
| [tengbao/vanta](https://github.com/tengbao/vanta) | Fundos animados 3D com WebGL e Three.js (Waves, Net, Rings, Birds, Cells, Globe) | Requer Three.js/p5.js; precisa de cleanup com `destroy()` e respeito a `prefers-reduced-motion`. |
| [DavidHDev/react-bits](https://github.com/DavidHDev/react-bits) | Componentes de animação modulares para React (Text FX, SpotlightCard, Hyperspeed) | Modularidade individual; integre os componentes sem sobrecarregar bundles desnecessariamente. |
| [darkroomengineering/lenis](https://github.com/darkroomengineering/lenis) | Motor de rolagem inercial suave independente de framerate com sync GSAP | Zero dependências; sincroniza com ScrollTrigger; preserve touch nativo onde apropriado. |
| [Jakubantalik/Libraries.dev](https://github.com/Jakubantalik/Libraries.dev) | Diretório supremo de 1.000+ bibliotecas modernas para desenvolvimento web criativo | Repertório consultivo para seleção de ferramentas de 3D, áudio, física e shaders. |

## Skills locais

| Nome | Uso | Observação |
|---|---|---|
| `generating-knowledge-graphs` | Grafo de código e dependências | Versão LAY em `refactored_skills/context/generating-knowledge-graphs`; consulte a variante atual Windows/Codex na fonte completa. |
| `compressing-agent-messages` | Comunicação concisa | Versão LAY em `refactored_skills/context/compressing-agent-messages`; mantenha legibilidade e informação decisiva; porcentagem de economia não foi medida aqui. |
| `quality` | Checagens proporcionais de lint, tipos, testes e build | Adapte ao projeto; o exemplo original tem foco web. |
| `taste` | Princípios de identidade visual | Ponto de partida, não paleta ou estilo obrigatório. |
| `impeccable` | Refinamento e acessibilidade visual | Confirme contraste, teclado e comportamento no resultado. |
| `ui-ux-pro` | Usabilidade e ergonomia | Use diretrizes pertinentes à plataforma e ao público. |
| `rendering-vanta-backgrounds` | Fundos 3D WebGL com Three.js/p5.js | Destrua no unmount (`destroy()`); desligue movimento quando reduzido. |
| `animating-react-bits-components` | Microinterações e efeitos de texto em React | Efeitos como DecryptedText, BlurText, SpotlightCard e Hyperspeed. |
| `orchestrating-smooth-scroll` | Rolagem suave com GSAP ScrollTrigger | Suporte a delta-time independente de Hz e Next.js App Router. |
| `selecting-creative-libraries` | Seleção de ferramentas criativas modernas | Curadoria arquitetural a partir de 1.000+ bibliotecas do Libraries.dev. |

## Termos

- **Fonte**: clone completo com SHA e licença preservados em `upstream/`.
- **Entrada global**: `SKILL.md` curto, com namespace `lay-*`, que aponta para o arquivo original completo no bundle local.
- **Bundle**: cópia completa e versionada da fonte no diretório global `~/.lay-skills/bundles/`.
- **Repertório**: biblioteca, README ou aplicativo consultável sem `SKILL.md` público canônico.
- **Graphify executado**: grafo realmente gerado/consultado; **mapa local** é inventário provisório, rotulado como tal.
- **Atualizado**: commit novo aplicado e conferido; **já atual**, **pendente** e **indisponível** são estados diferentes.
- **Scan**: triagem heurística local; não é prova de segurança completa.
