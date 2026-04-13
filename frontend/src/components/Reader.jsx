import React, { useState, useEffect, useRef } from 'react';

const STATUS_NOT_READING = -1;

export default function Reader({ documentData, onBack }) {
  const [currentPageIndex, setCurrentPageIndex] = useState(0);
  const [currentChunkIndex, setCurrentChunkIndex] = useState(STATUS_NOT_READING);
  const [isPlaying, setIsPlaying] = useState(false);
  
  // Ref for the Text-to-Speech Engine
  const synthRef = useRef(window.speechSynthesis);
  const utteranceRef = useRef(null);

  const pages = documentData.document;
  const currentPage = pages[currentPageIndex] || { chunks: [] };

  // Save bookmark to local storage
  useEffect(() => {
    localStorage.setItem('lectorpdf_bookmark', JSON.stringify({
      filename: documentData.filename,
      pageIndex: currentPageIndex
    }));
  }, [currentPageIndex, documentData.filename]);

  // Handle "Karaoke" playback sync
  useEffect(() => {
    // If playing...
    if (isPlaying && currentChunkIndex < currentPage.chunks.length) {
      const textToRead = currentPage.chunks[currentChunkIndex];
      if (!textToRead) {
        // End of page reached
        handleNextPage();
        return;
      }

      synthRef.current.cancel(); // Stop previous audios

      const utterance = new SpeechSynthesisUtterance(textToRead);
      utterance.lang = 'es-ES'; // Default, ideally received as parameter
      utterance.rate = 1.0;
      
      utterance.onend = () => {
        // Move to the next chunk
        setCurrentChunkIndex((prev) => prev + 1);
      };

      utterance.onerror = (e) => {
        if(e.error === 'interrupted' || e.error === 'canceled') return; // Expected
        console.error("Speech error", e);
        setIsPlaying(false);
      };

      utteranceRef.current = utterance;
      synthRef.current.speak(utterance);
    } 
    
    // If paused, cancel audio but keep the index
    if (!isPlaying) {
      synthRef.current.cancel();
    }

    return () => {
      synthRef.current.cancel(); // Cleanup on unmount/re-render
    };
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [isPlaying, currentChunkIndex, currentPageIndex]);

  const toggleReading = () => {
    if (!isPlaying && currentChunkIndex === STATUS_NOT_READING) {
      // Start from beginning
      setCurrentChunkIndex(0);
    }
    setIsPlaying(!isPlaying);
  };

  const handleNextPage = () => {
    if (currentPageIndex < pages.length - 1) {
      setCurrentPageIndex(prev => prev + 1);
      setCurrentChunkIndex(0); // Auto-reset for the new page
    } else {
      setIsPlaying(false);
      setCurrentChunkIndex(STATUS_NOT_READING); // End of book
    }
  };

  const handlePrevPage = () => {
    if (currentPageIndex > 0) {
      setCurrentPageIndex(prev => prev - 1);
      setCurrentChunkIndex(0); 
    }
  };

  return (
    <div className="reader-ui animate-fade-in" style={{ display: 'flex', flexDirection: 'column', flex: 1, height: '100%' }}>
      
      {/* Top Bar */}
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '2rem' }}>
        <button onClick={() => { setIsPlaying(false); onBack(); }} style={{ background: 'transparent', border: '1px solid var(--surface-border)' }}>
          ← Volver
        </button>
        <div className="heading-font" style={{ fontSize: '1.2rem', color: 'var(--text-secondary)' }}>
          {documentData.filename} - Página {currentPage.page} de {pages[pages.length-1]?.page || pages.length}
        </div>
      </div>

      {/* Reflow-style Reading Area */}
      <div className="glass-panel" style={{ flex: 1, padding: '3rem', overflowY: 'auto', textAlign: 'left', lineHeight: '1.8', fontSize: '1.2rem' }}>
        {currentPage.chunks.length === 0 ? (
          <div>No hay texto legible en esta página.</div>
        ) : (
          currentPage.chunks.map((chunk, idx) => {
            const isHighlight = idx === currentChunkIndex;
            return (
              <span 
                key={idx} 
                className={isHighlight ? 'chunk-active' : 'chunk-inactive'} 
                style={{ cursor: 'pointer', marginRight: '0.4rem' }}
                onClick={() => {
                  setCurrentChunkIndex(idx);
                  setIsPlaying(true);
                }}
              >
                {chunk}
              </span>
            );
          })
        )}
      </div>

      {/* Smart Controls */}
      <div className="controls glass-panel" style={{ display: 'flex', justifyContent: 'center', gap: '1.5rem', marginTop: '2rem', padding: '1rem' }}>
        <button onClick={handlePrevPage} disabled={currentPageIndex === 0} style={{ background: 'var(--surface-color)' }}>
          Anterior Pág.
        </button>
        <button onClick={toggleReading} style={{ padding: '0.8em 3em', fontSize: '1.2rem' }}>
          {isPlaying ? '⏸ Pausa' : '▶ Reproducir'}
        </button>
        <button onClick={handleNextPage} disabled={currentPageIndex === pages.length - 1} style={{ background: 'var(--surface-color)' }}>
          Siguiente Pág.
        </button>
      </div>

    </div>
  );
}
