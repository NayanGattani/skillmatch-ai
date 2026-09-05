import {
  Check,
  X,
  TriangleAlert,
  Eye,
  AlignLeft,
  FileText,
  Files,
  LayoutList,
  ListChecks,
  Columns,
  Table,
  Image as ImageIcon,
  ScanLine,
  PanelTop,
  Repeat,
  GraduationCap,
  Briefcase,
  User,
  Building2,
  type LucideIcon,
} from "lucide-react";
import type { AtsReport, DocumentInfo } from "@/lib/api";
import { InfoHint } from "@/components/InfoHint";
import { formatCareerStage, humanizeEnum } from "@/lib/format";

type Tone = "good" | "warn" | "bad" | "neutral";

const TONE_CLASS: Record<Tone, string> = {
  good: "text-positive",
  warn: "text-amber-600 dark:text-amber-400",
  bad: "text-destructive",
  neutral: "text-foreground",
};

function Fact({
  label,
  value,
  icon: Icon,
  tone = "neutral",
  hint,
}: {
  label: string;
  value?: unknown;
  icon: LucideIcon;
  tone?: Tone;
  hint?: string;
}) {
  if (value === undefined || value === null || value === "") return null;
  if (typeof value === "object") return null;
  const display =
    typeof value === "boolean"
      ? value
        ? "YES"
        : "NO"
      : typeof value === "number"
        ? Number.isInteger(value)
          ? String(value)
          : value.toFixed(2)
        : String(value);
  return (
    <div className="flex items-baseline justify-between gap-3 border-b border-border py-1.5 last:border-b-0">
      <span className="label-mono flex min-w-0 items-center gap-2 text-muted-foreground">
        <Icon className="size-3.5 shrink-0 text-muted-foreground" aria-hidden="true" />
        <span className="min-w-0">{label}</span>
        {hint && <InfoHint text={hint} label={label.toLowerCase()} />}
      </span>
      <span
        className={
          "shrink-0 text-right text-xs font-bold uppercase tabular-nums " + TONE_CLASS[tone]
        }
      >
        {display}
      </span>
    </div>
  );
}


function boolTone(
  value: boolean | undefined,
  goodWhen: boolean,
  badTone: Tone = "warn",
): Tone {
  if (typeof value !== "boolean") return "neutral";
  return value === goodWhen ? "good" : badTone;
}

function countTone(value: number | undefined, warnAbove: number): Tone {
  if (typeof value !== "number") return "neutral";
  return value > warnAbove ? "warn" : "neutral";
}

function Snapshot({
  label,
  value,
  icon: Icon,
}: {
  label: string;
  value: string;
  icon: LucideIcon;
}) {
  return (
    <div className="flex items-start gap-3 border border-border-strong bg-card px-4 py-4">
      <Icon className="mt-0.5 size-4 shrink-0 text-muted-foreground" aria-hidden="true" />
      <div className="min-w-0">
        <p className="label-mono text-muted-foreground">{label}</p>
        <p className="mt-1 break-words text-sm font-bold uppercase tracking-[0.02em]">
          {value}
        </p>
      </div>
    </div>
  );
}

export function ATSReadiness({
  ats,
  document,
}: {
  ats?: AtsReport | null | undefined;
  document?: DocumentInfo | null | undefined;
}) {
  if (!ats) return null;

  const score = typeof ats.score === "number" ? Math.max(0, Math.min(100, ats.score)) : null;
  const checks = ats.checks ?? [];
  const warnings = ats.warnings ?? [];

  const rawSections = document?.sections;
  const sectionsObj =
    rawSections !== null && typeof rawSections === "object" ? rawSections : undefined;
  const detected = sectionsObj?.detected;
  const sectionsCount =
    typeof rawSections === "number"
      ? rawSections
      : (sectionsObj?.count ?? (Array.isArray(detected) ? detected.length : detected));
  const standardSectionCount = document?.standard_section_count ?? sectionsObj?.standard_count;
  const parseWarnings = document?.parse_warnings ?? [];

  const scoreTone: Tone =
    score === null ? "neutral" : score >= 80 ? "good" : score >= 60 ? "warn" : "bad";
  const scoreAccent =
    scoreTone === "good"
      ? "bg-lime"
      : scoreTone === "warn"
        ? "bg-amber-400"
        : "bg-destructive";

  const experienceYears = document?.total_experience_years ?? document?.experience_years;
  const industry = document?.industry_focus ?? document?.industry;

  return (
    <section aria-labelledby="ats-heading" className="border-b border-border-strong pb-10">
      <h2 id="ats-heading" className="label-mono text-muted-foreground">
        ATS READINESS
      </h2>

      <div className="mt-6 grid gap-6 lg:grid-cols-[minmax(0,0.9fr)_minmax(0,1.4fr)]">
        <div className="border border-border-strong bg-card px-5 py-6 sm:px-7">
          {score !== null && (
            <>
              <p className="text-5xl font-extrabold tabular-nums tracking-[-0.04em]">
                {score.toFixed(0)}
                <span className={TONE_CLASS[scoreTone]}>%</span>
              </p>
              <div className="mt-4 h-2 w-full border border-foreground">
                <span
                  className={"block h-full " + scoreAccent}
                  style={{ width: `${score}%` }}
                />
              </div>
            </>
          )}
          {ats.status && (
            <p
              className={
                "mt-5 inline-block max-w-full break-words border border-foreground px-2.5 py-1 text-xs font-bold uppercase tracking-[0.06em] " +
                (scoreTone === "bad"
                  ? "bg-destructive text-destructive-foreground"
                  : scoreTone === "warn"
                    ? "bg-amber-300 text-foreground"
                    : "bg-lime text-lime-foreground")
              }
            >
              {ats.status}
            </p>
          )}
          {typeof ats.penalties === "number" && (
            <p className="label-mono mt-4 text-muted-foreground">
              PENALTIES — {ats.penalties}
            </p>
          )}
          <p className="mt-5 text-sm leading-snug text-muted-foreground">
            How easily automated screening software can read this resume. It is not a
            probability of passing any specific system.
          </p>

          {document && (
            <div className="mt-6 border-t border-border-strong pt-5">
              <p className="label-mono text-muted-foreground">HOW READABLE IS YOUR FILE</p>
              <div className="mt-3">
                <Fact
                  label="TEXT IS SELECTABLE"
                  value={document.text_extractable}
                  icon={Eye}
                  tone={boolTone(document.text_extractable, true, "bad")}
                />
                <Fact
                  label="TEXT DENSITY"
                  value={document.text_density}
                  icon={AlignLeft}
                  hint="How much readable text is present relative to the size of the document."
                />
                <Fact label="WORDS PER PAGE" value={document.words_per_page} icon={FileText} />
                <Fact label="PAGES" value={document.page_count} icon={Files} />
                <Fact
                  label="SECTIONS FOUND"
                  value={sectionsCount}
                  icon={LayoutList}
                  hint="Number of recognisable resume sections detected, such as Experience, Education or Skills."
                />
                <Fact
                  label="STANDARD SECTIONS"
                  value={standardSectionCount}
                  icon={ListChecks}
                  hint="How many of the detected sections use standard names that screening software expects."
                  tone={
                    typeof standardSectionCount === "number"
                      ? standardSectionCount >= 4
                        ? "good"
                        : "warn"
                      : "neutral"
                  }
                />
                <Fact
                  label="TWO-COLUMN LAYOUT"
                  value={document.likely_two_column}
                  icon={Columns}
                  tone={boolTone(document.likely_two_column, false)}
                />
                <Fact
                  label="LAYOUT CONFIDENCE"
                  value={document.column_confidence}
                  icon={Columns}
                  hint="How confident the parser is about the document layout it detected."
                />

                <Fact
                  label="TABLES USED"
                  value={document.tables}
                  icon={Table}
                  tone={countTone(document.tables, 0)}
                />
                <Fact label="IMAGES USED" value={document.images} icon={ImageIcon} />
                <Fact
                  label="SCANNED (IMAGE-ONLY) PAGES"
                  value={document.image_only_pages}
                  icon={ScanLine}
                  tone={
                    typeof document.image_only_pages === "number" &&
                    document.image_only_pages > 0
                      ? "bad"
                      : "neutral"
                  }
                />
                <Fact
                  label="HEADERS & FOOTERS DETECTED"
                  value={document.header_footer_signal}
                  icon={PanelTop}
                  tone={boolTone(document.header_footer_signal, false)}
                />
                <Fact
                  label="REPEATED HEADER LINES"
                  value={document.repeated_header_footer_lines}
                  icon={Repeat}
                  tone={countTone(document.repeated_header_footer_lines, 0)}
                />
              </div>

              {parseWarnings.length > 0 && (
                <div className="mt-4 border border-destructive px-3 py-3">
                  <p className="label-mono flex items-center gap-2 text-destructive">
                    <TriangleAlert className="size-4" aria-hidden="true" />
                    THINGS TO FIX IN THE FILE
                  </p>
                  <ul className="mt-2 space-y-1.5">
                    {parseWarnings.map((w) => (
                      <li key={w} className="text-sm leading-snug text-muted-foreground">
                        {w}
                      </li>
                    ))}
                  </ul>
                </div>
              )}
            </div>
          )}
        </div>

        <div>
          {checks.length > 0 ? (
            <ul className="divide-y divide-border border border-border-strong bg-card">
              {checks.map((check, i) => (
                <li
                  key={check.key ?? check.label ?? i}
                  className="flex gap-4 px-4 py-4 sm:px-6"
                >
                  <span
                    aria-hidden="true"
                    className={
                      "mt-0.5 grid size-5 shrink-0 place-items-center border " +
                      (check.passed
                        ? "border-foreground bg-lime text-lime-foreground"
                        : "border-destructive text-destructive")
                    }
                  >
                    {check.passed ? <Check className="size-3.5" /> : <X className="size-3.5" />}
                  </span>
                  <div className="min-w-0">
                    <p className="text-sm font-bold uppercase tracking-[0.03em]">
                      {check.label ?? humanizeEnum(check.key)}
                      <span className="sr-only">{check.passed ? " passed" : " failed"}</span>
                    </p>
                    {check.detail && (
                      <p className="mt-1 text-sm leading-snug text-muted-foreground">
                        {check.detail}
                      </p>
                    )}
                  </div>
                  {typeof check.weight === "number" && (
                    <span className="label-mono ml-auto shrink-0 text-muted-foreground">
                      W {check.weight}
                    </span>
                  )}
                </li>
              ))}
            </ul>
          ) : (
            <p className="body-copy border border-dashed border-border-strong px-5 py-6 text-muted-foreground">
              No readability checks were returned for this document.
            </p>
          )}

          {warnings.length > 0 && (
            <div className="mt-5 border border-destructive px-4 py-4 sm:px-6">
              <p className="label-mono flex items-center gap-2 text-destructive">
                <TriangleAlert className="size-4" aria-hidden="true" />
                WARNINGS
              </p>
              <ul className="mt-3 space-y-2">
                {warnings.map((w) => (
                  <li key={w} className="text-sm leading-snug text-muted-foreground">
                    {w}
                  </li>
                ))}
              </ul>
            </div>
          )}
        </div>
      </div>

      <div className="mt-8 grid gap-3 sm:grid-cols-2 lg:grid-cols-4">
        <Snapshot
          label="CAREER STAGE"
          value={formatCareerStage(document?.career_stage) || "Not detected"}
          icon={GraduationCap}
        />
        <Snapshot
          label="TOTAL EXPERIENCE"
          value={
            typeof experienceYears === "number"
              ? `${experienceYears % 1 === 0 ? experienceYears : experienceYears.toFixed(1)} ${
                  experienceYears === 1 ? "year" : "years"
                }`
              : "Not detected"
          }
          icon={Briefcase}
        />
        <Snapshot
          label="PRIMARY ROLE"
          value={humanizeEnum(document?.primary_role) || "Not detected"}
          icon={User}
        />
        <Snapshot
          label="INDUSTRY FOCUS"
          value={humanizeEnum(industry) || "Not detected"}
          icon={Building2}
        />
      </div>
    </section>
  );
}
