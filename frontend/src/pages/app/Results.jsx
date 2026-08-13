import { useEffect, useState } from 'react'
import { Link, useLocation, useParams } from 'react-router-dom'

import Badge from '../../components/ui/Badge'
import Button from '../../components/ui/Button'
import Skeleton from '../../components/ui/Skeleton'
import Alert from '../../components/ui/Alert'
import { getInterviewQuestions, getResult } from '../../services/interviews'
import { friendlyError } from '../../utils/errors'

const RECOMMENDATION_TONE = {
  'Strong Hire': 'green',
  Hire: 'green',
  Borderline: 'amber',
  'No Hire': 'red',
}

function scoreTone(score) {
  if (score >= 70) return 'text-emerald-600'
  if (score >= 50) return 'text-amber-600'
  return 'text-red-600'
}

function scoreBadge(score) {
  if (score >= 7) return 'green'
  if (score >= 4) return 'amber'
  return 'red'
}

export default function Results() {
  const { id } = useParams()
  const location = useLocation()

  const [result, setResult] = useState(location.state?.result || null)
  const [questions, setQuestions] = useState([])
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(!result)

  useEffect(() => {
    if (result) {
      getInterviewQuestions(id)
        .then((res) => setQuestions(res.data.questions))
        .catch(() => {})
      return
    }

    Promise.all([getResult(id), getInterviewQuestions(id)])
      .then(([res, qs]) => {
        setResult(res.data)
        setQuestions(qs.data.questions)
      })
      .catch((err) => setError(friendlyError(err, 'Failed to load the evaluation.')))
      .finally(() => setLoading(false))
  }, [id, result])

  if (loading) {
    return (
      <div className="mx-auto max-w-3xl space-y-6">
        <Skeleton className="mx-auto h-8 w-56" />
        <Skeleton className="h-56 w-full" />
        <Skeleton className="h-64 w-full" />
      </div>
    )
  }

  if (!result) {
    return (
      <div className="mx-auto max-w-2xl space-y-4">
        <Alert>{error}</Alert>
        <Link to="/app/dashboard" className="inline-block text-sm font-medium text-brand-700 hover:text-brand-800">
          ← Back to dashboard
        </Link>
      </div>
    )
  }

  const byOrder = Object.fromEntries(questions.map((q) => [q.question_order, q]))

  return (
    <div className="mx-auto max-w-3xl space-y-8">
      <header className="text-center">
        <h1 className="text-2xl font-semibold tracking-tight text-ink-900">Interview results</h1>
        <p className="mt-1 text-sm text-ink-500">
          Your detailed evaluation is ready.
        </p>
      </header>

      {/* Score summary */}
      <section className="rounded-lg border border-ink-200 bg-white p-8 shadow-card">
        <div className="flex flex-col items-center gap-6 md:flex-row md:justify-between">
          <div className="flex items-center gap-5">
            <div className="flex h-24 w-24 flex-col items-center justify-center rounded-full border-4 border-ink-100">
              <span className={`text-3xl font-semibold ${scoreTone(result.overall_score)}`}>
                {result.overall_score}
              </span>
              <span className="text-xs text-ink-400">/ 100</span>
            </div>
            <div className="text-left">
              <p className="text-sm text-ink-500">Overall score</p>
              <Badge
                tone={RECOMMENDATION_TONE[result.recommendation] || 'neutral'}
                className="mt-2 px-3 py-1"
              >
                {result.recommendation}
              </Badge>
            </div>
          </div>
        </div>

        <p className="mt-6 border-t border-ink-100 pt-6 text-sm leading-relaxed text-ink-600">
          {result.summary}
        </p>

        <div className="mt-8 grid gap-8 md:grid-cols-2">
          <div>
            <h3 className="text-sm font-semibold text-emerald-700">Strengths</h3>
            <ul className="mt-3 space-y-2.5">
              {result.strengths.map((item, i) => (
                <li key={i} className="flex gap-2.5 text-sm leading-relaxed text-ink-600">
                  <span className="mt-0.5 text-emerald-500" aria-hidden="true">✓</span>
                  {item}
                </li>
              ))}
            </ul>
          </div>
          <div>
            <h3 className="text-sm font-semibold text-amber-700">Areas to improve</h3>
            <ul className="mt-3 space-y-2.5">
              {result.improvements.map((item, i) => (
                <li key={i} className="flex gap-2.5 text-sm leading-relaxed text-ink-600">
                  <span className="mt-0.5 text-amber-500" aria-hidden="true">→</span>
                  {item}
                </li>
              ))}
            </ul>
          </div>
        </div>
      </section>

      {/* Question review */}
      <section>
        <h2 className="mb-3 text-sm font-semibold uppercase tracking-wide text-ink-500">
          Question review
        </h2>
        <div className="space-y-3">
          {(result.question_evaluations || []).map((qe) => {
            const q = byOrder[qe.question_order]
            return (
              <div key={qe.question_order} className="rounded-lg border border-ink-200 bg-white p-5 shadow-card">
                <div className="flex items-start justify-between gap-4">
                  <div className="min-w-0">
                    <p className="text-[13px] text-ink-500">
                      Question {qe.question_order}
                      {q ? ` · ${q.skill}` : ''}
                    </p>
                    <p className="mt-1 font-medium leading-relaxed text-ink-900">
                      {q ? q.question : `Question ${qe.question_order}`}
                    </p>
                  </div>
                  <Badge tone={scoreBadge(qe.score)} className="shrink-0 px-3 py-1 text-[13px] font-semibold">
                    {qe.score}/10
                  </Badge>
                </div>
                {qe.feedback && (
                  <p className="mt-3 border-t border-ink-100 pt-3 text-sm leading-relaxed text-ink-600">
                    {qe.feedback}
                  </p>
                )}
              </div>
            )
          })}
        </div>
      </section>

      <div className="flex justify-center gap-3 pb-4">
        <Link to="/app/interviews">
          <Button variant="secondary">All interviews</Button>
        </Link>
        <Link to="/app/dashboard">
          <Button>Back to dashboard</Button>
        </Link>
      </div>
    </div>
  )
}
