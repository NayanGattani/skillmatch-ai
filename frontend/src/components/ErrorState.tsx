import { RotateCcw } from "lucide-react";
import { ApiError } from "@/lib/api";

interface Props {
  error: unknown;
  onRetry: () => void;
}

function describe(error: unknown): { code: string; title: string; body: string } {
  if (error instanceof ApiError) {
    if (error.kind === "network")
      return {
        code: "CONNECTION",
        title: "Can't reach the analysis service",
        body: error.message,
      };
    if (error.kind === "malformed")
      return {
        code: "RESPONSE",
        title: "Unreadable response",
        body: error.message,
      };
    return {
      code: error.status ? `HTTP ${error.status}` : "REQUEST",
      title: "The analysis failed",
      body: error.message,
    };
  }
  return {
    code: "UNKNOWN",
    title: "Something went wrong",
    body: error instanceof Error ? error.message : "An unexpected error occurred.",
  };
}

export function ErrorState({ error, onRetry }: Props) {
  const { code, title, body } = describe(error);

  return (
    <section
      role="alert"
      className="border border-destructive bg-card px-5 py-8 sm:px-8 sm:py-10"
    >
      <p className="label-mono text-destructive">ERROR — {code}</p>
      <h2 className="display-lg mt-3">{title}</h2>
      <p className="body-copy mt-4 max-w-[52ch]">{body}</p>
      <button
        type="button"
        onClick={onRetry}
        className="mt-7 inline-flex items-center gap-3 border border-foreground px-5 py-3 text-sm font-bold uppercase tracking-[0.08em] transition-colors hover:bg-foreground hover:text-background"
      >
        <RotateCcw className="size-4" aria-hidden="true" />
        Try again
      </button>
    </section>
  );
}
