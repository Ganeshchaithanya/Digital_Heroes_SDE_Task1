# PAGEPULSE — Website Inspection Platform

PAGEPULSE is a full-stack website inspection application built with a **Python 3.12 / FastAPI** backend and a **React / TypeScript / Tailwind CSS** frontend.

The platform accepts any valid website URL, fetches the HTML, measures quantitative technical metrics, evaluates them deterministically using JSON policy standards, and optionally produces AI explanations powered by Groq LLM.

---

## ⚡ Architecture Overview

```text
User ➔ React Frontend ➔ FastAPI Backend ➔ Inspection Engine ➔ HTML Parser ➔ Feature Extractor ➔ Policy Engine ➔ AI Summary ➔ JSON Response
```

- **Core Core Application**: Operates deterministically without depending on AI.
- **Fail-Safe AI**: If AI fails or is disabled, technical metrics and scores remain 100% accurate.

---

## 🛠️ Quick Local Setup

### Backend
```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

### Frontend
```powershell
cd frontend
npm install
npm run dev
```

---

## 🌐 API Endpoint

`POST /api/v1/inspect`

**Request Body:**
```json
{
  "url": "https://example.com"
}
```

---

## 📄 License
MIT License. Built for Digital Heroes Software Engineering Assignment.
