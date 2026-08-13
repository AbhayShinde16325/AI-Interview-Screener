import { useId } from 'react'

export default function Input({
  label,
  error,
  hint,
  id,
  className = '',
  rightSlot,
  ...props
}) {
  const autoId = useId()
  const inputId = id || autoId
  const describedBy = error ? `${inputId}-error` : hint ? `${inputId}-hint` : undefined

  return (
    <div className={className}>
      {label && (
        <label htmlFor={inputId} className="mb-1.5 block text-sm font-medium text-ink-800">
          {label}
        </label>
      )}

      <div className="relative">
        <input
          id={inputId}
          aria-invalid={error ? true : undefined}
          aria-describedby={describedBy}
          className={`w-full rounded-lg border bg-white px-3.5 text-[15px] text-ink-900 placeholder:text-ink-400 transition-colors focus:outline-none focus:ring-2 ${
            error
              ? 'border-red-400 focus:border-red-500 focus:ring-red-500/25'
              : 'border-ink-300 focus:border-brand-500 focus:ring-brand-600/20'
          } ${props.type === 'password' ? 'pr-11' : ''} h-10`}
          {...props}
        />
        {rightSlot && (
          <div className="absolute inset-y-0 right-0 flex items-center pr-2">{rightSlot}</div>
        )}
      </div>

      {error ? (
        <p id={`${inputId}-error`} className="mt-1.5 text-[13px] text-red-600">
          {error}
        </p>
      ) : hint ? (
        <p id={`${inputId}-hint`} className="mt-1.5 text-[13px] text-ink-500">
          {hint}
        </p>
      ) : null}
    </div>
  )
}
