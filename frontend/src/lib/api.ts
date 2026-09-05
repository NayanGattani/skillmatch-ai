/**
 * API layer for the existing FastAPI backend.
 * Single endpoint: POST {BASE}/analyze  (multipart: file, job_description)
 * No scoring, no business logic here — presentation layer only.
 */

export const API_BASE_URL =
  (import.meta.env["VITE_API_URL"] as string | undefined)?.replace(/\/$/, "") ||
  "http://127.0.0.1:8000";

export interface SkillGroup {
  matched?: string[];
  missing?: string[];
  matched_count?: number;
  total_count?: number;
  coverage_percent?: number;
}

export type EvidenceLevel = "strong" | "moderate" | "listed" | "weak" | (string & {});

export interface SkillEvidence {
  locations?: string[];
  evidence_level?: EvidenceLevel;
}

export interface Scoring {
  job_match_score?: number;
  ats_score?: number;
  signal_quality?: string;
  keyword_coverage?: number;
  method?: string;
  required?: SkillGroup;
  preferred?: SkillGroup;
  evidence?: Record<string, SkillEvidence>;
  earnings?: {
    earned_points?: number;
    possible_points?: number;
  };
}

export interface AtsCheck {
  key?: string;
  label?: string;
  passed?: boolean;
  weight?: number;
  detail?: string;
}

export interface AtsReport {
  score?: number;
  status?: string;
  checks?: AtsCheck[];
  warnings?: string[];
  method?: string;
  penalties?: number;
}

export interface ResumeHealthIssue {
  severity?: "high" | "medium" | "low" | (string & {});
  category?: string;
  message?: string;
}

export interface ResumeHealth {
  score?: number;
  categories?: {
    content?: number;
    structure?: number;
    completeness?: number;
    clarity?: number;
    evidence?: number;
  };
  issues?: ResumeHealthIssue[];
  recommendations?: string[];
  signals?: {
    career_stage?: string;
    bullet_count?: number;
    quantified_bullet_count?: number;
    generic_bullet_count?: number;
    action_led_bullet_count?: number;
    word_count?: number;
  };
  method?: string;
}

export interface DocumentInfo {
  page_count?: number;
  word_count?: number;
  character_count?: number;
  line_count?: number;
  bullet_count?: number;
  bullet_ratio?: number;
  email_detected?: boolean;
  phone_detected?: boolean;
  linkedin_detected?: boolean;
  github_detected?: boolean;
  portfolio_detected?: boolean;
  url_count?: number;
  date_count?: number;
  date_range_count?: number;
  sections?:
    | number
    | {
        detected?: string[] | number;
        count?: number;
        standard_count?: number;
      };
  section_names?: string[];
  standard_section_count?: number;
  images?: number;
  tables?: number;
  likely_two_column?: boolean;
  column_confidence?: number;
  repeated_header_footer_lines?: number;
  header_footer_signal?: boolean;
  image_only_pages?: number;
  avg_characters_per_page?: number;
  unique_character_ratio?: number;
  replacement_character_count?: number;
  control_character_count?: number;
  text_extractable?: boolean;
  text_density?: number;
  words_per_page?: number;
  career_stage?: string;
  total_experience_years?: number;
  experience_years?: number;
  primary_role?: string;
  industry_focus?: string;
  industry?: string;
  parse_warnings?: string[];
}

export interface AiAnalysis {
  summary?: string;
  strengths?: string[];
  weaknesses?: string[];
  recommendations?: string[];
  experience_relevance?: string;
  skill_gap_analysis?: string;
}

export interface AnalyzeResponse {
  success?: boolean;
  filename?: string;
  text?: string;
  resume_skills?: string[];
  required_skills?: string[];
  preferred_skills?: string[];
  scoring?: Scoring;
  ats?: AtsReport;
  resume_health?: ResumeHealth;
  document?: DocumentInfo;
  ai_analysis?: AiAnalysis | null;
  message?: string;
}


export class ApiError extends Error {
  kind: "network" | "http" | "malformed";
  status: number | undefined;

  constructor(message: string, kind: ApiError["kind"], status?: number) {
    super(message);
    this.name = "ApiError";
    this.kind = kind;
    this.status = status;
  }
}

export const MAX_PDF_BYTES = 10 * 1024 * 1024;

export function validatePdf(file: File): string | null {
  const isPdf =
    file.type === "application/pdf" || file.name.toLowerCase().endsWith(".pdf");
  if (!isPdf) return "Only PDF resumes are supported. Please select a .pdf file.";
  if (file.size === 0) return "That file appears to be empty.";
  if (file.size > MAX_PDF_BYTES) return "That PDF is larger than 10 MB.";
  return null;
}

export async function analyzeResume(
  file: File,
  jobDescription: string,
  signal?: AbortSignal,
): Promise<AnalyzeResponse> {
  const form = new FormData();
  form.append("file", file);
  form.append("job_description", jobDescription);

  let response: Response;
  try {
    response = await fetch(`${API_BASE_URL}/analyze`, {
      method: "POST",
      body: form,
      ...(signal ? { signal } : {}),
    });
  } catch (error) {
    if ((error as Error)?.name === "AbortError") throw error;
    throw new ApiError(
      `Could not reach the analysis service at ${API_BASE_URL}. Make sure the backend is running.`,
      "network",
    );
  }

  const raw = await response.text();
  let data: unknown = null;
  if (raw) {
    try {
      data = JSON.parse(raw);
    } catch {
      data = null;
    }
  }

  if (!response.ok) {
    const detail =
      (data as { detail?: unknown } | null)?.detail ??
      (data as { message?: unknown } | null)?.message;
    throw new ApiError(
      typeof detail === "string" && detail
        ? detail
        : `The analysis request failed (HTTP ${response.status}).`,
      "http",
      response.status,
    );
  }

  if (!data || typeof data !== "object") {
    throw new ApiError(
      "The service returned a response the app could not read.",
      "malformed",
    );
  }

  const result = data as AnalyzeResponse;
  if (result.success === false) {
    throw new ApiError(
      result.message || "The analysis could not be completed.",
      "http",
      response.status,
    );
  }
  const score = result.scoring?.job_match_score ?? result.scoring?.ats_score;
  if (!result.scoring || typeof score !== "number") {
    throw new ApiError(
      "The analysis response was missing its score data.",
      "malformed",
    );
  }


  return result;
}
