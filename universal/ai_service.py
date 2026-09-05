"""Bounded LLM interpretation layer.

Deterministic analysis owns every score, requirement classification, and evidence level.
The model only turns those signals into concise prose. Provider support is compatible
with both OpenAI and OpenAI-compatible Groq deployments.
"""
from __future__ import annotations

import json
import os
import re
from typing import Any

from dotenv import load_dotenv

load_dotenv()
client = None
provider: str | None = None


def init_client() -> bool:
    global client, provider
    openai_key = os.getenv("OPENAI_API_KEY")
    groq_key = os.getenv("GROQ_API_KEY")
    if openai_key:
        from openai import OpenAI
        client = OpenAI(api_key=openai_key)
        provider = "openai"
        return True
    if groq_key:
        from openai import OpenAI
        client = OpenAI(api_key=groq_key, base_url="https://api.groq.com/openai/v1")
        provider = "groq"
        return True
    return False


def _parse_json_response(content: str) -> dict | None:
    if not content:
        return None
    cleaned = content.strip()
    if cleaned.startswith("```json"):
        cleaned = cleaned[7:]
    elif cleaned.startswith("```"):
        cleaned = cleaned[3:]
    if cleaned.endswith("```"):
        cleaned = cleaned[:-3]
    try:
        parsed = json.loads(cleaned.strip())
        return parsed if isinstance(parsed, dict) else None
    except json.JSONDecodeError:
        return None


def _bounded_string_list(value: Any, limit: int) -> list[str]:
    if not isinstance(value, list):
        return []
    out=[]
    for item in value[:limit]:
        if isinstance(item, str) and item.strip():
            out.append(item.strip())
    return out


def _validate_output(data: dict | None, analysis: dict) -> dict | None:
    """Validate shape and reject evidence claims that contradict deterministic data."""
    if not isinstance(data, dict):
        return None
    required = {"summary", "strengths", "weaknesses", "recommendations", "experience_relevance", "skill_gap_analysis"}
    if not required.issubset(data):
        return None
    out = {
        "summary": data["summary"] if isinstance(data["summary"], str) else "",
        "strengths": _bounded_string_list(data["strengths"], 4),
        "weaknesses": _bounded_string_list(data["weaknesses"], 4),
        "recommendations": _bounded_string_list(data["recommendations"], 5),
        "experience_relevance": data["experience_relevance"] if isinstance(data["experience_relevance"], str) else "",
        "skill_gap_analysis": data["skill_gap_analysis"] if isinstance(data["skill_gap_analysis"], str) else "",
    }
    if not out["summary"]:
        return None

    # The model must never upgrade weak/listed evidence. Reject the whole response
    # rather than silently presenting a contradictory interpretation to the user.
    evidence = analysis.get("scoring", {}).get("evidence", {})
    joined = " ".join([out["summary"], *out["strengths"], *out["weaknesses"], out["experience_relevance"], out["skill_gap_analysis"]]).lower()
    for skill, signal in evidence.items():
        level = signal.get("evidence_level")
        if level in {"listed", "weak"}:
            escaped = re.escape(skill.lower())
            if re.search(rf"(?:hands[- ]on|direct(?:ly)? (?:used|implemented|built|developed|demonstrated)|proven (?:experience|expertise)|production (?:experience|use)).{{0,80}}{escaped}|{escaped}.{{0,80}}(?:hands[- ]on|direct(?:ly)? (?:used|implemented|built|developed|demonstrated)|proven (?:experience|expertise)|production (?:experience|use))", joined):
                return None
    return out


def _build_prompt(resume_text: str, job_description: str, analysis: dict) -> str:
    scoring = analysis.get("scoring", {})
    ats = analysis.get("ats", {})
    health = analysis.get("resume_health", {})
    return f"""
You are the qualitative interpretation layer of a resume-to-job analyzer.

NON-NEGOTIABLE RULES:
1. Do not invent candidate facts, employers, projects, metrics, years, certifications, or experience.
2. Do not calculate, alter, or reinterpret numerical scores. The deterministic engine owns scores.
3. Do not claim an ATS pass probability.
4. Treat the deterministic evidence map as authoritative.
5. Evidence level 'strong' = demonstrated in experience, projects, or research.
6. Evidence level 'moderate' = contextual mention in profile, education, certification, leadership, etc.; do not call it hands-on.
7. Evidence level 'listed' = found only in skills/competencies; this is NOT proof of practical use.
8. Evidence level 'weak' = insufficient evidence; do not call it demonstrated.
9. If a skill is listed but not demonstrated, explicitly say so when relevant.
10. Do not say a required skill is missing if deterministic matching says it is matched.
11. Recommendations must be truthful and actionable, and must not tell the candidate to invent metrics.
12. Judge resume structure in context of career stage and occupation. Do not assume a CS-style resume.

RESUME:
{resume_text[:12000]}

JOB DESCRIPTION:
{job_description[:9000]}

DETERMINISTIC JOB MATCH:
{json.dumps(scoring, ensure_ascii=False)}

DETERMINISTIC ATS READINESS:
{json.dumps(ats, ensure_ascii=False)}

DETERMINISTIC RESUME HEALTH:
{json.dumps(health, ensure_ascii=False)}

Return ONLY JSON with exactly these fields:
{{
  "summary": "2-3 concise sentences",
  "strengths": ["up to 4 evidence-based strengths"],
  "weaknesses": ["up to 4 evidence-based weaknesses"],
  "recommendations": ["up to 5 concrete recommendations"],
  "experience_relevance": "concise explanation grounded in evidence",
  "skill_gap_analysis": "concise explanation of missing or weakly evidenced requirements"
}}
"""


def analyze_with_ai(resume_text: str, job_description: str, analysis: dict) -> dict | None:
    if client is None and not init_client():
        return None
    model = os.getenv("OPENAI_MODEL") if provider == "openai" else os.getenv("GROQ_MODEL", "openai/gpt-oss-120b")
    try:
        kwargs = {
            "model": model,
            "messages": [{"role": "user", "content": _build_prompt(resume_text, job_description, analysis)}],
            "temperature": 0.1,
            "max_tokens": 1400,
            "response_format": {"type": "json_object"},
        }
        response = client.chat.completions.create(**kwargs)
        content = response.choices[0].message.content or ""
        return _validate_output(_parse_json_response(content), analysis)
    except Exception as exc:
        print(f"AI analysis failed: {exc}")
        return None


def _build_resume_only_prompt(resume_text: str, analysis: dict) -> str:
    ats = analysis.get("ats", {})
    health = analysis.get("resume_health", {})

    return f"""
You are the qualitative interpretation layer of a resume analysis system.

This is a RESUME-ONLY analysis. There is no job description.

NON-NEGOTIABLE RULES:
1. Do not invent candidate facts, employers, projects, metrics, years, certifications, or experience.
2. Do not calculate or alter numerical scores.
3. Judge the resume in context of its apparent career stage and occupation.
4. Do not assume the candidate is a software/CS candidate.
5. Student/project-heavy resumes are valid and should not be penalized merely for lacking employment.
6. Recommendations must be truthful and actionable.
7. Never tell the candidate to invent metrics or experience.
8. Use only information actually present in the resume and deterministic analysis.
9. If something cannot be determined reliably, say so rather than guessing.

RESUME:
{resume_text[:12000]}

DETERMINISTIC ATS READINESS:
{json.dumps(ats, ensure_ascii=False)}

DETERMINISTIC RESUME HEALTH:
{json.dumps(health, ensure_ascii=False)}

Return ONLY JSON with exactly these fields:

{{
  "summary": "2-3 concise sentences about the overall resume",
  "strengths": ["up to 4 evidence-based strengths"],
  "weaknesses": ["up to 4 evidence-based weaknesses"],
  "recommendations": ["up to 6 concrete recommendations"],
  "career_stage": "human-readable career stage",
  "total_experience": "human-readable estimate based only on explicit evidence",
  "primary_role": "most evident role/domain from the resume",
  "industry_focus": "most evident industry/domain from the resume"
}}

Important:
- career_stage must be human-readable, e.g. "Student/Entry level", not "student_or_entry_level".
- total_experience must not be invented. If the resume does not provide enough evidence, say "Not clearly stated".
- primary_role and industry_focus must work for ANY occupation, including finance, accounting, marketing, business, design, engineering, etc.
"""


def analyze_resume_with_ai(resume_text: str, analysis: dict) -> dict | None:
    if client is None and not init_client():
        return None

    model = (
        os.getenv("OPENAI_MODEL")
        if provider == "openai"
        else os.getenv("GROQ_MODEL", "openai/gpt-oss-120b")
    )

    try:
        kwargs = {
            "model": model,
            "messages": [
                {
                    "role": "user",
                    "content": _build_resume_only_prompt(resume_text, analysis),
                }
            ],
            "temperature": 0.1,
            "max_tokens": 1400,
            "response_format": {"type": "json_object"},
        }

        response = client.chat.completions.create(**kwargs)
        content = response.choices[0].message.content or ""
        data = _parse_json_response(content)

        if not isinstance(data, dict):
            return None

        required = {
            "summary",
            "strengths",
            "weaknesses",
            "recommendations",
            "career_stage",
            "total_experience",
            "primary_role",
            "industry_focus",
        }

        if not required.issubset(data):
            return None

        return {
            "summary": data["summary"] if isinstance(data["summary"], str) else "",
            "strengths": _bounded_string_list(data["strengths"], 4),
            "weaknesses": _bounded_string_list(data["weaknesses"], 4),
            "recommendations": _bounded_string_list(data["recommendations"], 6),
            "career_stage": (
                data["career_stage"]
                if isinstance(data["career_stage"], str)
                else ""
            ),
            "total_experience": (
                data["total_experience"]
                if isinstance(data["total_experience"], str)
                else ""
            ),
            "primary_role": (
                data["primary_role"]
                if isinstance(data["primary_role"], str)
                else ""
            ),
            "industry_focus": (
                data["industry_focus"]
                if isinstance(data["industry_focus"], str)
                else ""
            ),
        }

    except Exception as exc:
        print(f"Resume-only AI analysis failed: {exc}")
        return None
