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
}

export interface Scoring {
  ats_score?: number;
  required?: SkillGroup;
  preferred?: SkillGroup;
  earnings?: {
    earned_points?: number;
    possible_points?: number;
  };
  [key: string]: unknown;
}

export interface AiAnalysis {
  summary?: string;
  strengths?: string[];
  weaknesses?: string[];
  recommendations?: string[];
  experience_relevance?: string;
  skill_gap_analysis?: string;
  [key: string]: unknown;
}

export interface AnalyzeResponse {
  success?: boolean;
  filename?: string;
  text?: string;
  resume_skills?: string[];
  required_skills?: string[];
  preferred_skills?: string[];
  scoring?: Scoring;
  ai_analysis?: AiAnalysis | null;
  message?: string;
  [key: string]: unknown;
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
  if (!result.scoring || typeof result.scoring.ats_score !== "number") {
    throw new ApiError(
      "The analysis response was missing its score data.",
      "malformed",
    );
  }

  return result;
}
