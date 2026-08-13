import { useEffect, useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'

import AuthLayout from '../components/auth/AuthLayout'
import PasswordInput from '../components/auth/PasswordInput'
import Button from '../components/ui/Button'
import Input from '../components/ui/Input'
import Alert from '../components/ui/Alert'
import { login as apiLogin, getMe } from '../services/auth'
import { useAuthStore } from '../store/authStore'
import { validateEmail } from '../utils/validation'
import { friendlyError } from '../utils/errors'

export default function Login() {
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [fieldErrors, setFieldErrors] = useState({})
  const [serverError, setServerError] = useState('')
  const [loading, setLoading] = useState(false)
  const [sessionExpired, setSessionExpired] = useState(
    sessionStorage.getItem('session_expired') === '1',
  )

  const setAuth = useAuthStore((state) => state.setAuth)
  const navigate = useNavigate()

  useEffect(() => {
    // Clear the expired-session notice once it has been shown.
    sessionStorage.removeItem('session_expired')
  }, [])

  const validate = () => {
    const errors = {}
    const emailError = validateEmail(email)
    if (emailError) errors.email = emailError
    if (!password) errors.password = 'Password is required.'
    return errors
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    setServerError('')

    const errors = validate()
    setFieldErrors(errors)
    if (Object.keys(errors).length > 0) return

    setLoading(true)
    try {
      const { data } = await apiLogin({ email: email.trim(), password })
      setAuth(data.access_token, null)

      const me = await getMe()
      setAuth(data.access_token, me.data)

      sessionStorage.removeItem('session_expired')
      navigate('/app/dashboard', { replace: true })
    } catch (err) {
      if (err.response?.status === 401) {
        setServerError('Email or password is incorrect.')
      } else {
        setServerError(friendlyError(err, 'Sign in failed. Please try again.'))
      }
    } finally {
      setLoading(false)
    }
  }

  return (
    <AuthLayout>
      <h1 className="text-2xl font-semibold tracking-tight text-ink-900">Welcome back</h1>
      <p className="mt-1.5 text-sm text-ink-500">Sign in to continue your interview preparation.</p>

      <form onSubmit={handleSubmit} noValidate className="mt-8 space-y-5">
        {sessionExpired && (
          <Alert tone="info" title="Your session has expired">
            Please sign in again to continue.
          </Alert>
        )}
        {serverError && <Alert>{serverError}</Alert>}

        <Input
          label="Email"
          type="email"
          name="email"
          autoComplete="email"
          placeholder="you@example.com"
          value={email}
          onChange={(e) => {
            setEmail(e.target.value)
            if (fieldErrors.email) setFieldErrors((p) => ({ ...p, email: '' }))
          }}
          error={fieldErrors.email}
        />

        <PasswordInput
          label="Password"
          name="password"
          autoComplete="current-password"
          placeholder="Your password"
          value={password}
          onChange={(e) => {
            setPassword(e.target.value)
            if (fieldErrors.password) setFieldErrors((p) => ({ ...p, password: '' }))
          }}
          error={fieldErrors.password}
        />

        <Button type="submit" size="lg" loading={loading} loadingText="Signing in…" className="w-full">
          Sign in
        </Button>
      </form>

      <p className="mt-6 text-center text-sm text-ink-500">
        New to InterviewDesk?{' '}
        <Link to="/register" className="font-semibold text-brand-700 hover:text-brand-800">
          Create an account
        </Link>
      </p>
    </AuthLayout>
  )
}
