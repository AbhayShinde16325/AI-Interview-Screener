export default function InterviewProgress({ current, total }) {
  const pct = Math.round(((current + 1) / total) * 100)

  return (
    <div>
      <div className="flex items-center justify-between text-[13px] font-medium text-ink-500">
        <span>
          Question {current + 1} of {total}
        </span>
        <span>{pct}%</span>
      </div>
      <div className="mt-2 h-1.5 w-full overflow-hidden rounded-full bg-ink-100" role="progressbar" aria-valuenow={pct} aria-valuemin={0} aria-valuemax={100}>
        <div
          className="h-full rounded-full bg-brand-600 transition-all duration-300"
          style={{ width: `${pct}%` }}
        />
      </div>
    </div>
  )
}
