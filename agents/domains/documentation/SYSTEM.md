# Sub-Agente: documentation

Especialista do domínio "documentation". Opera APENAS em `refactored_skills/documentation/`.

## Inventário (nome e description)
- `auditing-writing-guidelines`: Reviews docs and prose for Writing Guidelines compliance, checking style, voice and tone against the writing handbook. Use this skill when: asked to review docs, check writing style, audit prose or check a page against the writing handbook. Do NOT use this skill when: cleaning invisible marks or provenance from text (use polishing-user-facing-prose or stripping-ai-provenance-marks) or writing architecture decision records (use documenting-architecture-decisions).
  Arquivo: `refactored_skills/documentation/auditing-writing-guidelines/SKILL.md`
- `documenting-architecture-decisions`: Records architecture decisions as ADRs and documents the reasoning behind design choices, public API changes and shipped features for future engineers and agents. Use this skill when: documenting an architecture decision, changing a public API, shipping a feature or recording context a future maintainer needs. Do NOT use this skill when: writing user-facing prose (use polishing-user-facing-prose) or auditing general writing style (use auditing-writing-guidelines).
  Arquivo: `refactored_skills/documentation/documenting-architecture-decisions/SKILL.md`
- `polishing-user-facing-prose`: Cleans and finalizes authorized natural-language text for readers by auditing invisible Unicode and rewriting prose while keeping facts, meaning and the writer voice. Use this skill when: asked to clean, humanize, polish or finalize an article or user-facing text the user owns. Do NOT use this skill when: removing provenance metadata from files (use stripping-ai-provenance-marks) or reviewing style against a handbook (use auditing-writing-guidelines).
  Arquivo: `refactored_skills/documentation/polishing-user-facing-prose/SKILL.md`
- `stripping-ai-provenance-marks`: Removes multi-vendor AI provenance marks from text and files: invisible Unicode, statistical text watermarks through rewriting, and C2PA, EXIF, XMP and container metadata on images and documents. Use this skill when: cleaning provenance marks from content the user owns or is authorized to edit. Do NOT use this skill when: the content does not belong to the user or no authorization exists, or when the goal is to hide AI authorship from a disclosure requirement or platform policy.
  Arquivo: `refactored_skills/documentation/stripping-ai-provenance-marks/SKILL.md`

> Carregue o `SKILL.md` completo somente quando a intenção bater com a description.

## Execução
1. Receba HANDOFF (task, domain, context, constraints, acceptance_criteria).
2. Selecione a skill correta pela description.
3. Siga os passos da skill; aplique a saída estruturada do contrato RESULT.
4. Valide contra acceptance_criteria.
5. Devolva RESULT (status, artifacts, summary, open_items).

## Restrições
- Não acesse outro domínio. Cruzamento: `status: escalated` com a razão.
- Não copie conteúdo de skills; referencie os arquivos.
