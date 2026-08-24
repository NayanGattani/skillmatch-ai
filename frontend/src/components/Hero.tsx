import { GapFragment, ResumeFragment, ScoreFragment } from "./Artifacts";

export function Hero() {
  return (
    <section className="relative border-b border-border-strong" aria-labelledby="hero-heading">
      <div className="mx-auto max-w-[1400px] px-5 pb-14 pt-12 sm:px-8 sm:pb-20 sm:pt-16">
        <div className="grid gap-10 lg:grid-cols-[minmax(0,1fr)_320px] lg:items-end">
          <div>
            <p className="label-mono text-muted-foreground">
              01 — RESUME × JOB MATCHING
            </p>
            <h1 id="hero-heading" className="display-xl mt-5">
              Know where
              <br />
              you{" "}
              <span className="inline-block bg-lime px-2 leading-[0.9] text-lime-foreground">
                stand.
              </span>
            </h1>
            <p className="body-copy mt-7 max-w-[46ch] text-balance">
              Upload a resume. Add a job description. Get a weighted match score,
              an exact skill-gap breakdown, and AI-written recommendations —
              in one pass.
            </p>

            <ul className="label-mono mt-8 flex flex-wrap items-center gap-x-3 gap-y-2 text-muted-foreground">
              <li>UPLOAD RESUME</li>
              <li aria-hidden="true" className="text-foreground">+</li>
              <li>ADD JOB DESCRIPTION</li>
              <li aria-hidden="true" className="text-foreground">=</li>
              <li className="bg-foreground px-2 py-1 text-background">MATCH ANALYSIS</li>
            </ul>
          </div>

          <div className="relative hidden h-[320px] lg:block" aria-hidden="true">
            <ResumeFragment className="absolute right-6 top-0 rotate-[-2deg]" />
            <ScoreFragment className="absolute left-0 top-[150px] rotate-[1.5deg]" />
            <GapFragment className="absolute bottom-0 right-0 rotate-[-1deg]" />
          </div>
        </div>
      </div>
    </section>
  );
}
