import io
from fastapi.testclient import TestClient
from unittest.mock import patch
from app.main import app
import os

client = TestClient(app)

@patch("app.main.PDFParser")
@patch("app.main.TextCleaner")
@patch("app.main.TTSHandler")
def test_upload_pdf_success(mock_tts, mock_cleaner, mock_parser):
    # Setup mocks
    mock_parser_instance = mock_parser.return_value
    mock_parser_instance.extract_text.return_value = [{"page": 1, "text": "Raw Text"}]
    
    mock_cleaner_instance = mock_cleaner.return_value
    mock_cleaner_instance.clean_text_list.return_value = [{"page": 1, "text": "Clean Text"}]
    
    mock_tts_instance = mock_tts.return_value
    mock_tts_instance.chunk_text.return_value = ["Clean Text."]
    
    # Crear PDF valido simulado
    file_content = b"%PDF-1.4\n%EOF\n"
    
    response = client.post(
        "/upload",
        files={"file": ("dummy.pdf", io.BytesIO(file_content), "application/pdf")},
        data={"lang": "es"}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["filename"] == "dummy.pdf"
    assert len(data["document"]) == 1
    assert data["document"][0]["page"] == 1
    assert "Clean Text." in data["document"][0]["chunks"]
    
    # Check that temporary file is deleted
    assert not os.path.exists("uploads/dummy.pdf")
