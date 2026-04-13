import re
from collections import defaultdict

class TextCleaner:
    def __init__(self):
        pass
        
    def _find_repetitive_headers_footers(self, pages_data):
        """ Finds highly repetitive lines at the top or bottom of the pages. """
        line_counts = defaultdict(int)
        
        # Collect potential headers/footers (first and last lines of each page)
        for p in pages_data:
            lines = [line.strip() for line in p.get("text", "").split('\n') if line.strip()]
            if not lines: continue
            
            # Check the first 3 and last 3 lines, avoiding duplicates on extremely short pages
            if len(lines) <= 6:
                boundary_lines = lines
            else:
                boundary_lines = lines[:3] + lines[-3:]
            for bline in boundary_lines:
                # Remove all digits to ignore page numbers, e.g. '86 Chapter 4' -> ' Chapter '
                normalized = re.sub(r'\d+', '', bline).strip()
                # If it has enough text length, count it
                if len(normalized) > 5:
                    line_counts[normalized] += 1
                    
        # Consider it a 'noisy header' if the normalized line appears in more than 15% of the pages
        # Use max(2, ...) to ensure it works on short test PDFs (minimum 2 occurrences)
        threshold = max(2, len(pages_data) * 0.15)
        repetitive_patterns = {k for k, v in line_counts.items() if v >= threshold}
        
        return repetitive_patterns

    def clean_text_list(self, pages_data):
        """
        Cleans the extracted text page by page.
        - Dynamically removes headers based on repetition algorithms.
        - Reconstructs paragraphs and removes ghost hyphens.
        """
        # 1. Learn which lines are headers/footers
        repetitive_patterns = self._find_repetitive_headers_footers(pages_data)
        
        cleaned_pages = []
        for p in pages_data:
            # 2. Split page into individual lines
            lines = [line.strip() for line in p.get("text", "").split('\n') if line.strip()]
            filtered_lines = []
            
            # 3. Filter and remove detected noise
            for line in lines:
                normalized = re.sub(r'\d+', '', line).strip()
                # If line is a repetitive and long header, remove it
                if normalized in repetitive_patterns and len(normalized) > 5:
                    continue
                filtered_lines.append(line)
            
            # 4. Rejoin surviving lines
            text = '\n'.join(filtered_lines)
            
            # 5. Classic logic: Remove end-of-line hyphens and cure carriage returns
            text = re.sub(r'-\s*\n\s*', '', text)
            text = re.sub(r'(?<![.\!\?])\s*\n\s*', ' ', text)
            text = re.sub(r'\s{2,}', ' ', text)
            
            cleaned_pages.append({
                "page": p.get("page"),
                "text": text.strip()
            })
            
        return cleaned_pages
