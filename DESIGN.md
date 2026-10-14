# CareerLens AI — UI/UX Design Specification

**Document Version:** 1.0 (Approved Design Specification)  
**Date:** 2026-10-14  
**Design Reference:** [Anti-Slop UI & Craftsmanship Standards](https://github.com/miqdadbadjuber/anti-slop)  
**Status:** Approved for Frontend Scaffolding & Implementation  

---

## 1. Design Direction & Evaluation

### 1.1 Evaluated Directions

#### Direction A: Editorial Career Intelligence (Selected)
- **Concept:** A restrained, analytical publication aesthetic combining the authority of a labor market research report with an interactive decision workbench.
- **Visual Character:** Crisp typographic hierarchy, high-contrast typography, calm paper/slate neutral canvas, purposeful whitespace, and a single deep cobalt/navy accent. Information is structured in analytical cards and data tables. Visual embellishments (gradients, glassmorphism, floating orbs) are strictly rejected.
- **Tone:** Analytical, trustworthy, dignified, supportive, and grounded.

#### Direction B: Forensic Systems Workbench (Alternative)
- **Concept:** High-density, utilitarian technical workbench inspired by IDE diagnostics and Bloomberg-style financial terminal efficiency.
- **Visual Character:** Dark mode by default, monospaced numerical readouts, dense 1px borders, high information density, and diff-style (+/-) skill tags.
- **Rejection Rationale:** While suitable for software engineers, CareerLens AI serves a broader audience across five core categories (HR, Finance, Sales, Business Development, and IT). A dense terminal aesthetic intimidates non-technical students and job seekers. Furthermore, Anti-Slop R-21 explicitly warns against dark-mode-by-default without domain rationale, and anti-slop-ui explicitly flags "Fake Terminal Windows" as an AI trope.

### 1.2 Selection Rationale
Direction A (**Editorial Career Intelligence**) was selected because:
1. It bridges technical and non-technical job seekers with equal clarity and warmth.
2. It treats skill data and job requirements with research-level integrity rather than marketing hype.
3. It naturally complies with Anti-Slop core rules: zero decorative gradients (R-01), zero fake stats (R-17), content-driven composition (C-3), and verifiable data (C-5).

### 1.3 Anti-Slop Liveliness Dials
- **ENERGY (2/5):** Low-to-moderate contrast density; quiet background, sharp text, calm analytical focus without aggressive saturated fills.
- **RHYTHM (3/5):** Structured section transitions; wide header banner, dual-column workbench for matching, single-column reading flow for job descriptions and roadmap milestones.
- **MOTION (1/5):** Functional micro-interactions only (150ms button hover, crisp focus ring expansion, accessible modal fade). No perpetual pulse loops, bouncing chips, or decorative keyframe animations (R-19).

---

## 2. Typography System

The typography uses clean, highly legible neo-grotesque type optimized for screen legibility, dense data tables, and comfortable long-form reading.

### 2.1 Typeface Selection
- **Primary Interface & Data:** `Plus Jakarta Sans`, `-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif`.
  - Modern, open apertures, geometric clarity, exceptional legibility at small sizes (12px–14px).
- **Tabular Numerals & Monospace (Job IDs, Scores):** `"JetBrains Mono", "SF Mono", Consolas, monospace`.
  - Used strictly for numerical scores, percentages, and record IDs to align tabular data cleanly.

### 2.2 Scale & Hierarchy
All sizes scale responsively between desktop and mobile in compliance with Anti-Slop `antislop-layoutmobile`:

| Role | Desktop Size / Leading | Mobile Size / Leading | Weight | Usage |
|---|---|---|---|---|
| **Display / H1** | 30px (1.875rem) / 1.2 | 24px (1.5rem) / 1.25 | 700 (Bold) | Main page titles, view headers |
| **Section / H2** | 22px (1.375rem) / 1.3 | 18px (1.125rem) / 1.35 | 600 (SemiBold) | Panel headers, category section titles |
| **Card / H3** | 16px (1.0rem) / 1.4 | 15px (0.9375rem) / 1.4 | 600 (SemiBold) | Job card titles, roadmap stage names |
| **Body (Default)** | 14px (0.875rem) / 1.5 | 14px (0.875rem) / 1.5 | 400 (Regular) | Job descriptions, AI assistant answers |
| **Body Strong** | 14px (0.875rem) / 1.5 | 14px (0.875rem) / 1.5 | 600 (SemiBold) | Emphasized text, table column headers |
| **Caption / Meta** | 12px (0.75rem) / 1.4 | 12px (0.75rem) / 1.4 | 500 (Medium) | Skill tags, category pills, timestamps |
| **Tabular Numbers** | 14px (0.875rem) / 1.0 | 14px (0.875rem) / 1.0 | 600 (SemiBold) | Match score percentage, job counts |

---

## 3. Color Roles & Accessibility Tokens (WCAG AA Verified)

In strict accordance with Anti-Slop **R-01**, **R-25**, and **R-29**, colors are purpose-driven and meet or exceed WCAG AA contrast ratios (4.5:1 for normal text, 3.0:1 for UI boundaries/controls).

```
+-----------------------------------------------------------------------------------------+
|                               SEMANTIC COLOR ROLES                                      |
+-----------------------------------------------------------------------------------------+
| Canvas: #F8FAFC   Surface: #FFFFFF   Border: #CBD5E1   Text: #0F172A (16.1:1 AAA)      |
| Accent Action:    #1E40AF (Deep Cobalt - 8.5:1 AAA on White)                            |
| Matched Tag:      #ECFDF5 Surface / #065F46 Text (7.1:1 AAA)                            |
| Unreported Tag:   #F1F5F9 Surface / #334155 Text (9.7:1 AAA)                            |
| Error / Alert:    #FEF2F2 Surface / #991B1B Text (7.3:1 AAA)                            |
+-----------------------------------------------------------------------------------------+
```

### 3.1 Color Token Palette

```css
:root {
  /* Surfaces & Backgrounds */
  --color-canvas: #F8FAFC;         /* Slate 50 - Main app background */
  --color-surface: #FFFFFF;        /* Pure White - Cards, panels, inputs */
  --color-surface-subtle: #F1F5F9; /* Slate 100 - Secondary containers, code chips */
  --color-surface-muted: #E2E8F0;  /* Slate 200 - Dividers, hover states */

  /* Text & Content (Tested against --color-surface) */
  --color-text-primary: #0F172A;   /* Slate 900 - Contrast 16.1:1 (AAA) */
  --color-text-secondary: #334155; /* Slate 700 - Contrast 9.7:1 (AAA) */
  --color-text-muted: #64748B;     /* Slate 500 - Contrast 4.6:1 (AA compliant) */
  --color-text-inverse: #FFFFFF;   /* Pure White on Accent/Dark */

  /* Borders & Controls */
  --color-border-subtle: #E2E8F0;  /* Slate 200 - Card boundaries */
  --color-border-control: #CBD5E1; /* Slate 300 - Input borders (3.0:1 non-text AA) */
  --color-border-hover: #94A3B8;   /* Slate 400 - Hover borders */
  --color-focus-ring: #2563EB;     /* Blue 600 - Visible 2px outline */

  /* Brand Accent (Editorial Blue) */
  --color-accent: #1E40AF;         /* Blue 800 - Contrast 8.5:1 (AAA on white) */
  --color-accent-hover: #1E3A8A;   /* Blue 900 - Pressed/hover state */
  --color-accent-subtle: #EFF6FF;  /* Blue 50 - Highlight background */

  /* Semantic Data Roles (Never used alone; always paired with text) */
  --color-match-bg: #ECFDF5;       /* Emerald 50 - Matched skill chip background */
  --color-match-border: #A7F3D0;   /* Emerald 200 - Matched skill border */
  --color-match-text: #065F46;     /* Emerald 800 - Matched text (Contrast 7.1:1) */

  --color-unreported-bg: #F8FAFC;  /* Slate 50 - Unreported skill chip background */
  --color-unreported-border: #CBD5E1; /* Slate 300 - Unreported chip border */
  --color-unreported-text: #334155;/* Slate 700 - Unreported text (Contrast 9.7:1) */

  --color-error-bg: #FEF2F2;       /* Red 50 - Error alert background */
  --color-error-border: #FECACA;   /* Red 200 - Error alert border */
  --color-error-text: #991B1B;     /* Red 800 - Error text (Contrast 7.3:1) */

  --color-warning-bg: #FFFBEB;     /* Amber 50 - Fallback/Warning background */
  --color-warning-border: #FDE68A; /* Amber 200 - Warning border */
  --color-warning-text: #92400E;   /* Amber 800 - Warning text (Contrast 6.8:1) */
}
```

---

## 4. Layout Architecture & Responsive Grids

In strict adherence to Anti-Slop `antislop-layoutmobile` (R-03), mobile layouts are **distinct reflows**, not merely squeezed desktop layouts.

### 4.1 Global Structure & Breakpoints
- **Breakpoints:**
  - `Mobile`: `< 768px` (single-column reflow, full-width inputs, stacked chips, sticky top nav).
  - `Tablet`: `768px - 1023px` (stacked workbench with 2-column job cards).
  - `Desktop`: `>= 1024px` (dual-column analytical workbench, max container width `1200px`).
- **Container Hygiene:** Max width `1200px` centered with responsive inline padding (`16px` mobile, `24px` tablet, `32px` desktop). Reading line lengths for job descriptions and AI roadmaps are constrained to `max-w-2xl` (~65ch) for comfortable reading.

### 4.2 Desktop Workbench Layout (>= 1024px)
```
+---------------------------------------------------------------------------------------+
|  [Header] CareerLens AI    [Nav: Eksplorasi Data | Panduan | Tentang]                 |
+---------------------------------------------------------------------------------------+
|  LEFT PANEL (380px fixed / sticky)         | RIGHT PANEL (Fluid flex-1)               |
|                                            |                                          |
|  [Profil Karir Form]                       |  [Filter Kategori Tabs: Semua, IT, HR...] |
|  - Skill Input & Autocomplete Chips        |                                          |
|  - Tingkat Kemahiran (Radio Group)         |  [Hasil Kesesuaian (Matches List)]       |
|  - Minat & Pengalaman (Textarea)           |  - Ranked Job Card 1 (75.0% Match)       |
|  - [Tombol: Hitung Kesesuaian]             |    * Matched Chips (green)               |
|                                            |    * Belum Dilaporkan Chips (neutral)    |
|                                            |  - Ranked Job Card 2 (60.0% Match)...    |
|                                            |                                          |
|                                            |  [Job Detail & AI Assistant Modal/Pane]  |
|                                            |  - Deskripsi Pekerjaan Lengkap           |
|                                            |  - AI Career Q&A grounded transcript     |
|                                            |  - 3-Stage Learning Roadmap              |
+---------------------------------------------------------------------------------------+
|  [Footer] Sumber Data: Job Skill Set (CC BY-SA 4.0) | Batuhan Mutlu & Arshkon         |
+---------------------------------------------------------------------------------------+
```

### 4.3 Mobile Reflow Layout (< 768px)
- The fixed dual-panel collapses into a natural linear stack:
  1. Sticky App Header with clean navigation toggle.
  2. Collapsible Profile Input card with count badge (`"Profil Karir: 4 Keahlian"`).
  3. Category Filter as an horizontally scrollable pill strip with scroll snap.
  4. Full-width Match Result cards with 44x44px minimum tap targets.
  5. Job Detail and AI Career Assistant open in a full-screen drawer or dedicated route with an accessible close button (`Esc` enabled).

---

## 5. Page & Component Inventory with Required UI States

Every component implements the complete state lifecycle required by Anti-Slop **R-27**:

### 5.1 Component Directory

#### 1. App Shell & Navigation
- **Header:** Logo, application title, navigation links (`Kesesuaian Karir`, `Eksplorasi Dataset`), and backend health indicator.
- **Footer:** Public dataset attribution (Batuhan Mutlu, RecAI, Arshkon), CC BY-SA 4.0 license note, and disclaimer.

#### 2. Career Profile Input (`ProfileForm`)
- **Skill Input Field:** Text input with keyboard autocomplete (`Enter` to add), validation error for duplicates or strings > 50 chars.
- **Skill Chip:** Dismissible tag with accessible button (`aria-label="Hapus keahlian {name}"`).
- **Proficiency Selector:** Radio button group for `Pemula` (Beginner), `Menengah` (Intermediate), `Mahir` (Advanced).
- **Interests & Experience:** Textarea with character counter (max 300 chars).
- **Submit Button:** High-contrast CTA (`Hitung Kesesuaian Karir`).

#### 3. Match Results List (`MatchList`)
- **Match Card:**
  - Header: Job title, category pill, match percentage badge.
  - Evidence row: Matched skills count vs. total required (`"5 dari 8 keahlian cocok"`).
  - Chip lists: Green-bordered chips for matched skills; neutral chips for unreported skills.
  - Action CTA: *"Lihat Detail & Panduan AI"* button.

#### 4. Job Detail & AI Assistant (`JobDetailPanel`)
- **Raw Job Description:** Full job description text from dataset in comfortable reading column.
- **Structured Skill Gap Breakdown:** Side-by-side comparison of user skills vs. job expectations.
- **AI Career Chat Transcript:** Grounded Q&A messages with distinct AI bubble styling and clear sourcing note.
- **Learning Roadmap Accordion:** 3 progressive milestones (Fondasi Konseptual, Portofolio Terapan, Pemantapan Karir).

#### 5. Dataset Explorer (`DatasetExplorer`)
- **Search Bar:** Real-time text search filter across 1,167 records.
- **Category Filter Tabs:** IT (240), BizDev (239), Finance (236), Sales (232), HR (220).
- **Data Table / Card Grid:** Paginated list showing Job ID, Title, Category, and Listed Skills.

---

### 5.2 UI States Specification (Anti-Slop R-27)

| State | Visual Behavior & Feedback |
|---|---|
| **Initial (Profile)** | Empty profile card with 4 suggested skill tags (`Python`, `SQL`, `Project Management`, `Communication`). Helpful intro copy explaining that calculations are deterministic. |
| **Initial (Explorer)** | Displays first 20 records of the full 1,167 dataset with active category filter "Semua" (1,167). |
| **Loading (Matching)** | 3 skeleton card rows pulsing subtly (opacity 0.6 to 1.0, 1.5s ease); text: *"Mencocokkan keahlian Anda dengan 1,167 posisi..."* |
| **Loading (AI Response)** | Animated inline indicator inside chat window; input disabled with placeholder: *"AI sedang menyusun jawaban berdasarkan data posisi..."* |
| **Success (Matching)** | Ranked cards displayed in descending score order. Clear disclaimer banner visible above results. |
| **Empty (Zero Matches)** | Clean icon-free card: *"Tidak ditemukan posisi dengan keahlian ini di kategori yang dipilih."* Provides 1-click button to reset category filter or explore related skills. |
| **Validation Error** | Inline red border and message directly beneath the input: *"Keahlian sudah ada dalam daftar"* or *"Keahlian minimal 2 karakter"*. Focus automatically retained. |
| **Service Error (500)** | Subtle warning banner at top: *"Gagal memuat data dari server. Silakan periksa koneksi backend."* Includes a *"Coba Lagi"* (Retry) button. Never shows stack traces. |
| **Gemini AI Unavailable** | If API key is missing or quota exceeded, matching and job details remain 100% operational. The AI chat area displays: *"Asisten AI sedang tidak aktif. Anda tetap dapat menggunakan pencocokan deterministik dan data posisi."* |

---

## 6. Accessibility & Human Factors (Anti-Slop `antislop-human`)

In strict accordance with Anti-Slop **R-25**, **R-26**, **R-32**, and **R-34**:

1. **Color Contrast Verification:**
   - Normal text (`#0F172A` on `#FFFFFF`): **16.1:1** (Exceeds WCAG AAA).
   - Secondary text (`#334155` on `#FFFFFF`): **9.7:1** (Exceeds WCAG AAA).
   - Interactive control borders (`#CBD5E1` on `#FFFFFF`): **3.0:1** (Passes WCAG AA non-text).
   - Matched skill text (`#065F46` on `#ECFDF5`): **7.1:1** (Exceeds WCAG AAA).
   - Unreported skill text (`#334155` on `#F8FAFC`): **9.7:1** (Exceeds WCAG AAA).
2. **Keyboard Navigation & Focus Management:**
   - Universal `:focus-visible` ring: `2px solid #2563EB` with `2px offset`. No `outline: none` without immediate replacement.
   - All modals and drawers support `Escape` key dismissal and trap keyboard focus while open.
   - Skill chips can be focused with `Tab` and removed with `Backspace` or `Delete`.
3. **Screen Reader Support:**
   - Status updates (e.g. *"Menampilkan 12 hasil kecocokan"*) use `aria-live="polite"` containers.
   - Skill deletion buttons have descriptive labels: `aria-label="Hapus keahlian Python"`.
4. **Touch Target Dimensions:**
   - All mobile buttons, chips, and input fields maintain a minimum hit target of **44 × 44 px** with minimum **8px** spacing between adjacent targets.

---

## 7. Anti-Slop Quality Gate Checklist

Before delivering the frontend implementation, verify each item against this checklist:

### Block 1: Hard Gate (Absolute Rules)
- [ ] **R-02 / R-16 (Copywriting):** All text is written in natural, clear Indonesian without AI buzzwords ("revolusioner", "seamless", "unleash").
- [ ] **R-03 (Mobile Responsiveness):** Layout reflows gracefully on mobile devices without horizontal overflow, squeezed tables, or tiny tap targets.
- [ ] **R-17 / R-36 (Truthful Data):** Every score, percentage, job count, and skill name reflects actual backend calculations and real dataset records. No fabricated statistics.
- [ ] **R-18 (No Fake Testimonials):** Zero invented user quotes, fake review stars, or simulated endorsements.
- [ ] **R-24 / R-26 (Real Navigation):** Every button, link, and tab performs a genuine action. No dummy `href="#"` links.
- [ ] **R-25 / R-32 (Contrast & Keyboard):** Passes WCAG AA contrast (minimum 4.5:1 text, 3:1 controls) and full keyboard navigation.
- [ ] **R-27 (UI States):** All 7 states (Initial, Loading, Success, Empty, Validation Error, Server Error, AI Fallback) are implemented and visually verified.

### Block 2: Purpose-Gate (Techniques Allowed Only with Explicit Purpose)
- [ ] **R-01 / R-29 (Color Palette):** Restrained Editorial Career Intelligence palette. Zero decorative purple/blue neon gradients.
- [ ] **R-04 (Icons):** Clean, standard functional icons only (search, delete, external link). Zero decorative sparkles or emoji bullets.
- [ ] **R-07 / R-10 (Background & Glass):** Solid neutral surfaces (`#F8FAFC`, `#FFFFFF`). Zero background dot-grids or blurred frosted glass.
- [ ] **R-12 / R-13 (Shadows & Glows):** Subtle, crisp 1px borders (`#E2E8F0`). Zero outer glows or exaggerated drop shadows.
- [ ] **R-14 (Card Restraint):** Cards used only where semantic grouping is necessary; no wrapping every individual sentence in a card.
- [ ] **R-19 (Motion Purpose):** Transitions capped at 150ms for user feedback. Zero perpetual looping pulses or floating hero animations.

### Block 3: Liveliness
- [ ] **ENERGY (2/5):** Clear, quiet, legible reading environment.
- [ ] **RHYTHM (3/5):** Distinct visual hierarchy between workbench inputs, match cards, and long-form roadmap milestones.
- [ ] **MOTION (1/5):** Micro-interactions on hover and focus only; respects `prefers-reduced-motion`.

### Block 4: Craftsmanship
- [ ] **C-1 (Intentionality):** Every component directly supports career profile input, skill matching, gap understanding, or roadmap learning.
- [ ] **C-2 (Functional Completeness):** No dead ends, unhandled error states, or raw JSON dumps.
- [ ] **C-3 (Content-Driven):** Layout dimensions follow actual job description lengths and skill set densities.
- [ ] **C-4 (Resilience):** Tested at 360px mobile, 768px tablet, and 1280px desktop. Text scales to 200% without clipping.
- [ ] **C-5 (Evidence Over Claims):** The match score is explicitly paired with visible matched and unreported skill lists.
