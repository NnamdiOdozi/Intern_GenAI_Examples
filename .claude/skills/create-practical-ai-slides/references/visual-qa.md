# Visual and package QA

## Before export

- Give every slide one clear primary read.
- Keep titles to one line where intended.
- Check diagram arrows, image aspect ratios, labels, footers, and appendix links.
- Confirm speaker notes and source blocks are attached to the correct slides.

## After export

1. Render every slide from the final PPTX.
2. Inspect each slide individually at full size.
3. Run the presentations overflow test.
4. Run `audit_pptx.py`.
5. Check slide count, note count, source blocks, external hyperlinks, and required or forbidden phrases.
6. Inspect all slides containing complex diagrams, screenshots, tables, or citations at original resolution.
7. Correct clipping, overlap, unexpected wrapping, stale footers, broken links, blurred assets, and empty placeholders.

For a revision, render both source and final decks and compare every slide. Only the requested slides should differ unless the user approved broader changes.

Do not deliver scratch files, inspection sidecars, or temporary renders unless requested.