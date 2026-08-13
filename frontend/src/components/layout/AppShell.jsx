import { NavLink, Link, Outlet, useNavigate, useLocation } from 'react-router-dom'

import Logo from '../ui/Logo'
import { useAuthStore } from '../../store/authStore'

const NAV_ITEMS = [
  {
    to: '/app/dashboard',
    label: 'Overview',
    icon: (
      <svg viewBox="0 0 20 20" fill="currentColor" className="h-[18px] w-[18px]" aria-hidden="true">
        <path d="M7 3a1 1 0 000 2h6a1 1 0 100-2H7zM4 7a1 1 0 011-1h10a1 1 0 110 2H5a1 1 0 01-1-1zM3 11a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1zM5 15a1 1 0 100 2h10a1 1 0 100-2H5z" />
      </svg>
    ),
  },
  {
    to: '/app/resume',
    label: 'Resume',
    icon: (
      <svg viewBox="0 0 20 20" fill="currentColor" className="h-[18px] w-[18px]" aria-hidden="true">
        <path d="M6 2a2 2 0 00-2 2v12a2 2 0 002 2h8a2 2 0 002-2V7.414A2 2 0 0015.414 6L12 2.586A2 2 0 0010.586 2H6z" />
        <path d="M11 2.5V6a1 1 0 001 1h3.5L11 2.5z" />
        <path d="M7 11a1 1 0 011-1h4a1 1 0 110 2H8a1 1 0 01-1-1zM7 14a1 1 0 011-1h2a1 1 0 110 2H8a1 1 0 01-1-1z" />
      </svg>
    ),
  },
  {
    to: '/app/interviews',
    label: 'Interviews',
    icon: (
      <svg viewBox="0 0 20 20" fill="currentColor" className="h-[18px] w-[18px]" aria-hidden="true">
        <path d="M5 3a2 2 0 00-2 2v9a2 2 0 002 2h1.6l2.28 2.44a1 1 0 001.44 0L12.6 16h2.4a2 2 0 002-2V5a2 2 0 00-2-2H5z" />
        <path d="M6.5 8a.75.75 0 000 1.5h7a.75.75 0 000-1.5h-7zM6.5 11a.75.75 0 000 1.5h4a.75.75 0 000-1.5h-4z" />
      </svg>
    ),
  },
  {
    to: '/app/settings',
    label: 'Settings',
    icon: (
      <svg viewBox="0 0 20 20" fill="currentColor" className="h-[18px] w-[18px]" aria-hidden="true">
        <path d="M11.55 2.5a1.06 1.06 0 011.06-.87h.78a1.06 1.06 0 011.06.87l.28 1.45a1.06 1.06 0 00.61.73l1.37.57a1.06 1.06 0 001.26-.42l.46-.7a1.06 1.06 0 011.5-.25l.6.5a1.06 1.06 0 01.25 1.5l-.7 1.02a1.06 1.06 0 000 1.24l.7 1.02a1.06 1.06 0 01-.25 1.5l-.6.5a1.06 1.06 0 01-1.5-.25l-.46-.7a1.06 1.06 0 00-1.26-.42l-1.37.57a1.06 1.06 0 00-.61.73l-.28 1.45a1.06 1.06 0 01-1.06.87h-.78a1.06 1.06 0 01-1.06-.87l-.28-1.45a1.06 1.06 0 00-.61-.73l-1.37-.57a1.06 1.06 0 00-1.26.42l-.46.7a1.06 1.06 0 01-1.5.25l-.6-.5a1.06 1.06 0 01-.25-1.5l.7-1.02a1.06 1.06 0 000-1.24l-.7-1.02a1.06 1.06 0 01.25-1.5l.6-.5a1.06 1.06 0 011.5.25l.46.7a1.06 1.06 0 001.26.42l1.37-.57a1.06 1.06 0 00.61-.73l.28-1.45z" />
        <circle cx="11.99" cy="10" r="2.5" />
      </svg>
    ),
  },
]

function initials(name = '') {
  return name
    .split(' ')
    .filter(Boolean)
    .slice(0, 2)
    .map((p) => p[0]?.toUpperCase())
    .join('') || 'U'
}

function Sidebar() {
  const user = useAuthStore((state) => state.user)
  const logout = useAuthStore((state) => state.logout)
  const navigate = useNavigate()

  const handleLogout = () => {
    logout()
    navigate('/login')
  }

  return (
    <aside className="sticky top-0 hidden h-screen w-60 shrink-0 flex-col border-r border-ink-200 bg-white md:flex">
      <div className="flex h-16 items-center border-b border-ink-200 px-5">
        <Link to="/app/dashboard" aria-label="InterviewDesk dashboard" className="focus-ring rounded-md">
          <Logo size="sm" />
        </Link>
      </div>

      <nav className="flex-1 space-y-0.5 p-3" aria-label="Dashboard navigation">
        {NAV_ITEMS.map((item) => (
          <NavLink
            key={item.to}
            to={item.to}
            className={({ isActive }) =>
              `flex items-center gap-2.5 rounded-lg px-3 py-2 text-sm font-medium transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-brand-600/40 ${
                isActive
                  ? 'bg-brand-50 text-brand-800'
                  : 'text-ink-600 hover:bg-ink-50 hover:text-ink-900'
              }`
            }
          >
            {item.icon}
            {item.label}
          </NavLink>
        ))}
      </nav>

      <div className="border-t border-ink-200 p-3">
        <div className="flex items-center gap-2.5 rounded-lg px-2 py-2">
          <span className="flex h-8 w-8 shrink-0 items-center justify-center rounded-full bg-ink-900 text-xs font-semibold text-white">
            {initials(user?.full_name)}
          </span>
          <div className="min-w-0 flex-1">
            <p className="truncate text-sm font-medium text-ink-900">{user?.full_name || 'Candidate'}</p>
            <p className="truncate text-xs text-ink-400">{user?.email}</p>
          </div>
        </div>
        <button
          onClick={handleLogout}
          className="mt-1 flex w-full items-center gap-2.5 rounded-lg px-3 py-2 text-sm font-medium text-ink-500 transition-colors hover:bg-ink-50 hover:text-ink-900 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-brand-600/40"
        >
          <svg viewBox="0 0 20 20" fill="currentColor" className="h-[18px] w-[18px]" aria-hidden="true">
            <path
              fillRule="evenodd"
              d="M3 4.25A2.25 2.25 0 015.25 2h5.5A2.25 2.25 0 0113 4.25v2a.75.75 0 01-1.5 0v-2a.75.75 0 00-.75-.75h-5.5a.75.75 0 00-.75.75v11.5c0 .414.336.75.75.75h5.5a.75.75 0 00.75-.75v-2a.75.75 0 011.5 0v2A2.25 2.25 0 0110.75 18h-5.5A2.25 2.25 0 013 15.75V4.25z"
              clipRule="evenodd"
            />
            <path
              fillRule="evenodd"
              d="M19 10a.75.75 0 00-.75-.75H8.704l1.048-.943a.75.75 0 10-1.004-1.114l-2.5 2.25a.75.75 0 000 1.114l2.5 2.25a.75.75 0 001.004-1.114l-1.048-.943h9.546A.75.75 0 0019 10z"
              clipRule="evenodd"
            />
          </svg>
          Sign out
        </button>
      </div>
    </aside>
  )
}

function MobileNav() {
  const location = useLocation()

  // Interview workspace runs full-screen; hide the bottom nav there.
  if (location.pathname.startsWith('/app/interviews/') && location.pathname !== '/app/interviews' && !location.pathname.endsWith('/results')) {
    return null
  }

  return (
    <nav
      className="fixed inset-x-0 bottom-0 z-40 flex border-t border-ink-200 bg-white pb-[env(safe-area-inset-bottom)] md:hidden"
      aria-label="Dashboard navigation"
    >
      {NAV_ITEMS.map((item) => (
        <NavLink
          key={item.to}
          to={item.to}
          className={({ isActive }) =>
            `flex flex-1 flex-col items-center gap-1 py-2.5 text-[11px] font-medium transition-colors ${
              isActive ? 'text-brand-700' : 'text-ink-500 hover:text-ink-800'
            }`
          }
        >
          {item.icon}
          {item.label}
        </NavLink>
      ))}
    </nav>
  )
}

function MobileTopBar() {
  const user = useAuthStore((state) => state.user)

  return (
    <header className="sticky top-0 z-30 flex h-14 items-center justify-between border-b border-ink-200 bg-white px-4 md:hidden">
      <Link to="/app/dashboard" aria-label="InterviewDesk dashboard" className="focus-ring rounded-md">
        <Logo size="sm" wordmark={false} />
      </Link>
      <div className="flex items-center gap-2">
        <span className="text-sm font-medium text-ink-700">{user?.full_name?.split(' ')[0] || 'Candidate'}</span>
        <span className="flex h-7 w-7 items-center justify-center rounded-full bg-ink-900 text-[11px] font-semibold text-white">
          {initials(user?.full_name)}
        </span>
      </div>
    </header>
  )
}

export function AppShell() {
  return (
    <div className="flex min-h-screen">
      <Sidebar />
      <div className="flex min-w-0 flex-1 flex-col">
        <MobileTopBar />
        <main className="flex-1 pb-24 md:pb-10">
          <div className="mx-auto w-full max-w-page px-4 pt-8 sm:px-6">
            <Outlet />
          </div>
        </main>
        <MobileNav />
      </div>
    </div>
  )
}
