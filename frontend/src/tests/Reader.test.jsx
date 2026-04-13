import { describe, it, expect } from 'vitest';
import { render, screen, fireEvent } from '@testing-library/react';
import Reader from '../components/Reader';

describe('Reader Component', () => {
  beforeAll(() => {
    global.window.speechSynthesis = {
      cancel: vi.fn(),
      speak: vi.fn(),
      pause: vi.fn(),
      resume: vi.fn(),
      getVoices: vi.fn().mockReturnValue([])
    };
    // Mock SpeechSynthesisUtterance if needed by the component
    global.window.SpeechSynthesisUtterance = vi.fn();
  });

  const dummyDocument = {
    filename: 'test.pdf',
    document: [
      {
        page: 1,
        chunks: ['Oracion uno.', 'Oracion dos repetida.']
      },
      {
        page: 2,
        chunks: ['Esto es la pagina dos.']
      }
    ]
  };

  it('renders chunks and titles properly for page 1', () => {
    render(<Reader documentData={dummyDocument} onReset={() => {}} />);
    
    expect(screen.getByText(/test\.pdf/)).toBeDefined();
    expect(screen.getByText('Oracion uno.')).toBeDefined();
    expect(screen.getByText('Oracion dos repetida.')).toBeDefined();
  });

  it('paginates forwards and backwards correctly', () => {
    render(<Reader documentData={dummyDocument} onReset={() => {}} />);
    
    // We are on page 1, check presence of 'Página 1 de 2'
    expect(screen.getByText(/Página 1 de 2/)).toBeDefined();
    
    // Click Next
    const nextBtn = screen.getByText('Siguiente Pág.');
    fireEvent.click(nextBtn);
    
    // Now we should see page 2
    expect(screen.getByText('Esto es la pagina dos.')).toBeDefined();
    expect(screen.getByText(/Página 2 de 2/)).toBeDefined();
    
    // Click Previous
    const prevBtn = screen.getByText('Anterior Pág.');
    fireEvent.click(prevBtn);
    
    // Back to page 1
    expect(screen.getByText('Oracion uno.')).toBeDefined();
  });
});
