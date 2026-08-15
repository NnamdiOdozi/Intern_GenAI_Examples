# Course design reference

## Communication job

Design for analytically capable professionals who may be beginners in AI, Python, APIs, software architecture, and machine learning. The deck should help them understand the technology accurately, identify practical uses, recognise risks, and experiment responsibly.

Slides are anchors for a live presenter. Do not turn them into a textbook. Prefer a low-density slide that can support several minutes of explanation.

## Source-first workflow

Inspect the entire source folder recursively. Sources may include PPTX, PDF, DOCX, screenshots, images, URLs, course notes, papers, and speaker notes. Build a source inventory before planning. Identify useful pages or slides, reusable graphics, key claims, exclusions, and gaps that require research.

Treat user-provided files as primary material. Preserve good source diagrams when permitted. Do not redraw a complex graphic merely to impose a house style. Never use an explicitly excluded source.

When internet research is needed, prefer original papers, official documentation, regulators, professional bodies, company publications, and reporting that directly supports the claim. Never embellish an organisational example. State when a conclusion is an inference.

## Narrative

Use a cumulative learning progression, normally with five visible parts:

1. What changed, and why does it matter?
2. How the technology works
3. Models, data, context, and systems
4. Tools, agents, and professional applications
5. Risks, governance, and responsible action

Adjust the labels to the course. Use section dividers. Make each part answer a question created by the previous part.

Aim for roughly 30 to 40 slides only as a planning range. Do not split one coherent topic to hit a target. Add a slide when an essential concept needs space; combine or remove repetitive material.

Include an appendix for source documents, papers, courses, articles, and useful follow-up links. Make every displayed URL a genuine PowerPoint hyperlink.

## Beginner pedagogy

Use plain language before jargon. Define abbreviations on first use. Connect unfamiliar AI ideas to familiar professional concepts. Explain what a diagram is for before discussing its internal parts.

Avoid dense boxes, paragraphs inside diagrams, tiny labels, unexplained acronyms, ambiguous examples, and unnecessary architecture detail. A beginner diagram should normally contain no more than about six essential entities.

Use realistic modern failure examples. Fabricated citations, unsupported niche facts, incorrect current information, and invented statistics are better hallucination examples than elementary geography mistakes. Label fabricated teaching examples explicitly.

## Slide writing

Use takeaway titles that express a claim, such as `An LLM builds an answer one token at a time`. Keep visible copy concise and audience-facing. Use British English unless directed otherwise.

Give each slide one narrative job. If a topic belongs together and can be explained with one strong visual, keep it on one slide. If a slide becomes crowded, reduce content or change the composition before reducing type size.

## Visual choices

Use visuals only when they clarify relationships, sequence, comparison, hierarchy, or evidence. Suitable treatments include:

- a segmented rectangle for a training pipeline;
- a probability bar chart for next-token selection;
- a sequence showing context accumulation;
- a compact architecture diagram;
- a comparison table for model types;
- an existing embedding plot or neural-network illustration;
- an authentic screenshot of a reported incident.

Simple diagrams should remain editable PowerPoint shapes. Complex source diagrams should generally be preserved as images. Use consistent arrow semantics and make bidirectional interaction visible where it matters.

## Participation and humour

Use interaction to reinforce learning: pair discussions, show-of-hands questions, next-token completion, delegation boundaries, spot-the-hallucination, or `Two truths and a hallucination`.

Use gentle, profession-aware humour rather than forced jokes. Recurring devices work well, such as an agent being a very fast graduate trainee who still needs supervision. Do not trivialise legal, regulatory, security, or ethical risks.

## Two-stage default

Unless the user says `build now`, first provide a concise source inventory and numbered slide plan with purpose, visuals, interactions, and appendix. Wait for feedback. Then create the editable deck, render every slide, inspect the output, fix defects, and deliver the final PPTX.