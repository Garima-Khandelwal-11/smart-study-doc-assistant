import { useState } from 'react'
import { uploadDocument } from '../api'

function UploadView({ documentId, onUploaded }) {
  const [file, setFile] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)
  const [numChunks, setNumChunks] = useState(null)

  async function handleUpload(e) {
    e.preventDefault()
    if (!file) return
    setLoading(true)
    setError(null)
    try {
      const result = await uploadDocument(file)
      onUploaded(result.document_id, file.name)
      setNumChunks(result.num_chunks)
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="view">
      <h2>Upload a document</h2>
      <form onSubmit={handleUpload}>
        <input
          type="file"
          accept=".pdf,.docx,.pptx,.txt"
          onChange={(e) => setFile(e.target.files[0] ?? null)}
        />
        <button type="submit" disabled={!file || loading}>
          {loading ? 'Uploading...' : 'Upload'}
        </button>
      </form>
      {error && <p className="error">{error}</p>}
      {documentId && (
        <p className="success">
          Document ID: <code>{documentId}</code>
          {numChunks !== null && ` (${numChunks} chunks)`}
        </p>
      )}
    </div>
  )
}

export default UploadView
