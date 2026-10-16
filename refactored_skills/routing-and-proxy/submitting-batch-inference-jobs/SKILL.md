---
name: submitting-batch-inference-jobs
description: >
  Submits and monitors batch inference jobs from the CLI, uploads files for batch processing, retrieves results and integrates batch pipelines with CI/CD workflows. Use this skill when: running large batches of inference from the terminal or a CI pipeline. Do NOT use this skill when: sending single real-time requests (use executing-omniroute-inference).
---

# Submissão e Monitoramento de Lotes de Inferência (Batch)

Submete, acompanha e extrai resultados de processamento em lote de inferência (Batch Inference) a partir do CLI do OmniRoute: upload de arquivos JSONL, monitoramento de progresso assíncrono e download de saídas com desconto de custo.

## Input/Output Signature
Input:
- batchInputFilePath: string # Caminho do arquivo JSONL contendo as requisições em lote
- targetModelIdentifier: string # Modelo de IA selecionado para o processamento em lote
- completionWindowHours: number # Janela máxima de tempo para conclusão do lote (default: 24)
- autoDownloadResults: boolean # Se deve aguardar e baixar o arquivo de resultados automaticamente (default: false)
Output:
- batchJobId: string # Identificador único do job de lote atribuído pelo provedor
- batchStatus: string # Estado atual do job (validating, in_progress, completed, failed)
- processedRequestsCount: number # Quantidade de requisições processadas no lote
- resultsOutputFilePath: string # Caminho onde o arquivo de resultados foi gravado

## Router and Selection Matrix
| Operação de Lote | Comando CLI Recomendado | Grau de Liberdade |
|---|---|---|
| Submissão de Novo Arquivo de Lote | Executa `omniroute batches create --file <path> --model <model>` | [FRÁGIL] Exige validação estrita de sintaxe JSONL antes do upload |
| Monitoramento de Progresso de Job | Executa `omniroute batches status <jobId>` exibindo percentual | [FLEXÍVEL] Acompanha evolução sem sobrecarregar a API com polling rápido |
| Download de Resultados Concluídos | Executa `omniroute batches download <jobId> --output <path>` | [FRÁGIL] Valida integridade do arquivo de resultados baixado |
| Cancelamento de Lote em Execução | Executa `omniroute batches cancel <jobId>` interrompendo o processamento | [FRÁGIL] Ação imediata para estancar custos em lotes incorretos |

## Imperative Execution Workflow
1. Validar Sintaxe do Arquivo de Entrada JSONL [FRÁGIL]:
   - Verifique que cada linha do arquivo `batchInputFilePath` é um objeto JSON válido contendo `custom_id` e `body`.
2. Disparar Submissão do Job via CLI [FRÁGIL]:
   - Execute `omniroute batches create` enviando o arquivo e capturando o `batchJobId` gerado.
3. Acompanhar Status do Processamento com Intervalo Seguro [FLEXÍVEL]:
   - Consulte o status periodicamente (polling a cada 60s) respeitando os limites da API do provedor.
4. Baixar Arquivo de Saída ao Concluir [FRÁGIL]:
   - Quando o status transitar para `completed`, dispare o download do arquivo de resultados para o disco local.
5. Auditar Erros Parciais nos Registros de Saída [FLEXÍVEL]:
   - Inspecione as linhas do arquivo baixado identificando eventuais requisições individuais que falharam.

## Execution Checklist
- [ ] Validar conformidade de formato de cada linha do arquivo JSONL
- [ ] Submeter o arquivo de lote via comando CLI
- [ ] Monitorar a evolução do processamento do job de lote
- [ ] Baixar os resultados concluídos para o caminho especificado
- [ ] Checar taxa de sucesso e erros parciais nas respostas geradas

## On Failure
- **Gatilho de Erro**: Arquivo JSONL malformatado, limite de taxa de upload excedido ou cancelamento pelo provedor.
- **Ação Imediata**: Pausar a submissão e validar as linhas do arquivo localmente com validador JSON.
- **Rollback**: Se o lote for submetido com erros conceituais, disparar `omniroute batches cancel` imediatamente.
- **Fallback**: Dividir o arquivo de lote grande em lotes menores com menor contagem de requisições.
- **Logs**: Registrar número da linha com erro de sintaxe, ID do lote cancelado e mensagem de erro do provedor.

## Reference Documentation
Consulte a documentação técnica completa: [Referência Técnica](reference.md).
