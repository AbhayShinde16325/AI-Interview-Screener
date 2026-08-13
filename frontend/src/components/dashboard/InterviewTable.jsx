import { Link } from 'react-router-dom'

import Badge from '../ui/Badge'
import Button from '../ui/Button'
import Skeleton from '../ui/Skeleton'

function formatDate(iso) {
  if (!iso) return '—'
  return new Date(iso).toLocaleDateString('en-US', {
    month: 'short',
    day: 'numeric',
    year: 'numeric',
  })
}

function StatusBadge({ status }) {
  if (status === 'COMPLETED') return <Badge tone="green" dot>Completed</Badge>
  return <Badge tone="blue" dot>In progress</Badge>
}

function SkeletonRows({ rows = 4 }) {
  return (
    <div className="divide-y divide-ink-100">
      {Array.from({ length: rows }).map((_, i) => (
        <div key={i} className="flex items-center gap-6 px-5 py-4">
          <div className="flex-1 space-y-2">
            <Skeleton className="h-3.5 w-40" />
            <Skeleton className="h-3 w-24" />
          </div>
          <Skeleton className="hidden h-3.5 w-16 sm:block" />
          <Skeleton className="h-7 w-24" />
        </div>
      ))}
    </div>
  )
}

export default function InterviewTable({
  interviews,
  questionCounts = {},
  showQuestions = false,
  loading = false,
  emptyState,
}) {
  if (loading) return <SkeletonRows />

  if (!interviews.length) return emptyState || null

  return (
    <div className="overflow-hidden rounded-lg border border-ink-200 bg-white">
      <div className="overflow-x-auto">
        <table className="w-full min-w-[560px] text-left text-sm">
          <thead>
            <tr className="border-b border-ink-200 bg-ink-50/70 text-xs font-semibold uppercase tracking-wide text-ink-500">
              <th scope="col" className="px-5 py-3">Role</th>
              <th scope="col" className="px-5 py-3">Date</th>
              {showQuestions && <th scope="col" className="px-5 py-3">Questions</th>}
              <th scope="col" className="px-5 py-3">Status</th>
              <th scope="col" className="px-5 py-3">Score</th>
              <th scope="col" className="px-5 py-3 text-right">Action</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-ink-100">
            {interviews.map((interview) => {
              const completed = interview.status === 'COMPLETED'
              const hasScore = interview.score != null
              return (
                <tr key={interview.id} className="transition-colors hover:bg-ink-50/50">
                  <td className="px-5 py-4">
                    <p className="font-medium text-ink-900">{interview.role}</p>
                  </td>
                  <td className="whitespace-nowrap px-5 py-4 text-ink-500">
                    {formatDate(interview.started_at)}
                  </td>
                  {showQuestions && (
                    <td className="whitespace-nowrap px-5 py-4 text-ink-500">
                      {questionCounts[interview.id] ?? '—'}
                    </td>
                  )}
                  <td className="px-5 py-4">
                    <StatusBadge status={interview.status} />
                  </td>
                  <td className="whitespace-nowrap px-5 py-4">
                    {hasScore ? (
                      <span className="font-semibold text-ink-900">{interview.score}/100</span>
                    ) : (
                      <span className="text-ink-400">—</span>
                    )}
                  </td>
                  <td className="whitespace-nowrap px-5 py-4 text-right">
                    {completed && hasScore ? (
                      <Link to={`/app/interviews/${interview.id}/results`}>
                        <Button size="sm" variant="secondary">
                          View results
                        </Button>
                      </Link>
                    ) : (
                      <Link to={`/app/interviews/${interview.id}`}>
                        <Button size="sm" variant="ghost">
                          Continue
                        </Button>
                      </Link>
                    )}
                  </td>
                </tr>
              )
            })}
          </tbody>
        </table>
      </div>
    </div>
  )
}
