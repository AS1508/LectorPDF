import { useState } from 'react'
import Uploader from './components/Uploader'
import Reader from './components/Reader'

function App() {
  const [docData, setDocData] = useState(null)

  return (
    <div className="app-container">
      {/* Navbar Minimalista */}
      <nav className="nav-header">
        <div className="brand">LectorPDF</div>
        <div style={{ color: 'var(--text-secondary)' }}>
          Transforma lectura en audiolibro iterativo
        </div>
      </nav>

      <main style={{ flex: 1, display: 'flex', flexDirection: 'column' }}>
        {!docData ? (
          <Uploader onUploadSuccess={(data) => setDocData(data)} />
        ) : (
          <Reader documentData={docData} onBack={() => setDocData(null)} />
        )}
      </main>
    </div>
  )
}

export default App
