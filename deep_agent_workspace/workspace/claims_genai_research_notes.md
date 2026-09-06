# Generative AI in claims operations — research notes

## Benefits (analyst)
- Strongest near-term value: human augmentation in document-heavy and communication-intensive work.
- Use cases: FNOL transcription/extraction, claim summaries/timelines, triage/routing, medical and invoice review, adjuster copilots, drafting communications, fraud/anomaly leads, subrogation recovery.
- Named/self-reported evidence: Prudential/Google Cloud reported doubled automation rate for medical claim reviews in proof-of-concept; Milliman reported 70% productivity improvement in an anonymized document-review case; Swiss Re reported 1,000+ potential irregularity alerts and additional recovery opportunities; Allstate reported large-scale AI-assisted claims communications; vendor cases report lower processing time.
- Evidence is strongest for productivity, documentation, and drafting—not autonomous coverage, settlement, or fraud decisions. Most quantified figures are company/vendor reported, not independently audited industry benchmarks.
- Recommended benefit metrics: FNOL completeness and time to first review; routing accuracy/reassignment; extraction accuracy and rework; adjuster prep time; fraud alert yield and false positives; communication timeliness/readability/repeat contacts; subrogation opportunities/recovery.

## Risks (reviewer)
- Claims contain medical/health, financial, location, legal, behavioral and fraud-investigation data. Key risks: leakage, re-identification, vendor retention/training, confidentiality/privilege, cross-tenant exposure, insecure logs/backups/subprocessors.
- GenAI adds confabulation/hallucination, omission, prompt injection, sensitive-data disclosure, opaque reasoning and model/version drift.
- Bias/discrimination can arise from proxies, historical labels, language, geography and vendor data; risk is highest for denial/payment, health, vulnerable consumers and fraud referral. Traditional automated claims enforcement cases are relevant but not proof of GenAI-specific harm.
- Governance controls: use-case classification; privacy/security impact assessment; approved enterprise environment; data minimization/redaction; vendor contracts and audit rights; source-grounded outputs; meaningful human review; fairness/outcome testing; prompt-injection and red-team testing; immutable logs; retention/deletion schedule; model inventory, validation and change management; appeal/correction routes.
- Presumptive no-go without enhanced controls: autonomous denial/payment reduction, fraud referral, medical necessity/coverage determination, unrestricted claims-repository access, public GenAI for identifiable claims data, or deployments that cannot reconstruct the decision.

## Sources cited by subagents
- NAIC AI Model Bulletin (4 Dec 2023): https://content.naic.org/sites/default/files/cmte-h-big-data-artificial-intelligence-wg-ai-model-bulletin.pdf.pdf
- EIOPA AI in insurance (13 Sep 2023): https://www.eiopa.europa.eu/publications/ai-insurance-sector-industry-adoption-and-regulatory-developments_en
- NIST AI 600-1 (26 Jul 2024): https://www.nist.gov/publications/artificial-intelligence-risk-management-framework-generative-artificial-intelligence
- EDPB Opinion 28/2024 (18 Dec 2024): https://www.edpb.europa.eu/documents/opinion-of-the-board-art-64/opinion-282024-on-certain-data-protection-aspects-related-to_en
- Prudential/Google Cloud (24 Oct 2024): https://www.prudentialplc.com/en/newsroom/company-news/2024/prudential-pioneers-use-of-generative-ai-for-faster-and-more-frictionless-medical-claims-in-global-first-partnership-with-google-cloud/
- Swiss Re ClaimsGenAI (2025): https://www.swissre.com/risk-knowledge/advancing-societal-benefits-digitalisation/how-generative-ai-is-transforming-insurance-claims-claimsgenai.html
- OWASP LLM Top 10 (2025): https://genai.owasp.org/llm-top-10/
- ICO AI/data protection guidance: https://ico.org.uk/for-organisations/uk-gdpr-guidance-and-resources/artificial-intelligence/guidance-on-ai-and-data-protection/
- EU AI Act 2024/1689: https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=celex%3A32024R1689
