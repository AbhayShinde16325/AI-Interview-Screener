import { useNavigate } from 'react-router-dom'

import Button from '../../components/ui/Button'
import { useAuthStore } from '../../store/authStore'

export default function Settings() {
  const user = useAuthStore((state) => state.user)
  const logout = useAuthStore((state) => state.logout)
  const navigate = useNavigate()

  const handleLogout = () => {
    logout()
    navigate('/login')
  }

  const initials =
    (user?.full_name || '')
      .split(' ')
      .filter(Boolean)
      .slice(0, 2)
      .map((p) => p[0]?.toUpperCase())
      .join('') || 'U'

  return (
    <div className="mx-auto max-w-2xl space-y-8">
      <header>
        <h1 className="text-2xl font-semibold tracking-tight text-ink-900">Settings</h1>
        <p className="mt-1 text-sm text-ink-500">Your account details.</p>
      </header>

      <section className="rounded-lg border border-ink-200 bg-white p-6 shadow-card">
        <div className="flex items-center gap-4">
          <span className="flex h-14 w-14 shrink-0 items-center justify-center rounded-full bg-ink-900 text-lg font-semibold text-white">
            {initials}
          </span>
          <div className="min-w-0">
            <p className="font-semibold text-ink-900">{user?.full_name || 'Candidate'}</p>
            <p className="truncate text-sm text-ink-500">{user?.email}</p>
          </div>
        </div>

        <dl className="mt-6 divide-y divide-ink-100 border-t border-ink-100 text-sm">
          <div className="flex items-center justify-between py-3">
            <dt className="text-ink-500">Member since</dt>
            <dd className="font-medium text-ink-900">
              {user?.created_at
                ? new Date(user.created_at).toLocaleDateString('en-US', {
                    month: 'long',
                    day: 'numeric',
                    year: 'numeric',
                  })
                : '—'}
            </dd>
          </div>
          <div className="flex items-center justify-between py-3">
            <dt className="text-ink-500">Session</dt>
            <dd className="font-medium text-ink-900">Signed in</dd>
          </div>
        </dl>

        <div className="mt-6 flex justify-end border-t border-ink-100 pt-5">
          <Button variant="secondary" onClick={handleLogout}>
            Sign out
          </Button>
        </div>
      </section>

      <p className="text-[13px] text-ink-400">
        Profile editing is coming soon. Your account details are managed through the
        authentication service.
      </p>
    </div>
  )
}
