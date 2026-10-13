---
name: designing-industrial-brutalist-interfaces
description: >
  Designs raw industrial interfaces that fuse Swiss typographic print with tactical telemetry:
  rigid visible grids, extreme type-scale contrast, one utilitarian accent and light analog
  degradation. Use this skill when: the user explicitly asks for an industrial, brutalist, Swiss-
  print or telemetry style for a dashboard, portfolio or editorial site. Do NOT use this skill
  when: the product must follow the LAY brand identity (use governing-lay-brand-aesthetics), a
  calm minimalist or pastel look is wanted (use designing-minimalist-interfaces), or the user has
  not chosen this direction.
---

# Designing industrial brutalist interfaces

> **Atribuição:** derivada da skill `industrial-brutalist-ui` do projeto [taste-skill](https://github.com/Leonxlnx/taste-skill), de Leonxlnx, licença MIT. Adaptada ao padrão LAY: a direção só é aplicada quando o usuário a escolhe, e a identidade LAY tem prioridade.

Use this direction only when the user asks for it. It fuses Swiss typographic print with tactical telemetry: rigid visible grids, extreme type-scale contrast, one utilitarian accent and light analog degradation.

## Imperative Execution Workflow

1. [FRÁGIL] Confirm the direction and record one archetype: `swiss-print` (light substrate) or `telemetry` (dark substrate). Never mix both substrates in one interface.
2. [FRÁGIL] Fix the palette once. Light: background `#F4F4F0` or `#EAE8E3`, ink `#111111` or darker. Dark: background `#121212` or `#0A0A0A` (avoid pure `#000000`), text `#EAEAEA`. Accent `#E61919` or `#FF2A2A` is the only accent colour.
3. [FLEXÍVEL] Set the type system. Headings: heavy grotesk or extended sans, uppercase, tight tracking, leading 0.85 to 0.95, fluid size with `clamp()`. Metadata, navigation and data: monospace at 10px to 14px, generous tracking, uppercase. A serif is a rare accent and always degraded.
4. [FLEXÍVEL] Build the layout on a visible grid with CSS Grid. Separate zones with 1px or 2px rules and full-width horizontal rules. Alternate dense monospace data blocks with large calculated empty space.
5. [FRÁGIL] Set `border-radius: 0` on every element. Do not use gradients, soft shadows or translucent glass.
6. [FLEXÍVEL] Use ASCII framing (`[ SECTION ]`, `>>>`, `+` at grid intersections) and unit identifiers as structure, not as decoration over content.
7. [FLEXÍVEL] Add at most one analog effect per view: a halftone or dither pattern on a large image, CRT scanlines (dark archetype only), or a low-opacity noise layer.
8. [FRÁGIL] Verify contrast. Body text and data meet WCAG AA (4.5:1). Test the red accent on each substrate before using it for text.
9. [FRÁGIL] Keep semantics. Use `<data>`, `<samp>`, `<kbd>`, `<output>` and `<dl>` where the content matches them.

## Checklist

- [ ] One archetype and one substrate in the interface
- [ ] One accent colour, used only for emphasis
- [ ] `border-radius: 0`; no gradients or soft shadows
- [ ] Headings scale fluidly and stay legible at phone width
- [ ] Body and data text meet WCAG AA contrast
- [ ] Registration and trademark glyphs (®, ™) appear only as graphic marks, never as claims about third-party brands
- [ ] Scanline, flicker or noise animation is off under `prefers-reduced-motion`

## Boundaries

- Use `governing-lay-brand-aesthetics` when the product must carry the LAY identity.
- Use `designing-minimalist-interfaces` for calm editorial layouts with muted pastels.
- Use `applying-legacy-design-taste` only when exact taste-skill v1 behaviour is required.
