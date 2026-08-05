from fastapi import FastAPI, File, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
from services import extract_skills, calculate_ats_score
import pdfplumber

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create uploads folder if it doesn't exist
UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

@app.get("/")
def read_root():
    return {"message": "Hello, skillmatch-ai!"}

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.post("/analyze")
async def analyze_resume(file: UploadFile = File(...), job_description: str = Form(...)):
    """
    Analyze a resume against a job description.
    """
    try:
        # Save the file
        file_path = UPLOAD_DIR / file.filename
        with open(file_path, "wb") as buffer:
            contents = await file.read()
            buffer.write(contents)
        
        # Extract text from PDF
        text = ""
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
        
        # Extract skills from both
        resume_skills = extract_skills(text)
        job_skills = extract_skills(job_description)
        
        # Calculate ATS score
        scoring = calculate_ats_score(resume_skills, job_skills)
        
        return {
            "success": True,
            "filename": file.filename,
            "text": text,
            "resume_skills": resume_skills,
            "job_skills": job_skills,
            "matched_skills": scoring["matched_skills"],
            "missing_skills": scoring["missing_skills"],
            "ats_score": scoring["ats_score"],
            "message": "Resume analyzed successfully"
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }