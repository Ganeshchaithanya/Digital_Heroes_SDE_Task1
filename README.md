# PAGEPULSE

AI-Assisted Website Inspection Platform built with FastAPI and React.

Built for the Digital Heroes Software Development Internship Task.

---

## Overview

PAGEPULSE is a deterministic website inspection platform that analyzes any public website and evaluates technical, SEO, content, and accessibility metrics using policy-based evaluation.

The platform performs all measurements deterministically. AI is used only to explain the findings and never to compute them.

---

## Features

- **Validation vs. Inspection Separation**: Syntactically valid URLs (e.g. `https://localhost.com`) that fail network fetch display `✔ URL Valid | ✖ Website Unreachable` instead of mislabeling valid URL strings.
- **Error Taxonomy & Status Mapping**: Specialized exceptions for DNS failure, connection refusal, SSL errors, request timeouts, and protocol restrictions.
- **Live Pipeline Stepper UI**: Animated 6-step progress stepper demonstrating live execution of inspection stages in the frontend dashboard.
- **Smart Image ALT Parsing**: Decorative images (`alt=""`), presentation images (`role="presentation"`, `aria-hidden="true"`), and inline icons are recognized so accessibility is evaluated accurately without over-reporting issues.
- **Graduated Penalty Scoring Engine**: Partial credit scoring for minor numerical range variances (e.g. title length 61 vs max 60 incurs a minor 2% deduction rather than a catastrophic binary failure).
- **Expandable Category Rule Inspection**: Interactive UI drawers displaying rule-by-rule status (`✓ Passed`, `⚠️ Variance`, `❌ Issue`).
- **AI Executive Summary (Groq)**: Friendly human English executive insights, key strengths, prioritized issues, and action plans powered by Groq LLM (`llama-3.3-70b-versatile`).
- **Mandatory Digital Heroes Footer**: Persistent footer on all pages with hyperlink pointing to `https://digitalheroesco.com`.

---

## 🚦 Status Mapping Taxonomy

| Situation | UI Status | HTTP Code / Exception |
| --- | --- | --- |
| Malformed URL | `❌ Invalid URL Format` | HTTP 400 (`INVALID_URL_FORMAT`) |
| Unsupported scheme | `❌ Unsupported Protocol` | HTTP 400 (`UNSUPPORTED_PROTOCOL`) |
| Private IP Restricted | `❌ Restricted Network Access` | HTTP 400 (`RESTRICTED_NETWORK_ACCESS`) |
| DNS lookup failed | `❌ Domain Not Found` | HTTP 502 (`DOMAIN_NOT_FOUND`) |
| Connection refused | `❌ Server Unreachable` | HTTP 502 (`SERVER_UNREACHABLE`) |
| SSL Error | `❌ SSL Certificate Error` | HTTP 502 (`SSL_ERROR`) |
| Request timeout | `⚠ Request Timed Out` | HTTP 504 (`REQUEST_TIMED_OUT`) |
| HTTP 404 / 403 / 500 | `⚠ HTTP status code` | Serves report with status indicator |
| HTTP 200 | `✅ Website Reachable` | Serves complete inspection report |

---

## System Architecture

```text
User
 │
 ▼
React Frontend (Pipeline Stepper)
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

### 2. Category Weights for Overall Score
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
.\.venv\Scripts\Activate.ps1
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

## API Documentation

### `POST /api/v1/inspect`

#### Request
```json
{
  "url": "https://example.com"
}
```

---

## License

MIT License.

---

## Built For

Built for <a href="https://digitalheroesco.com" target="_blank" rel="noopener noreferrer">Digital Heroes Training Task</a>
