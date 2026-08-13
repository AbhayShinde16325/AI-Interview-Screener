export default function Spinner({ label, size = 'md', className = '' }) {
  const dims = size === 'sm' ? 'h-4 w-4' : size === 'lg' ? 'h-10 w-10' : 'h-6 w-6'

  return (
    <div className={`flex flex-col items-center justify-center gap-3 ${className}`}>
      <svg className={`${dims} animate-spin text-brand-600`} viewBox="0 0 24 24" fill="none" aria-hidden="true">
        <circle
          className="opacity-25"
          cx="12"
          cy="12"
          r="10"
          stroke="currentColor"
          strokeWidth="4"
        />
        <path
          className="opacity-90"
          fill="currentColor"
          d="M4 12a8 8 0 018-8v3a5 5 0 00-5 5H4z"
        />
      </svg>
      {label && <p className="text-sm text-ink-500">{label}</p>}
    </div>
  )
}
