from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
import os

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
os.makedirs("uploads", exist_ok=True)

@app.get("/")
def read_root():
    return {"message": "Hello, skillmatch-ai!"}

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.post("/upload-resume")
async def upload_resume(file: UploadFile = File(...)):
    """
    Receive a PDF, save it locally.
    """
    try:
        # Save the file to the uploads folder
        file_path = f"uploads/{file.filename}"
        with open(file_path, "wb") as buffer:
            contents = await file.read()
            buffer.write(contents)
        
        return {
            "success": True,
            "filename": file.filename,
            "message": f"File saved to {file_path}"
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }