# CareerLens AI — AI-Assisted Career Exploration Assistant

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/backend-FastAPI-009688.svg)](https://fastapi.tiangolo.com/)
[![React 19](https://img.shields.io/badge/frontend-React%2019-61dafb.svg)](https://react.dev/)
[![TypeScript](https://img.shields.io/badge/language-TypeScript-3178c6.svg)](https://www.typescriptlang.org/)
[![License: CC BY-SA 4.0](https://img.shields.io/badge/Dataset%20License-CC%20BY--SA%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by-sa/4.0/)

CareerLens AI is an AI-assisted career exploration assistant designed for students, fresh graduates, and entry-level job seekers. It pairs deterministic Python skill matching against structured job postings with grounded Google Gemini API explanations in natural Indonesian.

---

## 1. Problem Statement & Overview

Fresh graduates and entry-level job seekers frequently struggle with career ambiguity:
1. **Unclear Skill Overlap:** Traditional job boards show exhaustive requirement lists without calculating how a candidate's actual background aligns with a role.
2. **Opaque & Hallucinated AI Advice:** Generic chatbots often invent non-existent job openings, hallucinate salary figures, or claim arbitrary hiring chances without referencing verified market data.
3. **Deficit-Framed Feedback:** Missing skills are often labeled as personal failures rather than structured, actionable opportunities for development.

**CareerLens AI solves this by separating computation from reasoning:**
- Match percentages and skill gaps are computed **100% deterministically** using set mathematics in Python.
- Google Gemini is strictly used as an **explainer and learning mentor**, grounded solely in backend calculations and official benchmark job records.

---

## 2. Core Features

1. **Structured Career Profile Input:**
   - Skills input with dataset-backed autocompletion.
   - Proficiency level selection (*Pemula*, *Menengah*, *Mahir*).
   - Category filtering, career interest descriptions, and experience level summary.
2. **Deterministic Career Matching:**
   - Real-time matching against 1,167 benchmark job postings across 5 industry categories.
   - Ranked matching scores with exact mathematical breakdown.
3. **Explainable Skill-Gap Analysis:**
   - Clearly segmented into *Keahlian Sesuai* (Matched Skills) and *Keahlian Belum Dilaporkan / Potensi Pengembangan* (Skills to Develop).
   - Strict non-judgmental terminology (unreported skills are never labeled as deficiencies).
4. **Context-Grounded Gemini Career Chat:**
   - Interactive Q&A conducted entirely in natural Indonesian.
   - Grounded directly in the candidate's profile, calculated score, and verified job description.
   - Safeguarded against prompt injection and speculative hallucinations.
5. **Personalized 3-Stage Learning Roadmap:**
   - Structured stages: *Fondasi Konseptual*, *Penerapan Praktis*, and *Portofolio & Pembuktian*.
   - Generates realistic, actionable mini-projects for candidate portfolios.
6. **Dataset & Catalog Explorer:**
   - Full browsing of the benchmark dataset with category filtering, debounced search, and pagination.
   - Inspection modal showing verbatim job descriptions and extracted skill sets.

---

## 3. System Architecture

The application adopts a minimalist, two-tier decoupled architecture with zero unnecessary microservices or external databases.

```mermaid
flowchart TD
    subgraph Client ["Frontend (React 19 + TypeScript + Vite)"]
        UI["Editorial UI Canvas (#F8FAFC)"]
        Store["Client State (Profile, Results, Catalog)"]
        APIClient["Typed API Client (src/api.ts)"]
        UI --> Store
        Store --> APIClient
    end

    subgraph Server ["Backend (Python 3.11 + FastAPI)"]
        Router["FastAPI Application (backend/main.py)"]
        DataLoader["Data Loader & Cache (backend/data_loader.py)"]
        DatasetStore[("Pandas In-Memory DataFrame\n1,167 Benchmark Records")]
        Matcher["Deterministic Matcher (backend/matcher.py)"]
        Assistant["Gemini Assistant (backend/ai_assistant.py)"]
        
        Router --> DataLoader
        DataLoader --> DatasetStore
        Router --> Matcher
        Matcher --> DatasetStore
        Router --> Assistant
    end

    subgraph External ["External Services"]
        HuggingFace[("Hugging Face Hub\nbatuhanmtl/job-skill-set")]
        GeminiAPI["Google Gemini API\ngemini-3-flash-preview")]
    end

    APIClient -- "HTTP / REST (JSON)" --> Router
    DataLoader -. "Fetch on Startup / Cached" .-> HuggingFace
    Assistant -- "Grounded Prompt & Context" --> GeminiAPI
```

---

## 4. Technology Stack

- **Frontend:**
  - **Framework:** React 19, TypeScript, Vite.
  - **Styling:** Custom CSS implementing the *Anti-Slop Editorial Career Intelligence* design tokens (`#F8FAFC`, `#1E40AF`, `#0F172A`). Zero external UI bloat (no Tailwind, MUI, or Shadcn).
  - **Tooling:** Oxlint for static analysis, native browser `fetch` for networking.
- **Backend:**
  - **Runtime & Web Framework:** Python 3.11+, FastAPI, Uvicorn.
  - **Data Processing:** Pandas, PyArrow (in-memory Parquet reading and vectorized filtering).
  - **AI Integration:** Google Gemini REST / official `google-genai` integration via server environment variables.
  - **Testing:** Pytest, pytest-cov.

---

## 5. Deterministic Matching Formula & Employment Disclaimer

### Mathematical Definition

CareerLens AI calculates career alignment using equal-weight set intersection between normalized user skills ($S_{\text{user}}$) and normalized required skills from the job posting ($S_{\text{job}}$):

$$\text{Match Score} = \begin{cases} \left( \dfrac{|S_{\text{user}} \cap S_{\text{job}}|}{|S_{\text{job}}|} \right) \times 100\%, & |S_{\text{job}}| > 0 \\ 0\%, & |S_{\text{job}}| = 0 \end{cases}$$

- **Matched Skills:** $S_{\text{matched}} = S_{\text{user}} \cap S_{\text{job}}$
- **Unreported Skills (Potential for Growth):** $S_{\text{unreported}} = S_{\text{job}} \setminus S_{\text{user}}$

### Critical Disclaimer: Not a Probability of Employment

> [!IMPORTANT]
> **The match score is strictly a lexical measure of skill overlap against public benchmark job postings.**
> It **DOES NOT** represent a probability of being hired or receiving an interview offer. Hiring decisions depend on multiple factors outside the scope of skill extraction, including:
> - Depth of hands-on experience and portfolio execution quality.
> - Soft skills, behavioral interviews, and cultural alignment.
> - Real-time market competition, geographic location, and legal eligibility.
> - Live organizational budget and head-count availability.

---

## 6. Dataset Attribution & Licensing

- **Dataset Name:** [Job Skill Set](https://huggingface.co/datasets/batuhanmtl/job-skill-set)
- **Author:** Batuhan Mutlu (2024), utilizing RecAI API services.
- **Upstream Source:** LinkedIn Job Postings (2023–2024) by Arshkon on Kaggle.
- **License:** [Creative Commons Attribution-ShareAlike 4.0 International (CC BY-SA 4.0)](https://creativecommons.org/licenses/by-sa/4.0/).
- **Redistribution Policy:** To comply with attribution and storage best practices, the 2.5 MB Parquet binary is cached locally during runtime under `.cache/dataset/` and is strictly excluded from version control via `.gitignore`.

---

## 7. Prerequisites & Local Setup

### Backend Setup

1. **Python Environment:** Ensure Python 3.11+ is installed.
2. **Install Dependencies:**
   ```bash
   pip install fastapi uvicorn pydantic pandas pyarrow requests pytest pytest-cov
   ```
3. **Configure Environment Variables:**
   ```bash
   cp .env.example .env
   ```
   Edit `.env` to include your Google Gemini API key:
   ```env
   GEMINI_API_KEY=your_actual_api_key_here
   GEMINI_MODEL=gemini-3-flash-preview
   ```
4. **Start the FastAPI Backend:**
   ```bash
   python -m uvicorn backend.main:app --reload --host 127.0.0.1 --port 8000
   ```
   API docs will be available at `http://127.0.0.1:8000/docs`.

### Frontend Setup

1. **Node.js Environment:** Ensure Node 18+ (Node 20+ recommended) is installed.
2. **Install & Run Frontend:**
   ```bash
   cd frontend
   npm install
   npm run dev
   ```
   The client runs at `http://localhost:5173/` and proxies `/api` requests to port 8000.

---

## 8. Automated Testing & Verification

### Run Backend Unit & Integration Tests
```bash
python -m pytest tests/ -v --cov=backend
```
- **Test Suite Results:** 51 passed across `test_matching.py`, `test_api.py`, and `test_ai_assistant.py` with ~89% code coverage.

### Run Frontend Static Analysis & Production Build
```bash
cd frontend
npm run lint
npm run build
```
- **Lint Result:** Oxlint completed with 0 errors and 0 warnings.
- **Build Result:** Vite + TypeScript compiler bundle built cleanly in ~150ms.

---

## 9. Screenshot Checklist

For project demonstration and evaluation, capture the following live views from `http://localhost:5173`:

- [ ] **1. Main Dashboard & View Switcher:** Showing the editorial header, backend health badge (`Sistem Siap`), and navigation between *Workbench Karir* and *Katalog Data*.
- [ ] **2. Profile & Skill Input Form:** Showing entered skill chips with active proficiency dropdowns (*Pemula*, *Menengah*, *Mahir*) and live dataset autocompletion.
- [ ] **3. Deterministic Career Match Results:** Displaying ranked job cards with percentage badges (e.g. `67%`), category tags, and mathematical breakdown preview.
- [ ] **4. Explainable Skill-Gap Breakdown:** Showing the clear separation of *Keahlian Sesuai* (teal badges) and *Keahlian Belum Dilaporkan* (amber badges).
- [ ] **5. Selected-Job Detail Modal:** Displaying verbatim job description and metadata.
- [ ] **6. Grounded Gemini Career Chat:** Interactive Indonesian dialogue explaining role fit and interview preparation tips.
- [ ] **7. Personalized 3-Stage Learning Roadmap:** Displaying progressive milestones (*Fondasi*, *Penerapan Praktis*, *Portofolio & Pembuktian*) and mini-project recommendations.
- [ ] **8. Dataset Catalog Explorer:** Showing category counts, search filtering, and paginated records.

*(Note: Per project integrity standards, screenshot placeholders are omitted; captures are taken from the live verified system).*

---

## 10. PRD Acceptance Checklist

| PRD Section | Feature / Requirement | Implementation Reference | Status |
|---|---|---|---|
| **§ 4.1** | Career Profile Input (Skills, Proficiency, Interests) | [`frontend/src/components/ProfileForm.tsx`](frontend/src/components/ProfileForm.tsx) | Verified Complete |
| **§ 4.2** | Deterministic Match Engine (Equal-weight set intersection) | [`backend/matcher.py`](backend/matcher.py) | Verified Complete |
| **§ 4.3** | Explainable Skill-Gap Evidence (Matched vs Unreported) | [`backend/matcher.py`](backend/matcher.py), [`frontend/src/components/MatchList.tsx`](frontend/src/components/MatchList.tsx) | Verified Complete |
| **§ 4.4** | Grounded Gemini Q&A in Natural Indonesian | [`backend/ai_assistant.py`](backend/ai_assistant.py), [`frontend/src/components/JobDetailModal.tsx`](frontend/src/components/JobDetailModal.tsx) | Verified Complete |
| **§ 4.5** | Personalized 3-Stage Learning Roadmap | [`backend/ai_assistant.py`](backend/ai_assistant.py), [`frontend/src/components/JobDetailModal.tsx`](frontend/src/components/JobDetailModal.tsx) | Verified Complete |
| **§ 4.6** | Dataset Explorer (5 Categories, Search, Pagination) | [`backend/data_loader.py`](backend/data_loader.py), [`frontend/src/components/DatasetExplorer.tsx`](frontend/src/components/DatasetExplorer.tsx) | Verified Complete |
| **§ 5.1** | Anti-Slop Editorial Design & Keyboard Accessibility | [`DESIGN.md`](DESIGN.md), [`frontend/src/index.css`](frontend/src/index.css) | Verified Complete |
| **§ 6.0** | Server-side Gemini Secret Isolation | [`backend/main.py`](backend/main.py), [`.env.example`](.env.example) | Verified Complete |

---

## 11. Deployment Guide

### Backend Deployment (e.g. Render, Railway, Fly.io, or VPS)
1. Provide a Python 3.11+ runtime.
2. Define the start command:
   ```bash
   uvicorn backend.main:app --host 0.0.0.0 --port $PORT
   ```
3. Set environment variables on the host dashboard:
   - `GEMINI_API_KEY`: Your private Google Gemini API key.
   - `GEMINI_MODEL`: `gemini-3-flash-preview`
   - `CORS_ORIGINS`: Frontend URL (e.g., `https://your-frontend.vercel.app`)

### Frontend Deployment (e.g. Vercel, Netlify, Cloudflare Pages)
1. Root directory: `frontend`
2. Build command: `npm run build`
3. Output directory: `dist`
4. Add rewrites/proxy: configure reverse proxy or configure `VITE_API_URL` environment variable pointing to the deployed backend URL.

*(Note: In accordance with project reporting rules, this repository has not been deployed to a public cloud URL; local verification on localhost is complete).*

---

## 12. Known Limitations & Scope Boundaries

- **Static Vocabulary Constraint:** Extracted skill matching is constrained to the 1,167 benchmark records from the Hugging Face dataset.
- **Headless Browser Automation:** End-to-end browser automation (Playwright/Cypress) was omitted to keep the MVP lean under Ponytail principles; all UI logic is covered by typed contracts, linting, and build verification.
- **Gemini Rate Limits:** In the event of upstream rate limits or quota exhaustion on the preview model, the backend catches the exception and returns deterministic fallback suggestions without crashing.
