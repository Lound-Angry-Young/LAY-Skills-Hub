---
name: debugging-root-causes
description: >
  Runs systematic root-cause diagnosis for compile failures, broken tests and unexpected behavior, without random trial-and-error attempts. Use this skill when: investigating bugs, build breaks or behavior that diverged from expectations. Do NOT use this skill when: building automatic failover or runtime service recovery (use recovering-system-errors).
---

# Diagnóstico Sistemático de Causa-Raiz

Investiga falhas de compilação, testes quebrados e regressões de comportamento através de método científico e diagnóstico sistemático (stop-the-line), rejeitando tentativas aleatórias de tentativa e erro.

## Input/Output Signature
Input:
- failureSymptom: string # Descrição do erro observado, mensagem de falha ou código de exceção
- reproductionSteps: array # Passos exatos para reproduzir a falha localmente
- relevantFilesList: array # Arquivos e módulos diretamente envolvidos no trajeto do erro
Output:
- rootCauseAnalysis: string # Explicação técnica e comprovada da causa fundamental da falha
- minimalReproductionTest: string # Teste automatizado que falha antes da correção e passa depois
- proposedFixDiff: string # Correção mínima necessária e suficiente para eliminar o defeito
- validationEvidence: string # Evidência de aprovação da suíte de testes pós-correção

## Router and Selection Matrix
| Tipo de Falha | Abordagem de Diagnóstico | Grau de Liberdade |
|---|---|---|
| Quebra de Compilação / Tipos | Rastreia assinaturas alteradas e conflitos de dependências no AST | [FRÁGIL] Exige correção exata na raiz do tipo sem uso de supressões |
| Teste de Regressão Quebrado | Isole o teste, reproduza isoladamente e inspecione diff recente | [FRÁGIL] Obrigatório regra Stop-the-line: não avançar sem teste reproduzível |
| Erro em Tempo de Execução / Nulo | Rastreia fluxo de controle e estados inválidos que originaram o nulo | [FLEXÍVEL] Adiciona asserções e checagens defensivas nos limites |
| Comportamento Não-Determinístico | Isola variáveis de ambiente, concorrência, tempo e mocks assíncronos | [FLEXÍVEL] Cria cenário reproduzível estressando condições de corrida |

## Imperative Execution Workflow
1. Aplicar Regra Stop-the-Line [FRÁGIL]:
   - Pare imediatamente qualquer adição de novas funcionalidades ou alterações especulativas no código.
2. Isolar Reprodução Mínima Determinística [FRÁGIL]:
   - Reproduza a falha com o menor número possível de passos ou escreva um teste unitário que capture o erro (vermelho).
3. Rastrear Cadeia Causal até a Causa-Raiz [FLEXÍVEL]:
   - Inspecione a pilha de chamadas, variáveis de estado e commits recentes para identificar onde a premissa falhou.
4. Formular e Aplicar Correção Mínima Focada [FRÁGIL]:
   - Implemente apenas as alterações estritamente necessárias para solucionar a causa-raiz identificada.
5. Validar com Teste Anteriormente Falho (Verde) [FRÁGIL]:
   - Execute o teste de reprodução confirmando aprovação e rode a suíte completa para afastar regressões secundárias.

## Execution Checklist
- [ ] Congelar desenvolvimento de novos recursos (Stop-the-line)
- [ ] Criar caso de teste mínimo que reproduz a falha de forma consistente
- [ ] Rastrear o defeito até a sua causa fundamental, sem remendos superficiais
- [ ] Aplicar correção atômica e minimalista
- [ ] Validar que o teste reproduzível agora passa e que a suíte geral permanece verde

## On Failure
- **Gatilho de Erro**: Correção proposta mascara o erro sem resolver a causa, falha persiste ou novos testes quebram.
- **Ação Imediata**: Desfazer a tentativa de correção imediatamente para manter o repositório limpo.
- **Rollback**: Executar `git checkout` ou `git restore` nos arquivos alterados durante a tentativa frustrada.
- **Fallback**: Expandir instrumentação de telemetria local e logs detalhados para coletar mais dados do ciclo de vida.
- **Logs**: Registrar hipótese testada, resultado observado e motivos pelos quais a hipótese foi refutada.

## Reference Documentation
Consulte a documentação técnica completa: [Referência Técnica](reference.md).
