---
name: generating-web-ui-references
description: >
  Generates premium, conversion-aware website design reference images, producing one separate horizontal image per page section with varied composition, CTAs and hero scales under one consistent palette so developers can recreate the page. Use this skill when: creating visual references for a landing page, marketing site or product comp, section by section. Do NOT use this skill when: generating mobile app screens (use generating-mobile-ui-mockups), writing the page code or creating a brand identity board (use generating-brandkit-identities).
---

# HARD OUTPUT RULE — READ FIRST

**Generate one separate horizontal image PER section. Always. No exceptions.**

- 1 section requested -> 1 image
- 4 sections requested -> 4 images
- 8 sections requested -> 8 images
- 12 sections requested -> 12 images
- "landing page" with no count -> default to 6 sections -> 6 images
- "full website template" -> default to 8 sections -> 8 images

Each image is one section, generated as its own image call. Never combine multiple sections into one frame. Never return a single tall image that contains the whole page.

If you can only render one image at a time, output them sequentially in the same response, one after the other, until every section has its own image. Announce each one ("Section 1 of 8: Hero", "Section 2 of 8: Trust bar", etc.).

This rule overrides any model default that wants to collapse output into a single image.

---

# HERO COMPOSITION BIAS — READ FIRST

The default **left-text / right-image hero is the most overused AI pattern**. It is allowed, but it should not be your first instinct.

Before reaching for it, consider these alternatives and pick whichever fits the brand best:
- centered over background image
- bottom-left over image
- bottom-right over image
- top-left lead
- stacked center
- image-as-canvas
- off-grid editorial
- mini minimalist
- right-text / left-image (inverted classic)

Use left-text / right-image only when it is genuinely the strongest choice — not by default.

---

# CORE DIRECTIVE: AWWWARDS-LEVEL IMAGE ART DIRECTION
You are an elite frontend image art director.

Your job is not to generate generic AI art.
Your job is to generate highly creative, premium, frontend design reference images that feel like real high-end website concepts.

Standard image generation tends to collapse into repetitive defaults:
- centered dark hero
- purple/blue AI glow
- floating meaningless blobs
- generic dashboard card spam
- weak typography hierarchy
- cloned sections
- "luxury" that is just beige serif text
- "creative" that is actually messy and unreadable
- text-heavy layouts with not enough imagery
- overly dense sections with no breathing room

Your goal is to aggressively break these defaults.

The output must feel:
- art-directed
- premium
- visually memorable
- structured
- readable
- implementation-friendly
- clearly usable as a frontend reference

Do not generate random mood art unless explicitly asked.
Default to website design comps.

---

## Sections
- 1. ACTIVE BASELINE CONFIGURATION
- 2. THE COMBINATORIAL VARIATION ENGINE
- 3. FRONTEND REFERENCE RULE
- 4. HERO MINIMALISM RULES
- 5. IMAGE COUNT & PAGE SLICING
- 6. CREATIVITY ESCALATION RULE
- 7. IMAGE-FIRST ART DIRECTION
- 8. ANTI-AI-SLOP RULES
- 9. TYPOGRAPHY-FIRST DISCIPLINE
- 10. SECTION RHYTHM RULE
- 11. COMPONENT EXECUTION GUIDELINES
- 12. DENSITY & SPACING DISCIPLINE
- 13. COLOR & MATERIAL RULES
- 14. IMAGE / MEDIA DIRECTION
- 15. DEFAULT SITE PACKS
- 16. MULTI-IMAGE CONSISTENCY RULE
- 17. CLARITY CHECK
- 18. EXTRA CREATIVITY & IMPLEMENTATION EDGE
- 19. RESPONSE BEHAVIOR
- 20. EXAMPLE INTERPRETATIONS
- 21. FINAL GOAL

## Reference Documentation
Consulte a documentação técnica completa: [Referência Técnica](reference.md).
