import type { Scoring, SkillEvidence } from "@/lib/api";

function levelStyle(level: string) {
  switch (level.toLowerCase()) {
    case "strong":
      return "border-foreground bg-lime text-lime-foreground";
    case "moderate":
      return "border-foreground bg-transparent text-foreground";
    case "listed":
      return "border-border-strong bg-card text-muted-foreground";
    case "weak":
      return "border-dashed border-border-strong bg-card text-muted-foreground";
    default:
      return "border-border-strong bg-card text-muted-foreground";
  }
}

export function EvidenceStrength({ scoring }: { scoring: Scoring }) {
  const evidence = scoring.evidence ?? {};
  const relevant = new Set(
    [
      ...(scoring.required?.matched ?? []),
      ...(scoring.required?.missing ?? []),
      ...(scoring.preferred?.matched ?? []),
      ...(scoring.preferred?.missing ?? []),
    ].map((s) => s.toLowerCase()),
  );

  const rows = Object.entries(evidence).filter(([skill, data]: [string, SkillEvidence]) => {
    const hasData = Boolean(data?.evidence_level) || Boolean(data?.locations?.length);
    return hasData && (relevant.size === 0 || relevant.has(skill.toLowerCase()));
  });

  if (!rows.length) return null;

  return (
    <div className="mt-6 border border-border-strong bg-card px-5 py-6 sm:px-7">
      <p className="label-mono text-muted-foreground">02 — C</p>
      <h3 className="mt-2 text-lg font-extrabold uppercase tracking-[-0.01em]">
        Evidence strength
      </h3>
      <p className="mt-1 text-sm leading-snug text-muted-foreground">
        Where each skill actually appears in the resume, as reported by the analyzer.
      </p>

      <ul className="mt-5 divide-y divide-border border-t border-border">
        {rows.map(([skill, data]) => (
          <li
            key={skill}
            className="flex flex-col gap-2 py-3 sm:flex-row sm:items-center sm:gap-4"
          >
            <span className="min-w-0 flex-1 text-sm font-bold uppercase tracking-[0.03em]">
              {skill}
            </span>
            {data.evidence_level && (
              <span
                className={
                  "w-fit border px-2 py-0.5 text-[11px] font-bold uppercase tracking-[0.08em] " +
                  levelStyle(data.evidence_level)
                }
              >
                {data.evidence_level}
              </span>
            )}
            <span className="label-mono flex-1 text-muted-foreground sm:text-right">
              {(data.locations ?? []).join(" · ") || "—"}
            </span>
          </li>
        ))}
      </ul>
    </div>
  );
}
