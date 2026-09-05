import { TriangleAlert } from "lucide-react";
import type { Scoring } from "@/lib/api";
import { InfoHint } from "@/components/InfoHint";

function Stat({
  label,
  value,
  hint,
}: {
  label: string;
  value: string;
  hint?: string;
}) {
  return (
    <div className="border border-border px-4 py-3">
      <p className="label-mono flex items-center gap-1.5 text-muted-foreground">
        <span className="min-w-0">{label}</span>
        {hint && <InfoHint text={hint} label={label.toLowerCase()} />}
      </p>
      <p className="mt-1 text-base font-extrabold uppercase tracking-[-0.01em] tabular-nums">
        {value}
      </p>
    </div>
  );
}

function pct(n?: number): string | null {
  return typeof n === "number" ? `${Math.round(n)}%` : null;
}


export function ATSScore({ scoring, filename }: { scoring: Scoring; filename?: string | undefined }) {
  const raw = scoring.job_match_score ?? scoring.ats_score;
  const score = typeof raw === "number" ? raw : 0;
  const clamped = Math.max(0, Math.min(100, score));
  const earned = scoring.earnings?.earned_points;
  const possible = scoring.earnings?.possible_points;

  const requiredCoverage =
    pct(scoring.required?.coverage_percent) ??
    (typeof scoring.required?.matched_count === "number" &&
    typeof scoring.required?.total_count === "number"
      ? `${scoring.required.matched_count}/${scoring.required.total_count}`
      : null);
  const preferredCoverage =
    pct(scoring.preferred?.coverage_percent) ??
    (typeof scoring.preferred?.matched_count === "number" &&
    typeof scoring.preferred?.total_count === "number"
      ? `${scoring.preferred.matched_count}/${scoring.preferred.total_count}`
      : null);
  const keyword = pct(scoring.keyword_coverage);

  const signal = scoring.signal_quality;
  const lowSignal = typeof signal === "string" && /low|poor|weak|insufficient/i.test(signal);

  return (
    <section aria-labelledby="score-heading" className="border-b border-border-strong pb-10">
      <div className="grid gap-8 lg:grid-cols-[minmax(0,1.1fr)_minmax(0,1fr)] lg:items-end">
        <div>
          <h2 id="score-heading" className="label-mono text-muted-foreground">
            JOB MATCH SCORE
          </h2>
          <p className="numeric-xl mt-4">
            {clamped.toFixed(2)}
            <span className={lowSignal ? "text-muted-foreground" : "text-lime"}>%</span>
          </p>
          <p className="body-copy mt-3 max-w-[46ch] text-muted-foreground">
            Overlap between this resume and the job description. Not a hiring
            probability.
          </p>
          {typeof earned === "number" && typeof possible === "number" && (
            <p className="label-strong mt-4 text-muted-foreground">
              {earned} / {possible} weighted points
            </p>
          )}
          {lowSignal && (
            <div className="mt-5 max-w-[52ch] border border-amber-500 px-4 py-3">
              <p className="label-mono flex items-center gap-2 text-amber-700 dark:text-amber-400">
                <TriangleAlert className="size-4 shrink-0" aria-hidden="true" />
                THIS SCORE MAY NOT BE RELIABLE
              </p>
              <p className="mt-2 text-sm leading-snug text-muted-foreground">
                The job description you pasted contains very little meaningful
                detail — few clear skills, tools, or requirements to match against.
                Paste the full job description to get a score you can trust.
              </p>
            </div>
          )}
        </div>

        <div>
          <div
            className="h-3 w-full border border-foreground"
            role="meter"
            aria-valuenow={Number(clamped.toFixed(2))}
            aria-valuemin={0}
            aria-valuemax={100}
            aria-label="Job match score"
          >
            <span
              className={"block h-full " + (lowSignal ? "bg-amber-400" : "bg-lime")}
              style={{ width: `${clamped}%` }}
            />
          </div>
          <div className="label-mono mt-2 flex justify-between text-muted-foreground">
            <span>0</span>
            <span>50</span>
            <span>100</span>
          </div>

          <div className="mt-6 grid grid-cols-2 gap-3 sm:grid-cols-2">
            {signal && (
              <Stat
                label="SIGNAL QUALITY"
                value={signal}
                hint="How much meaningful, usable information the job description contains for matching. Low signal means the score is based on very little detail."
              />
            )}
            {requiredCoverage && (
              <Stat
                label="REQUIRED COVERAGE"
                value={requiredCoverage}
                hint="How much of the job's required qualifications this resume demonstrates."
              />
            )}
            {preferredCoverage && (
              <Stat
                label="PREFERRED COVERAGE"
                value={preferredCoverage}
                hint="How much of the job's preferred (nice-to-have) qualifications this resume demonstrates."
              />
            )}
            {keyword && (
              <Stat
                label="KEYWORD COVERAGE"
                value={keyword}
                hint="How much relevant terminology overlaps between the resume and the job description."
              />
            )}
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
