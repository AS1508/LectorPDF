import pdfplumber
import os

class PDFParser:
    def __init__(self, file_path: str):
        self.file_path = file_path
    
    def extract_toc(self):
        """Intenta extraer el índice de marcadores nativos del PDF."""
        # En pdfplumber no hay una obtención directa de estructurados TOC fácil sin explorar los metadatos raw.
        # Simparemos una heurística o estructura básica.
        # Por simplicidad, leeremos páginas completas.
        return [{"level": 1, "title": "Inicio del Documento", "page": 1}]
    
    def extract_text(self):
        """Extrae el texto crudo página por página, usando los bounding_boxes para mantener columnas."""
        extracted_pages = []
        try:
            with pdfplumber.open(self.file_path) as pdf:
                for page_num, page in enumerate(pdf.pages):
                    # Recortar el 8% superior y 8% inferior para evitar headers y footers espurios
                    width = page.width
                    height = page.height
                    bbox = (0, height * 0.08, width, height * 0.92)
                    cropped_page = page.crop(bbox)
                    
                    # Extraer texto de izquierda a derecha, de arriba a abajo.
                    text = cropped_page.extract_text(x_tolerance=2, y_tolerance=3)
                    if text:
                        extracted_pages.append({
                            "page": page_num + 1,
                            "text": text
                        })
        except Exception as e:
            print(f"Error parsing PDF: {e}")
        return extracted_pages

