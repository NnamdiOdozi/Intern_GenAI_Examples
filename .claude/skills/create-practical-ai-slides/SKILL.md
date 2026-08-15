---
name: create-practical-ai-slides
description: Create clear, sourced, beginner-friendly Practical AI training presentations from folders containing PowerPoint decks, PDFs, Word documents, images, notes, and links. Use for source discovery, course planning, AI teaching narratives, editable PowerPoint generation, speaker notes, citations, hyperlinks, diagrams, audience activities, and final visual QA.
---

# Create Practical AI Slides

Create an editable, source-grounded training deck for intelligent professionals who may have limited software engineering, AI, Python, or machine-learning experience.

## Route the work

1. Use the available presentations skill for every PPTX creation or edit. Follow its complete implementation and render-and-verify workflow.
2. Use the PDF and documents skills when those formats are present.
3. Use image generation only when a new bitmap visual is genuinely needed. Prefer strong user-provided diagrams and screenshots over recreating them.
4. Read `references/course-design.md` before planning the course.
5. Read `references/ai-training-content.md` when selecting or explaining AI topics.
6. Read `references/artifact-tool-patterns.md` before writing presentation JavaScript.
7. Read `references/visual-qa.md` before final validation.

## Discover sources

Run `scripts/inventory_sources.py <source-folder> --output <tmp-dir>/source-inventory.json`.

Inspect all potentially relevant files recursively. Review PowerPoint speaker notes, PDF pages, Word content, supplied screenshots, URLs, bibliographies, and explicit exclusions. Record source provenance in the presentation workspace. Do not use an excluded source.

For a large source collection with independent file groups, delegate read-only inspection to parallel subagents when available. Keep one main course architect and one PowerPoint writer. Never allow several agents to edit the same deck concurrently.

## Plan before building

Unless the user explicitly says `build now`, first return a concise source inventory and a proposed numbered slide plan. Use approximately five visible sections and give each slide one narrative job. Include suggested visuals, interactions, and appendix resources. Wait for approval before building.

Do not chase a slide-count target by splitting coherent topics. Prefer one strong slide over two weak slides. Treat slides as presentation anchors rather than a textbook.

## Research accurately

Browse when claims are current, organisation-specific, regulated, niche, or explicitly requested. Prefer primary sources, regulators, official documentation, research papers, and direct reporting. Distinguish user statements, source-supported facts, and inference. Label hypothetical architectures, fabricated examples, and illustrative probabilities clearly.

## Build the deck

Use `@oai/artifact-tool` through JavaScript ES modules, as required by the presentations skill. Keep text concise, define abbreviations, use British English by default, and use takeaway-style titles.

Design for beginners:

- Use one main idea per slide.
- Keep diagram labels short.
- Use native shapes only for simple diagrams.
- Reuse high-quality complex source graphics without flattening their meaning.
- Add working PowerPoint hyperlinks, not merely styled URL text.
- Add presenter notes and `[Sources]` blocks for non-trivial claims and external assets.
- Include light interaction or humour only when it reinforces learning.

Use `scripts/inspect_deck.mjs` from an initialized artifact-tool workspace when focused source-deck inspection is helpful.

## Validate

Render every slide from the final PPTX. Inspect each at full size. Run the presentations skill's overflow test, then run:

```text
python scripts/audit_pptx.py <final.pptx> --require-source-blocks
```

Check slide count, notes, sources, hyperlinks, excluded material, image crops, text wrapping, footers, appendix links, and unresolved placeholders. Correct all unintended overlap and clipping before delivery.

Deliver only the final editable PowerPoint and a short summary of the result, sources, slide count, and any unresolved verification limitations.