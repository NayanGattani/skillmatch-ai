import { Info } from "lucide-react";
import {
  Tooltip,
  TooltipContent,
  TooltipProvider,
  TooltipTrigger,
} from "@/components/ui/tooltip";

/**
 * Small ⓘ affordance used to explain non-obvious metrics.
 * Presentation only — carries no data or calculations.
 */
export function InfoHint({ text, label }: { text: string; label?: string }) {
  return (
    <TooltipProvider delayDuration={120}>
      <Tooltip>
        <TooltipTrigger
          type="button"
          aria-label={label ? `What ${label} means` : "More information"}
          className="inline-flex shrink-0 items-center text-muted-foreground transition-colors hover:text-foreground focus-visible:text-foreground"
        >
          <Info className="size-3.5" aria-hidden="true" />
        </TooltipTrigger>
        <TooltipContent
          side="top"
          className="max-w-[16rem] rounded-none border border-foreground text-[11px] leading-snug"
        >
          {text}
        </TooltipContent>
      </Tooltip>
    </TooltipProvider>
  );
}
