import { ArrowRight, Loader2 } from "lucide-react";

interface Props {
  onClick: () => void;
  disabled?: boolean;
  loading?: boolean;
}

export function AnalyzeButton({ onClick, disabled, loading }: Props) {
  return (
    <button
      type="button"
      onClick={onClick}
      disabled={disabled || loading}
      className="group inline-flex w-full items-center justify-between gap-6 border border-foreground bg-lime px-6 py-5 text-lime-foreground transition-colors hover:bg-foreground hover:text-background disabled:cursor-not-allowed disabled:border-border-strong disabled:bg-muted disabled:text-muted-foreground sm:w-auto"
    >
      <span className="text-base font-bold uppercase tracking-[0.08em]">
        {loading ? "Analyzing" : "Analyze match"}
      </span>
      {loading ? (
        <Loader2 className="size-5 animate-spin" aria-hidden="true" />
      ) : (
        <ArrowRight
          className="size-5 transition-transform group-hover:translate-x-1"
          aria-hidden="true"
        />
      )}
    </button>
  );
}
