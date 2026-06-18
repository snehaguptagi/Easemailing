# Architecture

Easemailing is an AI email-automation agent: a **Flask** API + a **React** frontend that drafts, sends, and researches email.

## Components

**Backend — Flask (`app.py`)**, runs on `PORT` (default 5000). Endpoints:
- `GET /health`
- `POST /generate-email` — AI draft
- `POST /send-email` — deliver

Supporting modules:
- **`email_management.py` / `email_lam_model.py`** — OpenAI GPT email-content generation.
- **`lam_email_automation.py` / `email_utils.py`** — compose + send via SendGrid.
- **`gmail_auth.py` / `gmail_oauth.py` / `gmail_service.py`** — Gmail API auth + read/send.
- **`extract_email_info.py`** — parse structured fields out of incoming mail.
- **`serper_search.py` / `reddit_scraper.py`** — optional web/Reddit context to ground drafts.

**Frontend — React (`src/`)**: `App.jsx`, `pages/` (Home, Compose, Dashboard), `components/` (Navbar, Footer). Talks to the Flask API.

## Data flow
```
Compose (frontend)
   → POST /generate-email → OpenAI draft  (optionally grounded by Serper / Reddit)
   → review
   → POST /send-email → SendGrid / Gmail delivery

incoming mail → gmail_service → extract_email_info → structured data
```

## Key decisions
- **Keys via env only.** OpenAI / SendGrid / Serper / Reddit keys come from a gitignored `.env` (see `.env.example`) — none are hardcoded.
- **Connectors kept separate.** Gmail (read/send) lives in its own modules, isolated from the SendGrid send path, so either can change independently.
- **Pluggable research.** Serper + Reddit are optional context sources, decoupled from generation.

## Layout
```
app.py                   Flask API (/health, /generate-email, /send-email)
email_management.py …    OpenAI content generation
lam_email_automation.py  compose + SendGrid send
gmail_*.py               Gmail auth + service (read/send)
serper_search.py
reddit_scraper.py        research / context
src/                     React frontend (pages, components)
```
