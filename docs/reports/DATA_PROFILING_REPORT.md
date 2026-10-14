# CareerLens AI — Dataset Profiling & Matching Engine Report

**Document Version:** 1.0  
**Date:** 2026-10-14  
**Audit Executable:** [`scripts/audit_dataset.py`](file:///c:/Users/panpe/Downloads/careerlens-ai/scripts/audit_dataset.py)  
**Test Suite:** [`tests/test_matching.py`](file:///c:/Users/panpe/Downloads/careerlens-ai/tests/test_matching.py)  
**Status:** Completed & Empirically Verified  

---

## 1. Executive Summary

This report documents the completion of the **data-audit stage** for CareerLens AI. All tasks outlined in the brief have been implemented and verified:
1. The Job Skill Set dataset was loaded, verified, and profiled using lightweight standard tooling (`pandas`, `pyarrow`, `urllib.request`).
2. The schema, data types, missing value counts, uniqueness, and category distributions were empirically audited.
3. The format of `job_skill_set` was analyzed from raw data (stringified Python lists of skills).
4. A small, deterministic skill normalizer and parser was implemented in [`backend/matcher.py`](file:///c:/Users/panpe/Downloads/careerlens-ai/backend/matcher.py), maintaining original display strings for UI presentation while performing canonical token comparison.
5. Missing values, empty sets, duplicate skills, and syntax anomalies are safely handled.
6. The baseline career matching algorithm was defined, implemented, and covered by a comprehensive automated test suite (25/25 passing tests).
7. Dataset attribution and CC BY-SA 4.0 licensing limitations are recorded.

---

## 2. Empirical Dataset Profile & Integrity Findings

The audit was executed via `python scripts/audit_dataset.py` against the cached benchmark Parquet file:
- **Local Cache Location:** `.cache/dataset/train-00000-of-00001.parquet`
- **File Size:** 2,515,687 bytes (~2.4 MB)
- **Source:** Hugging Face `batuhanmtl/job-skill-set`

### 2.1 Volume, Schema & Quality
| Column Name | Storage Type | Pandas Dtype | Missing Count | Quality Check |
|---|---|---|---|---|
| `job_id` | `int64` | `int64` | 0 | 100% unique (1,167 distinct IDs, 0 duplicates) |
| `category` | `string` | `object` | 0 | 100% complete across 5 balanced domains |
| `job_title` | `string` | `object` | 0 | 100% complete, distinct job titles |
| `job_description` | `string` | `object` | 0 | 100% complete, detailed English text |
| `job_skill_set` | `string` | `object` | 0 | 100% complete, stringified list representation |

- **Total Rows:** 1,167
- **Duplicate Rows:** 0 (Entire dataset is unique)

### 2.2 Category Distribution
The dataset is well-balanced across 5 primary functional domains:

| Category | Record Count | Percentage |
|---|---|---|
| `INFORMATION-TECHNOLOGY` | 240 | 20.57% |
| `BUSINESS-DEVELOPMENT` | 239 | 20.48% |
| `FINANCE` | 236 | 20.22% |
| `SALES` | 232 | 19.88% |
| `HR` | 220 | 18.85% |
| **Total** | **1,167** | **100.0%** |

### 2.3 `job_skill_set` Representation & Parsing Integrity
- **Real Examples Inspected:**
  - *Example 1 (HR, ID 3902668440):*
    ```python
    "['employee relations', 'talent acquisition', 'performance management', 'compensation and benefits', 'employment laws and regulations', 'analytical skills', ...]"
    ```
  - *Example 2 (HR, ID 3905823748):*
    ```python
    "['Talent Acquisition', 'Employee Performance Management', 'Legal Compliance', 'Payroll Processing', 'Microsoft Office', 'Policy Development', ...]"
    ```
  - *Example 3 (HR, ID 3906250451):*
    ```python
    "['Microsoft Office', 'Data analysis', 'Employee onboarding', 'Strategic thinking', 'Problem solving', 'Time management', ...]"
    ```
- **Representation Format:** Stored as Python string representations of lists containing string skill literals.
- **Parsing Robustness:** `ast.literal_eval` parses 100% of rows (0 syntax errors across 1,167 jobs).
- **Skill Quantity Statistics:**
  - Minimum skills per job: **5**
  - Maximum skills per job: **43**
  - Average skills per job: **17.85**
  - Total skill mentions: **20,833**
  - Unique canonical skills across dataset: **4,968**

---

## 3. Deterministic Skill Normalization Pipeline

Implemented in [`backend/matcher.py`](file:///c:/Users/panpe/Downloads/careerlens-ai/backend/matcher.py):

### 3.1 Normalization Strategy (`normalize_skill`)
1. **Trimming & Casing:** Strips whitespace, quotes, and converts characters to lowercase.
2. **Whitespace & Delimiter Unification:** Collapses internal hyphens (`-`), underscores (`_`), and whitespace into single spaces (`re.sub(r"[\s\-_]+", " ", s)`).
   - `"Problem-Solving"` $\rightarrow$ `"problem solving"`
   - `"Machine Learning "` $\rightarrow$ `"machine learning"`
   - `"front-end development"` $\rightarrow$ `"front end development"`
3. **Symbol Preservation:** Preserves critical technology identifiers:
   - `C++` $\rightarrow$ `c++`
   - `C#` $\rightarrow$ `c#`
   - `Node.js` $\rightarrow$ `node.js`
   - `.NET Core` $\rightarrow$ `.net core`
4. **Display Fidelity:** The matcher compares canonical tokens internally, but **returns original display strings** from the job record (e.g., `"Human Resources Management"`, `"Microsoft Office"`).

### 3.2 Robust Parser (`parse_skill_set`)
Handles:
- Stringified Python lists (`"['Python', 'SQL']"`) via `ast.literal_eval`.
- JSON array strings (`'["Python", "SQL"]'`) via `json.loads`.
- Delimited strings (`"Python, SQL; Git"`) via regex split.
- Native Python lists/tuples/sets.
- Missing values, `None`, empty strings, and malformed strings safely without throwing unhandled exceptions.

---

## 4. Matching Algorithm & Scoring Formula

### 4.1 Formula
$$\text{Match Score} = \begin{cases} 
0.0 & \text{if } |\text{Job Required Skills}| = 0 \\
\operatorname{round}\left( \frac{|\text{Matched Skills}|}{|\text{Job Required Skills}|} \times 100, 1 \right) & \text{if } |\text{Job Required Skills}| > 0
\end{cases}$$

Where:
- $\text{Matched Skills} = \text{Job Skills} \cap \text{User Skills}$ (based on normalized canonical tokens).
- $\text{Unreported Skills} = \text{Job Skills} \setminus \text{Matched Skills}$.

### 4.2 Score Boundaries & Safeguards
1. **Division by Zero Protection:** If a job record has 0 required skills, the score evaluates to `0.0` immediately without mathematical division.
2. **Deduplication Safeguard:** Repeated or duplicate user skills (`["Python", "python", "PYTHON"]`) are deduplicated during parsing so they count as exactly 1 match and cannot artificially inflate the score.
3. **Bounded Range:** Scores are strictly constrained in $[0.0, 100.0]$.
4. **Unreported Skills (Gap Analysis):** Unmatched skills are extracted directly from the structured set difference and labeled as *"Keahlian Belum Dilaporkan / Keahlian untuk Dikembangkan"* (Not Reported / Potential Skills to Develop).

### 4.3 Explicit Limitations of the Score
- **Keyword Overlap Only:** The score reflects pure skill keyword overlap between the user's input and listed job requirements.
- **Not a Hiring Probability:** The score does not measure candidate competence, cultural fit, soft skills, or likelihood of being hired.
- **Equal Weighting (MVP):** All skills listed for a job are weighted equally. In MVP, domain-critical vs. nice-to-have skill distinctions are not mathematically weighted because the benchmark dataset does not classify skill tiers.

---

## 5. Verification & Test Suite Execution

A 25-case automated test suite was developed in [`tests/test_matching.py`](file:///c:/Users/panpe/Downloads/careerlens-ai/tests/test_matching.py) and executed via `pytest`:

```text
tests/test_matching.py::TestSkillNormalization::test_basic_lowercase_and_strip PASSED
tests/test_matching.py::TestSkillNormalization::test_hyphen_and_underscore_normalization PASSED
tests/test_matching.py::TestSkillNormalization::test_tech_symbols_preserved PASSED
tests/test_matching.py::TestSkillNormalization::test_quotes_and_empty_inputs PASSED
tests/test_matching.py::TestSkillSetParsing::test_parse_python_stringified_list PASSED
tests/test_matching.py::TestSkillSetParsing::test_parse_json_array_string PASSED
tests/test_matching.py::TestSkillSetParsing::test_parse_comma_delimited_string PASSED
tests/test_matching.py::TestSkillSetParsing::test_parse_native_list PASSED
tests/test_matching.py::TestSkillSetParsing::test_parse_deduplicates_repeated_tokens PASSED
tests/test_matching.py::TestSkillSetParsing::test_parse_none_and_empty PASSED
tests/test_matching.py::TestSkillSetParsing::test_parse_malformed_syntax_fallback PASSED
tests/test_matching.py::TestCalculateMatch::test_normal_partial_match PASSED
tests/test_matching.py::TestCalculateMatch::test_perfect_100_percent_match PASSED
tests/test_matching.py::TestCalculateMatch::test_zero_percent_disjoint_match PASSED
tests/test_matching.py::TestCalculateMatch::test_empty_user_skills_safe PASSED
tests/test_matching.py::TestCalculateMatch::test_empty_job_skills_prevents_zero_division PASSED
tests/test_matching.py::TestCalculateMatch::test_user_duplicates_do_not_inflate_score PASSED
tests/test_matching.py::TestCalculateMatch::test_case_and_whitespace_insensitivity PASSED
tests/test_matching.py::TestCalculateMatch::test_preserves_original_job_casing PASSED
tests/test_matching.py::TestMatchProfileAgainstJobs::test_ranking_sort_order PASSED
tests/test_matching.py::TestMatchProfileAgainstJobs::test_category_filtering PASSED
tests/test_matching.py::TestMatchProfileAgainstJobs::test_limit_parameter PASSED
tests/test_matching.py::TestRealDatasetIntegration::test_match_against_live_dataset PASSED
tests/test_matching.py::TestRealDatasetIntegration::test_categories_summary PASSED
tests/test_matching.py::TestRealDatasetIntegration::test_missing_required_columns_error PASSED

============================= 25 passed in 1.32s ==============================
Total Coverage: 87% across backend modules
```

---

## 6. Dataset Attribution & Licensing Transparency

### 6.1 Attribution Record
- **Dataset Title:** Job Skill Set Dataset (2024)
- **Curator:** Batuhan Mutlu (`batuhanmtl/job-skill-set` on Hugging Face)
- **Extraction Tooling:** RecAI API Services (`https://recai.tech`)
- **Upstream Source:** LinkedIn Job Postings (2023 - 2024) by Arshkon on Kaggle

### 6.2 License Constraints
- The dataset is governed by the upstream Kaggle license: **Creative Commons Attribution-ShareAlike 4.0 International (CC BY-SA 4.0)**.
- **Redistribution Policy:**
  - We do **not** commit the full 2.5 MB Parquet binary into version control.
  - The application automatically downloads and caches the benchmark dataset on initialization.
  - Public UI must present clear attribution to Batuhan Mutlu, RecAI, and Arshkon.
