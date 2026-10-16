---
name: configuring-prompt-compression
description: >
  Configures RTK (command output), Caveman (prose) and stacked compression modes, managing language packs and custom rules, and testing prompt compression that reduces tokens by 60-90%. Use this skill when: setting up or tuning prompt compression rules for an OmniRoute deployment. Do NOT use this skill when: only testing compression from the terminal (use testing-cli-prompt-compression) or changing context pipelines (use optimizing-rtk-prompt-contexts).
---

# Configuração de Compressão de Prompts

Gerencia políticas e modos de compressão de prompts no OmniRoute (RTK, Caveman e stacked), ajustando pacotes de idiomas, regras heurísticas e validação semântica para economia massiva de tokens.

## Input/Output Signature
Input:
- compressionMode: string # Modo operacional (rtk, caveman, stacked, none)
- languagePack: string # Pacote de regras linguísticas para Caveman (ex: pt-BR, en-US)
- routePrefix: string # Rota ou padrão de endpoint onde a compressão será aplicada
- dryRunTestSample: string # Prompt representativo para validação prévia de compressão
Output:
- activeConfig: object # Configuração consolidada e ativa no supervisor
- compressionRatio: number # Fator de compressão alcançado no teste de amostra
- tokenSavingsPercent: number # Percentual de tokens economizados
- status: string # Estado da operação (applied, validated, rolled_back)

## Router and Selection Matrix
| Condição / Cenário | Ação Recomendada | Grau de Liberdade |
|---|---|---|
| Saídas de Código e Terminal | Ativa compressão RTK com preservação de erros e stack traces | [FRÁGIL] Exige preservação de caminhos e números de linha |
| Diálogo em Linguagem Natural | Ativa modo Caveman conciso com Simplified Technical English | [FLEXÍVEL] Reduz pontuação e artigos sem distorcer o significado |
| Máxima Economia de Tokens | Ativa modo stacked (RTK sobre saídas CLI + Caveman em prosa) | [FRÁGIL] Requer validação estrita contra perda de contexto |
| Árvore de Acessibilidade DOM | Habilita filtro estrutural para agentes de navegação web | [FLEXÍVEL] Condensa atributos redundantes preservando seletores |

## Imperative Execution Workflow
1. Obter Configuração Atual do Supervisor [FRÁGIL]:
   - Consulte `GET /api/settings/compression` para inspecionar os filtros ativos e níveis de compressão configurados.
2. Selecionar Perfil Adequado à Carga [FLEXÍVEL]:
   - Defina o modo (`rtk`, `caveman`, `stacked`) com base no perfil da rota e tipo predominante de payload.
3. Testar Compressão com Amostra Representativa [FLEXÍVEL]:
   - Envie `POST /api/prompt/preview` com a amostra `dryRunTestSample` e avalie percentual de economia e clareza.
4. Aplicar e Persistir Novas Regras [FRÁGIL]:
   - Envie `POST /api/settings/compression` com as novas opções, language packs e rotas alvo selecionadas.
5. Auditar Integridade Semântica e Termos Técnicos [FRÁGIL]:
   - Confirme que paths, tokens de API, mensagens de erro exatas e comandos shell permaneceram inalterados.

## Execution Checklist
- [ ] Obter estado das configurações atuais de compressão
- [ ] Selecionar estratégia de compressão alinhada à carga de trabalho
- [ ] Executar preview com amostra real de prompt
- [ ] Aplicar atualização no endpoint de configuração do supervisor
- [ ] Validar integridade semântica de saídas de erro e comandos

## On Failure
- **Gatilho de Erro**: Corrupção de termos técnicos, perda de linhas de erro ou falha no endpoint de configuração.
- **Ação Imediata**: Desativar a compressão na rota afetada imediatamente.
- **Rollback**: Restaurar configuração anterior via `POST /api/settings/compression` a partir do snapshot prévio.
- **Fallback**: Comutar a rota para pass-through direto sem compressão até ajuste das regras.
- **Logs**: Registrar prompt original, versão comprimida defeituosa e contagem de tokens afetados.

## Reference Documentation
Consulte a documentação técnica completa: [Referência Técnica](reference.md).
