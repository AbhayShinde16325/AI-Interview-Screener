import { useCallback, useEffect, useState } from 'react'
import { Link } from 'react-router-dom'

import InterviewTable from '../../components/dashboard/InterviewTable'
import Button from '../../components/ui/Button'
import Alert from '../../components/ui/Alert'
import EmptyState from '../../components/ui/EmptyState'
import { listInterviews, getInterviewQuestions } from '../../services/interviews'
import { friendlyError } from '../../utils/errors'

export default function InterviewHistory() {
  const [interviews, setInterviews] = useState([])
  const [questionCounts, setQuestionCounts] = useState({})
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  const load = useCallback(async () => {
    setLoading(true)
    setError('')
    try {
      const res = await listInterviews()
      const items = res.data.interviews
      setInterviews(items)

      // Fetch question counts per interview (not part of the list response).
      const entries = await Promise.all(
        items.map(async (interview) => {
          try {
            const qs = await getInterviewQuestions(interview.id)
            return [interview.id, qs.data.questions.length]
          } catch {
            return [interview.id, null]
          }
        }),
      )
      setQuestionCounts(Object.fromEntries(entries))
    } catch (err) {
      setError(friendlyError(err, 'Failed to load your interviews.'))
    } finally {
      setLoading(false)
    }
  }, [])

  useEffect(() => {
    load()
  }, [load])

  return (
    <div className="space-y-6">
      <header className="flex flex-wrap items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl font-semibold tracking-tight text-ink-900">Interviews</h1>
          <p className="mt-1 text-sm text-ink-500">
            Your completed and in-progress interviews.
          </p>
        </div>
        <Link to="/app/interviews/new">
          <Button>New interview</Button>
        </Link>
      </header>

      {error && <Alert>{error}</Alert>}

      <InterviewTable
        interviews={interviews}
        questionCounts={questionCounts}
        showQuestions
        loading={loading}
        emptyState={
          <EmptyState
            title="No interviews yet"
            description="Your completed and in-progress interviews will appear here."
            action={
              <Link to="/app/interviews/new">
                <Button>Start your first interview</Button>
              </Link>
            }
          />
        }
      />
    </div>
  )
}
