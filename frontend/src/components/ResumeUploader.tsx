import { useId, useRef, useState } from "react";
import { FileText, Upload, X } from "lucide-react";
import { validatePdf } from "@/lib/api";

interface Props {
  file: File | null;
  onChange: (file: File | null) => void;
  disabled?: boolean;
}

function formatSize(bytes: number) {
  if (bytes < 1024) return `${bytes} B`;
  if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(0)} KB`;
  return `${(bytes / (1024 * 1024)).toFixed(1)} MB`;
}

export function ResumeUploader({ file, onChange, disabled }: Props) {
  const inputRef = useRef<HTMLInputElement>(null);
  const [dragOver, setDragOver] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const inputId = useId();
  const errorId = `${inputId}-error`;

  function accept(next: File | undefined) {
    if (!next) return;
    const problem = validatePdf(next);
    if (problem) {
      setError(problem);
      onChange(null);
      return;
    }
    setError(null);
    onChange(next);
  }

  return (
    <div>
      <input
        ref={inputRef}
        id={inputId}
        type="file"
        accept="application/pdf,.pdf"
        className="sr-only"
        disabled={disabled}
        aria-describedby={error ? errorId : undefined}
        onChange={(e) => accept(e.target.files?.[0])}
      />

      {file ? (
        <div className="flex items-start justify-between gap-4 border border-border-strong bg-card px-4 py-4">
          <div className="flex min-w-0 items-start gap-3">
            <FileText className="mt-0.5 size-5 shrink-0" aria-hidden="true" />
            <div className="min-w-0">
              <p className="truncate text-sm font-semibold">{file.name}</p>
              <p className="label-mono mt-1 text-muted-foreground">
                PDF · {formatSize(file.size)}
              </p>
            </div>
          </div>
          <div className="flex shrink-0 items-center gap-2">
            <button
              type="button"
              disabled={disabled}
              onClick={() => inputRef.current?.click()}
              className="label-strong border border-border-strong px-3 py-2 transition-colors hover:bg-foreground hover:text-background disabled:opacity-40"
            >
              Replace
            </button>
            <button
              type="button"
              disabled={disabled}
              onClick={() => {
                onChange(null);
                if (inputRef.current) inputRef.current.value = "";
              }}
              aria-label={`Remove ${file.name}`}
              className="border border-border-strong p-2 transition-colors hover:bg-foreground hover:text-background disabled:opacity-40"
            >
              <X className="size-4" aria-hidden="true" />
            </button>
          </div>
        </div>
      ) : (
        <label
          htmlFor={inputId}
          onDragOver={(e) => {
            e.preventDefault();
            if (!disabled) setDragOver(true);
          }}
          onDragLeave={() => setDragOver(false)}
          onDrop={(e) => {
            e.preventDefault();
            setDragOver(false);
            if (disabled) return;
            accept(e.dataTransfer.files?.[0]);
          }}
          className={
            "flex cursor-pointer items-center gap-4 border border-dashed px-4 py-6 transition-colors " +
            (dragOver
              ? "border-foreground bg-lime/20"
              : "border-border-strong hover:bg-muted") +
            (disabled ? " pointer-events-none opacity-50" : "")
          }
        >
          <Upload className="size-5 shrink-0" aria-hidden="true" />
          <span className="text-sm">
            <span className="font-semibold">Drop your resume here</span>
            <span className="block text-muted-foreground">
              or click to browse — PDF only, up to 10 MB
            </span>
          </span>
        </label>
      )}

      {error && (
        <p id={errorId} role="alert" className="label-mono mt-3 text-destructive">
          × {error}
        </p>
      )}
    </div>
  );
}
