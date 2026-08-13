import { useCallback, useEffect, useState } from 'react'
import { Link } from 'react-router-dom'

import InterviewTable from '../../components/dashboard/InterviewTable'
import Button from '../../components/ui/Button'
import Skeleton from '../../components/ui/Skeleton'
import Alert from '../../components/ui/Alert'
import EmptyState from '../../components/ui/EmptyState'
import { getLatestResume } from '../../services/resumes'
import { listInterviews } from '../../services/interviews'
import { useAuthStore } from '../../store/authStore'
import { friendlyError } from '../../utils/errors'

function greeting() {
  const hour = new Date().getHours()
  if (hour < 12) return 'Good morning'
  if (hour < 17) return 'Good afternoon'
  return 'Good evening'
}

function StartInterviewCard() {
  return (
    <section className="flex flex-col items-start justify-between gap-4 rounded-lg border border-ink-200 bg-white p-6 shadow-card sm:flex-row sm:items-center">
      <div>
        <h2 className="text-lg font-semibold tracking-tight text-ink-900">Start a new interview</h2>
        <p className="mt-1 max-w-md text-sm text-ink-500">
          Choose a target role and we'll build an interview around your resume.
        </p>
      </div>
      <Link to="/app/interviews/new">
        <Button size="lg">Start interview</Button>
      </Link>
    </section>
  )
}

function ResumeStatus({ resume, loading }) {
  if (loading) {
    return (
      <div className="rounded-lg border border-ink-200 bg-white p-6 shadow-card">
        <Skeleton className="h-4 w-32" />
        <Skeleton className="mt-3 h-3.5 w-56" />
        <Skeleton className="mt-5 h-8 w-28" />
      </div>
    )
  }

  if (!resume) {
    return (
      <EmptyState
        title="No resume yet"
        description="Upload your resume to create a personalized interview."
        action={
          <Link to="/app/resume">
            <Button>Upload resume</Button>
          </Link>
        }
      />
    )
  }

  return (
    <section className="flex flex-col items-start justify-between gap-4 rounded-lg border border-ink-200 bg-white p-6 shadow-card sm:flex-row sm:items-center">
      <div className="min-w-0">
        <div className="flex items-center gap-2">
          <svg className="h-4 w-4 text-ink-400" viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
            <path d="M6 2a2 2 0 00-2 2v12a2 2 0 002 2h8a2 2 0 002-2V7.414A2 2 0 0015.414 6L12 2.586A2 2 0 0010.586 2H6z" />
            <path d="M11 2.5V6a1 1 0 001 1h3.5L11 2.5z" />
          </svg>
          <h3 className="truncate font-medium text-ink-900">{resume.filename}</h3>
        </div>
        <p className="mt-1.5 text-sm text-ink-500">
          Uploaded {new Date(resume.created_at).toLocaleDateString()} ·{' '}
          {resume.skills.length} skills detected
        </p>
        {resume.summary && (
          <p className="mt-2 line-clamp-2 max-w-lg text-sm text-ink-600">{resume.summary}</p>
        )}
      </div>
      <Link to="/app/resume" className="shrink-0">
        <Button variant="secondary">View resume</Button>
      </Link>
    </section>
  )
}

export default function Dashboard() {
  const user = useAuthStore((state) => state.user)
  const [resume, setResume] = useState(null)
  const [resumeMissing, setResumeMissing] = useState(false)
  const [interviews, setInterviews] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  const load = useCallback(async () => {
    setLoading(true)
    setError('')
    try {
      try {
        const res = await getLatestResume()
        setResume(res.data)
      } catch (err) {
        if (err.response?.status === 404) {
          setResumeMissing(true)
        } else {
          throw err
        }
      }

      const interviewsRes = await listInterviews()
      setInterviews(interviewsRes.data.interviews)
    } catch (err) {
      setError(friendlyError(err, 'Failed to load your dashboard.'))
    } finally {
      setLoading(false)
    }
  }, [])

  useEffect(() => {
    load()
  }, [load])

  const firstName = user?.full_name?.split(' ')[0] || 'there'

  return (
    <div className="space-y-8">
      <header>
        <h1 className="text-2xl font-semibold tracking-tight text-ink-900">
          {greeting()}, {firstName}
        </h1>
        <p className="mt-1 text-sm text-ink-500">Prepare for your next technical interview.</p>
      </header>

      {error && <Alert>{error}</Alert>}

      <StartInterviewCard />

      <section>
        <div className="mb-3 flex items-center justify-between">
          <h2 className="text-sm font-semibold uppercase tracking-wide text-ink-500">
            Your resume
          </h2>
        </div>
        <ResumeStatus resume={resumeMissing ? null : resume} loading={loading} />
      </section>

      <section>
        <div className="mb-3 flex items-center justify-between">
          <h2 className="text-sm font-semibold uppercase tracking-wide text-ink-500">
            Recent interviews
          </h2>
          {interviews.length > 0 && (
            <Link
              to="/app/interviews"
              className="text-sm font-semibold text-brand-700 hover:text-brand-800"
            >
              View all
            </Link>
          )}
        </div>

        <InterviewTable
          interviews={interviews.slice(0, 5)}
          loading={loading}
          emptyState={
            <EmptyState
              title="No interviews yet"
              description="Your completed and in-progress interviews will appear here."
              action={
                <Link to="/app/interviews/new">
                  <Button variant="secondary">Start your first interview</Button>
                </Link>
              }
            />
          }
        />
      </section>
    </div>
  )
}
