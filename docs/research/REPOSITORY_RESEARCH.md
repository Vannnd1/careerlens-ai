# Repository & Methodology Research Report: CareerLens AI

**Document Version:** 1.0  
**Date:** 2026-10-14  
**Author:** Antigravity AI  
**Status:** Complete — Ready for Review & Approval  

---

## 1. Executive Summary

This research report documents the foundational methodologies, design standards, and technical environment required for the development of **CareerLens AI**. In accordance with [AGENTS.md](file:///c:/Users/panpe/Downloads/careerlens-ai/AGENTS.md), [PRD.md](file:///c:/Users/panpe/Downloads/careerlens-ai/PRD.md), and [DESIGN.md](file:///c:/Users/panpe/Downloads/careerlens-ai/DESIGN.md), this report evaluates:

1. **Anti-Slop UI/Design Rules** ([miqdadbadjuber/anti-slop](https://github.com/miqdadbadjuber/anti-slop))
2. **Ponytail Coding Skill** ([DietrichGebert/ponytail](https://github.com/DietrichGebert/ponytail))
3. **Workspace Runtimes, Package Managers & Existing Libraries**
4. **Integration Architecture & Execution Guardrails**

*Note on verification:* Every claim in this document distinguishes between verified facts (checked against actual repository files, network responses, and environment commands) and recommendations or assumptions.

---

## 2. Source 1: Anti-Slop UI & Design Guidance

### 2.1 Exact Source Locations & Files Inspected
- **Repository:** `https://github.com/miqdadbadjuber/anti-slop`
- **Files Read & Audited:**
  - `README.md` (`https://raw.githubusercontent.com/miqdadbadjuber/anti-slop/main/README.md`) — 242 lines, 12,489 bytes.
  - `GUIDE.md` (`https://raw.githubusercontent.com/miqdadbadjuber/anti-slop/main/GUIDE.md`) — 759 lines, 43,464 bytes.
  - `skills/antislop/SKILL.md` (`https://raw.githubusercontent.com/miqdadbadjuber/anti-slop/main/skills/antislop/SKILL.md`) & `antislop.md` — 724 lines, 57,719 bytes.
  - `skills/antislop-ui/SKILL.md` (`https://raw.githubusercontent.com/miqdadbadjuber/anti-slop/main/skills/antislop-ui/SKILL.md`) — 311 lines, 26,829 bytes.
  - `rules/antislop.md` (`https://raw.githubusercontent.com/miqdadbadjuber/anti-slop/main/rules/antislop.md`) — 12 lines, 1,046 bytes.
  - Inspected referenced auxiliary skills: `skills/antislop-human/SKILL.md`, `skills/antislop-layoutmobile/SKILL.md`, `skills/antislop-copywriting/SKILL.md`, `skills/antislop-code/SKILL.md`.

### 2.2 Core Philosophy & Operating Model
- **Filter, Not a Style Guide:** Anti-Slop is explicitly **not** an aesthetic theme or UI library. It does not dictate colors or fonts; it functions as a rigorous negative filter that eliminates AI-generated clichés, decorative filler, fake metrics, and generic templates. The actual visual direction must come from [DESIGN.md](file:///c:/Users/panpe/Downloads/careerlens-ai/DESIGN.md) (R-37).
- **The Craftsmanship Standard (C-1 to C-5):**
  - **C-1 Intentionality:** Every line, token, card, and animation must serve an articulated user goal.
  - **C-2 Functional Completeness:** No dead navigation links, non-functional mock controls, or unhandled states.
  - **C-3 Content-Driven Composition:** Layout shapes reflect actual data density and decision workflows, not prefabricated 3-card or bento grids.
  - **C-4 Resilience:** UI remains legible and fully operable across light/dark themes, all mobile/desktop breakpoints, and keyboard-only navigation.
  - **C-5 Evidence Over Claims:** No decorative numbers, simulated metrics, or fake testimonials.

### 2.3 Rule Architecture (38 Mandatory Rules)
Anti-Slop organizes rules into three distinct tiers:
1. **Group 1: Hard Gate (Absolute — No Exceptions):**
   - **R-02 & R-16:** Clear, human copywriting without AI buzzwords ("revolutionary", "unleash", "seamless").
   - **R-03:** True mobile responsiveness without horizontal clipping, truncation, or awkward touch targets.
   - **R-17 & R-36:** No fabricated numbers, fake stats, or invented claims. Real dataset values only.
   - **R-18:** No fake user testimonials or placeholder quotes.
   - **R-24 & R-26:** Navigation and interactive elements must work; no dummy links.
   - **R-25 & R-32:** WCAG AA color contrast (minimum 4.5:1 text, 3:1 controls) and full keyboard accessibility.
   - **R-27:** Explicit UI states required: Initial, Loading, Empty, Success, Validation Error, Service Error, and AI-Unavailable fallback.
   - **R-34:** Every theme shipped must be verified and legible.
   - **R-35:** Verify before delivery; run the delivery gate report.
   - **R-37:** A written design direction (`DESIGN.md`) is mandatory.
   - **R-38:** Real content or honest placeholders (`"e.g. Python, SQL"`, not `"John Doe"`).
2. **Group 2: Purpose-Gate (Techniques Allowed Only with Explicit Written UX Purpose):**
   - **R-01 & R-29:** No generic purple/blue gradients or rainbow palettes. Palette must stem from design system tokens.
   - **R-04:** No emoji as bullet points or generic sparkles/stars.
   - **R-07 & R-10:** No decorative grid backgrounds or unnecessary frosted glassmorphism.
   - **R-12 & R-13:** Restrained shadows; no glowing borders or outer glows.
   - **R-14:** Cards used only when semantic grouping is genuinely needed.
   - **R-19:** Motion must have a clear UX purpose, respect `prefers-reduced-motion`, and never run endless pulsing loops.
3. **Group 3: Quality Locks (Consistency & Integrity):**
   - **R-05:** Varying layout rhythm rather than repeating the same card shape down the page.
   - **R-09:** No redundant pill/eyebrow badges repeating what the heading already states.
   - **R-11:** Consistent border-radius hierarchy (cards vs. buttons vs. inputs).
   - **R-30:** Do not clone popular SaaS clones (Linear, Stripe, Vercel) blindly.

### 2.4 The Liveliness Toolkit & Delivery Gate
- **Three Dials (Declared per Project):**
  - **ENERGY (1–5):** Visual contrast, density, and assertiveness. Recommended for CareerLens AI: **2–3** (Editorial Career Intelligence, restrained, high-clarity).
  - **RHYTHM (1–5):** Variation in layout composition and whitespace. Recommended: **3** (structured sections, analytical focus).
  - **MOTION (1–5):** Micro-interactions and transitions. Recommended: **1–2** (functional transitions only, no endless animations).
- **Mandatory Delivery Gate:** Prior to shipping any UI feature, a structured 4-block PASS/FAIL audit report must be produced verifying Hard Gate, Purpose-Gate, Liveliness, and Craftsmanship compliance.

---

## 3. Source 2: Ponytail Coding Skill

### 3.1 Exact Source Locations & Files Inspected
- **Local Installed Plugin:** `C:\Users\panpe\.gemini\config\plugins\ponytail\skills\ponytail\SKILL.md` (121 lines, 6,757 bytes).
- **Remote Repository:** `https://github.com/DietrichGebert/ponytail`
- **Remote Skill File:** `https://raw.githubusercontent.com/DietrichGebert/ponytail/main/skills/ponytail/SKILL.md` (53 lines, 3,492 bytes).

### 3.2 Working Principles in Plain Terms
Ponytail embodies the disciplined restraint of a seasoned senior engineer who has responded to 3:00 AM production outages caused by over-engineered abstractions. The core philosophy is that **the best code is the code that never had to be written**.

Key working principles:
1. **The 7-Rung Ladder (Stop at the first rung that holds):**
   - *Rung 1: Does this need to exist at all?* Skip speculative features (YAGNI).
   - *Rung 2: Already in this codebase?* Look before writing; reuse existing helpers, types, and modules.
   - *Rung 3: Standard library does it?* Use Python/TypeScript stdlib before writing custom utilities.
   - *Rung 4: Native platform feature covers it?* Native HTML tags, CSS layout, or database constraints over custom JS.
   - *Rung 5: Already-installed dependency solves it?* Never add a new library when existing dependencies suffice.
   - *Rung 6: Can it be one line?* Write the clear one-liner.
   - *Rung 7: Only then write the minimum viable complete code.*
2. **Read Fully Before Editing:**
   - *Crucial Distinction:* Laziness applies to the *solution complexity*, never to *problem comprehension*.
   - Trace the entire flow, inspect all affected callers, examine configuration, and understand edge cases before touching code. Shoddy reading that ships a superficial diff is dangerous slop.
3. **Bug Fixes: Root Cause Over Symptom:**
   - Grep all callers of a faulty function. Fix the root cause in the shared function once rather than spraying individual guards across multiple callers.
4. **Testing Non-Trivial Logic:**
   - Code without verification is unfinished.
   - Any non-trivial logic (branching conditions, parsing, matching algorithms, security checks) must leave behind **one runnable check** that fails if the logic breaks (e.g., an assertion-based test or a compact `pytest` case).
   - Trivial one-liners do not need bloated test suites (YAGNI applies to tests too).
5. **Safeguards That Must NEVER Be Removed:**
   - Input validation at trust boundaries (API parameters, dataset rows).
   - Error handling that prevents data loss or service crashes.
   - Security controls (keeping `GEMINI_API_KEY` strictly backend-only, preventing path traversal).
   - Accessibility fundamentals (semantic HTML, focus indicators, ARIA where needed).
   - Explicit user-requested features.
6. **Output Discipline:**
   - Deliver code first, followed by at most 1–3 concise lines: what was skipped and when to add it.
   - Format: `[code] -> skipped: [X], add when [Y].`

---

## 4. Current Workspace & Environment Inspection

### 4.1 Verified System Capabilities
Commands executed against the host Windows environment verified the following:

| Component | Verified Version | Status / Notes |
|---|---|---|
| **Operating System** | Windows 11 (x64) | PowerShell host environment |
| **Python** | 3.11.9 (64-bit) | Installed via Windows Store Python Foundation |
| **Package Manager (Python)** | pip 24.0, uv 0.11.29 | `uv` is available for ultra-fast virtualenv/package management |
| **Node.js** | v24.8.0 | Verified |
| **npm** | 11.6.0 | Verified |
| **git** | 2.52.0.windows.1 | Verified |
| **pnpm / yarn** | Not installed | Use `npm` for frontend package management |

### 4.2 Verified Pre-Installed Python Packages
Inspection via `pip list` confirmed that critical high-performance data and web libraries are **already installed** in the global Python environment:
- **Web Framework:** `fastapi` 0.136.1, `starlette` 1.0.0, `uvicorn` 0.46.0, `pydantic` 2.13.4
- **Data Processing:** `pandas` 2.2.3, `pyarrow` 20.0.0, `numpy` 2.4.4
- **Testing:** `pytest` 8.3.4, `pytest-cov` 6.0.0
- **HTTP Client:** `requests` 2.32.3, `urllib3` 2.2.1
- **LLM SDKs:** `google.genai` and `google.generativeai` are currently **not installed**. (Standard `requests` or `urllib.request` can call the Gemini REST API directly without adding new dependencies, or `google-genai` can be installed in a virtualenv upon user approval).

### 4.3 Workspace Repository Contents
Inspected `c:\Users\panpe\Downloads\careerlens-ai`:
- [AGENTS.md](file:///c:/Users/panpe/Downloads/careerlens-ai/AGENTS.md) (4,988 bytes) — Project instructions and governance.
- [PRD.md](file:///c:/Users/panpe/Downloads/careerlens-ai/PRD.md) (9,098 bytes) — Product scope, user stories, matching formula, and acceptance criteria.
- [DESIGN.md](file:///c:/Users/panpe/Downloads/careerlens-ai/DESIGN.md) (5,731 bytes) — Design specification and Editorial Career Intelligence visual direction.
- *Status:* No application code or scaffolding exists yet. Existing files are untouched and intact.

---

## 5. Integration Strategy for Both Repositories

### 5.1 Ponytail Integration Status & Method
- **Status:** **VERIFIED ACTIVE.**
- **Verification Evidence:** The Antigravity customization plugin `ponytail` is already installed and loaded at `C:\Users\panpe\.gemini\config\plugins\ponytail\skills\ponytail\SKILL.md`. It appears in the active agent `<skills>` manifest.
- **Operating Level:** Default to **full** mode. Apply the 7-rung ladder and output discipline on all coding tasks.

### 5.2 Anti-Slop Integration Status & Smallest Practical Approach
- **Status:** **NOT INSTALLED AS A PLUGIN** (verified that `C:\Users\panpe\.gemini\config\plugins\antislop` does not currently exist).
- **Compliance with Instruction E:** *Never claim a skill is active unless verified.* Therefore, Anti-Slop is **not** claimed as an active plugin.
- **Smallest Practical Integration Approaches:**
  1. *Approach A (Project-Level Reference & Delivery Gate — Zero New Tooling):*
     - We embed the 38 Anti-Slop rules, Craftsmanship Standards, and the Delivery Gate checklist directly into our implementation planning, [DESIGN.md](file:///c:/Users/panpe/Downloads/careerlens-ai/DESIGN.md) review gate, and QA test procedures.
     - Advantage: Requires zero external downloads, zero npm global scripts, and zero shell modifications. 100% compliant with Ponytail rung 1 & 2.
  2. *Approach B (Project-Level Skill Directory):*
     - Place `skills/antislop` and `skills/antislop-ui` into `.agents/skills/` within this repository so Antigravity can discover them natively without touching the global environment.
  3. *Approach C (Global Antigravity Plugin):*
     - Run `agy plugin install https://github.com/miqdadbadjuber/anti-slop` if the user desires the plugin globally across all projects.
- **Recommendation:** Proceed with **Approach A** for immediate planning and, if formal plugin activation is desired by the user, request explicit approval before running any plugin installation commands.

---

## 6. Ponytail Principles Checklist for Future Implementation

Before writing any application code, evaluate every planned change against this checklist:

- [ ] **YAGNI Rung 1:** Did anyone ask for this? If speculative, delete it or skip it.
- [ ] **Codebase Reuse Rung 2:** Did I search for existing helpers, types, or services in this repository before writing a new one?
- [ ] **Stdlib / Platform First Rungs 3–5:** Can Python's `ast`, `json`, `math`, `re` or native HTML `<input>`, `<dialog>`, `<details>` solve this without a new package?
- [ ] **Dependency Gate:** Does this feature reuse already installed packages (`fastapi`, `pandas`, `pyarrow`, `pytest`) rather than adding new ones?
- [ ] **Comprehension Gate:** Did I trace all callers, imports, and side effects across the entire flow before proposing the diff?
- [ ] **Root-Cause Bug Fixing:** Did I fix the problem in the shared upstream function rather than wrapping defensive checks around individual callers?
- [ ] **Runnable Verification:** Does this non-trivial logic have at least one test or self-checking assertion that fails if broken?
- [ ] **Safeguards Preserved:** Are input validation, security controls, API key isolation, and error boundaries strictly intact?
- [ ] **Output Discipline:** Is the code presented first, followed by at most 3 lines summarizing what was skipped and when to upgrade?
- [ ] **Explicit Shortcut Tracking:** If a deliberate compromise was made, is it commented as `# ponytail: <limit>, <when to upgrade>`?

---

## 7. Proposed Technology Stack & Unresolved Questions

### 7.1 Proposed Minimal Technology Stack
1. **Backend Service:**
   - **Framework:** FastAPI (`fastapi==0.136.1`, `uvicorn==0.46.0`). Already installed.
   - **Data Handling:** Pandas 2.2.3 & PyArrow 20.0.0. Dataset (`1,167` records) loaded directly into memory at startup as an immutable DataFrame/in-memory index. Fast, zero-database architecture.
   - **Skill Normalization & Matching:** Deterministic Python matching engine using set intersection over normalized lowercase tokens.
   - **LLM Integration:** Server-side Gemini API calls using either Python `requests` (zero new dependencies) or `google-genai` if user prefers official SDK.
   - **Testing:** `pytest` (already installed).
2. **Frontend Application:**
   - **Scaffold:** Vite + React + TypeScript. Minimal, performant, standard.
   - **Styling:** Tailwind CSS or clean CSS variables following [DESIGN.md](file:///c:/Users/panpe/Downloads/careerlens-ai/DESIGN.md) design tokens (Editorial Career Intelligence). No generic UI component libraries (Chakra/MUI/Shadcn bloat avoided to strictly uphold Anti-Slop and Ponytail).
   - **Icons & Visuals:** Minimal inline SVGs or standard icons strictly tied to navigation/actions; no decorative emoji or generic sparkles.

### 7.2 Unresolved Questions for User Approval
1. **Gemini API Integration Method:**
   - *Option 1 (Ponytail Minimal):* Use the existing `requests` library to call Gemini API endpoints (`POST https://generativelanguage.googleapis.com/v1beta/models/...`). Requires 0 new packages.
   - *Option 2:* Install the official `google-genai` SDK via `pip` or `uv`.
2. **Anti-Slop Loading Preference:**
   - Confirm whether user prefers **Approach A** (manual enforcement of Anti-Slop rules + Delivery Gate) or **Approach B/C** (installing plugin via `agy plugin install`).
3. **Dataset Acquisition & Caching Strategy:**
   - Confirm whether the backend should fetch and cache the 2.5MB parquet file into a local `.cache/` folder on first startup, or if a download script should be run during setup.
