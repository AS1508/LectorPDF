import re
from collections import defaultdict

class TextCleaner:
    def __init__(self):
        pass
        
    def _find_repetitive_headers_footers(self, pages_data):
        """ Encuentra líneas que se repiten mucho al principio o final de las páginas. """
        line_counts = defaultdict(int)
        
        # Recolectamos posibles cabeceras/pies (primeras y últimas líneas de cada página)
        for p in pages_data:
            lines = [line.strip() for line in p.get("text", "").split('\n') if line.strip()]
            if not lines: continue
            
            # Revisar las primeras 3 y últimas 3 líneas sin duplicar en páginas muy cortas
            if len(lines) <= 6:
                boundary_lines = lines
            else:
                boundary_lines = lines[:3] + lines[-3:]
            for bline in boundary_lines:
                # Quitamos todos los dígitos para ignorar números de página, ej: '86 Capítulo 4' -> ' Capítulo '
                normalized = re.sub(r'\d+', '', bline).strip()
                # Si tiene suficiente texto, lo contamos
                if len(normalized) > 5:
                    line_counts[normalized] += 1
                    
        # Consideramos 'cabecera ruidosa' si la línea normalizada aparece en más del 15% de las hojas
        # Usamos max(2, ...) para que funcione también en PDF cortitos de prueba (mínimo 2 apariciones)
        threshold = max(2, len(pages_data) * 0.15)
        repetitive_patterns = {k for k, v in line_counts.items() if v >= threshold}
        
        return repetitive_patterns

    def clean_text_list(self, pages_data):
        """
        Limpia el texto extraído página por página.
        - Elimina dinámicamente Headers basados en algoritmos de repetición.
        - Reconstruye párrafos y borra guiones fantasma.
        """
        # 1. Aprender cuáles son las cabeceras/pies de página
        repetitive_patterns = self._find_repetitive_headers_footers(pages_data)
        
        cleaned_pages = []
        for p in pages_data:
            # 2. Separar página en líneas individuales
            lines = [line.strip() for line in p.get("text", "").split('\n') if line.strip()]
            filtered_lines = []
            
            # 3. Filtrar y eliminar el ruido detectado
            for line in lines:
                normalized = re.sub(r'\d+', '', line).strip()
                # Si la linea es la cabecera repetitiva y larga, la matamos
                if normalized in repetitive_patterns and len(normalized) > 5:
                    continue
                filtered_lines.append(line)
            
            # 4. Volver a unir las líneas que sobrevivieron
            text = '\n'.join(filtered_lines)
            
            # 5. Lógica clásica: Remover guiones de fin de línea y curar saltos de carro
            text = re.sub(r'-\s*\n\s*', '', text)
            text = re.sub(r'(?<![.\!\?])\s*\n\s*', ' ', text)
            text = re.sub(r'\s{2,}', ' ', text)
            
            cleaned_pages.append({
                "page": p.get("page"),
                "text": text.strip()
            })
            
        return cleaned_pages
