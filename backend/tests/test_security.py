import io
from fastapi.testclient import TestClient
from unittest.mock import patch
from app.main import app
import os

client = TestClient(app)

def test_security_mime_type_rejection():
    file_content = b"MZ\x90\x00\x03\x00\x00\x00"
    response = client.post(
        "/upload",
        files={"file": ("virus.exe", io.BytesIO(file_content), "application/x-msdownload")},
        data={"lang": "es"}
    )
    assert response.status_code == 415
    assert "Only PDF files are allowed" in response.json()["detail"]

@patch("app.main.PDFParser")
@patch("app.main.TextCleaner")
@patch("app.main.TTSHandler")
def test_security_path_traversal_protection(mock_tts, mock_cleaner, mock_parser):
    file_content = b"%PDF-1.4\n"
    malicious_name = "../../../windows/system32/cmd.pdf"
    
    response = client.post(
        "/upload",
        files={"file": (malicious_name, io.BytesIO(file_content), "application/pdf")},
        data={"lang": "es"}
    )
    
    assert response.status_code == 200
    # Fastapi upload might preserve the name in the return depending on how backend handles it.
    # Our backend should have used os.path.basename when saving, avoiding traversal.
    # We can be sure it didn't throw a Write Permission error.
    assert "windows" not in response.json().get("filename", "")
    assert not os.path.exists("../../../windows/system32/cmd.pdf")

def test_security_max_size_limit():
    # Creamos 51MB reales en RAM (es muy rápido en Python)
    file_content = b"0" * (51 * 1024 * 1024)
    file_obj = io.BytesIO(file_content)
    
    response = client.post(
        "/upload",
        files={"file": ("heavy.pdf", file_obj, "application/pdf")},
        data={"lang": "es"}
    )
    
    assert response.status_code == 413
    assert "exceeds" in response.json()["detail"].lower()
