export function Header({ status }: { status: "unknown" | "online" | "offline" }) {
  return (
    <header className="sticky top-0 z-40 border-b border-border-strong bg-background/90 backdrop-blur-sm">
      <div className="mx-auto flex max-w-[1400px] items-center justify-between gap-4 px-5 py-4 sm:px-8">
        <a
          href="/"
          className="inline-flex items-center gap-2 text-lg font-extrabold uppercase tracking-[-0.02em] sm:text-xl"
          aria-label="SkillMatch AI home"
        >
          <img
            src="/favicon.png"
            alt=""
            aria-hidden="true"
            className="h-7 w-7 shrink-0 object-contain"
          />
          <span aria-hidden="true" className="h-5 w-px shrink-0 bg-border-strong" />
          SKILLMATCH{" "}
          <span className="bg-lime px-1 text-lime-foreground">AI</span>
        </a>

        <p className="label-mono hidden text-muted-foreground md:block">
          RESUME × JOB MATCHING
        </p>
      </div>
    </header>
  );
}
