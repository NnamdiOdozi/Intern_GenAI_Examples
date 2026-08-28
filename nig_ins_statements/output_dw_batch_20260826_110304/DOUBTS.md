# DOUBTS — sterling_fcr_2023 run 20260826_110304

_2026-08-26 11:41:32_

1. **Round 1 over-segmented / mis-split multi-page tables.** Several tables print their title+header at the bottom of one page with the data body on the next (Table 3 revenue account = pdf p11+12; Table 7 general insurance claims paid = pdf p16+17). R1 discovery created header-only stubs (T04, T13) plus separate tables for the body pages (T05 'Net Insurance Revenue' = the p12 body of Table 3; T14/T15 on p17). Fixed T04/T13 by re-extracting across both pages. **Affects:** T04/T05 and T13/T14/T15 now overlap; the Round 3 document audit is relied on to flag the duplication, and both versions are kept (not silently merged) per skill policy. A human reviewer should decide final canonical form.

2. **possible_repeat_of is noisy** — R1 sometimes put freeform sentences in this field. Treated as advisory only; not used to consolidate tables.

3. **T04 (General business revenue account, pdf p11+12) manually aligned.** After 2 retries the 235B
   model returned all 32 rows but dropped 2 mid-row cells (a blank 2021 value and an unlabelled ratio
   row), leaving ragged widths. Per skill policy (flag after 2 retries), the 2 cells were inserted by
   hand from the page image and the table accepted with a concern; Round 3 validation re-checks it.
