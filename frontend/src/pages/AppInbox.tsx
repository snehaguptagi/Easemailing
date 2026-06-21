import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Alert, AlertDescription } from "@/components/ui/alert";
import { toast } from "sonner";
import {
  ArrowLeft, Wifi, WifiOff, Sparkles, Mail, AlertCircle, Loader2,
  ListChecks, Tag, Flag, Send, CheckCircle2,
} from "lucide-react";
import {
  getHealth, getInbox, analyzeEmail, act,
  type Email, type EmailAnalysis, type Health,
} from "@/lib/api";

const priorityColor: Record<string, string> = {
  high: "bg-red-500/15 text-red-500 border-red-500/30",
  medium: "bg-amber-500/15 text-amber-500 border-amber-500/30",
  low: "bg-slate-500/15 text-slate-400 border-slate-500/30",
};

const AppInbox = () => {
  const navigate = useNavigate();
  const [health, setHealth] = useState<Health | null>(null);
  const [connError, setConnError] = useState<string | null>(null);
  const [emails, setEmails] = useState<Email[]>([]);
  const [selected, setSelected] = useState<Email | null>(null);
  const [analysis, setAnalysis] = useState<EmailAnalysis | null>(null);
  const [engineUsed, setEngineUsed] = useState<string>("");
  const [draft, setDraft] = useState("");
  const [analyzing, setAnalyzing] = useState(false);
  const [acting, setActing] = useState(false);
  const [done, setDone] = useState(false);

  useEffect(() => {
    (async () => {
      try {
        const [h, inbox] = await Promise.all([getHealth(), getInbox()]);
        setHealth(h);
        setEmails(inbox.emails);
      } catch {
        setConnError("Can't reach the backend on port 8000. Start it with: cd backend && uvicorn main:app --port 8000");
      }
    })();
  }, []);

  const pick = (e: Email) => {
    setSelected(e);
    setAnalysis(null);
    setDone(false);
    setDraft("");
  };

  const runAnalyze = async () => {
    if (!selected) return;
    setAnalyzing(true);
    setAnalysis(null);
    try {
      const res = await analyzeEmail(selected);
      setAnalysis(res.analysis);
      setEngineUsed(res.engine);
      setDraft(res.analysis.draft_reply);
    } catch {
      toast.error("Analysis failed", { description: "Is the backend running?" });
    }
    setAnalyzing(false);
  };

  const runAction = async () => {
    if (!selected || !analysis) return;
    setActing(true);
    try {
      const res = await act(selected, analysis.suggested_action.type, draft);
      toast.success(res.message);
      setDone(true);
    } catch {
      toast.error("Action failed");
    }
    setActing(false);
  };

  return (
    <div className="min-h-screen p-6">
      <div className="max-w-6xl mx-auto">
        <Button variant="ghost" onClick={() => navigate("/")} className="mb-4">
          <ArrowLeft className="w-4 h-4 mr-2" /> Back to Home
        </Button>

        <div className="flex flex-wrap items-center justify-between gap-3 mb-6">
          <h1 className="text-3xl md:text-4xl font-bold text-foreground">Inbox → Action</h1>
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

        {connError && (
          <Alert className="mb-6 border-yellow-500/30 bg-yellow-500/10">
            <AlertCircle className="h-4 w-4 text-yellow-500" />
            <AlertDescription className="text-yellow-600 dark:text-yellow-400 whitespace-pre-wrap">
              {connError}
            </AlertDescription>
          </Alert>
        )}

        <div className="grid grid-cols-1 md:grid-cols-[340px_1fr] gap-6">
          {/* Inbox list */}
          <div className="space-y-2">
            {emails.map((e) => (
              <button
                key={e.id}
                onClick={() => pick(e)}
                className={`w-full text-left p-4 rounded-lg border transition-colors ${
                  selected?.id === e.id
                    ? "border-primary bg-primary/5"
                    : "border-border hover:bg-muted/40"
                }`}
              >
                <div className="flex items-center justify-between gap-2">
                  <span className="text-sm font-medium text-foreground truncate">
                    {e.from.split("<")[0].trim()}
                  </span>
                  {e.unread && <span className="w-2 h-2 rounded-full bg-primary shrink-0" />}
                </div>
                <p className="text-sm text-foreground/90 truncate mt-1">{e.subject}</p>
                <p className="text-xs text-muted-foreground truncate mt-0.5">{e.body}</p>
              </button>
            ))}
          </div>

          {/* Detail + analysis */}
          <div>
            {!selected && (
              <div className="h-full flex items-center justify-center text-muted-foreground border border-dashed border-border rounded-lg p-12">
                <div className="text-center">
                  <Mail className="w-8 h-8 mx-auto mb-3 opacity-50" />
                  Select an email to analyze.
                </div>
              </div>
            )}

            {selected && (
              <div className="space-y-4">
                <Card>
                  <CardHeader>
                    <CardTitle className="text-lg">{selected.subject}</CardTitle>
                    <p className="text-sm text-muted-foreground">{selected.from} · {selected.received}</p>
                  </CardHeader>
                  <CardContent>
                    <p className="text-sm text-foreground/90 whitespace-pre-wrap">{selected.body}</p>
                    <Button onClick={runAnalyze} disabled={analyzing} className="mt-4">
                      {analyzing ? <Loader2 className="w-4 h-4 mr-2 animate-spin" /> : <Sparkles className="w-4 h-4 mr-2" />}
                      {analyzing ? "Analyzing…" : "Analyze with AI"}
                    </Button>
                  </CardContent>
                </Card>

                {analysis && (
                  <Card className="border-primary/30">
                    <CardHeader className="flex flex-row items-center justify-between">
                      <CardTitle className="text-base flex items-center gap-2">
                        <Sparkles className="w-4 h-4 text-primary" /> AI Analysis
                      </CardTitle>
                      <Badge variant="outline" className="text-xs">{engineUsed}</Badge>
                    </CardHeader>
                    <CardContent className="space-y-4 text-sm">
                      <div>
                        <p className="text-muted-foreground">{analysis.summary}</p>
                      </div>

                      <div className="flex flex-wrap gap-2">
                        <Badge variant="outline"><Tag className="w-3 h-3 mr-1" />{analysis.category.replace(/_/g, " ")}</Badge>
                        <Badge className={priorityColor[analysis.priority]}>
                          <Flag className="w-3 h-3 mr-1" />{analysis.priority} priority
                        </Badge>
                      </div>

                      <div>
                        <p className="font-medium text-foreground flex items-center gap-2">
                          <ListChecks className="w-4 h-4" /> The ask
                        </p>
                        <p className="text-muted-foreground mt-1">{analysis.intent}</p>
                      </div>

                      {analysis.entities.length > 0 && (
                        <div>
                          <p className="font-medium text-foreground">Extracted</p>
                          <div className="mt-1 space-y-1">
                            {analysis.entities.map((en, i) => (
                              <div key={i} className="text-muted-foreground">
                                <span className="text-foreground/80">{en.field}:</span> {en.value}
                              </div>
                            ))}
                          </div>
                        </div>
                      )}

                      <div className="rounded-lg bg-muted/40 border border-border p-3">
                        <p className="font-medium text-foreground">{analysis.suggested_action.title}</p>
                        <p className="text-muted-foreground mt-0.5">{analysis.suggested_action.detail}</p>
                      </div>

                      <div>
                        <p className="font-medium text-foreground mb-1">Draft reply (editable)</p>
                        <textarea
                          value={draft}
                          onChange={(e) => setDraft(e.target.value)}
                          rows={6}
                          className="w-full rounded-lg border border-border bg-background p-3 text-sm text-foreground focus:outline-none focus:ring-2 focus:ring-primary/40"
                        />
                      </div>

                      <Button onClick={runAction} disabled={acting || done} className="w-full">
                        {done ? <CheckCircle2 className="w-4 h-4 mr-2" /> :
                          acting ? <Loader2 className="w-4 h-4 mr-2 animate-spin" /> : <Send className="w-4 h-4 mr-2" />}
                        {done ? "Done" : acting ? "Working…" : `Approve & ${analysis.suggested_action.title}`}
                      </Button>
                    </CardContent>
                  </Card>
                )}
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default AppInbox;
