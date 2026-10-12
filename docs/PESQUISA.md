# Base de decisão e alcance da evidência

As instruções deste hub são uma síntese de engenharia das fontes abaixo. Elas fundamentam descoberta econômica, metadados claros, especialização condicional e teste verificável. Não demonstram que instalar todas as fontes melhora automaticamente qualquer modelo ou produto.

| Fonte | Insight aplicado | Limite |
|---|---|---|
| [Anthropic — Agent Skills best practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices) | Metadados específicos, gatilhos claros, corpo curto, referências carregadas só quando necessárias, validação | Guia de prática; limites de tamanho são recomendações. |
| [OpenAI — Skills](https://developers.openai.com/api/docs/guides/tools-skills) | `SKILL.md` com frontmatter e arquivos de apoio descobertos sob demanda | A descoberta depende do cliente e de seu contexto. |
| [OpenAI — Rethinking skills and prompts](https://developers.openai.com/blog/rethinking-skills-and-prompts-for-gpt-6-astra) | Descrições extensas e instruções globais inchadas podem prejudicar roteamento | Observação de produto/modelo; não mede este hub. |
| [Skill-MAS, arXiv 2606.18837v3](https://arxiv.org/html/2606.18837v3) | Orquestração de habilidades deve ser avaliada por trajetória/tarefa, com revisão de regras deficientes | Preprint; ganhos relatados dependem de benchmarks, avaliações, custo e modelos testados. |
| [kju.ai — Agentic AI Skills](https://kju.ai/blog/agentic-ai-skills) | Competência operacional exige julgamento crítico e tratamento de exceções | Artigo comercial sobre pessoas/agentes, não teste do formato `SKILL.md`. |
| [kju.ai — Managing AI Agents at Scale](https://kju.ai/blog/managing-ai-agents-at-scale) | Responsabilidade, revisão e medidas de correção ajudam escala | Conselhos gerenciais; números promocionais não viram evidência do instalador. |
| [Medium solicitado](https://medium.com/engineering-in-the-age-of-ai/my-approach-to-agentic-skills-e08dc6c0d1cd) | Link registrado para consulta futura | HTTP 403 durante a pesquisa; não atribuímos regras ao texto não lido. |

Os subreddits indicados pelo usuário podem sinalizar casos práticos e dúvidas atuais. Posts não substituem documentação, repositórios de origem e testes. Evite importar instruções de comentários sem verificar origem, versão e pertinência. A pesquisa necessária a um design ou ferramenta específica deve consultar fontes atuais da decisão concreta.
