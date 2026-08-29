import os
import uuid
from pathlib import Path

import pdfplumber
from dotenv import load_dotenv
from fastapi import FastAPI, File, Form, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import select

from ai_service import analyze_with_ai
from database import SessionLocal
from models import Analysis
from s3_service import upload_resume
from services import calculate_ats_score, extract_skills, parse_job_sections

load_dotenv()

app = FastAPI()

# Allow requests from the local frontend during development
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

# Use local storage by default; EC2 can override this with an environment variable
UPLOAD_DIR = Path(os.getenv("UPLOAD_DIR", "uploads"))
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

# S3 is disabled locally and enabled in the AWS environment
S3_ENABLED = os.getenv("S3_ENABLED", "false").lower() == "true"


@app.get("/")
def read_root():
    return {
        "message": "Hello, skillmatch-ai!",
        "s3_enabled": S3_ENABLED,
    }


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.post("/analyze")
async def analyze_resume(
    file: UploadFile = File(...),
    job_description: str = Form(...),
):
    """Analyze a resume against a job description."""

    file_path = None
    db = None

    try:
        if not file.filename:
            return {
                "success": False,
                "error": "No filename provided.",
            }

        if not file.filename.lower().endswith(".pdf"):
            return {
                "success": False,
                "error": "Only PDF files are supported.",
            }

        original_filename = Path(file.filename).name
        unique_filename = f"{uuid.uuid4()}_{original_filename}"
        file_path = UPLOAD_DIR / unique_filename

        # Save the PDF temporarily for text extraction
        with open(file_path, "wb") as buffer:
            contents = await file.read()
            buffer.write(contents)

        s3_key = None

        # Store the resume in S3 when running in AWS
        if S3_ENABLED:
            s3_key = f"resumes/{unique_filename}"
            upload_resume(str(file_path), s3_key)

        # Extract text from the resume
        text = ""

        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()

                if page_text:
                    text += page_text + "\n"

        sections = parse_job_sections(job_description)

        resume_skills = extract_skills(text)
        required_skills = extract_skills(sections["required"])
        preferred_skills = extract_skills(sections["preferred"])

        # ATS score is calculated deterministically
        scoring = calculate_ats_score(
            resume_skills,
            required_skills,
            preferred_skills,
        )

        ai_analysis = analyze_with_ai(
            text,
            job_description,
            scoring,
        )

        # Store the analysis and its S3 reference in PostgreSQL
        db = SessionLocal()

        analysis = Analysis(
            resume_filename=original_filename,
            s3_key=s3_key,
            job_description=job_description,
            ats_score=scoring["ats_score"],
            required_matched=scoring["required"]["matched"],
            required_missing=scoring["required"]["missing"],
            preferred_matched=scoring["preferred"]["matched"],
            preferred_missing=scoring["preferred"]["missing"],
            ai_analysis=ai_analysis,
        )

        db.add(analysis)
        db.commit()
        db.refresh(analysis)

        return {
            "success": True,
            "filename": original_filename,
            "text": text,
            "resume_skills": resume_skills,
            "required_skills": required_skills,
            "preferred_skills": preferred_skills,
            "scoring": scoring,
            "ai_analysis": ai_analysis,
            "message": "Resume analyzed successfully",
        }

    except Exception as e:
        if db:
            db.rollback()

        return {
            "success": False,
            "error": str(e),
        }

    finally:
        if db:
            db.close()

        # Remove the temporary local copy after processing
        if file_path and file_path.exists():
            try:
                file_path.unlink()
            except OSError:
                pass


@app.get("/analyses")
def get_analyses():
    db = SessionLocal()

    try:
        statement = (
            select(Analysis)
            .order_by(Analysis.created_at.desc())
        )

        analyses = db.scalars(statement).all()

        return {
            "success": True,
            "analyses": [
                {
                    "id": analysis.id,
                    "resume_filename": analysis.resume_filename,
                    "s3_key": analysis.s3_key,
                    "ats_score": analysis.ats_score,
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