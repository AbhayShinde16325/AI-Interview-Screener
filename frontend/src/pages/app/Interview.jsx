import { useEffect, useMemo, useState } from 'react'
import { Link, useNavigate, useParams } from 'react-router-dom'

import Badge from '../../components/ui/Badge'
import Button from '../../components/ui/Button'
import Skeleton from '../../components/ui/Skeleton'
import Alert from '../../components/ui/Alert'
import InterviewProgress from '../../components/interview/InterviewProgress'
import InterviewExitModal from '../../components/interview/InterviewExitModal'
import Logo from '../../components/ui/Logo'
import { completeInterview, getInterviewQuestions, submitAnswer } from '../../services/interviews'
import { friendlyError } from '../../utils/errors'

const DIFFICULTY_TONE = {
  Easy: 'green',
  Medium: 'amber',
  Hard: 'red',
}

function QuestionSkeleton() {
  return (
    <div className="space-y-4">
      <div className="flex gap-2">
        <Skeleton className="h-6 w-20 rounded-full" />
        <Skeleton className="h-6 w-16 rounded-full" />
      </div>
      <Skeleton className="h-4 w-full" />
      <Skeleton className="h-4 w-11/12" />
      <Skeleton className="h-4 w-4/5" />
      <div className="space-y-2.5 pt-2">
        <Skeleton className="h-32 w-full rounded-lg" />
      </div>
    </div>
  )
}

function CompletionScreen({ interview, total, onViewResults, evaluating, error }) {
  return (
    <div className="flex flex-col items-center py-14 text-center">
      <span className="flex h-14 w-14 items-center justify-center rounded-full bg-emerald-50 text-emerald-600">
        <svg className="h-7 w-7" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
          <path d="M20 6 9 17l-5-5" />
        </svg>
      </span>
      <h1 className="mt-5 text-2xl font-semibold tracking-tight text-ink-900">Interview completed</h1>
      <p className="mt-2 max-w-md text-sm text-ink-500">
        You've answered all {total} questions{interview ? ` for the ${interview} interview` : ''}. Nice work.
      </p>

      {error && <Alert className="mt-6 w-full max-w-md">{error}</Alert>}

      <div className="mt-8 flex flex-col items-center gap-3 sm:flex-row">
        <Button size="lg" onClick={onViewResults} loading={evaluating} loadingText="Evaluating your answers…">
          View results
        </Button>
        <Link to="/app/dashboard">
          <Button size="lg" variant="secondary">
            Back to dashboard
          </Button>
        </Link>
      </div>
    </div>
  )
}

export default function Interview() {
  const { id } = useParams()
  const navigate = useNavigate()

  const [questions, setQuestions] = useState([])
  const [current, setCurrent] = useState(0)
  const [answer, setAnswer] = useState('')
  const [saving, setSaving] = useState(false)
  const [evaluating, setEvaluating] = useState(false)
  const [completed, setCompleted] = useState(false)
  const [exitOpen, setExitOpen] = useState(false)
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(true)
  const [role, setRole] = useState('')

  useEffect(() => {
    getInterviewQuestions(id)
      .then((res) => {
        // Preserve the question order returned by the backend.
        setQuestions(res.data.questions)
        setRole(res.data.role || '')
      })
      .catch((err) => setError(friendlyError(err, 'Failed to load your interview.')))
      .finally(() => setLoading(false))
  }, [id])

  const ordered = useMemo(
    () => [...questions].sort((a, b) => a.question_order - b.question_order),
    [questions],
  )

  const total = ordered.length
  const question = ordered[current]
  const isLast = current === total - 1
  const isMcq =
    !!question &&
    (question.question_type === 'MCQ' || (question.options?.length ?? 0) > 0)

  const handleSubmit = async () => {
    if (!answer.trim()) {
      setError(
        isMcq
          ? 'Please select an answer before continuing.'
          : 'Please write an answer before continuing.',
      )
      return
    }
    if (!question) return

    setError('')
    setSaving(true)
    try {
      await submitAnswer(id, question.id, answer)
      if (isLast) {
        setCompleted(true)
      } else {
        setAnswer('')
        setCurrent((c) => c + 1)
      }
    } catch (err) {
      setError(friendlyError(err, 'Failed to save your answer. Please try again.'))
    } finally {
      setSaving(false)
    }
  }

  const handleViewResults = async () => {
    setEvaluating(true)
    setError('')
    try {
      const { data } = await completeInterview(id)
      navigate(`/app/interviews/${id}/results`, { state: { result: data } })
    } catch (err) {
      setError(friendlyError(err, 'Evaluation is temporarily unavailable. Please try again later.'))
    } finally {
      setEvaluating(false)
    }
  }

  if (loading) {
    return (
      <div className="flex min-h-screen flex-col">
        <TopBar onLeave={() => navigate('/app/dashboard')} label="" role="" />
        <div className="mx-auto w-full max-w-3xl flex-1 px-4 py-8 sm:px-6">
          <Skeleton className="h-2 w-full rounded-full" />
          <div className="mt-8">
            <QuestionSkeleton />
          </div>
        </div>
      </div>
    )
  }

  if (error && total === 0) {
    return (
      <div className="flex min-h-screen flex-col items-center justify-center px-4">
        <Alert className="max-w-md">{error}</Alert>
        <Link to="/app/dashboard" className="mt-4 text-sm font-medium text-brand-700 hover:text-brand-800">
          ← Back to dashboard
        </Link>
      </div>
    )
  }

  return (
    <div className="flex min-h-screen flex-col bg-white">
      <TopBar
        onLeave={() => setExitOpen(true)}
        label={completed ? 'Finished' : `${current + 1} of ${total}`}
        role={role}
      />

      <main className="mx-auto w-full max-w-3xl flex-1 px-4 py-8 sm:px-6">
        {completed ? (
          <CompletionScreen
            interview={role}
            total={total}
            onViewResults={handleViewResults}
            evaluating={evaluating}
            error={error}
          />
        ) : (
          <div className="space-y-6">
            <InterviewProgress current={current} total={total} />

            {error && <Alert>{error}</Alert>}

            <section className="rounded-lg border border-ink-200 bg-white p-6 shadow-card sm:p-8">
              <div className="flex flex-wrap items-center gap-2">
                <Badge tone="blue">{question.skill}</Badge>
                <Badge tone={DIFFICULTY_TONE[question.difficulty] || 'neutral'}>
                  {question.difficulty}
                </Badge>
                <Badge tone="neutral">{question.question_type}</Badge>
              </div>

              <h2 className="mt-5 text-lg font-medium leading-relaxed text-ink-900 sm:text-xl">
                {question.question}
              </h2>

              {question.expected_topics?.length > 0 && (
                <div className="mt-5">
                  <p className="text-xs font-semibold uppercase tracking-wide text-ink-400">
                    Topics to cover
                  </p>
                  <div className="mt-2 flex flex-wrap gap-1.5">
                    {question.expected_topics.map((topic) => (
                      <Badge key={topic} tone="gray" className="px-2 py-0.5">
                        {topic}
                      </Badge>
                    ))}
                  </div>
                </div>
              )}

              <div className="mt-7">
                {isMcq ? (
                  <fieldset>
                    <legend className="text-sm font-medium text-ink-800">
                      Choose the best answer
                    </legend>
                    <div className="mt-2 space-y-2.5">
                      {question.options.map((option) => {
                        const selected = answer === option
                        return (
                          <label
                            key={option}
                            className={`flex cursor-pointer items-start gap-3 rounded-lg border px-3.5 py-3 transition-colors ${
                              selected
                                ? 'border-brand-500 bg-brand-50/60 ring-1 ring-brand-500/30'
                                : 'border-ink-300 bg-white hover:border-ink-400'
                            }`}
                          >
                            <input
                              type="radio"
                              name="answer"
                              value={option}
                              checked={selected}
                              onChange={() => setAnswer(option)}
                              className="mt-0.5 h-4 w-4 shrink-0 accent-brand-600"
                            />
                            <span className="text-[15px] leading-relaxed text-ink-900">
                              {option}
                            </span>
                          </label>
                        )
                      })}
                    </div>
                  </fieldset>
                ) : (
                  <>
                    <label htmlFor="answer" className="text-sm font-medium text-ink-800">
                      Your answer
                    </label>
                    <textarea
                      id="answer"
                      value={answer}
                      onChange={(e) => setAnswer(e.target.value)}
                      rows={8}
                      placeholder="Write your answer here…"
                      className="mt-2 w-full rounded-lg border border-ink-300 bg-white px-3.5 py-3 text-[15px] leading-relaxed text-ink-900 placeholder:text-ink-400 transition-colors focus:outline-none focus:ring-2 focus:ring-brand-600/20 focus:border-brand-500"
                    />
                  </>
                )}

                <div className="mt-5 flex flex-col-reverse items-stretch gap-3 sm:flex-row sm:items-center sm:justify-between">
                  <button
                    type="button"
                    onClick={() => setExitOpen(true)}
                    className="inline-flex h-10 items-center justify-center rounded-lg px-3 text-sm font-medium text-ink-500 transition-colors hover:text-ink-800 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-brand-600/40"
                  >
                    Leave interview
                  </button>
                  <Button
                    onClick={handleSubmit}
                    loading={saving}
                    loadingText={isLast ? 'Finishing…' : 'Saving…'}
                    className="sm:min-w-40"
                  >
                    {isLast ? 'Submit & finish' : 'Submit answer'}
                  </Button>
                </div>
              </div>
            </section>
          </div>
        )}
      </main>

      <InterviewExitModal
        open={exitOpen}
        onContinue={() => setExitOpen(false)}
        onLeave={() => navigate('/app/dashboard')}
      />
    </div>
  )
}

function TopBar({ onLeave, label, role }) {
  return (
    <header className="sticky top-0 z-30 border-b border-ink-200 bg-white/95 backdrop-blur-sm">
      <div className="mx-auto flex h-16 max-w-5xl items-center justify-between px-4 sm:px-6">
        <Link to="/app/dashboard" aria-label="Back to dashboard" className="focus-ring rounded-md">
          <Logo size="sm" wordmark={false} />
        </Link>

        <div className="flex items-center gap-3">
          <span className="text-sm font-semibold text-ink-900">{role || 'Interview'}</span>
          <span className="hidden text-[13px] text-ink-500 sm:inline">· {label}</span>
        </div>

        <button
          onClick={onLeave}
          className="rounded-lg px-3 py-2 text-sm font-medium text-ink-500 transition-colors hover:bg-ink-50 hover:text-ink-800 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-brand-600/40"
        >
          Leave
        </button>
      </div>
    </header>
  )
}
