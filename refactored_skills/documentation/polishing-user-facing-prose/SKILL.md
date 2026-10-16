---
name: polishing-user-facing-prose
description: >
  Cleans and finalizes authorized natural-language text for readers by auditing invisible Unicode and rewriting prose while keeping facts, meaning and the writer voice. Use this skill when: asked to clean, humanize, polish or finalize an article or user-facing text the user owns. Do NOT use this skill when: removing provenance metadata from files (use stripping-ai-provenance-marks) or reviewing style against a handbook (use auditing-writing-guidelines).
---

# Polimento e Humanização de Prosa Textual

Higieniza e aprimora textos em linguagem natural para publicação: remove caracteres Unicode invisíveis ou corrompidos, ajusta cadência e clareza da escrita e preserva rigorosamente termos técnicos e a voz do autor.

## Input/Output Signature
Input:
- sourceText: string # Texto bruto a ser revisado e polido
- languageLocale: string # Idioma pretendido (pt-BR, en-US)
- preserveTechnicalTerms: array # Lista de siglas, termos de código ou nomes próprios que devem ser mantidos idênticos
- aggressiveInvisibleAudit: boolean # Se deve remover caracteres de controle e espaços de largura zero (default: true)
Output:
- polishedText: string # Texto revisado, limpo e formatado
- removedInvisibleCharsCount: number # Quantidade de caracteres ocultos purgados
- readabilityMetrics: object # Indicadores de legibilidade e tamanho médio de frases
- auditSummary: string # Resumo das correções estilísticas e estruturais aplicadas

## Router and Selection Matrix
| Tipo de Texto / Propósito | Estilo de Polimento Recomendado | Grau de Liberdade |
|---|---|---|
| Documentação Técnica / Guias | Foco em frases ativas, eliminação de rodeios e clareza instrutiva | [FRÁGIL] Exige manutenção textual idêntica de comandos e variáveis |
| Artigos e Posts Autorais | Ajuste de ritmo e cadência natural preservando a personalidade do autor | [FLEXÍVEL] Evita vocabulário corporativo genérico e clichês de IA |
| Textos com Códigos Embutidos | Isola blocos de código e formatações markdown antes do polimento | [FRÁGIL] Proibido alterar qualquer caractere dentro de crases ou cercas |
| Higienização de Caracteres Ocultos | Varredura de zero-width spaces (`\u200B`), bidi overrides e lixo UTF-8 | [FRÁGIL] Remoção incondicional de artefatos de cópia de terminal |

## Imperative Execution Workflow
1. Isolar Trechos de Código e Termos Técnicos [FRÁGIL]:
   - Proteja blocos de código com crases e termos do array `preserveTechnicalTerms` para blindá-los contra mutação.
2. Executar Varredura e Limpeza de Caracteres Invisíveis [FRÁGIL]:
   - Purgue espaços de largura zero (`\u200B`), non-breaking spaces desnecessários e caracteres de controle bidi.
3. Eliminar Frases Clichês e Prolixidade Mecânica [FLEXÍVEL]:
   - Remova termos vazios ("vale ressaltar que", "em resumo podemos dizer", "é fundamental entender") tornando as frases diretas.
4. Ajustar Ritmo Sintático e Variância de Parágrafos [FLEXÍVEL]:
   - Alterne frases curtas com frases compostas para criar leitura envolvente e livre de monotonia.
5. Reintegrar Códigos e Validar Consistência Factual [FRÁGIL]:
   - Reinsira os blocos protegidos e confirme que nenhum fato técnico ou significado foi alterado.

## Execution Checklist
- [ ] Proteger termos técnicos e blocos de código contra alteração
- [ ] Auditar e remover caracteres Unicode invisíveis e de controle
- [ ] Cortar introduções redundantes e fórmulas prolixas
- [ ] Ajustar cadência com alternância equilibrada de frases
- [ ] Validar preservação do sentido original e integridade dos dados

## On Failure
- **Gatilho de Erro**: Adulteração de comandos de código, distorção do sentido pretendido pelo autor ou corrupção de formatação markdown.
- **Ação Imediata**: Reverter as edições textuais aplicadas na frase ou parágrafo afetado.
- **Rollback**: Restaurar o texto original fornecido na entrada `sourceText`.
- **Fallback**: Realizar apenas a higienização determinística de caracteres invisíveis mantendo a redação idêntica.
- **Logs**: Registrar lista de termos protegidos que foram acidentalmente modificados e caracteres especiais detectados.

## Reference Documentation
Consulte a documentação técnica completa: [Referência Técnica](reference.md).
