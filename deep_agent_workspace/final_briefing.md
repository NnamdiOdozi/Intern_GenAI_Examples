# Generative AI in insurance claims: a pragmatic briefing

## Executive view

A prudent near-term posture is to use generative AI (GenAI) primarily as a **claims-handler copilot and document-intelligence layer**, not as an autonomous decision-maker. Start with bounded, reversible tasks; retain accountable human judgment for coverage, liability, fraud, settlement and adverse-payment outcomes.

## Realistic uses and potential benefits

- **FNOL and intake:** transcribe calls, extract structured fields, identify missing information, translate and draft claimant communications. Intended benefits are less manual rekeying and faster first response; these should be proven against a baseline.
- **File understanding:** summarize chronologies across policies, correspondence, medical records, invoices and adjuster notes; retrieve relevant clauses and show supporting sources. This can reduce review time and help handlers spot open issues, but summaries may omit material facts.
- **Triage and investigation support:** classify complexity, recommend routing, highlight inconsistencies, and generate fraud or subrogation leads. These are prioritization aids—not findings of fraud, liability or misrepresentation.
- **Narrow workflows:** assist or automate tightly defined, low-complexity claims using deterministic rules and human approval. This is more defensible than open-ended autonomous adjustment.
- **Customer communication:** draft plain-language status updates and evidence requests, with approval gates and accessibility options.

Most of these workflows are **hybrid**: transcription, OCR, classification and rules may be conventional AI or software rather than GenAI. The model's exact role should be documented.

### Current evidence (company-reported)

Public evidence demonstrates feasibility, not independent proof of fairer or more accurate claim outcomes:

- **Prudential/Google Cloud (24 October 2024):** reported that a proof of concept doubled the automation rate for selected medical-claim reviews. This is not evidence of doubled end-to-end claims automation; baseline, sample and independent validation were not reported. [Source](https://www.prudentialplc.com/en/newsroom/company-news/2024/prudential-pioneers-use-of-generative-ai-for-faster-and-more-frictionless-medical-claims-in-global-first-partnership-with-google-cloud/)
- **Swiss Re (20 June 2025):** reported ClaimsGenAI supporting more than 40,000 corporate claims annually, over 1,000 potential-irregularity alerts and hundreds of additional recovery opportunities. These are activity metrics, not confirmed fraud, recoveries, savings or accuracy improvements. [Source](https://www.swissre.com/risk-knowledge/advancing-societal-benefits-digitalisation/how-generative-ai-is-transforming-insurance-claims-claimsgenai.html)
- **Allianz Australia (3 November 2025):** reported an 80% reduction in processing and settlement time for a narrowly defined food-spoilage workflow, with human payout approval. It is not an industry benchmark. [Source](https://www.allianz.com/en/mediacenter/news/articles/251103-when-the-storm-clears-so-should-the-claim-queue.html)
- **Zurich:** reported that its hybrid CATIA system identified 500 additional catastrophe claims and approximately $1.4 million in savings. Because CATIA combines traditional AI and GenAI, the result should not be attributed solely to GenAI. [Source](https://www.zurich.com/commercial-insurance/sustainability-and-insights/commercial-insurance-risk-insights/how-accurate-data-and-ai-can-transform-claims-and-help-customers-build-resilience)

## Failure modes

1. **Confabulation or omission:** invented or missing policy terms, endorsements, medical facts, dates, limits or claim history; incorrect citations; stale policy versions; bad OCR and poor scans.
2. **Bad execution:** incorrect entity matching or duplicate files; wrong routing; payment, reserve or workflow-tool errors; unauthorized external actions.
3. **Automation bias:** fluent recommendations are accepted without checking the underlying file, producing unsupported denials, payment reductions or fraud referrals.
4. **Fairness and access:** historical labels and proxy variables can produce unequal triage or investigation; language, disability, sparse records or lack of a digital channel can disadvantage claimants.
5. **Security and privacy:** PII/PHI leakage, excessive retention, insecure APIs, cross-claim disclosure, vendor training use, prompt injection through uploaded documents, and deepfake or manipulated evidence.
6. **Change and feedback risks:** silent vendor/model/prompt updates, retrieval drift, delayed outcome labels, under-represented subgroups, and human-override feedback loops.

NIST identifies GenAI confabulation, privacy, security and over-reliance risks in its [2024 GenAI profile](https://www.nist.gov/publications/artificial-intelligence-risk-management-framework-generative-artificial-intelligence). OWASP's [LLM risk guidance](https://genai.owasp.org/llmrisk/llm01-prompt-injection/) highlights prompt injection; uploaded claim documents must not be treated as trusted instructions.

## Controls that matter

- **Risk-tier the inventory.** Begin with summarization, retrieval, extraction and drafting. Do not permit autonomous denials, claim closures, payment reductions or fraud determinations without a separately justified, validated and lawful use case.
- **Ground and verify.** Restrict retrieval to current, authoritative policy and claim sources; display quoted/page-level evidence; verify citations; validate identities, dates, limits and calculations against systems of record; require abstention when evidence is missing or conflicting.
- **Make human review substantive.** Reviewers must see the underlying evidence, have authority to override, record rationale and escalate high-severity, vulnerable, conflicting or low-confidence files. Audit for rubber-stamping; a human in the loop is not a safe harbor.
- **Test outcomes, not just accuracy.** Before launch and after material changes, test known-outcome claims, ambiguity, poor scans, multilingual/accessibility cases, adversarial documents, prompt injection and manipulated images. Monitor hallucination and omission rates, false positives/negatives, overrides, delay, payment/reserve accuracy, complaints, appeals, reopened claims, settlement adequacy and subgroup disparities. Compare with a non-AI control group.
- **Protect data and operations.** Use tenant isolation, claim-level authorization outside the model, minimization/redaction, encryption, retention limits, data-location and subprocessor controls, no-training terms, DLP, logging, incident response, rollback and a kill switch. Require vendor audit and model-change notification rights, not merely a “private deployment.”
- **Preserve redress and auditability.** Retain model/prompt/retrieval versions, inputs, sources, outputs, edits, overrides, decisions and timestamps; provide appropriate notices, complaint/appeal routes, correction and non-digital access channels.

## Regulatory anchors

The **NAIC's 4 December 2023 model bulletin** covers claims, fraud and payment and says insurers remain responsible when third parties supply AI outputs; it is model guidance, not automatically binding law in every state. [NAIC bulletin](https://content.naic.org/sites/default/files/inline-files/2023-12-4%20Model%20Bulletin_Adopted_0.pdf)

The **UK FCA's 26 June 2024 Consumer Duty review** found insurers needed stronger monitoring of fair outcomes—not only timeliness and declined-claim rates—including settlement values, complaints and root causes. [FCA review](https://www.fca.org.uk/publications/multi-firm-reviews/insurance-multi-firm-review-outcomes-monitoring-under-consumer-duty)

The **EU AI Act (2024)** expressly treats life/health insurance risk assessment and pricing as high-risk; claims handling is not automatically high-risk and must be classified by actual function, profiling and material influence. [EU AI Act](https://eur-lex.europa.eu/eli/reg/2024/1689/oj/eng/pdf)

## Decision rule

Approve a pilot only where the insurer can demonstrate, against a comparable non-AI process, faster handling **without worse accuracy, fairness or claimant outcomes**, traceable evidence for material recommendations, acceptable hallucination/override/complaint rates, and a reconstructable audit trail. Treat vendor case studies as feasibility signals—not proof of claimant benefit.
