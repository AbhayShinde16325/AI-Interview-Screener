export default function Skeleton({ className = '', ...props }) {
  return (
    <div
      className={`animate-pulse rounded-md bg-ink-100 ${className}`}
      aria-hidden="true"
      {...props}
    />
  )
}
