# LlamaCloud design choices

## 2026-09-01 — Preserve real page context and provenance

The first ten-page benchmark concatenated selected table-bearing pages into a smaller PDF. This made the test inexpensive, but it removed some continuation pages and created artificial adjacency between unrelated source pages.

The active scripts now upload the original PDF and use LlamaCloud's page-range controls. Parse receives `page_ranges.target_pages`. Extract receives `target_pages`. This keeps the configured windows intact. Parse item page numbers refer directly to the PDF viewer. Extract page fields remain model-generated claims and must not be treated as authoritative provenance.

The installed `llama-cloud` 2.15.0 Extract configuration does not expose the older `num_pages_context` option. The implementation therefore uses contiguous source-page windows rather than sending an unsupported field.

## 2026-09-01 — Make silent Extract losses visible

The first run showed that Parse could reconstruct a table while Extract omitted it or detached its header. Table 8 on PDF pages 17–18 was the clearest example.

The shared prompt now requires separate handling of adjacent tables, explicit joining of continuations, preservation of repeated versions, and a final visible-table check. The Extract schema records the row's source page, every page belonging to the logical table, and the printed state of each cell.

LlamaCloud returned schema integer values as JSON numbers such as `1.0`. The old `isinstance(value, int)` check therefore discarded every local source-page mapping. Page values are now normalized only when they are integral and belong to the configured page range.

Prompting and schema constraints cannot prove completeness on their own. Each run must still compare the Parse table inventory against the Extract table inventory and visually inspect any mismatch.

## 2026-09-01 — Focused rerun result

The pages 11–14 and 16–19 Parse job returned all eight requested pages and 16 native table items. It preserved both fragments of Table 3, the 2022 class table, Table 7, and Table 8. The requested merge option did not combine cross-page fragments. Adjacent fragments therefore still need deterministic stitching before workbook export.

The equivalent Extract job returned 85 row objects across nine table labels. It omitted Table 7 and Table 8. Its model-generated page fields were also wrong for several tables. For example, retention tables visibly located on page 16 were labelled as page 11. The response contained no citation metadata even though citations and confidence scores were enabled.

The accepted source for complete table discovery and page provenance is therefore Parse's `items` tree. This follows LlamaCloud's financial-report guidance, which recommends walking table items and tagging them with each item's page number. Extract remains useful for optional semantic reshaping, but its output must be rejected when its inventory does not match Parse.

## 2026-09-01 — Full-document Parse result

The 52-page Agentic Parse returned every page, 62 table items, and 518 native rows. Every exported CSV exactly matched its native row array, and every native table Markdown block appeared in the page Markdown. This confirms that Markdown, rows, and CSV are consistent representations of one Parse result rather than competing extraction methods.

Continuation merging was selective. Llama merged pages 18–19 and 21–22, but left other clear continuations split. Focused and full-document runs also differed in row labelling, dash characters, header cleanup, and chart-derived values. Native rows are therefore the correct workbook substrate, but not audited financial data. The workbook stage must stitch fragments deterministically and reject approximate tables inferred from charts when an exact source table exists.
