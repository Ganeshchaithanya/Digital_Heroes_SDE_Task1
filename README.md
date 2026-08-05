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
- **Smart Image ALT Parsing**: Decorative images (`alt=""`), presentation images (`role="presentation"`, `aria-hidden="true"`), and inline icons are recognized so accessibility is evaluated accurately without over-reporting issues.
- **Feature Extraction**: Quantitative metric calculation into strongly typed `FeatureVector` models.
- **Graduated Penalty Scoring Engine**: Partial credit scoring for minor numerical range variances (e.g. title length 61 vs max 60 incurs a minor 2% deduction rather than a catastrophic binary failure).
- **Expandable Category Rule Inspection**: Interactive UI drawers displaying rule-by-rule status (`✓ Passed`, `⚠️ Variance`, `❌ Issue`).
- **Technical Metrics Dashboard**: Real-time display of response latency, image ALT coverage, heading counts, and word count.
- **AI Executive Summary (Groq)**: Friendly human English executive insights, key strengths, prioritized issues, and action plans powered by Groq LLM (`llama-3.3-70b-versatile`).
- **AI Verification Layer**: Strict Pydantic schema validation and factual numerical integrity checks.
- **Mandatory Digital Heroes Footer**: Persistent footer on all pages with hyperlink pointing to `https://digitalheroesco.com`.
- **Responsive React UI**: Clean, modern interface built with React 18, TypeScript, and Tailwind CSS.

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
 ├──────── Evaluation Engine (Graduated Scoring)
 ├──────── Evidence Generator
 ├──────── AI Service (Optional & Fail-safe)
 └──────── Response Builder
```

---

## 🧮 Scoring Methodology & Computation Formulas

The Evaluation Engine computes scores deterministically using weighted category formulas and proportional penalty functions.

### 1. Proportional Penalty Math (Partial Credit)
For rules with numerical range bounds (such as Title Length: 30–60 chars), minor variances receive partial credit instead of a binary zero:

$$\text{Deviation Ratio} = \max\left(0.0, 1.0 - \frac{|\text{Observed Value} - \text{Bound}|}{\text{Span}}\right)$$

*Example*: Title length of 61 characters (1 char over 60):  
$$\text{Score Ratio} = 1.0 - \frac{1}{60} = 0.98 \quad (98\% \text{ Pass Credit})$$

### 2. Category Weights for Overall Score
Category scores are aggregated into the Overall Health Score using explicit weights:

$$\text{Overall Score} = (\text{SEO} \times 0.35) + (\text{Performance} \times 0.25) + (\text{Accessibility} \times 0.25) + (\text{Content} \times 0.15)$$

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

---

## Evaluation Policies

The application evaluates websites using deterministic JSON policies stored in `backend/app/policies/v1/`:

- **Title Length**: `title_length.json` (Expected: 30 to 60 characters)
- **Meta Description**: `meta_description.json` (Expected: 70 to 160 characters)
- **H1 Count**: `h1_count.json` (Expected: Exactly 1 H1 tag)
- **Image ALT**: `image_alt.json` (Expected: 0 missing ALT attributes on content images)
- **Response Time**: `response_time.json` (Expected: Under 2000 ms)
- **Word Count**: `word_count.json` (Expected: At least 300 words)

---

## Deployment

- **Frontend**: Deploy on **Vercel** (Root: `frontend`, Framework: `Vite`, Build: `npm run build`).
- **Backend**: Deploy on **Render** (Root: `backend`, Build: `pip install -r requirements.txt`, Start: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`).

---

## License

MIT License.

---

## Built For

Built for <a href="https://digitalheroesco.com" target="_blank" rel="noopener noreferrer">Digital Heroes Training Task</a>
