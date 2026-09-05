import type { ResumeHealth as ResumeHealthData, ResumeHealthIssue } from "@/lib/api";
import { formatCareerStage } from "@/lib/format";

function Bar({ label, value }: { label: string; value?: number | undefined }) {
  if (typeof value !== "number") return null;
  const v = Math.max(0, Math.min(100, value));
  return (
    <div>
      <div className="label-mono flex items-baseline justify-between text-muted-foreground">
        <span>{label}</span>
        <span className="tabular-nums text-foreground">{Math.round(v)}</span>
      </div>
      <div className="mt-1.5 h-2 w-full border border-border-strong">
        <span className="block h-full bg-lime" style={{ width: `${v}%` }} />
      </div>
    </div>
  );
}

function Signal({ label, value }: { label: string; value?: string | number | undefined }) {
  if (value === undefined || value === null || value === "") return null;
  return (
    <div className="border border-border px-4 py-3">
      <p className="label-mono text-muted-foreground">{label}</p>
      <p className="mt-1 break-words text-sm font-extrabold uppercase leading-snug tabular-nums tracking-[-0.01em] sm:text-base">
        {value}
      </p>
    </div>
  );
}

const SEVERITY_ORDER = ["high", "medium", "low"] as const;

function severityStyle(severity: string) {
  if (severity === "high") return "border-destructive text-destructive";
  if (severity === "medium")
    return "border-amber-500 text-amber-700 dark:text-amber-400";
  if (severity === "low") return "border-positive text-positive";
  return "border-border-strong text-muted-foreground";
}


function IssueGroup({ severity, issues }: { severity: string; issues: ResumeHealthIssue[] }) {
  if (!issues.length) return null;
  return (
    <div className="mt-5 first:mt-0">
      <p
        className={
          "inline-block border px-2 py-0.5 text-[11px] font-bold uppercase tracking-[0.08em] " +
          severityStyle(severity)
        }
      >
        {severity} · {issues.length}
      </p>
      <ul className="mt-3 space-y-3">
        {issues.map((issue, i) => (
          <li key={(issue.message ?? "") + i} className="border-l-2 border-border pl-4">
            {issue.category && (
              <p className="label-mono text-muted-foreground">{issue.category}</p>
            )}
            <p className="mt-1 text-sm leading-snug">{issue.message}</p>
          </li>
        ))}
      </ul>
    </div>
  );
}

export function ResumeHealth({ health }: { health?: ResumeHealthData | null | undefined }) {
  if (!health) return null;

  const score = typeof health.score === "number" ? Math.max(0, Math.min(100, health.score)) : null;
  const categories = health.categories ?? {};
  const issues = health.issues ?? [];
  const recommendations = health.recommendations ?? [];
  const signals = health.signals ?? {};

  const grouped = SEVERITY_ORDER.map((severity) => ({
    severity,
    items: issues.filter((i) => (i.severity ?? "low") === severity),
  }));
  const other = issues.filter(
    (i) => !SEVERITY_ORDER.includes((i.severity ?? "low") as (typeof SEVERITY_ORDER)[number]),
  );

  return (
    <section aria-labelledby="health-heading" className="border-b border-border-strong pb-10">
      <h2 id="health-heading" className="label-mono text-muted-foreground">
        RESUME HEALTH
      </h2>

      <div className="mt-6 grid gap-6 lg:grid-cols-3">
        <div className="border border-border-strong bg-card px-5 py-6 sm:px-7">
          {score !== null && (
            <>
              <p className="text-5xl font-extrabold tabular-nums tracking-[-0.04em]">
                {score.toFixed(0)}
                <span className="text-lime">%</span>
              </p>
              <div className="mt-4 h-2 w-full border border-foreground">
                <span className="block h-full bg-lime" style={{ width: `${score}%` }} />
              </div>
            </>
          )}
          <div className="mt-6 space-y-4">
            <Bar label="CONTENT" value={categories.content} />
            <Bar label="STRUCTURE" value={categories.structure} />
            <Bar label="COMPLETENESS" value={categories.completeness} />
            <Bar label="CLARITY" value={categories.clarity} />
            <Bar label="EVIDENCE" value={categories.evidence} />
          </div>
        </div>

        <div className="border border-border-strong bg-card px-5 py-6 sm:px-7">
          <p className="text-base font-extrabold uppercase tracking-[0.02em]">Issues</p>
          {issues.length ? (
            <div className="mt-4">
              {grouped.map((g) => (
                <IssueGroup key={g.severity} severity={g.severity} issues={g.items} />
              ))}
              <IssueGroup severity="other" issues={other} />
            </div>
          ) : (
            <p className="body-copy mt-3 text-muted-foreground">
              No document-quality issues detected.
            </p>
          )}
        </div>

        <div className="border border-border-strong bg-card px-5 py-6 sm:px-7">
          <p className="text-base font-extrabold uppercase tracking-[0.02em]">
            Document recommendations
          </p>
          <p className="label-mono mt-1 text-muted-foreground">DETERMINISTIC</p>
          {recommendations.length ? (
            <ul className="mt-4 space-y-3">
              {recommendations.map((r) => (
                <li key={r} className="flex gap-3">
                  <span aria-hidden="true" className="label-mono mt-1 shrink-0">
                    <span className="bg-lime px-1 text-lime-foreground">→</span>
                  </span>
                  <span className="text-sm leading-snug">{r}</span>
                </li>
              ))}
            </ul>
          ) : (
            <p className="body-copy mt-3 text-muted-foreground">
              No deterministic recommendations for this document.
            </p>
          )}
        </div>
      </div>

      <div className="mt-6 grid grid-cols-2 gap-3 sm:grid-cols-3 lg:grid-cols-5">
        <Signal label="CAREER STAGE" value={formatCareerStage(signals.career_stage)} />
        <Signal label="WORD COUNT" value={signals.word_count} />
        <Signal label="BULLETS" value={signals.bullet_count} />
        <Signal label="QUANTIFIED BULLETS" value={signals.quantified_bullet_count} />
        <Signal label="ACTION-LED BULLETS" value={signals.action_led_bullet_count} />
      </div>
    </section>
  );
}
