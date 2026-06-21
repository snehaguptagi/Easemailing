"""AI Email Assistant — FastAPI backend.

Endpoints
  GET  /api/health            mode + whether Claude / Gmail are wired
  GET  /api/inbox             list emails (mock in demo mode, Gmail in live mode)
  POST /api/analyze           {email} -> structured analysis (Claude, or heuristic fallback)
  POST /api/act               {email, action, draft} -> perform/queue the action

Run:  uvicorn main:app --reload --port 8000   (from the backend/ directory)
"""
from __future__ import annotations

import os

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

import engine
import gmail_provider
from mock_data import MOCK_INBOX

load_dotenv()

# "live" pulls from Gmail; anything else (default) uses the mock inbox.
MODE = os.getenv("AIEA_MODE", "demo").lower()

app = FastAPI(title="AI Email Assistant")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # dev only; lock down in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def _live() -> bool:
    return MODE == "live" and gmail_provider.is_available()


@app.get("/api/health")
def health():
    return {
        "status": "ok",
        "mode": "live" if _live() else "demo",
        "claude": bool(os.getenv("ANTHROPIC_API_KEY")),
        "gmail": gmail_provider.is_available(),
        "model": engine.MODEL,
    }


@app.get("/api/inbox")
def inbox():
    if _live():
        try:
            return {"source": "gmail", "emails": gmail_provider.list_inbox()}
        except gmail_provider.GmailUnavailable as exc:
            return {"source": "mock", "emails": MOCK_INBOX, "note": str(exc)}
    return {"source": "mock", "emails": MOCK_INBOX}


class AnalyzeRequest(BaseModel):
    email: dict


@app.post("/api/analyze")
def analyze(req: AnalyzeRequest):
    result, used = engine.analyze(req.email)
    return {"engine": used, "analysis": result.model_dump()}


class ActRequest(BaseModel):
    email: dict
    action: str          # the chosen action type
    draft: str | None = None  # edited draft reply, if the action is a reply


@app.post("/api/act")
def act(req: ActRequest):
    to = req.email.get("from", "")
    subject = "Re: " + req.email.get("subject", "")

    if req.action in ("reply", "forward") and _live() and req.draft:
        try:
            draft_id = gmail_provider.create_draft(to, subject, req.draft)
            return {"status": "done", "message": f"Draft created in Gmail (id {draft_id}).",
                    "performed": True}
        except gmail_provider.GmailUnavailable as exc:
            return {"status": "error", "message": str(exc), "performed": False}

    # Demo mode (or non-email actions): simulate the action so the flow completes.
    labels = {
        "reply": f"Draft reply to {to} prepared.",
        "forward": f"Draft forward of \"{subject}\" prepared.",
        "schedule_meeting": "Calendar hold drafted — ready to send the invite.",
        "create_task": "Task created in your tracker.",
        "approve_request": "Approval recorded.",
        "archive": "Email archived.",
        "escalate": "Escalated to the right owner.",
    }
    return {
        "status": "done",
        "message": labels.get(req.action, "Action queued."),
        "performed": False,  # simulated in demo mode
    }
