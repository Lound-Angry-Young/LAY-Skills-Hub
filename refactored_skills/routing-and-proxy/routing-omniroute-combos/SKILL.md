---
name: routing-omniroute-combos
description: >
  Creates and manages routing combos with 19 strategies (priority, weighted, round-robin, auto-combo and more), configures fallback chains, tests routing outcomes and retrieves combo metrics. Use this skill when: designing or evaluating combo routing strategies through the API. Do NOT use this skill when: maintaining combos from the terminal (use managing-routing-combos-cli).
---

# Roteamento Inteligente com Combos e Cadeias de Fallback

Cria e gerencia combos de roteamento inteligente no OmniRoute utilizando 19 estratégias distintas (prioridade, ponderado, round-robin, menor latência, auto-combo), configurando cadeias de contingência (fallback) transparentes.

## Input/Output Signature
Input:
- comboAction: string # Ação (list, create, update, delete, test_route)
- comboIdentifierName: string # Nome único do combo de roteamento (ex: high-resilience-combo, fast-tier)
- routingStrategy: string # Estratégia de balanceamento (priority, weighted, round_robin, least_latency, cost_min)
- modelsChainList: array # Lista ordenada de modelos e conexões que compõem a cadeia de fallback
Output:
- comboConfigResult: object # Configuração estruturada do combo criado ou atualizado
- routeTestOutcome: object # Resultado da simulação de roteamento indicando o modelo selecionado
- activeComboList: array # Relação de todos os combos registrados no sistema
- executionLog: string # Registro das requisições e validações executadas

## Router and Selection Matrix
| Estratégia de Roteamento | Comportamento Operacional | Grau de Liberdade |
|---|---|---|
| Prioridade com Fallback (Priority) | Roteia sempre para o modelo primário; comuta para o secundário diante de 429/5xx | [FRÁGIL] Exige ordem estrita de precedência na cadeia de modelos |
| Balanceamento Ponderado (Weighted) | Distribui requisições proporcionalmente com base em pesos percentuais definidos | [FRÁGIL] A soma dos pesos deve totalizar exatamente 100% |
| Menor Latência Dinâmica (Least Latency) | Roteia requisições para o provedor com menor tempo de resposta p95 recente | [FLEXÍVEL] Ajusta roteamento continuamente com base na telemetria |
| Otimização Automática (Auto-Combo) | Alterna automaticamente entre modelos de alta capacidade e versões rápidas | [FLEXÍVEL] Balanceia complexidade da tarefa com custo e velocidade |

## Imperative Execution Workflow
1. Ler Combos Existentes e Estratégias Ativas [FLEXÍVEL]:
   - Consulte `GET /api/combos` para mapear os combos já configurados e evitar duplicidade de nomes.
2. Definir Cadeia de Modelos e Critérios de Fallback [FRÁGIL]:
   - Selecione os modelos participantes e ordene a cadeia garantindo que cada nó possua um substituto viável.
3. Validar Parâmetros da Estratégia Selecionada [FRÁGIL]:
   - Confirme pesos, limites de tentativas e tempos de timeout específicos para a estratégia escolhida.
4. Submeter Criação ou Atualização via API REST [FRÁGIL]:
   - Envie payload para `POST /api/combos` ou `PUT /api/combos/{id}` com autorização administrativa.
5. Executar Simulação de Roteamento (Dry-Run) [FLEXÍVEL]:
   - Teste a rota com requisição sintética e comprove que o modelo correto é acionado em condições normais e de erro.

## Execution Checklist
- [ ] Mapear modelos participantes e estratégia de balanceamento
- [ ] Validar integridade dos pesos ou prioridades da cadeia
- [ ] Submeter configuração de combo através do endpoint da API
- [ ] Simular roteamento e testar ativação de contingência
- [ ] Confirmar que o novo combo está disponível para inferência

## On Failure
- **Gatilho de Erro**: Modelo participante inexistente, pesos inválidos ou ausência de contingência na cadeia.
- **Ação Imediata**: Rejeitar a criação do combo e relatar inconsistência de parâmetros.
- **Rollback**: Restaurar a versão anterior do combo caso uma atualização tenha quebrado o roteamento.
- **Fallback**: Comutar tráfego para modelo individual direto em caso de falha no resolvedor de combos.
- **Logs**: Registrar payload do combo recusado, estratégia em conflito e erro de validação da API.

## Reference Documentation
Consulte a documentação técnica completa: [Referência Técnica](reference.md).
