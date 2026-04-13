from fastapi import FastAPI, UploadFile, File, Form
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
    file_location = f"uploads/{file.filename}"
    with open(file_location, "wb+") as file_object:
        shutil.copyfileobj(file.file, file_object)

    # 1. Extraer (El Cerebro)
    parser = PDFParser(file_location)
    raw_pages = parser.extract_text()
    
    # 2. Limpiar
    cleaner = TextCleaner()
    clean_pages = cleaner.clean_text_list(raw_pages)

    # 3. Preparar para TTS (Chunking)
    tts = TTSHandler(lang=lang)
    final_output = []

    for page in clean_pages:
        chunks = tts.chunk_text(page["text"])
        final_output.append({
            "page": page["page"],
            "chunks": chunks
        })

    # Eliminamos el archivo temp (opcional, por ahora lo dejamos o lo borramos para no hacer clutering de RAM)
    os.remove(file_location)

    return {"filename": file.filename, "document": final_output}
