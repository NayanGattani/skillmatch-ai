import { useState } from "react";
import { ChevronDown } from "lucide-react";
import type { DocumentInfo } from "@/lib/api";
import { formatCareerStage } from "@/lib/format";

function Row({ label, value }: { label: string; value?: unknown }) {
  if (value === undefined || value === null || value === "") return null;
  if (typeof value === "object") return null;
  const display =
    typeof value === "boolean" ? (value ? "YES" : "NO") : typeof value === "number"
      ? Number.isInteger(value)
        ? String(value)
        : value.toFixed(2)
      : String(value);
  return (
    <div className="flex items-baseline justify-between gap-4 border-b border-border py-2">
      <span className="label-mono text-muted-foreground">{label}</span>
      <span className="text-sm font-bold uppercase tabular-nums">{display}</span>
    </div>
  );
}

export function DocumentDiagnostics({ document }: { document?: DocumentInfo | null | undefined }) {
  const [open, setOpen] = useState(false);
  if (!document) return null;

  const warnings = document.parse_warnings ?? [];

  const rawSections = document.sections;
  const sectionsObj =
    rawSections !== null && typeof rawSections === "object" ? rawSections : undefined;
  const detected = sectionsObj?.detected;

  const sectionsCount =
    typeof rawSections === "number"
      ? rawSections
      : (sectionsObj?.count ?? (Array.isArray(detected) ? detected.length : detected));

  const standardSectionCount = document.standard_section_count ?? sectionsObj?.standard_count;

  const sectionNames =
    document.section_names ?? (Array.isArray(detected) ? detected : []);

  return (
    <section aria-labelledby="doc-heading" className="pb-4">
      <h2 id="doc-heading" className="label-mono text-muted-foreground">
        DOCUMENT &amp; PARSING
      </h2>

      <button
        type="button"
        onClick={() => setOpen((v) => !v)}
        aria-expanded={open}
        className="mt-4 flex w-full items-center justify-between gap-4 border border-border-strong bg-card px-5 py-4 text-left text-sm font-bold uppercase tracking-[0.06em] transition-colors hover:bg-foreground hover:text-background"
      >
        <span>{open ? "Hide diagnostics" : "Show diagnostics"}</span>
        <ChevronDown
          className={"size-4 transition-transform " + (open ? "rotate-180" : "")}
          aria-hidden="true"
        />
      </button>

      {open && (
        <div className="mt-5 grid gap-x-8 gap-y-0 border border-border-strong bg-card px-5 py-5 sm:px-7 lg:grid-cols-3">
          <div>
            <Row label="PAGE COUNT" value={document.page_count} />
            <Row label="WORD COUNT" value={document.word_count} />
            <Row label="WORDS PER PAGE" value={document.words_per_page} />
            <Row label="BULLET COUNT" value={document.bullet_count} />
            <Row label="BULLET RATIO" value={document.bullet_ratio} />
            <Row label="SECTIONS DETECTED" value={sectionsCount} />
            <Row label="STANDARD SECTIONS" value={standardSectionCount} />
          </div>
          <div>
            <Row label="TEXT EXTRACTABLE" value={document.text_extractable} />
            <Row label="TEXT DENSITY" value={document.text_density} />
            <Row label="IMAGE-ONLY PAGES" value={document.image_only_pages} />
            <Row label="IMAGES" value={document.images} />
            <Row label="TABLES" value={document.tables} />
            <Row label="LIKELY TWO-COLUMN" value={document.likely_two_column} />
            <Row label="CAREER STAGE" value={formatCareerStage(document.career_stage)} />
          </div>
          <div>
            <Row label="EMAIL DETECTED" value={document.email_detected} />
            <Row label="PHONE DETECTED" value={document.phone_detected} />
            <Row label="LINKEDIN DETECTED" value={document.linkedin_detected} />
            <Row label="GITHUB DETECTED" value={document.github_detected} />
            <Row label="PORTFOLIO DETECTED" value={document.portfolio_detected} />
            <Row label="URL COUNT" value={document.url_count} />
            <Row label="DATE COUNT" value={document.date_count} />
          </div>

          {sectionNames.length > 0 && (
            <div className="mt-5 lg:col-span-3">
              <p className="label-mono text-muted-foreground">SECTION NAMES</p>
              <ul className="label-mono mt-2 flex flex-wrap gap-x-3 gap-y-1">
                {sectionNames.map((s) => (
                  <li key={s}>{s.toUpperCase()}</li>
                ))}
              </ul>
            </div>
          )}

          {warnings.length > 0 && (
            <div className="mt-5 border border-destructive px-4 py-4 lg:col-span-3">
              <p className="label-mono text-destructive">PARSE WARNINGS</p>
              <ul className="mt-2 space-y-2">
                {warnings.map((w) => (
                  <li key={w} className="text-sm leading-snug text-muted-foreground">
                    {w}
                  </li>
                ))}
              </ul>
            </div>
          )}
        </div>
      )}
    </section>
  );
}
