from app.core.cleaner import TextCleaner

def test_cleaner_removes_newlines():
    cleaner = TextCleaner()
    # Mock de página extraída de PDF
    raw_data = [{
        "page": 1,
        "text": "Esta es la historia de una pala-\nbra que cruzó de renglón y se\nvolvió a unir. Pero este es otro punto.\nY este es otro renglón aislado."
    }]
    
    cleaned = cleaner.clean_text_list(raw_data)
    
    assert len(cleaned) == 1
    assert "palabra que cruzó de renglón y se volvió a unir." in cleaned[0]["text"]
    assert "Pero este es otro punto." in cleaned[0]["text"]

def test_cleaner_removes_repetitive_headers():
    cleaner = TextCleaner()
    # Simulamos un libro de 10 páginas
    raw_data = []
    for i in range(1, 11):
        raw_data.append({
            "page": i,
            "text": f"{i} Capítulo 4 Header molesto\nEste es el contenido propio de la página {i} principal del texto con un dato muy único {chr(65+i)}."
        })
        
    cleaned = cleaner.clean_text_list(raw_data)
    
    for page in cleaned:
        # El header debería ser podado por heurística (se repite en 10 páginas)
        assert "Capítulo 4 Header molesto" not in page["text"]
        # El contenido debería sobrevivir
        assert "principal del texto" in page["text"]
