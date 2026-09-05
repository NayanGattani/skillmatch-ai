/** Presentation-only formatting helpers. No business logic. */

const CAREER_STAGE_LABELS: Record<string, string> = {
  student_or_entry_level: "Student/Entry level",
  entry_level: "Entry level",
  early_career: "Early career",
  mid_level: "Mid level",
  mid_career: "Mid career",
  senior: "Senior",
  senior_level: "Senior level",
  lead: "Lead",
  manager: "Manager",
  executive: "Executive",
  career_changer: "Career changer",
  unknown: "Not determined",
};

/** Turns a machine-readable enum value into a human-readable label. */
export function humanizeEnum(value?: string | null): string {
  if (!value) return "";
  const cleaned = value.replace(/[_-]+/g, " ").trim().toLowerCase();
  return cleaned.charAt(0).toUpperCase() + cleaned.slice(1);
}

export function formatCareerStage(value?: string | null): string {
  if (!value) return "";
  return CAREER_STAGE_LABELS[value.toLowerCase()] ?? humanizeEnum(value);
}
