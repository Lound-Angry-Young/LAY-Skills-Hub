---
name: stripping-ai-provenance-marks
description: >
  Removes multi-vendor AI provenance marks from text and files: invisible Unicode, statistical text watermarks through rewriting, and C2PA, EXIF, XMP and container metadata on images and documents. Use this skill when: cleaning provenance marks from content the user owns or is authorized to edit. Do NOT use this skill when: the content does not belong to the user or no authorization exists, or when the goal is to hide AI authorship from a disclosure requirement or platform policy.
---

# Remove AI marks

Multi-vendor anti-detection hygiene for **text** (Unicode + statistical rewrite) and **files** (C2PA / AI metadata across common containers).

Read if needed:

- `references/mark-classes.md` — Unicode / sampling / C2PA / containers
- `references/vendor-notes.md` — Claude, Gemini/SynthID, OpenAI, open-LLM
- `references/removal-matrix.md` — which layer when
- `references/ethics.md` — intended use
- `references/how-claude-marks.md` — Anthropic-specific detail
- `references/markdiffusion.md` — optional MarkDiffusion image harness (schemes, honesty caveats)

This skill is a **thin client**. All deterministic cleaning machinery runs in a
separate HTTP service (this repo's `service/`), so the agent host needs no
Python, venvs, or cleaning tools. Call the service with `curl`; never run
cleaning scripts directly.

## Sections
- Service access
- HTTP API (curl)
- Ethics
- Workflow
- Limitations
- Service not reachable?

## Reference Documentation
Consulte a documentação técnica completa: [Referência Técnica](reference.md).
