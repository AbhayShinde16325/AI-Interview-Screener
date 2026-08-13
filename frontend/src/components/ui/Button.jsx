export default function Button({
  variant = 'primary',
  size = 'md',
  loading = false,
  loadingText,
  className = '',
  children,
  disabled,
  ...props
}) {
  const variants = {
    primary:
      'bg-brand-600 text-white hover:bg-brand-700 active:bg-brand-800 disabled:hover:bg-brand-600',
    secondary:
      'bg-white text-ink-800 border border-ink-300 hover:border-ink-400 hover:bg-ink-50 active:bg-ink-100',
    ghost: 'text-ink-700 hover:bg-ink-100 hover:text-ink-900',
    danger:
      'bg-white text-red-700 border border-red-300 hover:bg-red-50 active:bg-red-100',
    dangerSolid: 'bg-red-600 text-white hover:bg-red-700 active:bg-red-800',
  }

  const sizes = {
    sm: 'h-8 px-3 text-[13px]',
    md: 'h-10 px-4 text-sm',
    lg: 'h-11 px-5 text-[15px]',
  }

  return (
    <button
      className={`inline-flex items-center justify-center gap-2 rounded-lg font-medium transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-brand-600/50 focus-visible:ring-offset-1 disabled:cursor-not-allowed disabled:opacity-60 ${variants[variant]} ${sizes[size]} ${className}`}
      disabled={disabled || loading}
      {...props}
    >
      {loading && (
        <svg
          className={`animate-spin ${size === 'sm' ? 'h-3.5 w-3.5' : 'h-4 w-4'}`}
          viewBox="0 0 24 24"
          fill="none"
          aria-hidden="true"
        >
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
      )}
      {loading && loadingText ? loadingText : children}
    </button>
  )
}
