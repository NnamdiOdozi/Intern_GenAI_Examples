---
name: actuarial-ml-paper-brief
description: Summarize machine-learning or AI research papers for actuaries. Build a narrative bridging from familiar methods (GLM, GBM, chain-ladder, credibility theory) to the new approach. Include worked examples, failure modes, trade-offs, and plain definitions. Output is a prose brief, not a paraphrase.
---

# Actuarial ML Paper Brief

Use this when asked to summarize a machine-learning or AI research paper for an actuary. 

**Your reader:**
- Technically strong and knows machine learning well
- Not necessarily an expert in this specific method
- Not necessarily an expert in the applied field (health claims, telematics, cyber, catastrophe modelling, or anything else)

**Core principle:** Do not just read the paper and paraphrase it. Build a narrative that starts from something the reader already knows, then bridges across to the new method.

---

## Before writing

### Read the full text of the paper, not just the abstract
If a number, a name, or a detail isn't actually stated in the paper, don't present it as fact. If you infer something rather than find it stated, say so clearly in the text itself, for example: "Inference flag: the paper doesn't say this, but..."

### Pick the right starting point

Open from a familiar modelling baseline:

- **Default:** Generalized Linear Model (GLM) — the standard tool for pricing and claims-frequency modelling, since it's the most common shared reference point for actuaries
- **If more natural:** Compare to tree-based models like GBM, chain-ladder reserving methods, or credibility theory instead
- **Selection rule:** Pick whichever familiar method makes the new one easiest to understand by contrast
- **Important:** Treat this baseline as a stand-in for "a familiar structured model," not a literal claim that GLMs are the only relevant comparison

---

## Structure, section by section

Walk through the paper's major sections in order. For each one, cover:

1. **What problem this section solves** — in a sentence or two, plainly
2. **What any tables or numbers actually mean** — in words a non-specialist would follow
3. **Why it matters in a real production setting** — not just as research
4. **The trade-off or cost of this particular design choice**
5. **A likely failure mode or edge case**
6. **One sharp, specific question a careful reader should ask** — briefly answered

### Use worked examples

Include a small worked numerical example wherever it helps make an idea concrete. If you build a numerical example that isn't from the paper itself, say so plainly, right where you use it.

### Use comparison tables

Where two competing approaches are being compared (e.g., this paper's method versus an alternative like embeddings plus a downstream classifier, or prompting versus fine-tuning), use a short comparison table instead of a paragraph.

### Explain validation claims

Whenever a paper says something was "validated," "checked," or "tested," explain plainly what that actually involved:
- How many examples?
- Who did the checking?
- What was it compared against?

Never leave a claim like that unexplained. A vague verb like "checked" is not an explanation.

---

## Language rules (this is the part that matters most)

### Write in plain, short sentences
One idea per sentence where possible.

### Define every abbreviation and piece of jargon
Define them the first time you use them, in a plain phrase, not just a technical parenthetical. Assume the reader has not read the paper and does not work in its applied field.

### Do not write to sound clever
Avoid stacking several clauses into one sentence with dashes, semicolons, or nested parentheticals. If a sentence needs to be read twice to be understood, split it into two.

### Avoid dense listing sentences
Do not cram three ideas together with semicolons. Prefer short separate sentences, or a bulleted list.

---

## Ending

Close with:

1. **Five-sentence recap** of the whole paper
2. **Short list of concepts** the reader should now be able to explain to someone else, in their own words

---

## Length

Aim for a rough word-count target if one is given, but treat it as a target, not a hard limit. If covering every required element (definitions, trade-offs, failure modes, worked examples) pushes the piece longer, let it run longer, and say so, rather than cutting required content just to hit a number.
