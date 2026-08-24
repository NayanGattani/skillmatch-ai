/**
 * Product-specific decorative artifacts: small designed fragments of the
 * actual output (resume lines, match score, skill gap). CSS/typography only.
 * Hidden on small screens so mobile returns to plain document flow.
 */

export function ResumeFragment({ className = "" }: { className?: string }) {
  return (
    <div
      aria-hidden="true"
      className={"w-[168px] border border-border-strong bg-card p-3 " + className}
    >
      <p className="label-mono mb-2 text-muted-foreground">RESUME.PDF</p>
      <div className="space-y-1.5">
        <span className="block h-1.5 w-full bg-foreground/80" />
        <span className="block h-1.5 w-3/4 bg-foreground/25" />
        <span className="block h-1.5 w-5/6 bg-foreground/25" />
      </div>
      <ul className="label-mono mt-3 space-y-1">
        <li className="flex justify-between">
          <span>PYTHON</span>
          <span className="text-positive">✓</span>
        </li>
        <li className="flex justify-between">
          <span>FASTAPI</span>
          <span className="text-positive">✓</span>
        </li>
        <li className="flex justify-between text-muted-foreground">
          <span>AWS</span>
          <span>×</span>
        </li>
      </ul>
    </div>
  );
}

export function ScoreFragment({ className = "" }: { className?: string }) {
  return (
    <div
      aria-hidden="true"
      className={"w-[150px] border border-border-strong bg-foreground p-3 text-background " + className}
    >
      <p className="label-mono text-background/60">MATCH</p>
      <p className="mt-1 text-3xl font-extrabold tracking-[-0.04em] tabular-nums">
        61.54<span className="text-lime">%</span>
      </p>
      <div className="mt-2 h-1 w-full bg-background/25">
        <span className="block h-full w-[62%] bg-lime" />
      </div>
    </div>
  );
}

export function GapFragment({ className = "" }: { className?: string }) {
  return (
    <div
      aria-hidden="true"
      className={"w-[150px] border border-border-strong bg-card p-3 " + className}
    >
      <p className="label-mono text-muted-foreground">SKILL GAP</p>
      <ul className="mt-2 space-y-1 text-[0.8125rem] font-semibold uppercase tracking-[0.04em]">
        <li>Docker</li>
        <li>Kubernetes</li>
        <li className="text-muted-foreground">CI / CD</li>
      </ul>
    </div>
  );
}
