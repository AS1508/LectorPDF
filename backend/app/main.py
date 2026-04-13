from fastapi import FastAPI, UploadFile, File, Form, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
import shutil
import os

from app.core.pdf_parser import PDFParser
from app.core.cleaner import TextCleaner
from app.services.tts_handler import TTSHandler

app = FastAPI(title="LectorPDF API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

os.makedirs("uploads", exist_ok=True)

@app.post("/upload")
async def upload_pdf(file: UploadFile = File(...), lang: str = Form("es")):
    # Security: Validate Mime-Type
    if file.content_type != "application/pdf":
        raise HTTPException(status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE, detail="Only PDF files are allowed.")
    
    # Security: Validate 50MB limit (Spool limit API)
    MAX_MB = 50 * 1024 * 1024
    file.file.seek(0, 2)
    file_size = file.file.tell()
    if file_size > MAX_MB:
        raise HTTPException(status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE, detail="File exceeds 50MB limit.")
    file.file.seek(0)
    
    # Security: Isolate filename (Path Traversal Protection)
    safe_filename = os.path.basename(file.filename)
    file_location = f"uploads/{safe_filename}"
    
    with open(file_location, "wb+") as file_object:
        shutil.copyfileobj(file.file, file_object)

    # 1. Extract (The Parser)
    parser = PDFParser(file_location)
    raw_pages = parser.extract_text()
    
    # 2. Clean text chunks
    cleaner = TextCleaner()
    clean_pages = cleaner.clean_text_list(raw_pages)

    # 3. Prepare for TTS (Chunking)
    tts = TTSHandler(lang=lang)
    final_output = []

    for page in clean_pages:
        chunks = tts.chunk_text(page["text"])
        final_output.append({
            "page": page["page"],
            "chunks": chunks
        })

    # Delete temp file to avoid persistent disk clutter
    os.remove(file_location)

    return {"filename": safe_filename, "document": final_output}
