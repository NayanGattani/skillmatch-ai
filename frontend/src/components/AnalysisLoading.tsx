const STAGES = [
  "Extracting resume text",
  "Matching skills",
  "Calculating ATS score",
  "Generating AI insights",
];

export function AnalysisLoading() {
  return (
    <section
      aria-live="polite"
      aria-busy="true"
      className="border border-border-strong bg-card px-5 py-10 sm:px-10 sm:py-14"
    >
      <p className="label-mono text-muted-foreground">ANALYSIS IN PROGRESS</p>
      <h2 className="display-lg mt-4">Reading your<br />documents.</h2>
      <p className="body-copy mt-4 max-w-[42ch]">
        This usually takes a few seconds. The score is computed on the server —
        nothing here is estimated.
      </p>

      <ol className="mt-10 divide-y divide-border border-y border-border">
        {STAGES.map((stage, i) => (
          <li key={stage} className="flex items-center gap-4 py-4">
            <span className="label-mono w-8 text-muted-foreground">
              {String(i + 1).padStart(2, "0")}
            </span>
            <span className="text-sm font-semibold uppercase tracking-[0.06em]">
              {stage}
            </span>
            <span
              aria-hidden="true"
              className="ml-auto h-px flex-1 max-w-[240px] overflow-hidden bg-border"
            >
              <span
                className="block h-px w-1/3 animate-pulse bg-foreground"
                style={{ animationDelay: `${i * 250}ms` }}
              />
            </span>
          </li>
        ))}
      </ol>

      <p className="label-mono mt-6 text-muted-foreground">
        VISUAL STAGES ONLY — NO LIVE PROGRESS IS REPORTED BY THE SERVICE
      </p>
    </section>
  );
}
