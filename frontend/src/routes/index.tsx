import { createFileRoute } from "@tanstack/react-router";
import { useCallback, useEffect, useRef, useState } from "react";
import { Github, Linkedin, RotateCcw } from "lucide-react";

import { Header } from "@/components/Header";
import { Hero } from "@/components/Hero";
import { ResumeUploader } from "@/components/ResumeUploader";
import { JobDescriptionInput } from "@/components/JobDescriptionInput";
import { AnalyzeButton } from "@/components/AnalyzeButton";
import { AnalysisLoading } from "@/components/AnalysisLoading";
import { ATSScore } from "@/components/ATSScore";
import { SkillsBreakdown } from "@/components/SkillsBreakdown";
import { AIInsights } from "@/components/AIInsights";
import { ErrorState } from "@/components/ErrorState";
import { analyzeResume, type AnalyzeResponse } from "@/lib/api";

const TITLE = "SkillMatch AI — Resume vs. job description match score";
const DESCRIPTION =
  "Upload a resume and paste a job description to get a weighted ATS match score, an exact required vs. preferred skill gap breakdown, and AI recommendations.";

export const Route = createFileRoute("/")({
  head: () => ({
    meta: [
      { title: TITLE },
      { name: "description", content: DESCRIPTION },
      { property: "og:title", content: TITLE },
      { property: "og:description", content: DESCRIPTION },
      { property: "og:type", content: "website" },
      { name: "twitter:card", content: "summary_large_image" },
    ],
  }),
  component: Index,
});

const MIN_JD_CHARS = 40;

function Index() {
  const [file, setFile] = useState<File | null>(null);
  const [jobDescription, setJobDescription] = useState("");
  const [jdError, setJdError] = useState<string | null>(null);
  const [status, setStatus] = useState<"idle" | "loading" | "done" | "error">("idle");
  const [result, setResult] = useState<AnalyzeResponse | null>(null);
  const [error, setError] = useState<unknown>(null);
  const [apiStatus, setApiStatus] = useState<"unknown" | "online" | "offline">("unknown");

  const abortRef = useRef<AbortController | null>(null);
  const resultsRef = useRef<HTMLDivElement | null>(null);

  useEffect(() => () => abortRef.current?.abort(), []);

  useEffect(() => {
    if (status === "done" || status === "error") {
      resultsRef.current?.scrollIntoView({ behavior: "smooth", block: "start" });
    }
  }, [status]);

  const run = useCallback(async () => {
    if (!file) return;
    if (jobDescription.trim().length < MIN_JD_CHARS) {
      setJdError(`Add at least ${MIN_JD_CHARS} characters of job description.`);
      return;
    }
    setJdError(null);
    abortRef.current?.abort();
    const controller = new AbortController();
    abortRef.current = controller;

    setStatus("loading");
    setError(null);
    setResult(null);
    try {
      const data = await analyzeResume(file, jobDescription.trim(), controller.signal);
      setResult(data);
      setStatus("done");
      setApiStatus("online");
    } catch (e) {
      if ((e as Error)?.name === "AbortError") return;
      setError(e);
      setStatus("error");
      setApiStatus("offline");
    }
  }, [file, jobDescription]);

  function reset() {
    abortRef.current?.abort();
    setStatus("idle");
    setResult(null);
    setError(null);
  }

  const canAnalyze = Boolean(file) && jobDescription.trim().length >= MIN_JD_CHARS;

  return (
    <div className="min-h-screen bg-background text-foreground">
      <Header status={apiStatus} />
      <main>
        <Hero />

        <div className="mx-auto max-w-[1400px] px-5 py-14 sm:px-8 sm:py-20">
          <section aria-labelledby="input-heading" className="border-b border-border-strong pb-14">
            <h2 id="input-heading" className="label-mono text-muted-foreground">
              01 — INPUTS
            </h2>
            <div className="mt-6 grid gap-10 lg:grid-cols-2">
              <div>
                <p className="label-strong">Resume</p>
                <div className="mt-3">
                  <ResumeUploader
                    file={file}
                    onChange={setFile}
                    disabled={status === "loading"}
                  />
                </div>
              </div>
              <JobDescriptionInput
                value={jobDescription}
                onChange={(v) => {
                  setJobDescription(v);
                  if (jdError) setJdError(null);
                }}
                disabled={status === "loading"}
                error={jdError}
              />
            </div>

            <div className="mt-10 flex flex-col gap-4 sm:flex-row sm:items-center">
              <AnalyzeButton
                onClick={run}
                disabled={!canAnalyze}
                loading={status === "loading"}
              />
              {(status === "done" || status === "error") && (
                <button
                  type="button"
                  onClick={reset}
                  className="inline-flex items-center justify-center gap-3 border border-border-strong px-5 py-4 text-sm font-bold uppercase tracking-[0.08em] transition-colors hover:bg-foreground hover:text-background"
                >
                  <RotateCcw className="size-4" aria-hidden="true" />
                  Start over
                </button>
              )}
              {!canAnalyze && status !== "loading" && (
                <p className="label-mono text-muted-foreground">
                  RESUME PDF + JOB DESCRIPTION REQUIRED
                </p>
              )}
            </div>
          </section>

          <div ref={resultsRef} className="scroll-mt-24">
            {status === "loading" && (
              <div className="pt-14">
                <AnalysisLoading />
              </div>
            )}

            {status === "error" && (
              <div className="pt-14">
                <ErrorState error={error} onRetry={run} />
              </div>
            )}

            {status === "done" && result?.scoring && (
              <div className="space-y-14 pt-14">
                <ATSScore scoring={result.scoring} filename={result.filename} />
                <SkillsBreakdown
                  required={result.scoring.required}
                  preferred={result.scoring.preferred}
                  resumeSkills={result.resume_skills}
                />
                <AIInsights analysis={result.ai_analysis} />
              </div>
            )}
          </div>
        </div>
      </main>

      <footer className="border-t border-border-strong">
        <div className="mx-auto flex max-w-[1400px] items-center justify-center px-5 py-10 sm:px-8">
          <div className="flex items-center gap-4 label-mono text-base text-muted-foreground">
            <span>Built by Nayan Gattani</span>
            <a
              href="https://github.com/NayanGattani"
              target="_blank"
              rel="noopener noreferrer"
              aria-label="GitHub"
              className="transition-colors hover:text-foreground"
            >
              <Github className="size-5" aria-hidden="true" />
            </a>
            <a
              href="https://linkedin.com/in/nayangattani"
              target="_blank"
              rel="noopener noreferrer"
              aria-label="LinkedIn"
              className="transition-colors hover:text-foreground"
            >
              <Linkedin className="size-5" aria-hidden="true" />
            </a>
          </div>
        </div>
      </footer>
    </div>
  );
}
