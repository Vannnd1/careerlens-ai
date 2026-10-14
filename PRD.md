# CareerLens AI — Product Requirements Document (PRD)

**Document Version:** 1.0 (MVP Specification)  
**Date:** 2026-10-14  
**Status:** Approved for Implementation Planning — Grounded in Repository & Dataset Research  
**Author:** Pair Programming (Antigravity AI & Engineering Team)  

---

## 1. Product Overview & Problem Statement

### 1.1 Overview
**CareerLens AI** is an AI-assisted career exploration web application designed for university students, fresh graduates, and early-career job seekers. The platform bridges the gap between candidate qualifications and labor market expectations by comparing a user's self-reported career profile against empirical industry requirements extracted from the **Job Skill Set dataset**.

The application delivers:
1. Transparent, deterministic skill-overlap calculations.
2. Honest, non-judgmental skill-gap analysis.
3. Server-side Gemini API-powered contextual career Q&A.
4. Actionable, staged learning roadmaps generated in natural Indonesian.
5. An interactive dataset explorer providing full visibility into underlying market data.

### 1.2 Problem Statement
Job seekers entering the workforce frequently struggle with:
- **Opaque Job Requirements:** Descriptions filled with jargon make it difficult to identify concrete, learnable skills.
- **Over-engineered "Black Box" AI Tools:** Many modern career platforms present arbitrary "match percentages" or pseudo-scientific hiring probabilities that mislead candidates and invent qualifications.
- **Unclear Next Steps:** Candidates who identify a gap often do not know what practical project, tool, or portfolio exercise to pursue next.

CareerLens AI solves this by decoupling **transparent deterministic data calculation** (backend Python logic) from **explanatory synthesis** (Gemini LLM grounded strictly in calculated data and job records).

---

## 2. Target Users & Core User Stories

### 2.1 Target Personas
1. **University Student / Final Year:** Exploring prospective career paths; wants to know which tech, business, finance, or HR roles align with coursework skills.
2. **Fresh Graduate:** Actively preparing job applications; needs to identify unmentioned or undeveloped skills and prioritize what to learn over the next 4–8 weeks.
3. **Early-Career Career Switcher:** Transitioning across domains (e.g., Sales to Business Development or IT); requires clear visibility into transferable vs. domain-specific skills.

### 2.2 Core User Stories
1. **US-01 (Profile Creation):** As a user, I can input my skills (with selectable suggestions), proficiency levels (Beginner, Intermediate, Advanced), career interests, and past experience so the system can evaluate my profile.
2. **US-02 (Deterministic Matching):** As a user, I can see a ranked list of job roles matching my profile, each displaying an explainable, transparent overlap score.
3. **US-03 (Skill-Gap Inspection):** As a user, I can inspect the exact skills I matched alongside listed skills I have not yet reported, without being told I am "deficient".
4. **US-04 (Job Detail Examination):** As a user, I can inspect a job's complete record (title, category, raw description, and full skill list) directly from the dataset.
5. **US-05 (Grounded AI Career Q&A):** As a user, I can ask specific questions about a job match and receive answers grounded strictly in the official job description and my skill overlap, in natural Indonesian.
6. **US-06 (Actionable Learning Roadmap):** As a user, I can generate a staged learning roadmap (milestones, portfolio project ideas) tailored to bridge my unreported skills for a selected role.
7. **US-07 (Dataset Exploration):** As a user, I can search, filter, and inspect the raw 1,167 job records and 5 industry categories to understand the data grounding the application.
8. **US-08 (Graceful Resilience):** As a user, if the Gemini API is unreachable or unconfigured, I can still use all matching, gap analysis, and exploration features with clear system feedback.

---

## 3. Scope: MVP Features & Explicit Non-Goals

### 3.1 In-Scope MVP Features
- **Career Profile Form:** Multi-skill input with autocomplete chips, proficiency selector, freeform interests, and experience summary.
- **Deterministic Skill Matcher:** Case-normalized set-intersection engine with zero division safeguards.
- **Skill Gap Categorizer:** Clean separation between `Matched Skills` and `Belum Dilaporkan / Untuk Dikembangkan` (Not Reported / Potential Skills to Develop).
- **Dataset Explorer:** Paginated/filterable table and card view across all 5 dataset categories with real text search.
- **Server-Side Gemini Explainer:** Backend-orchestrated prompt grounding with Indonesian responses, strict guardrails against hallucinated salaries, hiring probabilities, or ungrounded statistics.
- **Staged Learning Roadmap:** 3-stage milestone generation (Fundamental, Applied/Portfolio, Advanced) focused on unreported skills.
- **State Handling & Accessibility:** Full compliance with Anti-Slop R-27 (loading skeletons, empty states, validation errors, service fallbacks) and WCAG AA contrast/keyboard access.

### 3.2 Explicit Non-Goals (Ponytail & Scope Discipline)
- **NO Database or ORM:** 1,167 records (~2.4 MB) are stored in an immutable in-memory DataFrame/cache at startup. No PostgreSQL, SQLite, or Redis.
- **NO Authentication or User Accounts:** Session state is client-side in React state or `sessionStorage`. No JWT, OAuth, or user database.
- **NO PDF Resume Scraping / Parsing:** User explicitly inputs skills via tags. No PyPDF/unstructured text extractors in the MVP flow.
- **NO Live Job Scraping:** The system uses the verified static benchmark dataset. No LinkedIn/Indeed crawlers.
- **NO Custom Machine Learning Models:** No custom PyTorch/TensorFlow embeddings or fine-tuned classifiers. Matching is deterministic set math.
- **NO Hiring Probability Claims:** Never tell the user they have an "X% chance of being hired". The score is strictly defined as "Persentase Kesesuaian Kebutuhan Keahlian" (Skill Requirement Overlap Percentage).

---

## 4. End-to-End User Flows

```
+-----------------------------------------------------------------------------------+
| 1. PROFILE INPUT                                                                 |
| User enters skills (autocomplete) + proficiency + interests + experience summary |
+-----------------------------------------------------------------------------------+
                                          |
                                          v
+-----------------------------------------------------------------------------------+
| 2. DETERMINISTIC MATCHING                                                         |
| POST /api/match -> Backend normalizes tokens, executes set intersection          |
| Returns ranked jobs with match score, matched list, and unreported list          |
+-----------------------------------------------------------------------------------+
                                          |
                                          v
+-----------------------------------------------------------------------------------+
| 3. MATCH RESULTS & JOB DETAIL                                                     |
| User filters by category, reviews ranked roles, selects target role               |
| Inspects raw description, matched skills, and potential skills to develop        |
+-----------------------------------------------------------------------------------+
                       |                                          |
                       v                                          v
+----------------------------------------+ +----------------------------------------+
| 4A. AI CAREER ASSISTANT (CHAT)         | | 4B. LEARNING ROADMAP GENERATION        |
| POST /api/chat                         | | POST /api/roadmap                      |
| User asks role-specific questions      | | Gemini generates 3-stage milestone plan|
| Gemini answers in Indonesian           | | Grounded in unreported skills & profile|
| Strictly grounded in job context       | | Practical portfolio project exercises  |
+----------------------------------------+ +----------------------------------------+
                                          |
                                          v
+-----------------------------------------------------------------------------------+
| 5. DATASET EXPLORER (PERSISTENT NAV)                                              |
| GET /api/categories & GET /api/jobs                                               |
| User searches all 1,167 records across IT, Finance, HR, Sales, & BizDev           |
+-----------------------------------------------------------------------------------+
```

---

## 5. Functional & Non-Functional Requirements

### 5.1 Functional Requirements (FR)
- **FR-01 (Skill Tokenization):** The frontend must allow users to add skills by typing and pressing Enter or selecting suggested popular skills. Skills can be removed via an accessible chip button.
- **FR-02 (Input Validation):** Skill strings must be validated: min 1 character, max 50 characters, duplicate tokens rejected, max 30 skills per profile.
- **FR-03 (Scoring Engine):** The backend must compute scores using the deterministic baseline formula:
  $$\text{Match Score} = \left( \frac{|\text{Matched Skills}|}{|\text{Job Required Skills}|} \right) \times 100$$
  The score must be rounded to 1 decimal place ($0.0\% - 100.0\%$).
- **FR-04 (Gap Labeling):** Unmatched job skills must be presented with the label *"Keahlian Belum Dilaporkan"* (Skills Not Reported). The UI must never claim the candidate "lacks" or "fails" these skills.
- **FR-05 (Contextual Grounding):** When invoking Gemini, the backend must supply:
  - Job Title and Category.
  - Job Description excerpt.
  - Matched skills list and Unreported skills list.
  - User's self-reported proficiency and career interests.
- **FR-06 (AI Language):** Gemini prompts must enforce Indonesian output for user explanations and roadmaps while citing technical skill names in their recognized English/industry standard form.
- **FR-07 (Service Isolation):** If `GEMINI_API_KEY` is invalid or unset, the API must return a structured fallback response (`ai_available: false`) with a helpful message, while keeping deterministic matching 100% operational.
- **FR-08 (Explorer Pagination & Filter):** The dataset explorer must support text search across titles/descriptions and category filtering across the 5 verified domains.

### 5.2 Non-Functional Requirements (NFR)
- **NFR-01 (Performance):** In-memory matching of 1,167 records must execute in under **50 ms** on the backend.
- **NFR-02 (Startup Speed):** Backend startup and Parquet reading into memory must take less than **2 seconds**.
- **NFR-03 (Security & Secret Management):** `GEMINI_API_KEY` must never be sent to the client, embedded in HTML, or logged in console logs. Handled exclusively via backend `.env`.
- **NFR-04 (Accessibility - WCAG AA):**
  - Minimum text contrast ratio of **4.5:1** against backgrounds.
  - Form controls with associated `<label>` elements and visible `:focus-visible` outlines.
  - Screen reader friendly chip removal (`aria-label="Hapus keahlian Python"`).
  - Keyboard accessible navigation across all interactive tabs and modals.
- **NFR-05 (Anti-Slop Visual Compliance):**
  - Zero ungrounded stats, zero fake testimonials, zero decorative bouncing animations.
  - Restrained Editorial Career Intelligence palette: high contrast neutral base, purposeful accent for primary CTAs.
  - Clear empty, loading, error, and success states across every view.

---

## 6. Dataset Schema & Skill Normalization Pipeline

### 6.1 Verified Dataset Properties (batuhanmtl/job-skill-set)
- **Total Rows:** 1,167 records.
- **Columns:**
  - `job_id` (`int64`): Primary key.
  - `category` (`string`): One of `INFORMATION-TECHNOLOGY`, `BUSINESS-DEVELOPMENT`, `FINANCE`, `SALES`, `HR`.
  - `job_title` (`string`): Official role title.
  - `job_description` (`string`): Full text overview and responsibilities.
  - `job_skill_set` (`string`): Python string literal representation of a list of skills.
- **Data Quality:** 0 nulls, 0 duplicate rows, 100% literal eval parse rate.

### 6.2 Skill Normalization Rules
To ensure robust, deterministic matching while preserving visual fidelity:
1. **Canonical Token for Matching:**
   $$\text{canonical\_token} = \text{regex\_replace}(r'[\s\-_]+', \text{' '}, \text{raw\_skill.strip().lower()})$$
   - Example: `"Problem-Solving "` $\rightarrow$ `"problem solving"`.
   - Example: `"Node.js"` $\rightarrow$ `"nodejs"` or normalized form `"node.js"` (consistent across user input and job list).
2. **Display Token Preservation:**
   The backend dictionary maintains a mapping: `canonical_token -> original_display_name`.
   When displaying matches or gaps, the official dataset casing (e.g., `"Microsoft Office"`, `"Employee Relations"`) is rendered to the user.
3. **Proficiency Level Assumption (Explicitly Documented):**
   - *User Input:* User selects `Beginner`, `Intermediate`, or `Advanced` for their skills.
   - *Matching Math:* In the MVP, **all skills are weighted equally** for the mathematical overlap score. Proficiency does **not** alter the mathematical ratio because the benchmark dataset lacks proficiency gradations.
   - *AI Utilization:* Proficiency levels **are passed to Gemini** so that the AI roadmap recommends beginner fundamentals vs. advanced architectural projects depending on the user's declared tier.

---

## 7. Mathematical Scoring Definition & Boundaries

### 7.1 Matching Formula
For a given job $J$ with required skill set $S_J = \{s_{j,1}, s_{j,2}, \dots, s_{j,m}\}$ and user profile $U$ with skill set $S_U = \{s_{u,1}, s_{u,2}, \dots, s_{u,n}\}$:

Let canonical normalized sets be:
$$\hat{S}_J = \{ \text{normalize}(s) \mid s \in S_J \}$$
$$\hat{S}_U = \{ \text{normalize}(s) \mid s \in S_U \}$$

The matched skill set is:
$$\hat{S}_{\text{matched}} = \hat{S}_J \cap \hat{S}_U$$

The match score is defined as:
$$\text{Score}(U, J) = \begin{cases} 
0.0 & \text{if } |\hat{S}_J| = 0 \\
\operatorname{round}\left( \frac{|\hat{S}_{\text{matched}}|}{|\hat{S}_J|} \times 100, 1 \right) & \text{if } |\hat{S}_J| > 0
\end{cases}$$

### 7.2 Boundary Conditions & Limitations
- **Division by Zero:** Guaranteed prevented by the $|\hat{S}_J| = 0$ guard. (In the verified dataset, minimum $|\hat{S}_J| = 5$, maximum $= 43$).
- **Score Cap:** Score is bounded in $[0.0, 100.0]$. User skills that are not part of $S_J$ do not increase or penalize the score.
- **Duplicate Input:** Deduplicated via set conversion before intersection; duplicates cannot inflate the score.
- **Mandatory UI Disclaimer:** Every score display must carry the following explanation:
  > *"Skor kecocokan ini dihitung berdasarkan persentase keahlian profil Anda yang tercantum dalam data historis posisi ini. Ini adalah indikator kesesuaian kata kunci keahlian, bukan prediksi atau jaminan penerimaan kerja."*

---

## 8. Backend API Specifications (FastAPI)

All endpoints return JSON and use standard HTTP status codes (`200 OK`, `400 Bad Request`, `422 Unprocessable Entity`, `500 Internal Server Error`).

### 8.1 `GET /api/health`
Health check and environment readiness status.
- **Response `200 OK`:**
  ```json
  {
    "status": "healthy",
    "dataset_loaded": true,
    "total_jobs": 1167,
    "gemini_configured": true
  }
  ```

### 8.2 `GET /api/categories`
List available dataset categories and job counts.
- **Response `200 OK`:**
  ```json
  {
    "categories": [
      { "id": "INFORMATION-TECHNOLOGY", "label": "Information Technology", "count": 240 },
      { "id": "BUSINESS-DEVELOPMENT", "label": "Business Development", "count": 239 },
      { "id": "FINANCE", "label": "Finance", "count": 236 },
      { "id": "SALES", "label": "Sales", "count": 232 },
      { "id": "HR", "label": "Human Resources", "count": 220 }
    ]
  }
  ```

### 8.3 `GET /api/jobs`
Searchable, paginated catalog of dataset records.
- **Query Parameters:**
  - `query` (optional string): Keyword search in title/description.
  - `category` (optional string): Filter by category.
  - `page` (int, default 1): Page number.
  - `page_size` (int, default 20, max 100): Records per page.
- **Response `200 OK`:**
  ```json
  {
    "total": 1167,
    "page": 1,
    "page_size": 20,
    "jobs": [
      {
        "job_id": 3902668440,
        "category": "HR",
        "job_title": "Sr Human Resource Generalist",
        "description_snippet": "Provides HR expertise across various functions...",
        "skills_count": 6,
        "skills": ["employee relations", "talent acquisition", "performance management", "compensation and benefits", "employment laws and regulations", "analytical skills"]
      }
    ]
  }
  ```

### 8.4 `GET /api/jobs/{job_id}`
Retrieve complete detail of a specific job record.
- **Response `200 OK`:**
  ```json
  {
    "job_id": 3902668440,
    "category": "HR",
    "job_title": "Sr Human Resource Generalist",
    "job_description": "FULL TEXT OF JOB DESCRIPTION...",
    "job_skill_set": ["employee relations", "talent acquisition", "performance management", "compensation and benefits", "employment laws and regulations", "analytical skills"]
  }
  ```
- **Response `404 Not Found`:** `{"detail": "Job record not found"}`

### 8.5 `POST /api/match`
Execute deterministic skill matching against the dataset.
- **Request Body:**
  ```json
  {
    "skills": [
      { "name": "Python", "proficiency": "Intermediate" },
      { "name": "SQL", "proficiency": "Advanced" },
      { "name": "Analytical Skills", "proficiency": "Intermediate" }
    ],
    "category_filter": "INFORMATION-TECHNOLOGY",
    "interests": "Data analysis and automation",
    "experience_summary": "1 year internship experience"
  }
  ```
- **Response `200 OK`:**
  ```json
  {
    "total_evaluated": 240,
    "matches": [
      {
        "job_id": 3906250451,
        "job_title": "Data Analyst",
        "category": "INFORMATION-TECHNOLOGY",
        "match_score": 60.0,
        "matched_skills": ["SQL", "Analytical Skills"],
        "unreported_skills": ["Tableau", "ETL", "Statistics"],
        "total_required_skills": 5
      }
    ]
  }
  ```

### 8.6 `POST /api/chat`
Contextually grounded career Q&A via server-side Gemini API.
- **Request Body:**
  ```json
  {
    "job_id": 3906250451,
    "question": "Mengapa keahlian Tableau penting untuk posisi ini dan bagaimana saya bisa memulainya?",
    "user_profile": {
      "skills": [{ "name": "SQL", "proficiency": "Advanced" }],
      "interests": "Data visualization"
    },
    "matching_context": {
      "match_score": 60.0,
      "matched_skills": ["SQL"],
      "unreported_skills": ["Tableau", "ETL"]
    }
  }
  ```
- **Response `200 OK`:**
  ```json
  {
    "job_id": 3906250451,
    "answer": "Berdasarkan deskripsi pekerjaan Data Analyst ini, Tableau digunakan untuk...",
    "grounding_sources": {
      "job_title": "Data Analyst",
      "matched_skills_count": 1,
      "unreported_skills_count": 2
    },
    "ai_available": true
  }
  ```

### 8.7 `POST /api/roadmap`
Generate a 3-stage learning roadmap focused on bridging unreported skills.
- **Request Body:**
  ```json
  {
    "job_id": 3906250451,
    "user_profile": {
      "skills": [{ "name": "SQL", "proficiency": "Advanced" }],
      "experience_summary": "Fresh graduate"
    },
    "unreported_skills": ["Tableau", "ETL", "Statistics"]
  }
  ```
- **Response `200 OK`:**
  ```json
  {
    "job_id": 3906250451,
    "job_title": "Data Analyst",
    "target_skills": ["Tableau", "ETL", "Statistics"],
    "milestones": [
      {
        "stage": "Tahap 1: Fondasi Konseptual (Minggu 1-2)",
        "skills_targeted": ["Statistics", "Tableau Basics"],
        "learning_objectives": "Memahami dasar-dasar statistik deskriptif dan antarmuka Tableau...",
        "recommended_exercise": "Membuat dashboard visualisasi data sederhana dari dataset publik."
      },
      {
        "stage": "Tahap 2: Proyek Portofolio Terapan (Minggu 3-5)",
        "skills_targeted": ["Tableau Advanced", "ETL Pipelines"],
        "learning_objectives": "Membangun alur ETL sederhana dari database SQL ke dashboard interaktif...",
        "recommended_exercise": "Mempublikasikan workbook Tableau Public yang mendemonstrasikan analisis bisnis."
      },
      {
        "stage": "Tahap 3: Pemantapan & Persiapan Karir (Minggu 6-8)",
        "skills_targeted": ["End-to-End Analytics Workflow"],
        "learning_objectives": "Mengintegrasikan seluruh pipeline dan mempersiapkan studi kasus wawancara...",
        "recommended_exercise": "Menulis dokumentasi teknis studi kasus di GitHub/LinkedIn."
      }
    ],
    "disclaimer": "Rencana belajar ini dibuat secara dinamis oleh AI sebagai referensi belajar mandiri."
  }
  ```

---

## 9. UI States & Experience Design (Anti-Slop Aligned)

In strict accordance with Anti-Slop **R-27** and **[DESIGN.md](file:///c:/Users/panpe/Downloads/careerlens-ai/DESIGN.md)**, every component and page must explicitly render:

| State | Visual Behavior & Feedback |
|---|---|
| **Initial / Empty Profile** | Clean input form with suggested skill badges (`Python`, `SQL`, `Project Management`, `Communication`). Helpful prompt explaining how matching works. |
| **Loading (Matching)** | Inline skeleton rows replacing result cards; clear text: *"Menganalisis kecocokan dengan 1,167 posisi..."* |
| **Loading (AI Chat/Roadmap)** | Restrained typing/generating indicator; send button disabled to prevent duplicate submissions. |
| **Success (Match Results)** | Ranked job cards sorted by match score. Each card shows score badge, matched chips (green border/text), and unreported chips (neutral border/text). |
| **Zero Matches Found** | Clear message explaining that no jobs in the selected category matched the entered skills; offers a 1-click option to remove category filter or add related suggestions. |
| **Validation Error** | Inline red helper text under input: e.g., *"Keahlian sudah ada dalam daftar"*, *"Nama keahlian maksimal 50 karakter"*. Form submission blocked until resolved. |
| **Backend Service Error** | Non-intrusive alert banner with human-readable error description and a *"Coba Lagi"* (Retry) button. Never exposes internal tracebacks. |
| **Gemini AI Unavailable Fallback** | Deterministic matching and job details remain fully active. The AI panel displays: *"Layanan AI sementara tidak tersedia. Anda tetap dapat melihat analisis kesesuaian dan daftar keahlian di atas."* |

---

## 10. Security, Privacy & Integrity Standards

1. **API Key Isolation:**
   `GEMINI_API_KEY` is loaded on the backend via standard environment variables or `.env`. No frontend code, Vite config, or build artifact shall ever reference this key.
2. **Untrusted Data Sanitization:**
   User text inputs (`interests`, `experience_summary`, `question`) and dataset job descriptions are treated as untrusted text:
   - Max request body size clamped to 256 KB.
   - String inputs stripped of control characters before embedding into prompt templates.
   - Prompt delimiters (e.g., `\"\"\"`) sanitized to prevent prompt injection.
3. **No PII Collection:**
   The application intentionally avoids collecting user names, email addresses, phone numbers, or addresses.
4. **Credential Leak Prevention:**
   A comprehensive `.gitignore` protects `.env`, `venv/`, `.cache/`, and temporary scratch files.

---

## 11. Acceptance Criteria & Test Plan

### 11.1 Acceptance Criteria
- [ ] **AC-01:** Parquet dataset loads reliably on backend startup into memory with zero missing rows across all 1,167 jobs.
- [ ] **AC-02:** Deterministic matching score produces identical results for identical inputs and never crashes on empty skill sets.
- [ ] **AC-03:** Unmatched skills are strictly labeled as *"Belum Dilaporkan / Untuk Dikembangkan"*, never as personal deficiencies.
- [ ] **AC-04:** AI responses from Gemini are grounded in the selected job description and calculated match context.
- [ ] **AC-05:** If Gemini API key is absent or invalid, matching and dataset exploration remain 100% operational with a graceful fallback UI.
- [ ] **AC-06:** All UI controls pass WCAG AA contrast (4.5:1) and support full keyboard-only navigation.
- [ ] **AC-07:** Anti-Slop Delivery Gate audit passes with zero fabricated stats and zero decorative animations.

### 11.2 Automated Test Plan (Backend `pytest`)
The backend must implement a comprehensive test suite in `tests/`:
1. `test_matching_normal`: Standard profile matching calculates exact expected mathematical percentage.
2. `test_matching_no_overlap`: Profile with disjoint skills returns $0.0\%$ score with empty matched list and full required list.
3. `test_matching_duplicates`: Submitting duplicate skills (`["Python", "python", "PYTHON"]`) deduplicates to one token without inflating score.
4. `test_matching_casing_and_punctuation`: Matches `"Problem Solving"` against `"problem-solving"` correctly.
5. `test_matching_empty_job_skills`: Synthetic fixture with empty skills returns $0.0\%$ without divide-by-zero exception.
6. `test_gemini_fallback`: Mocking Gemini API failure returns valid HTTP 200 fallback response with `ai_available: false`.
7. `test_dataset_integrity`: Validates in-memory dataset contains 1,167 rows, 5 categories, and valid stringified lists.

---

## 12. Dataset Attribution & Licensing Transparency

### 12.1 Required Public Attribution
The CareerLens AI application UI (Footer and Dataset Explorer modal) must prominently render the following attribution:
> **Sumber Data:** Dataset dikembangkan oleh **Batuhan Mutlu (2024)** menggunakan layanan ekstraksi **RecAI API**, bersumber dari dataset **LinkedIn Job Postings (2023 - 2024)** oleh **Arshkon** di Kaggle.  
> **Lisensi:** Berdasarkan ketentuan **Creative Commons Attribution-ShareAlike 4.0 International (CC BY-SA 4.0)**.

### 12.2 License Governance
- CareerLens AI does not redistribute the raw dataset as a proprietary asset.
- The backend downloads and caches the public benchmark file directly from Hugging Face for application execution.
- Small synthetic test fixtures in unit tests contain no proprietary scraped content.

---

## 13. Summary of Open Decisions for User Approval

1. **Gemini SDK Choice:**
   - *Option A (Ponytail Zero-Dependency):* Call the Gemini REST API directly using Python's existing `requests` library.
   - *Option B:* Install the official `google-genai` package.
2. **Anti-Slop Integration Route:**
   - *Option A (Recommended):* Manually apply and audit Anti-Slop rules & Delivery Gate within project files (zero external changes).
   - *Option B:* Formally install the plugin via `agy plugin install https://github.com/miqdadbadjuber/anti-slop`.
3. **Frontend Component Architecture:**
   - Use Tailwind CSS with semantic CSS variables for the Editorial Career Intelligence design tokens, without external component libraries (e.g., no MUI or Shadcn), to preserve absolute control over Anti-Slop and bundle size.
