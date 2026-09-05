from __future__ import annotations

import os
import uuid
from pathlib import Path

from dotenv import load_dotenv
from fastapi import FastAPI, File, Form, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import select

from ai_service import analyze_resume_with_ai, analyze_with_ai
from ats_service import calculate_ats_readiness
from database import SessionLocal
from models import Analysis
from resume_health import analyze_resume_health
from resume_parser import analyze_pdf
from s3_service import upload_resume
from services import calculate_job_match, extract_skills, parse_job_sections

load_dotenv()

app = FastAPI(title="SkillMatch AI API", version="3.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:8080",
        "http://127.0.0.1:8000",
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = Path(os.getenv("UPLOAD_DIR", "uploads"))
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
S3_ENABLED = os.getenv("S3_ENABLED", "false").lower() == "true"
MAX_UPLOAD_BYTES = 10 * 1024 * 1024


@app.get("/")
def read_root():
    return {"message": "SkillMatch AI API", "s3_enabled": S3_ENABLED}


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.post("/analyze")
async def analyze_resume(
    file: UploadFile = File(...),
    job_description: str = Form(...),
):
    """Analyze a resume for job fit, ATS readiness, and resume health."""
    file_path: Path | None = None
    db = None

    try:
        if not file.filename:
            raise HTTPException(status_code=400, detail="No filename provided.")
        if not file.filename.lower().endswith(".pdf"):
            raise HTTPException(status_code=400, detail="Only PDF files are supported.")
        if len(job_description.strip()) < 40:
            raise HTTPException(status_code=400, detail="Job description must contain at least 40 characters.")

        original_filename = Path(file.filename).name
        unique_filename = f"{uuid.uuid4()}_{original_filename}"
        file_path = UPLOAD_DIR / unique_filename

        contents = await file.read()
        if not contents:
            raise HTTPException(status_code=400, detail="The uploaded PDF is empty.")
        if len(contents) > MAX_UPLOAD_BYTES:
            raise HTTPException(status_code=413, detail="The PDF must be 10 MB or smaller.")
        if not contents.startswith(b"%PDF"):
            raise HTTPException(status_code=400, detail="The uploaded file is not a valid PDF document.")

        file_path.write_bytes(contents)

        s3_key = None
        if S3_ENABLED:
            s3_key = f"resumes/{unique_filename}"
            upload_resume(str(file_path), s3_key)

        document = analyze_pdf(str(file_path))
        text = document["text"]
        if not document["text_extractable"]:
            # We still return the analysis so the user gets a useful explanation
            # for image/scanned resumes instead of an opaque parser error.
            document["parse_warnings"].append("The PDF yielded very little machine-readable text.")

        sections = parse_job_sections(job_description)
        resume_skills = extract_skills(text)
        required_skills = extract_skills(sections["required"])
        preferred_skills = extract_skills(sections["preferred"])

        job_match = calculate_job_match(
            resume_text=text,
            resume_skills=resume_skills,
            required_skills=required_skills,
            preferred_skills=preferred_skills,
            job_description=job_description,
        )
        ats = calculate_ats_readiness(document)
        health = analyze_resume_health(document)

        # Preserve the old response key so the current frontend does not break.
        # It now represents JOB MATCH, not ATS readiness. New clients should use
        # job_match_score and ats.score explicitly.
        scoring = dict(job_match)
        scoring["ats_score"] = job_match["job_match_score"]

        deterministic = {
            "scoring": scoring,
            "ats": ats,
            "resume_health": health,
        }
        ai_analysis = analyze_with_ai(text, job_description, deterministic)

        db = SessionLocal()
        analysis = Analysis(
            resume_filename=original_filename,
            # Existing schema requires a non-null value. Local analyses have no S3 key.
            s3_key=s3_key or "",
            job_description=job_description,
            # Backwards-compatible database field; it stores job-match score.
            ats_score=job_match["job_match_score"],
            required_matched=job_match["required"]["matched"],
            required_missing=job_match["required"]["missing"],
            preferred_matched=job_match["preferred"]["matched"],
            preferred_missing=job_match["preferred"]["missing"],
            ai_analysis=ai_analysis,
        )
        db.add(analysis)
        db.commit()
        db.refresh(analysis)

        return {
            "success": True,
            "filename": original_filename,
            "resume_skills": resume_skills,
            "required_skills": required_skills,
            "preferred_skills": preferred_skills,
            "scoring": scoring,
            "ats": ats,
            "resume_health": health,
            "document": {
                key: value
                for key, value in document.items()
                if key not in {"text", "page_metrics"}
            },
            "ai_analysis": ai_analysis,
            "message": "Resume analyzed successfully",
        }

    except HTTPException:
        raise
    except Exception as exc:
        if db:
            db.rollback()
        print(f"Resume analysis failed: {exc}")
        raise HTTPException(status_code=500, detail="The resume could not be analyzed. Please try another PDF.") from exc
    finally:
        if db:
            db.close()
        if file_path and file_path.exists():
            try:
                file_path.unlink()
            except OSError:
                pass

@app.post("/analyze-resume")
async def analyze_resume_only(
    file: UploadFile = File(...),
):
    """Analyze a resume without requiring a job description."""

    file_path: Path | None = None

    try:
        if not file.filename:
            raise HTTPException(status_code=400, detail="No filename provided.")

        if not file.filename.lower().endswith(".pdf"):
            raise HTTPException(status_code=400, detail="Only PDF files are supported.")

        original_filename = Path(file.filename).name
        unique_filename = f"{uuid.uuid4()}_{original_filename}"
        file_path = UPLOAD_DIR / unique_filename

        contents = await file.read()

        if not contents:
            raise HTTPException(status_code=400, detail="The uploaded PDF is empty.")

        if len(contents) > MAX_UPLOAD_BYTES:
            raise HTTPException(
                status_code=413,
                detail="The PDF must be 10 MB or smaller.",
            )

        if not contents.startswith(b"%PDF"):
            raise HTTPException(
                status_code=400,
                detail="The uploaded file is not a valid PDF document.",
            )

        file_path.write_bytes(contents)

        document = analyze_pdf(str(file_path))
        text = document["text"]

        if not document["text_extractable"]:
            document["parse_warnings"].append(
                "The PDF yielded very little machine-readable text."
            )

        ats = calculate_ats_readiness(document)
        health = analyze_resume_health(document)

        deterministic = {
            "ats": ats,
            "resume_health": health,
        }

        ai_analysis = analyze_resume_with_ai(text, deterministic)

        return {
            "success": True,
            "filename": original_filename,
            "ats": ats,
            "resume_health": health,
            "ai_analysis": ai_analysis,
            "document": {
                key: value
                for key, value in document.items()
                if key not in {"text", "page_metrics"}
            },
            "message": "Resume analyzed successfully",
        }

    except HTTPException:
        raise

    except Exception as exc:
        print(f"Resume-only analysis failed: {exc}")
        raise HTTPException(
            status_code=500,
            detail="The resume could not be analyzed. Please try another PDF.",
        ) from exc

    finally:
        if file_path and file_path.exists():
            try:
                file_path.unlink()
            except OSError:
                pass


@app.get("/analyses")
def get_analyses():
    db = SessionLocal()
    try:
        statement = select(Analysis).order_by(Analysis.created_at.desc())
        analyses = db.scalars(statement).all()
        return {
            "success": True,
            "analyses": [
                {
                    "id": analysis.id,
                    "resume_filename": analysis.resume_filename,
                    "s3_key": analysis.s3_key,
                    "job_match_score": analysis.ats_score,
                    "required_matched": analysis.required_matched,
                    "required_missing": analysis.required_missing,
                    "preferred_matched": analysis.preferred_matched,
                    "preferred_missing": analysis.preferred_missing,
                    "ai_analysis": analysis.ai_analysis,
                    "created_at": analysis.created_at,
                }
                for analysis in analyses
            ],
        }
    finally:
        db.close()
