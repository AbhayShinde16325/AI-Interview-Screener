import { Link } from 'react-router-dom'

import Logo from '../components/ui/Logo'
import Button from '../components/ui/Button'
import { useAuthStore } from '../store/authStore'

function SiteHeader() {
  const token = useAuthStore((state) => state.token)

  return (
    <header className="sticky top-0 z-40 border-b border-ink-200 bg-white/90 backdrop-blur-sm">
      <div className="mx-auto flex h-16 max-w-page items-center justify-between px-4 sm:px-6">
        <Link to="/" aria-label="InterviewDesk home" className="focus-ring rounded-md">
          <Logo />
        </Link>

        <nav className="hidden items-center gap-1 md:flex" aria-label="Main">
          <a href="#how-it-works" className="focus-ring rounded-md px-3 py-2 text-sm font-medium text-ink-600 hover:text-ink-900">
            How it works
          </a>
          <a href="#preview" className="focus-ring rounded-md px-3 py-2 text-sm font-medium text-ink-600 hover:text-ink-900">
            The interview
          </a>
        </nav>

        <div className="flex items-center gap-2">
          {token ? (
            <Link to="/app/dashboard">
              <Button size="sm" variant="secondary">
                Go to dashboard
              </Button>
            </Link>
          ) : (
            <>
              <Link to="/login" className="focus-ring rounded-md px-3 py-2 text-sm font-medium text-ink-700 hover:text-ink-900">
                Sign in
              </Link>
              <Link to="/register">
                <Button size="sm">Get started</Button>
              </Link>
            </>
          )}
        </div>
      </div>
    </header>
  )
}

function InterviewPreview() {
  return (
    <div id="preview" className="overflow-hidden rounded-xl border border-ink-200 bg-white shadow-card">
      {/* Window chrome */}
      <div className="flex items-center gap-1.5 border-b border-ink-200 bg-ink-50 px-4 py-2.5">
        <span className="h-2.5 w-2.5 rounded-full bg-ink-300" />
        <span className="h-2.5 w-2.5 rounded-full bg-ink-300" />
        <span className="h-2.5 w-2.5 rounded-full bg-ink-300" />
        <span className="ml-3 text-xs font-medium text-ink-500">
          interview.interviewdesk.app
        </span>
      </div>

      <div className="p-5 sm:p-6">
        {/* Mock interview top bar */}
        <div className="flex items-center justify-between border-b border-ink-200 pb-4">
          <div className="flex items-center gap-2">
            <span className="inline-flex h-6 w-6 items-center justify-center rounded bg-brand-600 text-[10px] font-bold text-white">
              ID
            </span>
            <span className="text-sm font-semibold text-ink-900">AI/ML Engineer</span>
          </div>
          <span className="text-xs font-medium text-ink-500">Question 3 of 10</span>
        </div>

        {/* Progress */}
        <div className="mt-4 h-1.5 w-full overflow-hidden rounded-full bg-ink-100">
          <div className="h-full w-[30%] rounded-full bg-brand-600" />
        </div>

        {/* Question */}
        <div className="mt-5">
          <div className="flex items-center gap-2">
            <span className="rounded-full bg-brand-50 px-2 py-0.5 text-[11px] font-medium text-brand-800">
              Python
            </span>
            <span className="rounded-full bg-ink-100 px-2 py-0.5 text-[11px] font-medium text-ink-600">
              Medium
            </span>
          </div>
          <p className="mt-3 text-[15px] font-medium leading-relaxed text-ink-900">
            How would you design a system that serves personalized recommendations at scale?
          </p>
        </div>

        {/* Mock answer area */}
        <div className="mt-4 space-y-2 rounded-lg border border-ink-200 bg-ink-50/60 p-4">
          <div className="h-2 w-full rounded bg-ink-200/70" />
          <div className="h-2 w-11/12 rounded bg-ink-200/70" />
          <div className="h-2 w-4/5 rounded bg-ink-200/70" />
          <div className="h-2 w-2/3 rounded bg-ink-200/70" />
        </div>

        <div className="mt-4 flex justify-end">
          <span className="inline-flex h-8 items-center rounded-lg bg-brand-600 px-4 text-xs font-semibold text-white">
            Submit answer
          </span>
        </div>
      </div>
    </div>
  )
}

function HowItWorks() {
  const steps = [
    {
      num: '01',
      title: 'Upload your resume',
      body: 'Your experience becomes the foundation of the interview. Skills, projects, and background are parsed automatically.',
    },
    {
      num: '02',
      title: 'Choose your role',
      body: 'The interview adapts to the role you are targeting, drawing on role-specific technical knowledge.',
    },
    {
      num: '03',
      title: 'Take the interview',
      body: 'Answer technical questions generated around your actual background — not generic question banks.',
    },
    {
      num: '04',
      title: 'Understand your performance',
      body: 'Get a structured evaluation with per-question feedback and a clear hiring recommendation.',
    },
  ]

  return (
    <section id="how-it-works" className="border-t border-ink-200 bg-white">
      <div className="mx-auto max-w-page px-4 py-20 sm:px-6">
        <p className="text-[13px] font-semibold uppercase tracking-wide text-brand-700">
          How it works
        </p>
        <h2 className="mt-3 max-w-2xl text-3xl font-semibold tracking-tight text-ink-900">
          Four steps from resume to interview.
        </h2>

        <div className="mt-12 grid gap-10 sm:grid-cols-2 lg:grid-cols-4">
          {steps.map((step) => (
            <div key={step.num} className="border-t-2 border-ink-200 pt-5">
              <span className="text-sm font-semibold text-brand-600">{step.num}</span>
              <h3 className="mt-2 text-[15px] font-semibold text-ink-900">{step.title}</h3>
              <p className="mt-2 text-sm leading-relaxed text-ink-500">{step.body}</p>
            </div>
          ))}
        </div>
      </div>
    </section>
  )
}

function SiteFooter() {
  return (
    <footer className="border-t border-ink-200 bg-ink-50/60">
      <div className="mx-auto flex max-w-page flex-col items-start justify-between gap-4 px-4 py-8 sm:flex-row sm:items-center sm:px-6">
        <Logo size="sm" />
        <p className="text-xs text-ink-500">
          Practice interviews built around your experience. ·{' '}
          <span className="text-ink-400">AI Interview Screener</span>
        </p>
      </div>
    </footer>
  )
}

export default function Landing() {
  const token = useAuthStore((state) => state.token)

  return (
    <div className="min-h-screen bg-white">
      <SiteHeader />

      <main>
        {/* Hero */}
        <section className="border-b border-ink-200 bg-[#fafbfc]">
          <div className="mx-auto grid max-w-page items-center gap-12 px-4 py-16 sm:px-6 lg:grid-cols-2 lg:py-24">
            <div>
              <p className="inline-flex items-center gap-2 rounded-full border border-brand-200 bg-brand-50 px-3 py-1 text-[13px] font-medium text-brand-800">
                AI-powered technical interviewing
              </p>
              <h1 className="mt-5 text-4xl font-semibold leading-[1.15] tracking-tight text-ink-900 sm:text-[44px]">
                Practice interviews built around your experience.
              </h1>
              <p className="mt-5 max-w-xl text-base leading-relaxed text-ink-500">
                Upload your resume, choose your target role, and take a technical
                interview generated around your actual skills, projects, and
                experience.
              </p>

              <div className="mt-8 flex flex-wrap items-center gap-3">
                <Link to={token ? '/app/dashboard' : '/register'}>
                  <Button size="lg">Start an interview</Button>
                </Link>
                <a href="#how-it-works">
                  <Button size="lg" variant="secondary">
                    See how it works
                  </Button>
                </a>
              </div>

              <dl className="mt-10 grid max-w-md grid-cols-3 gap-6 border-t border-ink-200 pt-6">
                <div>
                  <dt className="text-2xl font-semibold text-ink-900">100%</dt>
                  <dd className="mt-1 text-[13px] text-ink-500">Personalized per resume</dd>
                </div>
                <div>
                  <dt className="text-2xl font-semibold text-ink-900">~10</dt>
                  <dd className="mt-1 text-[13px] text-ink-500">Technical questions</dd>
                </div>
                <div>
                  <dt className="text-2xl font-semibold text-ink-900">RAG</dt>
                  <dd className="mt-1 text-[13px] text-ink-500">Grounded in real knowledge</dd>
                </div>
              </dl>
            </div>

            <InterviewPreview />
          </div>
        </section>

        <HowItWorks />
      </main>

      <SiteFooter />
    </div>
  )
}
