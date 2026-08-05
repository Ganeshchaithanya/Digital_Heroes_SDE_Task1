# PAGEPULSE

AI-Assisted Website Inspection Platform built with FastAPI and React.

Built for the Digital Heroes Software Development Internship Task.

---

## Overview

PAGEPULSE is a deterministic website inspection platform that analyzes any public website and evaluates technical, SEO, content, and accessibility metrics using policy-based evaluation.

The platform performs all measurements deterministically. AI is used only to explain the findings and never to compute them.

---

## Features

- **URL Validation**: Syntax checking, protocol scheme normalization (`http`/`https`), and SSRF network restriction.
- **HTTP Inspection**: Measured response latency, status codes, and HTTP headers via `httpx`.
- **HTML Parsing**: Robust extraction of titles, meta descriptions, headings (H1-H6), paragraphs, images, and links via `BeautifulSoup4` & `lxml`.
- **Feature Extraction**: Quantitative metric calculation into strongly typed `FeatureVector` models.
- **Policy-Based Evaluation**: Dynamic rules evaluation using versioned JSON policy standards (`policies/v1/*.json`).
- **Technical Metrics Dashboard**: Real-time display of response latency, image ALT coverage, heading counts, and word count.
- **AI Executive Summary (Groq)**: Friendly human English executive insights, key strengths, prioritized issues, and action plans powered by Groq LLM (`llama-3.3-70b-versatile`).
- **AI Verification Layer**: Strict Pydantic schema validation and factual numerical integrity checks.
- **Responsive React UI**: Clean, modern glassmorphism interface built with React 18, TypeScript, and Tailwind CSS.
- **Structured API**: Clean FastAPI REST API exposing `POST /api/v1/inspect`.

---

## System Architecture

```text
User
 │
 ▼
React Frontend
 │
 ▼
FastAPI API Endpoint
 │
 ▼
Inspection Service
 │
 ├──────── Validation Layer
 ├──────── Inspection Engine
 ├──────── Document Parser
 ├──────── Feature Extraction
 ├──────── Policy Loader
 ├──────── Evaluation Engine
 ├──────── Evidence Generator
 ├──────── AI Service (Optional & Fail-safe)
 └──────── Response Builder
```

---

## Tech Stack

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

### AI
- Groq Cloud API (`llama-3.3-70b-versatile`)

---

## Project Structure

```text
Digital_Heroes_SDE_Task1/
├── backend/
│   ├── app/
│   │   ├── api/v1/inspect.py            # FastAPI Endpoint
│   │   ├── services/inspection_service.py # Service Layer Facade
│   │   ├── shared/                      # Constants, Enums, Exceptions, Helpers
│   │   ├── models/                      # Pydantic Domain Models
│   │   ├── validation/url_validator.py  # Validation Layer
│   │   ├── inspection/engine.py         # Network Fetcher
│   │   ├── parser/html_parser.py        # BeautifulSoup4 Parser
│   │   ├── features/                    # SEO, Performance & Content Extractors
│   │   ├── policies/                    # Policy Loader & Schema Validation
│   │   │   └── v1/*.json                # JSON Policy Standards
│   │   ├── evaluation/                  # Scoring & Evidence Generator
│   │   ├── ai/                          # PromptBuilder, GroqProvider, Verifier
│   │   └── observability/logger.py      # Structured Logger
│   ├── requirements.txt
│   └── .env
├── frontend/
│   ├── src/
│   │   ├── components/                  # Header & Footer Layout
│   │   ├── features/inspection/components/
│   │   │   ├── UrlInputForm.tsx         # Search Bar & Presets
│   │   │   ├── ScoreGauge.tsx           # Health Score Gauge
│   │   │   ├── CategoryBreakdown.tsx    # Category Progress Cards
│   │   │   ├── TechnicalMetricsGrid.tsx # Technical Metrics Grid
│   │   │   ├── IssuesAccordion.tsx      # Issues & Action Plan
│   │   │   └── AiSummaryCard.tsx        # Groq AI Executive Insights
│   │   ├── services/api.ts              # Axios Client
│   │   ├── types/inspection.ts          # TypeScript Types
│   │   ├── App.tsx                      # Dashboard Container
│   │   └── index.css                    # Tailwind CSS Styles
│   ├── package.json
│   ├── vite.config.ts
│   └── tailwind.config.js
└── README.md
```

---

## Installation

### Clone
```bash
git clone https://github.com/Ganeshchaithanya/Digital_Heroes_SDE_Task1.git
cd Digital_Heroes_SDE_Task1
```

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

### Frontend Setup
```bash
cd frontend
npm install
npm run dev
```

---

## Environment Variables

Create a `.env` file inside `backend/` directory:

```env
PROJECT_NAME=PAGEPULSE
API_V1_STR=/api/v1
GROQ_API_KEY=your_groq_api_key_here
GROQ_MODEL=llama-3.3-70b-versatile
HTTP_TIMEOUT_SECONDS=10
```

---

## API Documentation

### `POST /api/v1/inspect`

#### Example Request
```json
{
  "url": "https://example.com"
}
```

#### Example Response
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

---

## Evaluation Policies

The application evaluates websites using deterministic JSON policies stored in `backend/app/policies/v1/`:

- **Title Length**: `title_length.json` (Expected: 30 to 60 characters)
- **Meta Description**: `meta_description.json` (Expected: 70 to 160 characters)
- **H1 Count**: `h1_count.json` (Expected: Exactly 1 H1 tag)
- **Image ALT**: `image_alt.json` (Expected: 0 missing ALT attributes)
- **Response Time**: `response_time.json` (Expected: Under 2000 ms)
- **Word Count**: `word_count.json` (Expected: At least 300 words)

---

## AI Pipeline

```text
EvidenceBundle
      │
      ▼
Prompt Builder
      │
      ▼
Groq API (llama-3.3-70b-versatile)
      │
      ▼
Verifier (Fact Checker)
      │
      ▼
Executive Summary
```

- The AI **never computes metrics or scores**.
- It only explains deterministic evidence in friendly, natural human English.
- If AI fails or is disabled, the core technical metrics and scores return 100% intact.

---

## Deployment

- **Frontend**: Deploy on **Vercel** (Root: `frontend`, Framework: `Vite`, Build: `npm run build`).
- **Backend**: Deploy on **Render** (Root: `backend`, Build: `pip install -r requirements.txt`, Start: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`).

---

## Future Improvements

- Advanced Accessibility Audits (WCAG 2.1 compliance checks)
- Core Web Vitals & Performance Insights
- Multi-page Web Crawling
- Historical Inspection Reports & Trend Analytics
- PDF Report Export
- Google Lighthouse API Integration

---

## License

MIT License.

---

## Built For

Built for the **Digital Heroes Software Development Internship Task**.
