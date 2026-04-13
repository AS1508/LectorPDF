import { describe, it, expect, vi } from 'vitest';
import { render, screen, fireEvent } from '@testing-library/react';
import Uploader from '../components/Uploader';

describe('Uploader Component', () => {
  it('renders correct initial state elements', () => {
    render(<Uploader onUploadSuccess={() => {}} />);
    
    // Check titles and buttons
    expect(screen.getByText('Empieza a escuchar tu libro')).toBeDefined();
    expect(screen.getByText(/Haz clic para seleccionar/)).toBeDefined();
  });

  it('changes state when a file is selected', () => {
    const { container } = render(<Uploader onUploadSuccess={() => {}} />);
    
    // Find the hidden input file
    const fileInput = container.querySelector('input[type="file"]');
    
    // Mock a file selection
    const file = new File(['dummy content'], 'test.pdf', { type: 'application/pdf' });
    fireEvent.change(fileInput, { target: { files: [file] } });
    
    // It should now display the uploaded file name
    expect(screen.getByText(/test\.pdf/)).toBeDefined();
    
    // The main button should change text
    expect(screen.getByText('Convertir a Audiolibro interactivo')).toBeDefined();
  });
});
