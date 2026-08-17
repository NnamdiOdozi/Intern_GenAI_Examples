import csv

ts = open('/tmp/ifoa_batch2_ts.txt').read().strip()
out_path = f"/home/nodozi/projects/Intern_GenAI_Examples/ifoa_downloads/output/IFOA_AI_Papers_{ts}_batch2.csv"

header = [
    "S/N", "Topic", "Sub-topic", "URL", "Description", "Comments",
    "Date of publication (dd/mm/yyyy)", "Authors", "Area of practice",
    "Dataset (real/simulated; granularity)", "Dataset modality",
    "Code available? (language; link if any)",
    "ML/AI technique (granular label)",
    "Learning paradigm & task (supervised/unsupervised/etc; regression/classification)"
]

rows = [
    [
        "1",
        "Forecasting & Asset Projections",
        "Capital market assumption setting",
        "N/A",
        "Short IFoA magazine preview article (for the IFoA Asia Conference 2023 presentation) describing a machine learning-based quantitative model to identify commonalities among target companies for investment screening, plus NLP (named entity recognition) applied to companies' disclosures, prospectuses and annual reports to extract key financial/non-financial indicators and assess innovative ability, supporting credit ratings, ESG screening, and audit applications.",
        "This is a brief conference-preview/blog-style article, not a full technical paper - no methodology detail, no results, no dataset specifics, no code or citations provided. Extracted fields reflect what little is stated; most technical fields are N/A due to lack of detail in source.",
        "01/09/2023",
        "Muqiu Liu (Delta Analytics); Estelle Xu (Delta Analytics); Chengcheng Wang (China Universal Asset Management)",
        "Investment / Asset Management",
        "Inference: real (company disclosures, prospectuses, annual reports); granularity N/A - no dataset size, time period, or company count stated",
        "Text (unstructured financial disclosures, prospectuses, annual reports) and structured/quantitative company indicators",
        "N/A",
        "Machine learning-based quantitative/ranking model (unspecified algorithm) and NLP with Named Entity Recognition (NER)",
        "Inference: Unsupervised/semi-supervised for company clustering & ranking; NLP extraction task (NER) is not explicitly framed as supervised or unsupervised in the text",
    ],
    [
        "2",
        "N/A",
        "N/A",
        "N/A",
        "IFoA written submission to the UK Parliament Health and Social Care Committee's Inquiry into Food and Weight Management. Discusses GLP-1/anti-obesity medications (e.g. semaglutide, tirzepatide), their clinical effectiveness, cost, uptake trends, and implications for insurance, pensions, public policy and the healthcare landscape. Sourced from a Swiss Re Actuary magazine article and an LCP Think Piece.",
        "This paper contains no machine learning, AI, or data-science methodology - it is a policy/clinical review document. Topic/Sub-topic, Dataset, ML/AI technique, and Learning paradigm fields are N/A as this paper falls outside the AI/ML taxonomy scope entirely (included only because it was named in the assigned batch).",
        "13/11/2025",
        "N/A (authored/submitted by the IFoA; content sourced from a Swiss Re article in The Actuary magazine and an LCP Think Piece for the IFoA; contact given: Caroline Winchester)",
        "Health / Life & Pensions / Public Policy",
        "N/A",
        "N/A",
        "N/A",
        "N/A",
        "N/A",
    ],
]

with open(out_path, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(header)
    writer.writerows(rows)

print(out_path)
print(f"rows written: {len(rows)}")
