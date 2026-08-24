import { useId } from "react";

interface Props {
  value: string;
  onChange: (value: string) => void;
  disabled?: boolean;
  error?: string | null;
}

export function JobDescriptionInput({ value, onChange, disabled, error }: Props) {
  const id = useId();
  const errorId = `${id}-error`;

  return (
    <div>
      <label htmlFor={id} className="label-strong block">
        Job description
      </label>
      <textarea
        id={id}
        value={value}
        disabled={disabled}
        aria-invalid={error ? true : undefined}
        aria-describedby={error ? errorId : `${id}-hint`}
        onChange={(e) => onChange(e.target.value)}
        rows={12}
        placeholder={
          "Paste the full posting — responsibilities, required skills, preferred skills.\n\nThe more complete the text, the more accurate the required vs. preferred split."
        }
        className="mt-3 w-full resize-y border border-border-strong bg-card px-4 py-4 text-sm leading-relaxed placeholder:text-muted-foreground focus:outline-none focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-foreground disabled:opacity-50"
      />
      <div className="mt-2 flex items-center justify-between gap-4">
        <p id={`${id}-hint`} className="label-mono text-muted-foreground">
          {value.trim().length} CHARS
        </p>
        {error && (
          <p id={errorId} role="alert" className="label-mono text-destructive">
            × {error}
          </p>
        )}
      </div>
    </div>
  );
}
