const MARK = (
  <svg
    width="32"
    height="32"
    viewBox="0 0 32 32"
    fill="none"
    xmlns="http://www.w3.org/2000/svg"
    aria-hidden="true"
  >
    <rect width="32" height="32" rx="7" fill="currentColor" />
    <rect x="7" y="9" width="18" height="3.5" rx="1.75" fill="#fff" />
    <rect x="7" y="15" width="18" height="3.5" rx="1.75" fill="#fff" opacity="0.85" />
    <rect x="7" y="21" width="11" height="3.5" rx="1.75" fill="#fff" opacity="0.6" />
  </svg>
)

export default function Logo({
  wordmark = true,
  dark = false,
  className = '',
  size = 'md',
}) {
  const markSize = size === 'lg' ? 'h-9 w-9' : size === 'sm' ? 'h-7 w-7' : 'h-8 w-8'

  return (
    <span className={`inline-flex items-center gap-2 ${className}`}>
      <span className={`${markSize} text-brand-600 shrink-0`}>{MARK}</span>
      {wordmark && (
        <span
          className={`font-semibold tracking-tight ${
            size === 'lg' ? 'text-lg' : 'text-[15px]'
          } ${dark ? 'text-white' : 'text-ink-900'}`}
        >
          InterviewDesk
        </span>
      )}
    </span>
  )
}
