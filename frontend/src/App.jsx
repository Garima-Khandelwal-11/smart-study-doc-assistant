import { useState } from 'react'
import UploadView from './components/UploadView'
import QAView from './components/QAView'
import QuizView from './components/QuizView'
import './App.css'

const TABS = [
  { id: 'upload', label: 'Upload' },
  { id: 'qa', label: 'Q&A' },
  { id: 'quiz', label: 'Quiz' },
]

function App() {
  const [documentId, setDocumentId] = useState(null)
  const [documentName, setDocumentName] = useState(null)
  const [activeTab, setActiveTab] = useState('upload')

  function handleUploaded(id, name) {
    setDocumentId(id)
    setDocumentName(name)
  }

  return (
    <div className="app">
      <header>
        <h1>Smart Study Doc Assistant</h1>
        {documentId && (
          <p className="doc-status" title={`Document ID: ${documentId}`}>
            Active document: <code>{documentName}</code>
          </p>
        )}
      </header>
      <nav className="tabs">
        {TABS.map((tab) => (
          <button
            key={tab.id}
            className={activeTab === tab.id ? 'tab active' : 'tab'}
            onClick={() => setActiveTab(tab.id)}
          >
            {tab.label}
          </button>
        ))}
      </nav>
      <main>
        {activeTab === 'upload' && (
          <UploadView documentId={documentId} onUploaded={handleUploaded} />
        )}
        {activeTab === 'qa' && <QAView documentId={documentId} />}
        {activeTab === 'quiz' && <QuizView documentId={documentId} />}
      </main>
    </div>
  )
}

export default App
