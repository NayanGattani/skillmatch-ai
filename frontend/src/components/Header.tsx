import { API_BASE_URL } from "@/lib/api";

export function Header({ status }: { status: "unknown" | "online" | "offline" }) {
  const statusText =
    status === "online" ? "API CONNECTED" : status === "offline" ? "API OFFLINE" : "API IDLE";

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
            className="size-7 shrink-0"
          />
          SKILLMATCH{" "}
          <span className="bg-lime px-1 text-lime-foreground">AI</span>
        </a>

        <div className="flex items-center gap-4">
          <p className="label-mono hidden text-muted-foreground md:block">
            RESUME × JOB MATCHING
          </p>
          <p
            className="label-mono flex items-center gap-2 text-muted-foreground"
            title={API_BASE_URL}
          >
            <span
              aria-hidden="true"
              className={
                "inline-block size-2 " +
                (status === "online"
                  ? "bg-lime"
                  : status === "offline"
                    ? "bg-destructive"
                    : "bg-border-strong")
              }
            />
            <span className="sr-only">Backend status: </span>
            {statusText}
          </p>
        </div>
      </div>
    </header>
  );
}
