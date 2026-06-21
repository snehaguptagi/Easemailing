# AI Email Assistant

Turn your inbox into a task queue. AI Email Assistant reads an email, infers what the
sender actually wants, extracts the key facts, recommends the next action, and drafts a
reply — so you act on email instead of just reading it.

This is one end-to-end product:

- **Frontend** (`frontend/`) — React + Vite + TypeScript + Tailwind + shadcn/ui. A landing
  page plus a functional app at `/app`: inbox → pick an email → **Analyze with AI** →
  see summary / intent / category / priority / extracted entities / suggested action /
  editable draft → **Approve & run the action**.
- **Backend** (`backend/`) — FastAPI + a Claude-powered reasoning engine. Returns a
  validated structured analysis per email.

## Real + demo mode

It works with **zero credentials** and gets better as you add them:

| You provide | What happens |
|---|---|
| Nothing | Mock inbox + a built-in heuristic engine. Full UX, fully offline. |
| `ANTHROPIC_API_KEY` | Emails are analyzed by **Claude** (`claude-opus-4-8` by default). |
| Gmail OAuth + `AIEA_MODE=live` | Pulls your real inbox and drafts replies straight into Gmail. |

## Run it

**Backend** (terminal 1):

```bash
cd backend
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp ../.env.example .env          # optional: add ANTHROPIC_API_KEY for real analysis
uvicorn main:app --reload --port 8000
```

**Frontend** (terminal 2):

```bash
cd frontend
npm install
npm run dev                      # http://localhost:5173  →  open /app
```

Open `http://localhost:5173`, click **Open the App**, pick an email, and hit
**Analyze with AI**.

## API

| Method | Route | Purpose |
|---|---|---|
| `GET`  | `/api/health`  | mode + whether Claude / Gmail are wired |
| `GET`  | `/api/inbox`   | list emails (mock, or Gmail in live mode) |
| `POST` | `/api/analyze` | `{email}` → structured analysis |
| `POST` | `/api/act`     | `{email, action, draft}` → perform/queue the action |

## How the engine works

`backend/engine.py` defines a Pydantic `EmailAnalysis` schema and calls Claude via
`messages.parse()` so every response is validated against that schema. If no API key is
set, it falls back to a deterministic heuristic with the same shape, so the frontend
behaves identically in demo mode.
