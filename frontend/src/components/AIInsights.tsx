import type { AiAnalysis } from "@/lib/api";

function List({
  index,
  title,
  items,
  marker,
}: {
  index: string;
  title: string;
  items: string[];
  marker: string;
}) {
  if (!items.length) return null;
  return (
    <div className="border-t border-border pt-6">
      <p className="label-mono text-muted-foreground">{index}</p>
      <h3 className="mt-2 text-base font-extrabold uppercase tracking-[0.02em]">{title}</h3>
      <ul className="mt-4 space-y-3">
        {items.map((item) => (
          <li key={item} className="flex gap-3">
            <span aria-hidden="true" className="label-mono mt-1 shrink-0 text-lime-foreground">
              <span className="bg-lime px-1">{marker}</span>
            </span>
            <span className="body-copy">{item}</span>
          </li>
        ))}
      </ul>
    </div>
  );
}

export function AIInsights({ analysis }: { analysis?: AiAnalysis | null | undefined }) {
  if (!analysis) {
    return (
      <section aria-labelledby="ai-heading" className="pb-4">
        <h2 id="ai-heading" className="label-mono text-muted-foreground">
          AI ANALYSIS
        </h2>
        <p className="body-copy mt-4 border border-dashed border-border-strong px-5 py-6 text-muted-foreground">
          The service did not return AI insights for this analysis. The match score
          and skill breakdown above are unaffected.
        </p>
      </section>
    );
  }

  const strengths = analysis.strengths ?? [];
  const weaknesses = analysis.weaknesses ?? [];
  const recommendations = analysis.recommendations ?? [];

  return (
    <section aria-labelledby="ai-heading" className="pb-4">
      <h2 id="ai-heading" className="label-mono text-muted-foreground">
        AI ANALYSIS
      </h2>

      {analysis.summary && (
        <p className="mt-5 max-w-prose text-balance text-xl leading-snug">
          {analysis.summary}
        </p>
      )}

      <div className="mt-10 grid gap-8 lg:grid-cols-3">
        <List index="03 — A" title="Strengths" items={strengths} marker="+" />
        <List index="03 — B" title="Gaps" items={weaknesses} marker="−" />
        <List index="03 — C" title="Recommendations" items={recommendations} marker="→" />
      </div>

      {(analysis.experience_relevance || analysis.skill_gap_analysis) && (
        <div className="mt-10 grid gap-6 border-t border-border pt-8 lg:grid-cols-2">
          {analysis.experience_relevance && (
            <div>
              <p className="label-mono text-muted-foreground">EXPERIENCE RELEVANCE</p>
              <p className="mt-3 max-w-prose text-base leading-snug text-muted-foreground">
                {analysis.experience_relevance}
              </p>
            </div>
          )}
          {analysis.skill_gap_analysis && (
            <div>
              <p className="label-mono text-muted-foreground">SKILL GAP ANALYSIS</p>
              <p className="mt-3 max-w-prose text-base leading-snug text-muted-foreground">
                {analysis.skill_gap_analysis}
              </p>
            </div>
          )}
        </div>
      )}
    </section>
  );
}
