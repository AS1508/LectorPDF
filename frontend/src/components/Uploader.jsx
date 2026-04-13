import React, { useState } from 'react';

export default function Uploader({ onUploadSuccess }) {
  const [file, setFile] = useState(null);
  const [isUploading, setIsUploading] = useState(false);
  const [error, setError] = useState('');

  const handleFileChange = (e) => {
    if (e.target.files && e.target.files[0]) {
      setFile(e.target.files[0]);
      setError('');
    }
  };

  const handeUpload = async () => {
    if (!file) return;
    setIsUploading(true);
    setError('');

    const formData = new FormData();
    formData.append('file', file);
    formData.append('lang', 'es'); // Default por el momento

    try {
      // Configuramos para llamar al backend tomando la URL dinámica para Docker/Producción
      const apiUrl = import.meta.env.VITE_API_URL || 'http://localhost:8000';
      const response = await fetch(`${apiUrl}/upload`, {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        throw new Error('Ocurrió un error al procesar el archivo.');
      }

      const data = await response.json();
      // data.document tiene el array de páginas y chunks
      onUploadSuccess(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setIsUploading(false);
    }
  };

  return (
    <div className="uploader glass-panel animate-fade-in" style={{ padding: '3rem', maxWidth: '600px', margin: '4rem auto' }}>
      <h2 className="heading-font" style={{ marginBottom: '1rem', fontSize: '2rem' }}>Empieza a escuchar tu libro</h2>
      <p style={{ color: 'var(--text-secondary)', marginBottom: '2rem' }}>
        Sube un documento PDF y nuestro motor inteligente extraerá el texto, saltando las cabeceras y reconstruyendo cada oración para una lectura fluida.
      </p>

      <div style={{ marginBottom: '2rem' }}>
        <input 
          type="file" 
          accept="application/pdf" 
          id="pdf-upload" 
          onChange={handleFileChange}
          style={{ display: 'none' }}
        />
        <label 
          htmlFor="pdf-upload" 
          style={{
            display: 'block',
            padding: '2rem',
            border: '2px dashed var(--accent-color)',
            borderRadius: '16px',
            cursor: 'pointer',
            background: 'rgba(99, 102, 241, 0.05)',
            transition: 'all 0.2s',
          }}
        >
          {file ? (
            <div style={{ color: 'var(--text-highlight)', fontWeight: 'bold' }}>📄 {file.name}</div>
          ) : (
            <div>Haz clic para seleccionar tu PDF</div>
          )}
        </label>
      </div>

      {error && <div style={{ color: '#ef4444', marginBottom: '1rem' }}>{error}</div>}

      <button 
        onClick={handeUpload} 
        disabled={!file || isUploading}
        style={{ width: '100%', fontSize: '1.2rem', padding: '1rem' }}
      >
        {isUploading ? 'Procesando con IA...' : 'Convertir a Audiolibro interactivo'}
      </button>
    </div>
  );
}
