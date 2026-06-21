"""The reasoning engine for AI Email Assistant.

Given a single email, Claude produces a structured analysis: a one-line summary,
the sender's core ask, a category, a priority, the key entities present, one
recommended next action, and a ready-to-send draft reply.

Real mode  : uses Claude (claude-opus-4-8 by default) via the Anthropic SDK when
             ANTHROPIC_API_KEY is set.
Demo mode  : if no key is present, falls back to a deterministic heuristic so the
             whole product still works end-to-end with zero credentials.
"""
from __future__ import annotations

import os
import re
from typing import List, Literal

from pydantic import BaseModel, Field

# Default to the most capable model; override with AIEA_MODEL (e.g. claude-haiku-4-5
# for cheaper/faster classification).
MODEL = os.getenv("AIEA_MODEL", "claude-opus-4-8")

Category = Literal[
    "meeting_request",
    "customer_support",
    "sales_lead",
    "invoice_billing",
    "internal_update",
    "personal",
    "newsletter_promotion",
    "other",
]
Priority = Literal["high", "medium", "low"]
ActionType = Literal[
    "reply",
    "forward",
    "schedule_meeting",
    "create_task",
    "approve_request",
    "archive",
    "escalate",
]


class Entity(BaseModel):
    field: str = Field(description="What this value is, e.g. 'deadline', 'amount', 'order_id'")
    value: str = Field(description="The extracted value, verbatim from the email")


class SuggestedAction(BaseModel):
    type: ActionType
    title: str = Field(description="Short label for the action, e.g. 'Reply with availability'")
    detail: str = Field(description="One sentence on what the action does and why")


class EmailAnalysis(BaseModel):
    summary: str = Field(description="One-line summary of the email")
    intent: str = Field(description="The sender's core ask — what they want to happen")
    category: Category
    priority: Priority
    entities: List[Entity] = Field(description="Key facts present in the email; empty list if none")
    suggested_action: SuggestedAction
    draft_reply: str = Field(description="A concise, professional, ready-to-send reply")


SYSTEM = """You are the reasoning engine for "AI Email Assistant", a tool that turns an inbox into a task queue.

Given ONE email, produce a structured analysis:
- summary: one neutral line capturing what the email is about.
- intent: the sender's core ask — what they actually want to happen next.
- category: the single best-fitting category.
- priority: high (needs action today / time-sensitive / from an important sender), medium (needs action soon), or low (FYI, newsletter, no action).
- entities: only facts that are actually present — dates, deadlines, amounts, order IDs, names, links, meeting times. Do not invent any. Empty list if none.
- suggested_action: the single most useful next step, with a short title and one-sentence detail.
- draft_reply: a concise, professional reply the user could send as-is, in a warm but efficient voice. For emails that need no reply (newsletters, pure FYI), write a one-line note saying no reply is needed.

Be specific and grounded in the email. Never fabricate details that aren't in the text."""


def _email_to_prompt(email: dict) -> str:
    return (
        f"From: {email.get('from', 'unknown')}\n"
        f"Subject: {email.get('subject', '(no subject)')}\n"
        f"Received: {email.get('received', '')}\n\n"
        f"{email.get('body', '')}"
    )


def analyze_with_claude(email: dict) -> EmailAnalysis:
    """Run the real Claude analysis. Raises if the SDK/key is unavailable."""
    import anthropic  # imported lazily so demo mode needs no dependency

    client = anthropic.Anthropic()  # reads ANTHROPIC_API_KEY from the environment
    response = client.messages.parse(
        model=MODEL,
        max_tokens=2048,
        system=SYSTEM,
        messages=[{"role": "user", "content": _email_to_prompt(email)}],
        output_format=EmailAnalysis,
    )
    if response.stop_reason == "refusal" or response.parsed_output is None:
        raise RuntimeError("Model declined or returned no structured output")
    return response.parsed_output


# ---------------------------------------------------------------------------
# Demo fallback — deterministic, no API key required. Keeps the product fully
# functional offline; clearly labelled as heuristic in the API response.
# ---------------------------------------------------------------------------

def _heuristic_entities(body: str) -> List[Entity]:
    out: List[Entity] = []
    patterns = {
        "amount": r"(?:[$₹€£]\s?\d[\d,]*(?:\.\d+)?)",
        "order_id": r"(?:order\s*(?:id|number|#)?\s*[:#]?\s*)([A-Z0-9-]{4,})",
        "date": r"\b(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})\b",
        "link": r"(https?://[^\s)>\]]+)",
    }
    for field, pat in patterns.items():
        m = re.search(pat, body, re.IGNORECASE)
        if m:
            out.append(Entity(field=field, value=m.group(m.lastindex or 0).strip()))
    return out


def analyze_heuristic(email: dict) -> EmailAnalysis:
    subject = email.get("subject", "")
    body = email.get("body", "")
    sender = email.get("from", "someone")
    text = f"{subject}\n{body}".lower()

    if any(w in text for w in ("meeting", "call", "schedule", "calendar", "available", "sync")):
        category: Category = "meeting_request"
        action = SuggestedAction(type="schedule_meeting", title="Propose a time",
                                 detail="Sender wants to meet — reply with availability or send a calendar invite.")
        intent = "Schedule a meeting or call."
    elif any(w in text for w in ("invoice", "payment", "billing", "refund", "$", "charged")):
        category = "invoice_billing"
        action = SuggestedAction(type="approve_request", title="Review the billing item",
                                 detail="A payment or invoice matter that needs a decision.")
        intent = "Resolve a billing or payment question."
    elif any(w in text for w in ("issue", "help", "support", "not working", "error", "problem", "bug")):
        category = "customer_support"
        action = SuggestedAction(type="reply", title="Respond to the request",
                                 detail="A support question that needs an answer.")
        intent = "Get help with a problem."
    elif any(w in text for w in ("demo", "pricing", "interested", "quote", "trial", "buy")):
        category = "sales_lead"
        action = SuggestedAction(type="reply", title="Follow up with the lead",
                                 detail="A potential customer expressed interest — reply promptly.")
        intent = "Move a sales conversation forward."
    elif any(w in text for w in ("unsubscribe", "newsletter", "% off", "sale", "promo")):
        category = "newsletter_promotion"
        action = SuggestedAction(type="archive", title="Archive",
                                 detail="Promotional email — no reply needed.")
        intent = "Marketing message; no action required."
    else:
        category = "other"
        action = SuggestedAction(type="reply", title="Review and reply",
                                 detail="General message that may need a short reply.")
        intent = "General correspondence."

    priority: Priority = "high" if any(
        w in text for w in ("urgent", "asap", "today", "immediately", "deadline")) else (
        "low" if category == "newsletter_promotion" else "medium")

    name = sender.split("<")[0].strip() or "there"
    if category == "newsletter_promotion":
        draft = "No reply needed — this is a promotional email."
    else:
        draft = (f"Hi {name},\n\nThanks for your email regarding \"{subject}\". "
                 f"I've reviewed it and will follow up shortly.\n\nBest,\nSneha")

    return EmailAnalysis(
        summary=(subject or body[:80] or "Email").strip(),
        intent=intent,
        category=category,
        priority=priority,
        entities=_heuristic_entities(body),
        suggested_action=action,
        draft_reply=draft,
    )


def analyze(email: dict) -> tuple[EmailAnalysis, str]:
    """Return (analysis, engine) where engine is 'claude' or 'heuristic'."""
    if os.getenv("ANTHROPIC_API_KEY"):
        try:
            return analyze_with_claude(email), "claude"
        except Exception as exc:  # noqa: BLE001 — fall back gracefully in any failure
            print(f"[engine] Claude analysis failed ({exc}); falling back to heuristic")
    return analyze_heuristic(email), "heuristic"
