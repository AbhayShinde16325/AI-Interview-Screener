import { useEffect, useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'

import Button from '../../components/ui/Button'
import Select from '../../components/ui/Select'
import Skeleton from '../../components/ui/Skeleton'
import Alert from '../../components/ui/Alert'
import { getLatestResume } from '../../services/resumes'
import { startInterview } from '../../services/interviews'
import { friendlyError } from '../../utils/errors'

const ROLE_OPTIONS = [
  { value: 'AI/ML Engineer', label: 'AI/ML Engineer' },
  { value: 'Data Engineer', label: 'Data Engineer' },
  { value: 'Backend Engineer', label: 'Backend Engineer' },
  { value: 'Python Developer', label: 'Python Developer' },
  { value: 'Full Stack Developer', label: 'Full Stack Developer' },
]

export default function InterviewSetup() {
  const [role, setRole] = useState('AI/ML Engineer')
  const [resume, setResume] = useState(null)
  const [resumeMissing, setResumeMissing] = useState(false)
  const [loading, setLoading] = useState(true)
  const [starting, setStarting] = useState(false)
  const [error, setError] = useState('')

  const navigate = useNavigate()

  useEffect(() => {
    getLatestResume()
      .then((res) => setResume(res.data))
      .catch((err) => {
        if (err.response?.status === 404) setResumeMissing(true)
        else setError(friendlyError(err, 'Failed to load your resume.'))
      })
      .finally(() => setLoading(false))
  }, [])

  const handleStart = async () => {
    setStarting(true)
    setError('')
    try {
      const { data } = await startInterview(role)
      navigate(`/app/interviews/${data.interview_id}`)
    } catch (err) {
      setError(friendlyError(err, 'Something went wrong while starting the interview. Please try again.'))
    } finally {
      setStarting(false)
    }
  }

  if (loading) {
    return (
      <div className="max-w-2xl space-y-6">
        <Skeleton className="h-8 w-56" />
        <Skeleton className="h-40 w-full" />
        <Skeleton className="h-52 w-full" />
      </div>
    )
  }

  return (
    <div className="mx-auto max-w-2xl space-y-8">
      <header>
        <h1 className="text-2xl font-semibold tracking-tight text-ink-900">Set up your interview</h1>
        <p className="mt-1 text-sm text-ink-500">
          Tell us the role you're targeting. The interview is built around your resume.
        </p>
      </header>

      {error && <Alert>{error}</Alert>}

      {resumeMissing && (
        <Alert tone="info" title="Upload a resume first">
          An interview is generated from your resume. Upload a PDF to continue.
          <div className="mt-3">
            <Link to="/app/resume">
              <Button size="sm">Upload resume</Button>
            </Link>
          </div>
        </Alert>
      )}

      {!resumeMissing && (
        <>
          {/* Role */}
          <section className="rounded-lg border border-ink-200 bg-white p-6 shadow-card">
            <label className="text-sm font-medium text-ink-800">
              What role are you preparing for?
            </label>
            <div className="mt-2">
              <Select
                id="role"
                value={role}
                onChange={(e) => setRole(e.target.value)}
                options={ROLE_OPTIONS}
                hint="All roles are supported. Questions adapt to the role and your resume."
              />
            </div>

            <div className="mt-5 border-t border-ink-100 pt-4">
              <p className="text-sm font-medium text-ink-800">Interview based on</p>
              <div className="mt-2 flex items-center justify-between gap-3">
                <div className="flex min-w-0 items-center gap-2">
                  <svg className="h-4 w-4 shrink-0 text-ink-400" viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
                    <path d="M6 2a2 2 0 00-2 2v12a2 2 0 002 2h8a2 2 0 002-2V7.414A2 2 0 0015.414 6L12 2.586A2 2 0 0010.586 2H6z" />
                    <path d="M11 2.5V6a1 1 0 001 1h3.5L11 2.5z" />
                  </svg>
                  <span className="truncate text-sm text-ink-700">{resume?.filename}</span>
                </div>
                <Link
                  to="/app/resume"
                  className="shrink-0 text-sm font-semibold text-brand-700 hover:text-brand-800"
                >
                  Change resume
                </Link>
              </div>
            </div>
          </section>

          {/* Preview */}
          <section className="rounded-lg border border-ink-200 bg-white p-6 shadow-card">
            <h2 className="text-sm font-semibold text-ink-900">Your interview</h2>
            <dl className="mt-4 divide-y divide-ink-100 text-sm">
              <div className="flex items-center justify-between py-3">
                <dt className="text-ink-500">Target role</dt>
                <dd className="font-medium text-ink-900">{role}</dd>
              </div>
              <div className="flex items-center justify-between py-3">
                <dt className="text-ink-500">Resume</dt>
                <dd className="font-medium text-ink-900 capitalize">
                  {resume ? 'Parsed and ready' : 'Missing'}
                </dd>
              </div>
              <div className="flex items-center justify-between py-3">
                <dt className="text-ink-500">Questions</dt>
                <dd className="font-medium text-ink-900">
                  Up to 10, generated from your skills and projects
                </dd>
              </div>
              <div className="flex items-center justify-between py-3">
                <dt className="text-ink-500">Format</dt>
                <dd className="font-medium text-ink-900">Mixed multiple-choice and written answers</dd>
              </div>
            </dl>
          </section>

          <p className="text-sm text-ink-500">
            You'll receive technical questions based on your role, skills, projects, and resume.
          </p>

          <div className="flex flex-col gap-3 sm:flex-row sm:items-center">
            <Button
              size="lg"
              onClick={handleStart}
              disabled={starting}
              loading={starting}
              loadingText="Starting interview…"
            >
              Start interview
            </Button>
            <Link
              to="/app/dashboard"
              className="inline-flex h-11 items-center justify-center px-4 text-sm font-medium text-ink-600 hover:text-ink-900"
            >
              Cancel
            </Link>
          </div>
        </>
      )}
    </div>
  )
}
