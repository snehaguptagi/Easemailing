import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Alert, AlertDescription } from "@/components/ui/alert";
import {
  ArrowLeft, Wifi, WifiOff, Sparkles, AlertCircle, Loader2, Play,
  Inbox, Brain, FileText, ListChecks, Send, CheckCircle2, Circle,
} from "lucide-react";
import {
  getHealth, getInbox, analyzeEmail, act,
  type Email, type EmailAnalysis, type Health,
} from "@/lib/api";

/**
 * LiveDemo — a guided, step-by-step walkthrough of the whole pipeline,
 * running against the REAL backend (the same /api/inbox, /api/analyze and
 * /api/act the working app uses). It's the "watch it work" surface: one email
 * flows through Fetch → Understand → Extract → Recommend → Act, live.
 */

type StepKey = "fetch" | "understand" | "extract" | "recommend" | "act";
type StepStatus = "idle" | "running" | "done";

const STEP_META: Record<StepKey, { title: string; blurb: string; icon: JSX.Element }> = {
  fetch: { title: "Fetch", blurb: "Pull the latest email from the inbox", icon: <Inbox className="w-5 h-5" /> },
  understand: { title: "Understand", blurb: "Summarize it and read the sender's real ask", icon: <Brain className="w-5 h-5" /> },
  extract: { title: "Extract", blurb: "Pull the key facts — dates, amounts, IDs", icon: <FileText className="w-5 h-5" /> },
  recommend: { title: "Recommend", blurb: "Decide the single best next action + draft", icon: <ListChecks className="w-5 h-5" /> },
  act: { title: "Act", blurb: "Perform or queue the action", icon: <Send className="w-5 h-5" /> },
};

const ORDER: StepKey[] = ["fetch", "understand", "extract", "recommend", "act"];

const priorityColor: Record<string, string> = {
  high: "bg-red-500/15 text-red-500 border-red-500/30",
  medium: "bg-amber-500/15 text-amber-500 border-amber-500/30",
  low: "bg-slate-500/15 text-slate-400 border-slate-500/30",
};

const sleep = (ms: number) => new Promise((r) => setTimeout(r, ms));

const LiveDemo = () => {
  const navigate = useNavigate();
  const [health, setHealth] = useState<Health | null>(null);
  const [connError, setConnError] = useState<string | null>(null);
  const [emails, setEmails] = useState<Email[]>([]);
  const [running, setRunning] = useState(false);

  const [status, setStatus] = useState<Record<StepKey, StepStatus>>({
    fetch: "idle", understand: "idle", extract: "idle", recommend: "idle", act: "idle",
  });
  const [email, setEmail] = useState<Email | null>(null);
  const [analysis, setAnalysis] = useState<EmailAnalysis | null>(null);
  const [engineUsed, setEngineUsed] = useState("");
  const [actResult, setActResult] = useState<string | null>(null);

  useEffect(() => {
    (async () => {
      try {
        const [h, inbox] = await Promise.all([getHealth(), getInbox()]);
        setHealth(h);
        setEmails(inbox.emails);
      } catch {
        setConnError(
          "Can't reach the backend on port 8000. Start it with: cd backend && uvicorn main:app --port 8000",
        );
      }
    })();
  }, []);

  const setStep = (k: StepKey, s: StepStatus) =>
    setStatus((prev) => ({ ...prev, [k]: s }));

  const run = async (chosen?: Email) => {
    setRunning(true);
    setEmail(null);
    setAnalysis(null);
    setActResult(null);
    setStatus({ fetch: "idle", understand: "idle", extract: "idle", recommend: "idle", act: "idle" });

    try {
      // 1 — Fetch
      setStep("fetch", "running");
      await sleep(450);
      const picked = chosen ?? emails.find((e) => e.unread) ?? emails[0];
      if (!picked) throw new Error("no-email");
      setEmail(picked);
      setStep("fetch", "done");

      // 2/3/4 — Understand + Extract + Recommend all come from one analyze() call.
      setStep("understand", "running");
      const res = await analyzeEmail(picked);
      setAnalysis(res.analysis);
      setEngineUsed(res.engine);
      setStep("understand", "done");

      setStep("extract", "running");
      await sleep(500);
      setStep("extract", "done");

      setStep("recommend", "running");
      await sleep(500);
      setStep("recommend", "done");

      // 5 — Act
      setStep("act", "running");
      const a = await act(picked, res.analysis.suggested_action.type, res.analysis.draft_reply);
      setActResult(a.message);
      setStep("act", "done");
    } catch {
      setConnError("The pipeline hit an error mid-run. Is the backend running on port 8000?");
    }
    setRunning(false);
  };

  const StepIcon = ({ k }: { k: StepKey }) => {
    const s = status[k];
    if (s === "done") return <CheckCircle2 className="w-5 h-5 text-green-500" />;
    if (s === "running") return <Loader2 className="w-5 h-5 text-primary animate-spin" />;
    return <Circle className="w-5 h-5 text-muted-foreground/40" />;
  };

  return (
    <div className="min-h-screen p-6">
      <div className="max-w-5xl mx-auto">
        <Button variant="ghost" onClick={() => navigate("/")} className="mb-4">
          <ArrowLeft className="w-4 h-4 mr-2" /> Back to Home
        </Button>

        <div className="flex flex-wrap items-center justify-between gap-3 mb-2">
          <h1 className="text-3xl md:text-4xl font-bold text-foreground">Watch it work</h1>
          <div className="flex items-center gap-2">
            {health?.mode === "live" ? (
              <Badge className="bg-green-500/15 text-green-500 border-green-500/30">
                <Wifi className="w-3 h-3 mr-1" /> Live Gmail
              </Badge>
            ) : (
              <Badge className="bg-yellow-500/15 text-yellow-500 border-yellow-500/30">
                <WifiOff className="w-3 h-3 mr-1" /> Demo inbox
              </Badge>
            )}
            <Badge variant="outline" className="text-xs">
              <Sparkles className="w-3 h-3 mr-1" />
              {health?.claude ? `Claude · ${health.model}` : "Heuristic (no API key)"}
            </Badge>
          </div>
        </div>
        <p className="text-muted-foreground text-lg mb-6">
          One email, all the way through — fetched, understood, distilled to facts, turned into a
          recommended action, and acted on. This runs the same backend as the live app.
        </p>

        {connError && (
          <Alert className="mb-6 border-yellow-500/30 bg-yellow-500/10">
            <AlertCircle className="h-4 w-4 text-yellow-500" />
            <AlertDescription className="text-yellow-600 dark:text-yellow-400 whitespace-pre-wrap">
              {connError}
            </AlertDescription>
          </Alert>
        )}

        <Button onClick={() => run()} disabled={running || emails.length === 0} className="mb-8">
          {running ? <Loader2 className="w-4 h-4 mr-2 animate-spin" /> : <Play className="w-4 h-4 mr-2" />}
          {running ? "Running the pipeline…" : "Run the live pipeline"}
        </Button>

        <div className="grid grid-cols-1 md:grid-cols-[260px_1fr] gap-6">
          {/* Step rail */}
          <ol className="space-y-3">
            {ORDER.map((k, i) => (
              <li
                key={k}
                className={`flex items-start gap-3 p-3 rounded-lg border transition-colors ${
                  status[k] === "idle" ? "border-border opacity-60" : "border-primary/30 bg-primary/5"
                }`}
              >
                <StepIcon k={k} />
                <div>
                  <p className="text-sm font-medium text-foreground flex items-center gap-2">
                    <span className="text-muted-foreground">{i + 1}.</span>
                    {STEP_META[k].icon} {STEP_META[k].title}
                  </p>
                  <p className="text-xs text-muted-foreground mt-0.5">{STEP_META[k].blurb}</p>
                </div>
              </li>
            ))}
          </ol>

          {/* Live output */}
          <div className="space-y-4">
            {!email && !running && (
              <div className="h-full flex items-center justify-center text-muted-foreground border border-dashed border-border rounded-lg p-12 text-center">
                Press <span className="mx-1 font-medium text-foreground">Run the live pipeline</span> to watch
                an email flow through every step.
              </div>
            )}

            {email && (
              <Card>
                <CardHeader>
                  <CardTitle className="text-base flex items-center gap-2">
                    <Inbox className="w-4 h-4 text-primary" /> Fetched email
                  </CardTitle>
                </CardHeader>
                <CardContent className="text-sm">
                  <p className="font-medium text-foreground">{email.subject}</p>
                  <p className="text-muted-foreground">{email.from} · {email.received}</p>
                  <p className="text-foreground/90 whitespace-pre-wrap mt-2">{email.body}</p>
                </CardContent>
              </Card>
            )}

            {analysis && status.understand === "done" && (
              <Card className="border-primary/30">
                <CardHeader className="flex flex-row items-center justify-between">
                  <CardTitle className="text-base flex items-center gap-2">
                    <Brain className="w-4 h-4 text-primary" /> Understood
                  </CardTitle>
                  <Badge variant="outline" className="text-xs">{engineUsed}</Badge>
                </CardHeader>
                <CardContent className="space-y-3 text-sm">
                  <p className="text-muted-foreground">{analysis.summary}</p>
                  <div className="flex flex-wrap gap-2">
                    <Badge variant="outline">{analysis.category.replace(/_/g, " ")}</Badge>
                    <Badge className={priorityColor[analysis.priority]}>{analysis.priority} priority</Badge>
                  </div>
                  <div>
                    <p className="font-medium text-foreground">The ask</p>
                    <p className="text-muted-foreground mt-0.5">{analysis.intent}</p>
                  </div>
                </CardContent>
              </Card>
            )}

            {analysis && status.extract === "done" && (
              <Card>
                <CardHeader>
                  <CardTitle className="text-base flex items-center gap-2">
                    <FileText className="w-4 h-4 text-primary" /> Extracted facts
                  </CardTitle>
                </CardHeader>
                <CardContent className="text-sm">
                  {analysis.entities.length === 0 ? (
                    <p className="text-muted-foreground">No structured facts in this email.</p>
                  ) : (
                    <div className="space-y-1">
                      {analysis.entities.map((en, i) => (
                        <div key={i} className="text-muted-foreground">
                          <span className="text-foreground/80">{en.field}:</span> {en.value}
                        </div>
                      ))}
                    </div>
                  )}
                </CardContent>
              </Card>
            )}

            {analysis && status.recommend === "done" && (
              <Card>
                <CardHeader>
                  <CardTitle className="text-base flex items-center gap-2">
                    <ListChecks className="w-4 h-4 text-primary" /> Recommended action
                  </CardTitle>
                </CardHeader>
                <CardContent className="space-y-2 text-sm">
                  <div className="rounded-lg bg-muted/40 border border-border p-3">
                    <p className="font-medium text-foreground">{analysis.suggested_action.title}</p>
                    <p className="text-muted-foreground mt-0.5">{analysis.suggested_action.detail}</p>
                  </div>
                  <div>
                    <p className="font-medium text-foreground mb-1">Draft reply</p>
                    <p className="text-muted-foreground whitespace-pre-wrap rounded-lg border border-border bg-background p-3">
                      {analysis.draft_reply}
                    </p>
                  </div>
                </CardContent>
              </Card>
            )}

            {actResult && status.act === "done" && (
              <Card className="border-green-500/40 bg-green-500/5">
                <CardHeader>
                  <CardTitle className="text-base flex items-center gap-2">
                    <CheckCircle2 className="w-4 h-4 text-green-500" /> Acted
                  </CardTitle>
                </CardHeader>
                <CardContent className="text-sm text-foreground/90">
                  {actResult}
                  <div className="mt-4 flex gap-2">
                    <Button size="sm" variant="outline" onClick={() => run()} disabled={running}>
                      Run again
                    </Button>
                    <Button size="sm" onClick={() => navigate("/app")}>
                      Open the full app
                    </Button>
                  </div>
                </CardContent>
              </Card>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default LiveDemo;
