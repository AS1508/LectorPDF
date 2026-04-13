class TTSHandler:
    def __init__(self, lang="es"):
        pass # Spacy desactivado por falta de wheels en py 3.14 local. Usaremos fallback nativo.

    def chunk_text(self, text: str):
        """ Divide el texto en oraciones lógicas para ser procesadas secuencialmente por TTS. """
        # Fallback de separación básica
        return [t.strip() + "." for t in text.split('.') if len(t.strip()) > 1]
