---
name: grounding-source-documentation
description: >
  Grounds implementation decisions in official documentation: verifies an approach against the docs before implementing and produces source-cited code free from outdated patterns. Use this skill when: verifying an approach against official docs, or building with a framework or library where correctness matters. Do NOT use this skill when: the change is internal logic that no library documentation covers.
---

# Fundamentação em Documentação Primária de Origem

Valida decisões técnicas e padrões de código contra a documentação primária oficial das bibliotecas e frameworks, citando referências e eliminando APIs depreciadas ou inventadas por modelos de linguagem.

## Input/Output Signature
Input:
- frameworkOrLibraryName: string # Nome da biblioteca ou ferramenta (ex: react-19, nextjs-15, zod, playwright)
- targetApproachConcept: string # Abordagem, padrão ou API que se pretende utilizar no código
- currentInstalledVersion: string # Versão exata instalada no projeto (obtida do lockfile/package.json)
Output:
- verificationResult: string # Parecer de conformidade (verified, outdated, non_existent, alternative_found)
- officialDocCitation: string # Link ou citação de trecho da documentação primária consultada
- recommendedOfficialPattern: string # Exemplo canônico extraído da documentação oficial
- riskLevel: string # Nível de risco de obsolescência ou incompatibilidade (none, low, high)

## Router and Selection Matrix
| Cenário de Consulta | Ação Recomendada | Grau de Liberdade |
|---|---|---|
| Biblioteca com Major Recente (ex: React 19) | Valida breaking changes e descontinuações em relação a versões anteriores | [FRÁGIL] Exige conferência estrita de notas de versão e migration guides |
| API Incomum ou Não Canônica | Busca a assinatura no repositório oficial ou documentação antes de codificar | [FRÁGIL] Rejeita código baseado em palpites ou memória de modelos |
| Seleção de Pacote Externo | Confere se o recurso já existe de forma nativa no runtime ou stdlib | [FLEXÍVEL] Prefere recursos nativos a adicionar novas dependências |
| Consulta a Fontes Upstream Locais | Inspeciona código e documentação em `upstream/` do próprio repositório | [FLEXÍVEL] Aproveita referências cacheadas localmente no hub |

## Imperative Execution Workflow
1. Verificar Versão Exata Instalada no Projeto [FRÁGIL]:
   - Inspecione `package.json` ou o arquivo lockfile correspondente para fixar a versão alvo da biblioteca.
2. Localizar Documentação Primária Oficial [FLEXÍVEL]:
   - Consulte documentação local em `upstream/`, docs oficiais de repositórios ou sites canônicos de referência.
3. Validar Assinatura e Comportamento da API [FRÁGIL]:
   - Confirme a existência real dos métodos, parâmetros aceitos, retornos esperados e ciclo de vida.
4. Identificar Padrões Depreciados ou Anti-Padrões [FRÁGIL]:
   - Assegure que a abordagem não utilize propriedades marcadas como deprecated na versão instalada.
5. Emitir Parecer com Citação de Fonte Confiável [FLEXÍVEL]:
   - Apresente o padrão recomendado fundamentado na documentação oficial para guiar a implementação.

## Execution Checklist
- [ ] Checar a versão instalada da biblioteca no manifesto de dependências
- [ ] Consultar a documentação primária oficial para a versão correspondente
- [ ] Validar a assinatura dos métodos e parâmetros pretendidos
- [ ] Confirmar ausência de padrões obsoletos ou descontinuados
- [ ] Incluir citação da referência oficial no embasamento técnico

## On Failure
- **Gatilho de Erro**: Método inexistente na versão instalada, API depreciada ou documentação oficial contradizendo a abordagem.
- **Ação Imediata**: Vetar o uso da abordagem proposta antes que ela seja introduzida na base de código.
- **Rollback**: Descartar qualquer rascunho de código baseado na API incorreta.
- **Fallback**: Adotar o padrão canônico atual documentado na documentação oficial da biblioteca.
- **Logs**: Registrar versão da biblioteca consultada, método inválido pretendido e link da documentação de referência.

## Reference Documentation
Consulte a documentação técnica completa: [Referência Técnica](reference.md).
