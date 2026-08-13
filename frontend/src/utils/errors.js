/**
 * Translates backend + network errors into user-friendly copy.
 * Raw backend exceptions are never shown to the user.
 */
export function friendlyError(err, fallback = 'Something went wrong. Please try again.') {
  if (!err || !err.response) {
    return "We couldn't reach the server. Check your connection and try again."
  }

  const { status, data } = err.response
  const detail = data?.detail

  switch (status) {
    case 400:
      return typeof detail === 'string' ? detail : 'The request was invalid. Please review your input.'
    case 401:
      return 'Your session has expired. Please sign in again.'
    case 403:
      return "You don't have permission to do that."
    case 404:
      return "We couldn't find what you were looking for."
    case 409:
      return typeof detail === 'string' ? detail : 'That already exists. Please try something else.'
    case 422: {
      if (Array.isArray(detail) && detail[0]?.msg) return detail[0].msg
      if (typeof detail === 'string') return detail
      return 'Please check the information you entered.'
    }
    case 429:
      return 'Too many requests. Please wait a moment and try again.'
    case 500:
    case 502:
    case 503:
      return 'Something went wrong on our end. Please try again later.'
    default:
      return fallback
  }
}
