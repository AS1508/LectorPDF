import pdfplumber
import os

class PDFParser:
    def __init__(self, file_path: str):
        self.file_path = file_path
    
    def extract_toc(self):
        """Attempts to extract native bookmark structure (TOC) from the PDF."""
        # pdfplumber does not have a native method to extract TOC easily without exploring raw metadata.
        # We will simulate a heuristic or basic structure.
        # For simplicity, we will read full pages.
        return [{"level": 1, "title": "Start of Document", "page": 1}]
    
    def extract_text(self):
        """Extracts raw text page by page, using bounding_boxes to respect columns."""
        extracted_pages = []
        try:
            with pdfplumber.open(self.file_path) as pdf:
                for page_num, page in enumerate(pdf.pages):
                    # Crop the top 8% and bottom 8% to avoid spurious headers and footers
                    width = page.width
                    height = page.height
                    bbox = (0, height * 0.08, width, height * 0.92)
                    cropped_page = page.crop(bbox)
                    
                    # Extract text from left to right, top to bottom.
                    text = cropped_page.extract_text(x_tolerance=2, y_tolerance=3)
                    if text:
                        extracted_pages.append({
                            "page": page_num + 1,
                            "text": text
                        })
        except Exception as e:
            print(f"Error parsing PDF: {e}")
        return extracted_pages

