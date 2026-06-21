// src/lib/api.ts — client for the AI Email Assistant backend.
const BASE = (import.meta.env.VITE_API_BASE as string) || "http://localhost:8000";

export interface Email {
  id: string;
  from: string;
  subject: string;
  received: string;
  unread?: boolean;
  body: string;
}

export interface Entity {
  field: string;
  value: string;
}

export interface SuggestedAction {
  type: string;
  title: string;
  detail: string;
}

export interface EmailAnalysis {
  summary: string;
  intent: string;
  category: string;
  priority: "high" | "medium" | "low";
  entities: Entity[];
  suggested_action: SuggestedAction;
  draft_reply: string;
}

export interface Health {
  status: string;
  mode: "live" | "demo";
  claude: boolean;
  gmail: boolean;
  model: string;
}

export async function getHealth(): Promise<Health> {
  const r = await fetch(`${BASE}/api/health`);
  if (!r.ok) throw new Error("health check failed");
  return r.json();
}

export async function getInbox(): Promise<{ source: string; emails: Email[]; note?: string }> {
  const r = await fetch(`${BASE}/api/inbox`);
  if (!r.ok) throw new Error("inbox fetch failed");
  return r.json();
}

export async function analyzeEmail(email: Email): Promise<{ engine: string; analysis: EmailAnalysis }> {
  const r = await fetch(`${BASE}/api/analyze`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ email }),
  });
  if (!r.ok) throw new Error("analyze failed");
  return r.json();
}

export async function act(
  email: Email,
  action: string,
  draft?: string,
): Promise<{ status: string; message: string; performed: boolean }> {
  const r = await fetch(`${BASE}/api/act`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ email, action, draft }),
  });
  if (!r.ok) throw new Error("act failed");
  return r.json();
}
