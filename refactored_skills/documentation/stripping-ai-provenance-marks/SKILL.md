---
name: stripping-ai-provenance-marks
description: >
  Removes synthetic provenance markers, C2PA manifests, invisible metadata, and tool-watermark artifacts from authorized user-owned assets and media. Use this skill when: preparing authorized creative or textual assets for clean publication without synthetic provenance tags. Do NOT use this skill when: violating copyright or stripping legal attribution notices (use auditing-code-security).
---

# Remoção de Marcadores de Proveniência em Mídias

Higieniza ativos digitais e mídias autorizadas de propriedade do usuário, removendo manifestos C2PA, marcas d'água sintéticas invisíveis e metadados de ferramentas para publicação limpa e desimpedida.

## Input/Output Signature
Input:
- targetAssetFilePath: string # Caminho do arquivo de mídia ou texto a ser higienizado
- assetType: string # Tipo do ativo (image_png, image_jpeg, text_markdown, audio_wav)
- stripC2paManifest: boolean # Se deve remover blocos de metadados de proveniência C2PA (default: true)
- dryRunAuditOnly: boolean # Se verdadeiro, apenas reporta metadados encontrados sem modificar o arquivo (default: false)
Output:
- sanitizationSuccess: boolean # Status da operação de limpeza
- detectedProvenanceTags: array # Lista de manifestos e marcadores encontrados
- bytesStrippedCount: number # Total de bytes de metadados purgados do arquivo
- sanitizedAssetPath: string # Caminho do arquivo limpo resultante

## Router and Selection Matrix
| Tipo de Ativo / Metadado | Procedimento de Higienização | Grau de Liberdade |
|---|---|---|
| Imagem PNG / JPEG com C2PA | Remove chunks EXIF, XMP e blocos de manifesto C2PA sem recompressão com perda | [FRÁGIL] Preserva perfis de cor ICC e dimensões de pixels originais |
| Documento Markdown / Texto | Purgar comentários HTML ocultos, caracteres zero-width e metadados frontmatter indesejados | [FRÁGIL] Mantém formatação legível e blocos de código sem alteração |
| Ativo de Áudio / Vídeo | Remove tags ID3/RIFF de proveniência e trilhas de metadados secundárias | [FLEXÍVEL] Garante integridade das trilhas de mídia primárias |
| Modo Diagnóstico (Dry-Run) | Inspeciona cabeçalhos de arquivo e relata assinaturas de ferramentas sem alteração | [FLEXÍVEL] Modo seguro de auditoria de metadados |

## Imperative Execution Workflow
1. Inspecionar Cabeçalhos do Arquivo Alvo [FRÁGIL]:
   - Examine a estrutura de chunks e metadados em `targetAssetFilePath` identificando blocos de assinatura sintética.
2. Criar Cópia de Segurança Local [FRÁGIL]:
   - Gere backup temporário do arquivo antes de qualquer mutação binária ou textual.
3. Purgar Metadados e Marcadores de Proveniência [FRÁGIL]:
   - Remova blocos XMP, C2PA e assinaturas invisíveis utilizando manipulador seguro sem reencoding com perda.
4. Validar Integridade e Fidelidade do Ativo [FRÁGIL]:
   - Verifique que o arquivo resultante abre sem corrupção e mantém proporções, perfis de cor e resolução idênticos.
5. Substituir Arquivo ou Salvar Versão Higienizada [FLEXÍVEL]:
   - Grave o arquivo sanitizado em disco e descarte a cópia temporária de backup após confirmação de sucesso.

## Execution Checklist
- [ ] Inspecionar marcadores e manifestos presentes no arquivo
- [ ] Criar cópia de segurança antes da alteração
- [ ] Remover blocos de proveniência e metadados indesejados
- [ ] Confirmar que a mídia não sofreu perda de qualidade ou corrupção
- [ ] Registrar quantidade de bytes de metadados removidos

## On Failure
- **Gatilho de Erro**: Corrupção do arquivo durante a remoção de metadados, erro de formato binário ou falha de leitura.
- **Ação Imediata**: Interromper o processo e restaurar a cópia de segurança imediatamente.
- **Rollback**: Restaurar o arquivo original a partir da cópia de segurança criada no passo 2.
- **Fallback**: Manter o ativo original inalterado e notificar o usuário sobre a incompatibilidade do formato.
- **Logs**: Registrar o tipo de metadado que causou a falha e código de erro do analisador de mídia.

## Reference Documentation
Consulte a documentação técnica completa: [Referência Técnica](reference.md).
