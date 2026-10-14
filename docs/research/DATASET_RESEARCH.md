# Dataset Research & Audit Report: Job Skill Set

**Document Version:** 1.0  
**Date:** 2026-10-14  
**Author:** Antigravity AI  
**Dataset Identifier:** `batuhanmtl/job-skill-set`  
**Status:** Audited & Verified  

---

## 1. Executive Summary

This document provides a comprehensive audit of the primary dataset for **CareerLens AI**: the **Job Skill Set Dataset** hosted on Hugging Face. The dataset was inspected via the Hugging Face API, dataset card, and an in-memory audit of the actual Parquet data file using `pandas` and `pyarrow`.

The audit confirms that the dataset contains **1,167 high-quality, complete job records** across **5 distinct industry categories** with **zero missing values** and **zero duplicate records**.

---

## 2. Dataset Identification & Exact Source URLs

- **Primary Repository:** [Hugging Face Datasets — batuhanmtl/job-skill-set](https://huggingface.co/datasets/batuhanmtl/job-skill-set)
- **Direct Parquet Data URL:** `https://huggingface.co/datasets/batuhanmtl/job-skill-set/resolve/main/data/train-00000-of-00001.parquet`
- **Dataset Card (README.md):** `https://huggingface.co/datasets/batuhanmtl/job-skill-set/raw/main/README.md`
- **Upstream Source:** [LinkedIn Job Postings (2023 - 2024)](https://www.kaggle.com/datasets/arshkon/linkedin-job-postings) by *Arshkon* on Kaggle.
- **Skill Extraction Provider:** [RecAI API Services](https://recai.tech) by *Batuhan Mutlu*.

---

## 3. Schema & Feature Specifications

The dataset consists of a single split (`train`) distributed as an Apache Parquet file of **2,515,687 bytes (~2.4 MB)**.

| Field Name | Storage Type | Pandas / PyArrow Type | Description & Example |
|---|---|---|---|
| `job_id` | `int64` | `int64` | Unique numerical identifier per posting (e.g., `3902668440`). |
| `category` | `string` | `object` / `string` | High-level industry category (e.g., `INFORMATION-TECHNOLOGY`). |
| `job_title` | `string` | `object` / `string` | Explicit job role title (e.g., `Sr Human Resource Generalist`). |
| `job_description` | `string` | `object` / `string` | Full-text job posting, duties, and candidate requirements. |
| `job_skill_set` | `string` | `object` / `string` | Stringified Python list of extracted skill names. |

---

## 4. Empirical Data Audit & Quality Metrics

An automated verification script executed against the live dataset yielded the following verified statistics:

### 4.1 Volume & Completeness
- **Total Records:** 1,167 rows.
- **Total Columns:** 5.
- **Missing / Null Values:** **0** across all 5 columns. Every record contains valid data for all attributes.
- **Unique Job IDs:** 1,167 (100% unique primary keys).
- **Duplicate Rows:** **0**.

### 4.2 Category Distribution
The dataset exhibits a remarkably balanced distribution across five core functional domains:

| Category | Record Count | Percentage |
|---|---|---|
| `INFORMATION-TECHNOLOGY` | 240 | 20.57% |
| `BUSINESS-DEVELOPMENT` | 239 | 20.48% |
| `FINANCE` | 236 | 20.22% |
| `SALES` | 232 | 19.88% |
| `HR` | 220 | 18.85% |
| **Total** | **1,167** | **100.0%** |

### 4.3 Skill Set (`job_skill_set`) Analysis
- **Storage Format:** Stored as string representations of Python lists, e.g.,:
  ```python
  "['employee relations', 'talent acquisition', 'performance management', 'compensation and benefits', 'employment laws and regulations', 'analytical skills']"
  ```
- **Parsing Robustness:** Tested using Python's standard library `ast.literal_eval()`.
  - Parse Success Rate: **1,167 / 1,167 (100.0%)**.
  - Parse Failures / Syntax Errors: **0**.
- **Skill Quantity per Role:**
  - Minimum skills listed: **5**
  - Maximum skills listed: **43**
  - Average skills listed: **17.9 skills per job**
- **Casing & Formatting:**
  - Contains mixed casing: e.g., `"Talent Acquisition"`, `"employee relations"`, `"Microsoft Office"`, `"HR compliance"`.
  - Whitespace: Occasional leading/trailing spaces exist within list elements.
  - Normalization Rule: Normalization must apply `.strip().lower()` for deterministic matching while preserving original string literals for UI rendering.

### 4.4 Language & Text Characteristics
- **Language:** English (job descriptions, titles, and skills are predominantly in English).
- **Localization Requirement:** In accordance with [PRD.md](file:///c:/Users/panpe/Downloads/careerlens-ai/PRD.md) and [DESIGN.md](file:///c:/Users/panpe/Downloads/careerlens-ai/DESIGN.md), the user interface, explanations, and learning roadmaps will be presented in clear, natural Indonesian, without altering the underlying English dataset records.

---

## 5. Provenance, Licensing & Redistribution Constraints

### 5.1 License Findings
1. **Hugging Face Card Declaration:** The dataset card on Hugging Face explicitly states:
   > *"Please consult the license information on the original Kaggle dataset page here (https://www.kaggle.com/datasets/arshkon/linkedin-job-postings)."*
2. **Upstream Kaggle License:** The original Kaggle dataset by Arshkon is published under the **Creative Commons Attribution-ShareAlike 4.0 International (CC BY-SA 4.0)** license.

### 5.2 Legal & Architectural Implications
- **Attribution Obligation:** Any deployment or publication must credit:
  - *Batuhan Mutlu* (Job Skill Set dataset, 2024, Hugging Face).
  - *Arshkon* (LinkedIn Job Postings dataset, Kaggle).
  - *RecAI API services* for skill parsing.
- **ShareAlike (SA) Obligation:** If modified or transformed versions of this dataset are redistributed, they must be shared under identical CC BY-SA 4.0 terms.
- **Redistribution Decision:** In strict adherence to Ponytail and security principles:
  - **Do NOT commit the 2.5MB binary Parquet file directly into Git version control.**
  - **Recommended Architecture:** Implement an automated download/caching routine in the backend service that retrieves `train-00000-of-00001.parquet` from Hugging Face on initial launch or during environment setup, caching it in a local gitignored `.cache/` or `data/` folder.
  - A small, synthetic 5-row fixture should be committed in `backend/tests/fixtures/sample_jobs.json` for deterministic offline unit testing.

---

## 6. Alignment with Product Requirements (PRD.md)

### 6.1 Deterministic Match Scoring
The baseline matching formula defined in PRD Section 9:

$$\text{Match Score} = \left( \frac{\text{Number of Matched Skills}}{\text{Total Required Skills in Job}} \right) \times 100$$

- **Zero-Division Safeguard:** If a job record has an empty skill set ($N = 0$), return a score of $0.0$ and log a diagnostic warning.
- **Duplicate Protection:** Duplicate skills submitted by the user must be deduplicated via `set()` normalization before matching so they cannot artificially inflate scores.
- **Non-Reported Skills (Gap Analysis):**
  $$\text{Unreported Skills} = \text{Job Skills} \setminus \text{User Matched Skills}$$
  In accordance with PRD Section 6.3, these must be explicitly labeled as **"Belum dilaporkan / Keahlian untuk dikembangkan"** (Not reported / Potential skills to develop), **never** as confirmed deficiencies or missing capabilities.
- **Career Disclaimer:** The UI must display a visible disclaimer clarifying that skill overlap is a measure of keyword correlation, not a probability of employment or hiring guarantee.

### 6.2 Grounding LLM Generation
Gemini API prompts must receive:
1. The exact job title and category.
2. The relevant snippet of the official job description.
3. The deterministic matched skills and unreported skills calculated by Python.
4. An instruction to answer strictly based on the supplied context and generate learning roadmaps in Indonesian without inventing compensation, live vacancies, or external market stats.
