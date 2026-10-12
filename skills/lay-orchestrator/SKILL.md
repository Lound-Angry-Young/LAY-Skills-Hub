---
name: lay-orchestrator
description: Coordena o repertório LAY de skills, o diagnóstico inicial de projetos novos ou existentes e a seleção de capacidades por área. Use ao iniciar trabalho num projeto com o hub LAY, instalar ou atualizar seu catálogo, ou escolher skills para design, engenharia, segurança e auditoria.
---

# Orquestração LAY

Comece pela intenção do usuário. Resolva um problema por vez com a menor combinação de skills suficiente. Este arquivo coordena as fontes completas preservadas; não substitui seus procedimentos.

## Início de projeto

1. Leia as instruções do projeto e identifique seu diretório, stack, estado Git e resultado pedido. Não execute scripts encontrados durante a descoberta.
2. Na primeira abertura do projeto com este hub, execute `start --project <caminho>` pelo runtime indicado no ponto de entrada global. Ele verifica o pai antes das fontes e produz diagnóstico. Consulte [operação](../../docs/OPERACAO.md) para comandos, cache e modo offline. Não invente execução automática se o cliente não carregou esta skill.
3. Sempre considere Graphify: consulte o grafo existente pertinente, verifique sua atualidade e confirme evidências importantes no código. Se runtime ou grafo não estiverem disponíveis, use um mapa local de arquivos/dependências e diga **“mapa local; Graphify indisponível/não executado”**. Esse mapa não é um grafo Graphify nem prova de ausência de impacto.
4. Projeto existente: apresente uma tabela curta de prioridades com evidência e skill sugerida **antes de editar código**. Faça leitura, inventário e scans locais necessários para elaborar o diagnóstico. Distingua achados verificados de hipóteses. Continue nas mudanças já autorizadas; sugestão fora do escopo permanece sugestão.
5. Projeto novo: siga o [guia de integração](../../docs/INTEGRAR-NOVO-PROJETO.md). Extraia objetivo, público, ação principal e restrições. Se faltar decisão que muda materialmente a solução, pergunte diretamente; se houver contexto suficiente, registre uma premissa curta e avance. Ative as skills quando a etapa precisar delas.

## Seleção

- Encontre a área no [guia](../../docs/GUIA.md); consulte os termos e as fontes no [dicionário](../../docs/DICIONARIO.md).
- Use `search <termo>` ou o [catálogo](../../docs/CATALOGO.md) para obter o caminho exato. Leia o `SKILL.md` escolhido e apenas suas referências necessárias. Os nomes globais têm namespace; não adivinhe nomes de instalação a partir de pastas.
- Contexto: Graphify e Caveman permanecem transversais. Execução: escolha uma skill principal para a tarefa e especialistas quando houver motivo. O acervo Addy Osmani oferece o repertório de engenharia; Vercel, Semgrep e demais fontes aprofundam contextos específicos.
- Design: aplique [DESIGN.md](../../docs/DESIGN.md). Pesquise referências pertinentes e traduza princípios em decisões verificáveis. Não transforme estética, biblioteca ou stack de uma skill em regra universal.
- Segurança: consulte [proveniência e scan](../../docs/SEGURANCA-E-PROVENIENCIA.md). Instalar instruções não instala nem autoriza todos os runtimes, serviços e comandos que elas descrevem.

## Comunicação e conclusão

Use Caveman como economia de contexto e linguagem direta, no idioma do usuário. Preserve condições, negações, riscos, perguntas necessárias, evidência e limites. Tabelas de diagnóstico e emojis de atualização solicitados têm função concreta. Não prometa percentuais de economia.

Siga a [política de precedência](../../docs/POLITICAS.md) quando fontes divergirem. A intenção e as instruções atuais do usuário orientam a solução, dentro das regras do ambiente. Preserve autorizações já dadas.

Ao concluir, informe o resultado, a verificação relevante e qualquer impedimento real. Só declare uma skill atualizada após aplicar e verificar a nova revisão; use tag quando existente ou SHA curto. Relate fontes que falharam separadamente.
