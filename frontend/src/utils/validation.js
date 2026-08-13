const EMAIL_RE = /^[^\s@]+@[^\s@]+\.[^\s@]+$/

export function isValidEmail(value) {
  return EMAIL_RE.test(String(value).trim())
}

export function validateEmail(value) {
  const v = String(value ?? '').trim()
  if (!v) return 'Email is required.'
  if (!isValidEmail(v)) return 'Enter a valid email address.'
  return ''
}
