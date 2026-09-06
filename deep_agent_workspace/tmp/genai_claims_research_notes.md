# GenAI in claims operations — research notes

## Benefits (analyst)
- Strongest near-term value: adjuster/claims-ops copilot for document ingestion, summaries, chronology, missing info, drafting, intake and routing.
- Company-reported examples: Allstate ~50,000 claims messages/day and ~70% drafting-time reduction; AIG FNOL days to hours; Aviva/McKinsey 30% better routing accuracy and 23 fewer days for liability assessment (broader AI, not GenAI-only).
- Evidence thinner for fraud savings, reserve accuracy, autonomous adjudication, QA/leakage reduction. Often hybrid AI/ML/OCR/rules/computer vision, not GenAI alone.
- Metrics: cycle/triage/FNOL time, admin minutes, claims per FTE, extraction/routing accuracy, reopen/complaints, reserve adequacy, confirmed fraud dollars, false positives, customer effort.

## Risks/governance (reviewer)
- Sensitive health, financial, biometric/voice, geolocation, photos and third-party data; re-identification and leakage via prompts, logs, embeddings, fine tuning.
- Vendor/subprocessor, retention, secondary use and cross-border risks; confidentiality contract not enough.
- Hallucinations, bias/proxies, opaque post-hoc explanations, automation bias, adversarial prompt injection/data poisoning, security/integration risk.
- Need data minimization, approved/private deployment, no-training/no-secondary-use terms, DLP, access control, source-grounded outputs, human authority, audit logs, versioning, retention schedule, impact assessments, monitoring and fallback.
- Sources: NIST AI 600-1; NAIC AI Model Bulletin; NAIC Model Law 668; HHS HIPAA cloud/BA guidance; GDPR Articles 5/22; EU AI Act; FCA AI approach/Consumer Duty; FTC AI privacy commitments.

## Synthesis
- Start with low-risk summarization/retrieval/drafting, not autonomous adverse decisions.
- Treat capacity release as primary business case; test with control groups and quality guardrails.
- Preserve actual basis of decisions and provide escalation/redress.
