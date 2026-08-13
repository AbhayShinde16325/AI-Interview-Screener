import { useId } from 'react'

export default function Select({ label, error, hint, id, options = [], className = '', ...props }) {
  const autoId = useId()
  const selectId = id || autoId

  return (
    <div className={className}>
      {label && (
        <label htmlFor={selectId} className="mb-1.5 block text-sm font-medium text-ink-800">
          {label}
        </label>
      )}

      <select
        id={selectId}
        aria-invalid={error ? true : undefined}
        className={`w-full rounded-lg border bg-white px-3.5 text-[15px] text-ink-900 focus:outline-none focus:ring-2 h-10 ${
          error
            ? 'border-red-400 focus:border-red-500 focus:ring-red-500/25'
            : 'border-ink-300 focus:border-brand-500 focus:ring-brand-600/20'
        }`}
        {...props}
      >
        {options.map((opt) => (
          <option key={opt.value} value={opt.value} disabled={opt.disabled}>
            {opt.label}
          </option>
        ))}
      </select>

      {error && <p className="mt-1.5 text-[13px] text-red-600">{error}</p>}
      {!error && hint && <p className="mt-1.5 text-[13px] text-ink-500">{hint}</p>}
    </div>
  )
}
