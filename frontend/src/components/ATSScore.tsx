import type { Scoring } from "@/lib/api";

export function ATSScore({ scoring, filename }: { scoring: Scoring; filename?: string | undefined }) {
  const score = typeof scoring.ats_score === "number" ? scoring.ats_score : 0;
  const clamped = Math.max(0, Math.min(100, score));
  const earned = scoring.earnings?.earned_points;
  const possible = scoring.earnings?.possible_points;

  return (
    <section aria-labelledby="score-heading" className="border-b border-border-strong pb-10">
      <div className="grid gap-8 lg:grid-cols-[minmax(0,1.1fr)_minmax(0,1fr)] lg:items-end">
        <div>
          <h2 id="score-heading" className="label-mono text-muted-foreground">
            MATCH SCORE
          </h2>
          <p className="numeric-xl mt-4">
            {clamped.toFixed(2)}
            <span className="text-lime">%</span>
          </p>
          {typeof earned === "number" && typeof possible === "number" && (
            <p className="label-strong mt-5 text-muted-foreground">
              {earned} / {possible} weighted points
            </p>
          )}
        </div>

        <div>
          <div
            className="h-3 w-full border border-foreground"
            role="meter"
            aria-valuenow={Number(clamped.toFixed(2))}
            aria-valuemin={0}
            aria-valuemax={100}
            aria-label="ATS match score"
          >
            <span
              className="block h-full bg-lime"
              style={{ width: `${clamped}%` }}
            />
          </div>
          <div className="label-mono mt-2 flex justify-between text-muted-foreground">
            <span>0</span>
            <span>50</span>
            <span>100</span>
          </div>
          {filename && (
            <p className="label-mono mt-6 break-all text-muted-foreground">
              SOURCE — {filename}
            </p>
          )}
        </div>
      </div>
    </section>
  );
}
