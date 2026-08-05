# PAGEPULSE — AI-Assisted Website Inspection Platform

PAGEPULSE is a production-grade, deterministic website inspection platform built with **Python 3.12 / FastAPI** and **React 18 / TypeScript / Tailwind CSS**.

Built for the **Digital Heroes Software Development Internship Task**.

---

## 1. Project Overview

PAGEPULSE analyzes any public website URL, fetches raw HTML, measures quantitative technical metrics, evaluates them deterministically using policy-based evaluation standards, and optionally enriches reports with AI explanations using **Groq LLM (`llama-3.3-70b-versatile`)**.

The application **NEVER depends on AI for computation**. If AI is unavailable or disabled, all technical metrics, scores, issues, and recommendations return 100% intact.

---

## 2. Features

- **Validation & Network Inspection Separation**: Distinguishes syntax validation from network reachability (`✔ URL Valid | ✖ Website Unreachable`).
- **Specialized Error Taxonomy**: Handles DNS failures, connection refusals, SSL errors, request timeouts, and private IP restrictions.
- **Live Pipeline Stepper UI**: Animated 6-step progress indicator in the React frontend demonstrating live deterministic execution.
- **Smart Image ALT Parsing**: Differentiates content images from decorative (`alt=""`), presentation (`role="presentation"`), and SVG icons so accessibility is evaluated accurately without over-reporting issues.
- **Graduated Penalty Scoring Engine**: Proportional credit for minor numerical range variances (e.g. title length 61 vs max 60 incurs a minor ~2% penalty rather than a binary zero).
- **Expandable Category Rule Inspection**: Interactive UI drawers displaying rule-by-rule status (`✓ Passed`, `⚠️ Variance`, `❌ Issue`).
- **AI Executive Summary (Groq)**: Friendly human English executive insights, key strengths, prioritized issues, and developer action plans.
- **Mandatory Digital Heroes Footer**: Persistent footer on all pages with hyperlink pointing to `https://digitalheroesco.com`.

---

## 3. System Architecture

```text
User
 │
 ▼
React Frontend (Pipeline Stepper)
 │
 ▼
POST /api/v1/inspect (FastAPI API)
 │
 ▼
Inspection Service
 │
 ├──────── Validation Layer (Syntax, scheme, SSRF checks)
 ├──────── Inspection Engine (httpx async GET, latency, status)
 ├──────── Document Parser (BeautifulSoup4 / lxml -> PageDocument)
 ├──────── Feature Extraction (SEO, Performance, Content extractors)
 ├──────── Policy Loader (Validates & Loads policies/v1/*.json)
 ├──────── Evaluation Engine (Graduated scoring & category math)
 ├──────── Evidence Generator (EvidenceBundle containing observed vs expected)
 ├──────── AI Service (Optional & Fail-safe: PromptBuilder -> Groq -> Verifier)
 └──────── Response Builder (Assembles InspectionResponse DTO)
 │
 ▼
JSON Response
```

---

## 4. Tech Stack

### Frontend
- React 18
- TypeScript
- Vite
- TailwindCSS
- Axios
- Lucide Icons

### Backend
- FastAPI
- Python 3.12
- Uvicorn
- httpx
- BeautifulSoup4
- lxml
- Pydantic v2
- pydantic-settings

### AI
- Groq Cloud API (`llama-3.3-70b-versatile`)

---

## 5. Project Structure

```text
Digital_Heroes_SDE_Task1/
├── backend/
│   ├── app/
│   │   ├── api/v1/inspect.py            # FastAPI Endpoint (POST /api/v1/inspect)
│   │   ├── services/inspection_service.py # Service Layer Facade
│   │   ├── shared/                      # Constants, Enums, Exceptions, Helpers
│   │   ├── models/                      # Strongly-typed Pydantic Models
│   │   ├── validation/url_validator.py  # Validation Layer
│   │   ├── inspection/engine.py         # HTTP Network Inspector (httpx)
│   │   ├── parser/html_parser.py        # HTML Parser (BS4/lxml)
│   │   ├── features/                    # Feature Extractors (SEO, Performance, Content)
│   │   ├── policies/                    # Policy Loader & Schema Validation
│   │   │   └── v1/*.json                # Versioned Policy Standards
│   │   ├── evaluation/                  # Scoring & Evidence Generator
│   │   ├── ai/                          # PromptBuilder, GroqProvider, Verifier
│   │   └── observability/logger.py      # Structured Logging
│   ├── requirements.txt
│   └── .env
├── frontend/
│   ├── src/
│   │   ├── components/                  # Header & Footer Layout
│   │   ├── features/inspection/components/
│   │   │   ├── UrlInputForm.tsx         # Search Bar & Presets
│   │   │   ├── PipelineStepper.tsx      # Live Execution Progress Stepper
│   │   │   ├── ScoreGauge.tsx           # Health Score Gauge
│   │   │   ├── CategoryBreakdown.tsx    # Category Progress Cards & Drawers
│   │   │   ├── TechnicalMetricsGrid.tsx # Technical Metrics Grid
│   │   │   ├── IssuesAccordion.tsx      # Issues & Action Plan Checklist
│   │   │   └── AiSummaryCard.tsx        # Groq AI Executive Insights
│   │   ├── services/api.ts              # Axios Client
│   │   ├── types/inspection.ts          # TypeScript Types
│   │   ├── App.tsx                      # Dashboard Container
│   │   └── index.css                    # Tailwind CSS Styles
│   ├── package.json
│   ├── vite.config.ts
│   └── tailwind.config.js
├── render.yaml                          # Render Deployment Blueprint
├── vercel.json                          # Vercel Deployment Configuration
└── README.md
```

---

## 6. Installation & Local Setup

### Prerequisites
- Python 3.12+
- Node.js 18+

### Backend Setup
```bash
cd backend
python -m venv .venv

# Activate Virtual Environment:
# On Windows:
.\.venv\Scripts\Activate.ps1
# On Linux/Mac:
source .venv/bin/activate

pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```
Backend API will be live at: `http://localhost:8000/api/v1/inspect`  
Interactive OpenAPI Documentation: `http://localhost:8000/docs`

### Frontend Setup
```bash
cd frontend
npm install
npm run dev
```
Open **`http://localhost:5173`** in your browser.

---

## 7. Environment Variables

Create a `.env` file inside `backend/` directory:

```env
PROJECT_NAME=PAGEPULSE
API_V1_STR=/api/v1
GROQ_API_KEY=your_groq_api_key_here
GROQ_MODEL=llama-3.3-70b-versatile
HTTP_TIMEOUT_SECONDS=10
```

---

## 8. API Contract

### Endpoint: `POST /api/v1/inspect`

#### Example Request
```json
{
  "url": "https://example.com"
}
```

#### Example Success Response (HTTP 200 OK)
```json
{
  "url": "https://example.com/",
  "technical_metrics": {
    "title_length": 14,
    "meta_description_length": 0,
    "h1_count": 1,
    "h2_count": 0,
    "total_images_count": 0,
    "missing_alt_images_count": 0,
    "word_count": 19,
    "internal_links_count": 0,
    "external_links_count": 1,
    "response_time_ms": 515.18,
    "status_code": 200
  },
  "scores": {
    "seo": 38,
    "performance": 100,
    "accessibility": 100,
    "content": 0,
    "overall": 57
  },
  "issues": [
    {
      "issue": "meta_description",
      "category": "seo",
      "severity": "warning",
      "observed_value": 0,
      "expected_value": "70 to 160 characters",
      "recommendation": "Provide a meta description between 70 and 160 characters to summarize page content effectively."
    }
  ],
  "recommendations": [
    "Provide a meta description between 70 and 160 characters to summarize page content effectively."
  ],
  "ai_summary": {
    "executive_summary": "Your website, https://example.com/, has an overall score of 57, indicating room for improvement in SEO areas...",
    "key_strengths": ["Fast response time", "Optimal H1 heading count"],
    "prioritized_issues": ["Title length is too short", "Meta description is missing"],
    "action_plan": ["Update page title tag to 30-60 characters", "Add meta description tag"]
  }
}
```

#### Status Codes & Error Mapping
| HTTP Status | Error Code | Description / UI Status |
| --- | --- | --- |
| **200 OK** | Success | `✅ Website Reachable` |
| **400 Bad Request** | `INVALID_URL_FORMAT` | `❌ Invalid URL Format` |
| **400 Bad Request** | `UNSUPPORTED_PROTOCOL` | `❌ Unsupported Protocol` |
| **400 Bad Request** | `RESTRICTED_NETWORK_ACCESS` | `❌ Restricted Network Access` |
| **502 Bad Gateway** | `DOMAIN_NOT_FOUND` | `❌ Domain Not Found` |
| **502 Bad Gateway** | `SERVER_UNREACHABLE` | `❌ Server Unreachable` |
| **502 Bad Gateway** | `SSL_ERROR` | `❌ SSL Certificate Error` |
| **504 Gateway Timeout** | `REQUEST_TIMED_OUT` | `⚠ Request Timed Out` |
| **500 Internal Error** | `INTERNAL_SERVER_ERROR` | `❌ Server Internal Error` |

---

## 9. Engineering Design Decisions

### Design Decision 1 — Deterministic Evaluation Before AI
Instead of allowing the LLM to inspect HTML or calculate metrics directly, PAGEPULSE first performs deterministic feature extraction and policy evaluation. The AI layer receives only verified evidence (`EvidenceBundle`) generated by the Evaluation Engine.
- **Reasons**:
  - Prevents hallucinated technical metrics and invented numbers.
  - Makes results 100% reproducible across identical inputs.
  - Allows the application to function perfectly even when AI is unavailable or failing.
  - Keeps core business logic completely independent of the LLM provider.

### Design Decision 2 — Versioned JSON Policy Repository (`policies/v1/*.json`)
Evaluation rules are stored as versioned JSON policy files in `backend/app/policies/v1/` instead of being hardcoded inside Python code.
- **Reasons**:
  - Policies can be updated or tuned without modifying application code.
  - New metrics can be introduced simply by adding a new JSON file to the folder.
  - Keeps evaluation rules completely decoupled from execution logic.
  - Enables versioning of standards (e.g. `v1` vs `v2`) for backwards compatibility.

### Design Decision 3 — Thin API Layer with Central Inspection Service (`InspectionService`)
The API route layer (`inspect.py`) contains zero business logic. Instead, every inspection request is coordinated by a dedicated service facade (`InspectionService`).
- **Reasons**:
  - Keeps the API layer thin and focused purely on HTTP serialization & status code mapping.
  - Improves unit and integration testability.
  - Makes every sub-module independently reusable and replaceable.
  - Strictly follows separation of concerns and the Single Responsibility Principle (SRP).

### Design Decision 4 — Strongly Typed Domain Models Across Pipeline (`backend/app/models/`)
Every module communicates strictly using immutable Pydantic models (`InspectionResult`, `PageDocument`, `FeatureVector`, `EvaluationResult`, `EvidenceBundle`, `AISummaryResult`) rather than loosely typed dictionaries.
- **Reasons**:
  - Prevents runtime KeyError bugs and schema mismatch issues.
  - Enforces strict data contracts between pipeline stages.
  - Enables auto-completion and static analysis across the entire backend.

### Design Decision 5 — Optional AI Subsystem with Total Graceful Fallback (`AIService`)
The AI layer is wrapped in a fail-safe exception handler. If the Groq API key is missing, rate-limited, or throws an exception, the system catches the error silently and returns `ai_summary: null`.
- **Reasons**:
  - Ensures 100% application uptime regardless of third-party API reliability.
  - Guarantee that core technical inspection reports are delivered instantly without HTTP 500 errors.

### Design Decision 6 — Modular Specialized Feature Extractors (`backend/app/features/`)
Feature extraction is divided into specialized extractors (`seo.py`, `performance.py`, `content.py`) coordinated by `FeatureExtractor`.
- **Reasons**:
  - Prevents a single monolithic 600-line extraction file.
  - Allows SEO, Performance, and Content metrics to be maintained and extended independently.

### Design Decision 7 — Structured Verification & Fact-Checking Layer (`Verifier`)
Raw LLM JSON outputs are passed through a `Verifier` module before being included in the API response.
- **Reasons**:
  - Validates that the LLM output conforms strictly to the required Pydantic schema.
  - Rejects hallucinated numbers or contradictory statements before reaching the user.

---

## 10. Testing

The codebase includes modular test coverage for:
- URL Syntax Validation & Protocol Normalization
- HTML Parsing & Element Extraction
- Feature Extractor Aggregation
- Policy Repository Loading & Graduated Evaluation Engine Scoring
- AI Prompt Assembly & Fail-safe Error Handling
- FastAPI API Endpoint Integration

---

## 11. Deployment

- **Live Backend (Render)**: [https://digital-heroes-sde-task1.onrender.com](https://digital-heroes-sde-task1.onrender.com)
  - Root: `backend` | Build: `pip install -r requirements.txt` | Start: `cd backend && uvicorn app.main:app --host 0.0.0.0 --port $PORT`
- **Live Frontend (Vercel)**: [https://digital-heroes-sde-task1.vercel.app](https://digital-heroes-sde-task1.vercel.app)
  - Root: `frontend` | Framework: `Vite` | Output: `dist`

---

## 12. Future Improvements

- Advanced Accessibility Audits (WCAG 2.1 AA compliance checks)
- Core Web Vitals & Performance Insights
- Multi-page Website Crawling
- Historical Inspection Reports & Trend Analytics
- Export Inspection PDF Reports
- Google Lighthouse API Integration

---

## 13. License

Distributed under the MIT License.

---

## Built For

Built for <a href="https://digitalheroesco.com" target="_blank" rel="noopener noreferrer">Digital Heroes Training Task</a>
