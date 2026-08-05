from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
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
async def analyze_resume(file: UploadFile = File(...)):
    """
    Analyze a resume:
    1. Save PDF
    2. Extract text
    3. Return extracted text (+ score, suggestions later)
    
    One endpoint for the entire user journey.
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
                if page_text:  # Handle None if page has no text
                    text += page_text + "\n"
        
        # Return extracted text
        return {
            "success": True,
            "filename": file.filename,
            "text": text,
            "message": "Resume processed successfully"
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }