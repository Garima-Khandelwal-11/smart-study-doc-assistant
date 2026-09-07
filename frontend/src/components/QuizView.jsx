import { useState } from 'react'
import { generateQuiz } from '../api'

function QuizView({ documentId }) {
  const [quiz, setQuiz] = useState(null)
  const [answers, setAnswers] = useState({})
  const [score, setScore] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  async function handleGenerate() {
    setLoading(true)
    setError(null)
    setScore(null)
    setAnswers({})
    try {
      const result = await generateQuiz(documentId)
      setQuiz(result.quiz)
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  function selectAnswer(questionIndex, option) {
    if (score !== null) return
    setAnswers((prev) => ({ ...prev, [questionIndex]: option }))
  }

  function handleSubmit() {
    if (!quiz) return
    const correctCount = quiz.reduce(
      (count, q, i) => (answers[i] === q.correct_answer ? count + 1 : count),
      0,
    )
    setScore(correctCount)
  }

  if (!documentId) {
    return (
      <div className="view">
        <h2>Quiz</h2>
        <p>Upload a document first.</p>
      </div>
    )
  }

  return (
    <div className="view">
      <h2>Quiz</h2>
      <button onClick={handleGenerate} disabled={loading}>
        {loading ? 'Generating...' : 'Generate quiz'}
      </button>
      {error && <p className="error">{error}</p>}
      {quiz && (
        <>
          <ol className="quiz-list">
            {quiz.map((q, qi) => (
              <li key={qi}>
                <p className="quiz-question">{q.question}</p>
                <ul className="quiz-options">
                  {q.options.map((option, oi) => {
                    const isSelected = answers[qi] === option
                    const showResult = score !== null
                    const isCorrect = option === q.correct_answer
                    let className = 'quiz-option'
                    if (isSelected) className += ' selected'
                    if (showResult && isCorrect) className += ' correct'
                    if (showResult && isSelected && !isCorrect) className += ' incorrect'
                    return (
                      <li key={oi}>
                        <label className={className}>
                          <input
                            type="radio"
                            name={`question-${qi}`}
                            checked={isSelected}
                            disabled={score !== null}
                            onChange={() => selectAnswer(qi, option)}
                          />
                          {option}
                        </label>
                      </li>
                    )
                  })}
                </ul>
              </li>
            ))}
          </ol>
          {score === null ? (
            <button
              onClick={handleSubmit}
              disabled={Object.keys(answers).length !== quiz.length}
            >
              Submit
            </button>
          ) : (
            <p className="score">
              Score: {score} / {quiz.length}
            </p>
          )}
        </>
      )}
    </div>
  )
}

export default QuizView
