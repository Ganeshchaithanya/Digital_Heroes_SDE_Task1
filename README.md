# PAGEPULSE — Deterministic Website Inspection Platform

PAGEPULSE is a production-grade, full-stack website inspection application built with a **Python 3.12 / FastAPI** backend and a **React 18 / TypeScript / Tailwind CSS** frontend.

The platform accepts any valid website URL, fetches HTML, measures quantitative technical metrics, evaluates them deterministically using versioned JSON policy standards, and optionally enriches reports with AI explanations powered by **Groq LLM (`llama-3.3-70b-versatile`)**.

> **Core Architectural Principle**: The application **NEVER depends on AI for computation**. If AI is disabled or fails, the core technical metrics, scores, issues, and recommendations are returned 100% intact.

---

## 🏗️ Architecture & Pipeline

```text
User
 │
 ▼
React Frontend (Vite + TypeScript + Tailwind CSS)
 │
 ▼
POST /api/v1/inspect (FastAPI)
 │
 ▼
InspectionService
 │
 ├──────── 1. URLValidator (Syntax, scheme restriction, normalization, SSRF prevention)
 ├──────── 2. InspectionEngine (httpx async GET, response latency, HTTP status, headers)
 ├──────── 3. HTMLParser (BeautifulSoup4 / lxml -> PageDocument)
 ├──────── 4. FeatureExtractor (SEO, Performance & Content sub-extractors -> FeatureVector)
 ├──────── 5. PolicyLoader (Validates & Loads policies/v1/*.json rules dynamically)
 ├──────── 6. EvaluationEngine (Deterministic weighted category & overall scoring)
 ├──────── 7. EvidenceGenerator (Builds EvidenceBundle: Observed, Expected, Recommendation)
 ├──────── 8. AIService (Optional & Fail-safe)
 │       │
 │       ├── PromptBuilder (Receives EvidenceBundle, instructs natural human English output)
 │       ├── GroqProvider (httpx AsyncClient calling Groq Chat Completions API)
 │       └── Verifier (Pydantic model validation + fact checking against FeatureVector)
 └──────── 9. Response Assembly (Assembles InspectionResponse DTO)
 │
 ▼
JSON Response
```

---

## ⚡ Key Features

1. **11-Layer Modular Architecture**: Built following SOLID principles with strong typing across all domain models.
2. **Versioned Policy Repository (`policies/v1/*.json`)**: Zero hardcoded scoring values. Policies define thresholds, severity, weights, and recommendations.
3. **Natural Human AI Insights**: Groq LLM summarizes findings in warm, conversational English speaking directly to the developer.
4. **Resilient Fail-Safe Error Handling**: AI failure never crashes or delays the primary inspection report.
5. **Modern Glassmorphism UI**: Interactive dashboard featuring score gauges, category progress bars, technical metric cards, and actionable developer fix checklists.

---

## 📂 Project Directory Structure

```text
Digital_Heroes_SDE_Task1/
├── backend/
│   ├── app/
│   │   ├── api/v1/inspect.py            # FastAPI Endpoint (POST /api/v1/inspect)
│   │   ├── services/inspection_service.py # Service Layer Facade
│   │   ├── shared/                      # Constants, Enums, Exceptions, Helpers
│   │   ├── models/                      # Pydantic Domain Models
│   │   ├── validation/url_validator.py  # Validation Layer
│   │   ├── inspection/engine.py         # HTTP Network Inspector (httpx)
│   │   ├── parser/html_parser.py        # HTML Parser (BS4/lxml)
│   │   ├── features/                    # Feature Extractors (SEO, Performance, Content)
│   │   ├── policies/                    # Policy Loader & Schema Validation
│   │   │   └── v1/*.json                # JSON Policy Rules
│   │   ├── evaluation/                  # Scoring & Evidence Generator
│   │   ├── ai/                          # PromptBuilder, GroqProvider, Verifier
│   │   └── observability/logger.py      # Structured Logging
│   ├── requirements.txt
│   └── .env.example
└── frontend/
    ├── src/
    │   ├── components/                  # Header & Footer
    │   ├── features/inspection/components/
    │   │   ├── UrlInputForm.tsx         # URL Search & Sample Presets
    │   │   ├── ScoreGauge.tsx font      # Animated Score Gauge
    │   │   ├── CategoryBreakdown.tsx    # SEO, Performance, Accessibility & Content Cards
    │   │   ├── TechnicalMetricsGrid.tsx # Technical Metrics Grid
    │   │   ├── IssuesAccordion.tsx      # Policy Issues & Actionable Checklist
    │   │   └── AiSummaryCard.tsx        # Groq AI Executive Insights
    │   ├── services/api.ts              # Axios API Client
    │   ├── types/inspection.ts          # TypeScript Type Definitions
    │   ├── App.tsx                      # Root Application Dashboard
    │   └── index.css                    # Tailwind CSS + Glassmorphism Styles
    ├── package.json
    ├── vite.config.ts
    └── tailwind.config.js
```

---

## 🛠️ Local Setup & Execution Guide

### Prerequisites
- Python 3.12+
- Node.js 18+

### 1. Backend Setup & Launch
```powershell
# Navigate into backend directory
cd backend

# Create & activate virtual environment
python -m venv .venv
.\.venv\Scripts\Activate.ps1   # On Windows
source .venv/bin/activate       # On Linux/Mac

# Install dependencies
pip install -r requirements.txt

# Create .env file with your Groq API Key
# GROQ_API_KEY=your_groq_api_key_here

# Run backend development server
uvicorn app.main:app --reload --port 8000
```
Backend API will be accessible at: `http://127.0.0.1:8000/api/v1/inspect`  
Interactive OpenAPI Documentation: `http://127.0.0.1:8000/docs`

### 2. Frontend Setup & Launch
```powershell
# Navigate into frontend directory
cd frontend

# Install dependencies
npm install

# Launch Vite development server
npm run dev
```
Open **`http://localhost:5173`** in your web browser.

---

## 🚀 Deployment Instructions

### Backend → Render
1. Create a new **Web Service** on Render connected to your GitHub repository.
2. Root Directory: `backend`
3. Build Command: `pip install -r requirements.txt`
4. Start Command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
5. Environment Variable: Add `GROQ_API_KEY`.

### Frontend → Vercel
1. Create a new project on Vercel connected to your GitHub repository.
2. Root Directory: `frontend`
3. Framework Preset: `Vite`
4. Output Directory: `dist`

---

## 📄 License
Distributed under the MIT License. Built for Digital Heroes Software Engineering Assignment.
