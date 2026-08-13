import Logo from '../ui/Logo'

export default function AuthLayout({ children }) {
  return (
    <div className="flex min-h-screen bg-white">
      {/* Brand panel (desktop) */}
      <aside className="relative hidden w-[44%] shrink-0 flex-col justify-between overflow-hidden bg-ink-900 p-10 lg:flex">
        <div className="absolute -right-24 -top-24 h-72 w-72 rounded-full bg-brand-700/20 blur-3xl" aria-hidden="true" />
        <div className="absolute -bottom-32 -left-20 h-80 w-80 rounded-full bg-brand-600/10 blur-3xl" aria-hidden="true" />

        <Logo dark />

        <div className="relative">
          <h2 className="max-w-sm text-[28px] font-semibold leading-snug tracking-tight text-white">
            Technical interviews that understand your resume.
          </h2>
          <p className="mt-3 max-w-sm text-sm leading-relaxed text-ink-300">
            Questions generated from your skills and projects, grounded in
            role-specific technical knowledge.
          </p>
        </div>

        {/* Subtle interview preview */}
        <div className="relative rounded-lg border border-white/10 bg-white/[0.04] p-5 backdrop-blur-sm">
          <div className="flex items-center justify-between">
            <span className="text-xs font-medium text-ink-300">Backend Engineer</span>
            <span className="text-[11px] text-ink-400">Question 2 of 10</span>
          </div>
          <div className="mt-3 h-1 rounded-full bg-white/10">
            <div className="h-full w-1/5 rounded-full bg-brand-400" />
          </div>
          <p className="mt-4 text-sm leading-relaxed text-ink-100">
            Explain how you would design a rate limiter for a public API.
          </p>
          <div className="mt-4 space-y-1.5">
            <div className="h-1.5 w-full rounded bg-white/10" />
            <div className="h-1.5 w-4/5 rounded bg-white/10" />
          </div>
        </div>
      </aside>

      {/* Form panel */}
      <main className="flex flex-1 items-center justify-center px-4 py-10 sm:px-6">
        <div className="w-full max-w-md">
          <div className="mb-8 lg:hidden">
            <Logo />
          </div>
          {children}
        </div>
      </main>
    </div>
  )
}
