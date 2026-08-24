import type { SkillGroup } from "@/lib/api";

interface Props {
  required?: SkillGroup | undefined;
  preferred?: SkillGroup | undefined;
  resumeSkills?: string[] | undefined;
}

function Chip({ tone, children }: { tone: "matched" | "missing"; children: string }) {
  return (
    <li
      className={
        "border px-2.5 py-1 text-xs font-semibold uppercase tracking-[0.06em] " +
        (tone === "matched"
          ? "border-foreground bg-lime text-lime-foreground"
          : "border-border-strong bg-card text-muted-foreground line-through decoration-1")
      }
    >
      {children}
    </li>
  );
}

function Group({
  index,
  title,
  weightNote,
  group,
}: {
  index: string;
  title: string;
  weightNote: string;
  group?: SkillGroup | undefined;
}) {
  const matched = group?.matched ?? [];
  const missing = group?.missing ?? [];
  const total = group?.total_count ?? matched.length + missing.length;
  const count = group?.matched_count ?? matched.length;

  return (
    <div className="border border-border-strong bg-card px-5 py-6 sm:px-7 sm:py-8">
      <div className="flex items-start justify-between gap-4 border-b border-border pb-4">
        <div>
          <p className="label-mono text-muted-foreground">{index}</p>
          <h3 className="mt-2 text-lg font-extrabold uppercase tracking-[-0.01em]">
            {title}
          </h3>
          <p className="label-mono mt-1 text-muted-foreground">{weightNote}</p>
        </div>
        <p className="shrink-0 text-2xl font-extrabold tabular-nums tracking-[-0.03em]">
          {count}
          <span className="text-muted-foreground">/{total}</span>
        </p>
      </div>

      <div className="mt-5">
        <p className="label-mono text-muted-foreground">MATCHED</p>
        {matched.length ? (
          <ul className="mt-3 flex flex-wrap gap-2">
            {matched.map((s) => (
              <Chip key={s} tone="matched">
                {s}
              </Chip>
            ))}
          </ul>
        ) : (
          <p className="body-copy mt-2 text-muted-foreground">None found.</p>
        )}
      </div>

      <div className="mt-6">
        <p className="label-mono text-muted-foreground">MISSING</p>
        {missing.length ? (
          <ul className="mt-3 flex flex-wrap gap-2">
            {missing.map((s) => (
              <Chip key={s} tone="missing">
                {s}
              </Chip>
            ))}
          </ul>
        ) : (
          <p className="body-copy mt-2 text-muted-foreground">
            Nothing missing — full coverage.
          </p>
        )}
      </div>
    </div>
  );
}

export function SkillsBreakdown({ required, preferred, resumeSkills }: Props) {
  return (
    <section aria-labelledby="skills-heading" className="border-b border-border-strong pb-10">
      <h2 id="skills-heading" className="label-mono text-muted-foreground">
        SKILL BREAKDOWN
      </h2>

      <div className="mt-6 grid gap-6 lg:grid-cols-2">
        <Group index="02 — A" title="Required skills" weightNote="HIGHER WEIGHT" group={required} />
        <Group index="02 — B" title="Preferred skills" weightNote="LOWER WEIGHT" group={preferred} />
      </div>

      {resumeSkills && resumeSkills.length > 0 && (
        <div className="mt-6 border border-border px-5 py-5">
          <p className="label-mono text-muted-foreground">
            ALL SKILLS DETECTED IN RESUME — {resumeSkills.length}
          </p>
          <ul className="label-mono mt-3 flex flex-wrap gap-x-3 gap-y-1">
            {resumeSkills.map((s) => (
              <li key={s}>{s.toUpperCase()}</li>
            ))}
          </ul>
        </div>
      )}
    </section>
  );
}
