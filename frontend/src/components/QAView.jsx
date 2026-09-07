import { useState } from 'react'
import { askQuestion } from '../api'

function QAView({ documentId }) {
  const [question, setQuestion] = useState('')
  const [history, setHistory] = useState([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  async function handleAsk(e) {
    e.preventDefault()
    if (!question.trim()) return
    setLoading(true)
    setError(null)
    try {
      const result = await askQuestion(documentId, question)
      setHistory((prev) => [...prev, { question, answer: result.answer }])
      setQuestion('')
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  if (!documentId) {
    return (
      <div className="view">
        <h2>Ask a question</h2>
        <p>Upload a document first.</p>
      </div>
    )
  }

  return (
    <div className="view">
      <h2>Ask a question</h2>
      <form onSubmit={handleAsk}>
        <input
          type="text"
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
          placeholder="Ask something about the document..."
        />
        <button type="submit" disabled={loading || !question.trim()}>
          {loading ? 'Thinking...' : 'Ask'}
        </button>
      </form>
      <p className="hint">Try: &quot;What&apos;s the difference between X and Y?&quot;</p>
      {error && <p className="error">{error}</p>}
      <ul className="qa-history">
        {history
          .slice()
          .reverse()
          .map((item, i) => (
            <li key={i}>
              <p className="qa-question">Q: {item.question}</p>
              <p className="qa-answer">A: {item.answer}</p>
            </li>
          ))}
      </ul>
    </div>
  )
}

export default QAView
