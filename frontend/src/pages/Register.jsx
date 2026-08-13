import { useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'

import AuthLayout from '../components/auth/AuthLayout'
import PasswordInput from '../components/auth/PasswordInput'
import Button from '../components/ui/Button'
import Input from '../components/ui/Input'
import Alert from '../components/ui/Alert'
import { login as apiLogin, register as apiRegister, getMe } from '../services/auth'
import { useAuthStore } from '../store/authStore'
import { validateEmail } from '../utils/validation'
import { friendlyError } from '../utils/errors'

export default function Register() {
  const [fullName, setFullName] = useState('')
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [confirm, setConfirm] = useState('')
  const [fieldErrors, setFieldErrors] = useState({})
  const [serverError, setServerError] = useState('')
  const [loading, setLoading] = useState(false)

  const setAuth = useAuthStore((state) => state.setAuth)
  const navigate = useNavigate()

  const validate = () => {
    const errors = {}
    if (!fullName.trim()) errors.fullName = 'Full name is required.'
    else if (fullName.trim().length < 2) errors.fullName = 'Enter at least 2 characters.'

    const emailError = validateEmail(email)
    if (emailError) errors.email = emailError

    if (!password) errors.password = 'Password is required.'
    else if (password.length < 8) errors.password = 'Password must be at least 8 characters.'

    if (!confirm) errors.confirm = 'Please confirm your password.'
    else if (confirm !== password) errors.confirm = 'Passwords do not match.'

    return errors
  }

  const clearFieldError = (field) => {
    if (fieldErrors[field]) setFieldErrors((p) => ({ ...p, [field]: '' }))
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    setServerError('')

    const errors = validate()
    setFieldErrors(errors)
    if (Object.keys(errors).length > 0) return

    setLoading(true)
    try {
      await apiRegister({ full_name: fullName.trim(), email: email.trim(), password })

      // Auto sign-in after a successful registration.
      const { data } = await apiLogin({ email: email.trim(), password })
      setAuth(data.access_token, null)

      const me = await getMe()
      setAuth(data.access_token, me.data)

      navigate('/app/dashboard', { replace: true })
    } catch (err) {
      setServerError(friendlyError(err, 'Registration failed. Please try again.'))
    } finally {
      setLoading(false)
    }
  }

  return (
    <AuthLayout>
      <h1 className="text-2xl font-semibold tracking-tight text-ink-900">Create your account</h1>
      <p className="mt-1.5 text-sm text-ink-500">
        Upload your resume and get a role-specific technical interview.
      </p>

      <form onSubmit={handleSubmit} noValidate className="mt-8 space-y-5">
        {serverError && <Alert>{serverError}</Alert>}

        <Input
          label="Full name"
          name="fullName"
          autoComplete="name"
          placeholder="Jane Doe"
          value={fullName}
          onChange={(e) => {
            setFullName(e.target.value)
            clearFieldError('fullName')
          }}
          error={fieldErrors.fullName}
        />

        <Input
          label="Email"
          type="email"
          name="email"
          autoComplete="email"
          placeholder="you@example.com"
          value={email}
          onChange={(e) => {
            setEmail(e.target.value)
            clearFieldError('email')
          }}
          error={fieldErrors.email}
        />

        <PasswordInput
          label="Password"
          name="password"
          autoComplete="new-password"
          placeholder="At least 8 characters"
          hint="At least 8 characters."
          value={password}
          onChange={(e) => {
            setPassword(e.target.value)
            clearFieldError('password')
          }}
          error={fieldErrors.password}
        />

        <PasswordInput
          label="Confirm password"
          name="confirmPassword"
          autoComplete="new-password"
          placeholder="Re-enter your password"
          value={confirm}
          onChange={(e) => {
            setConfirm(e.target.value)
            clearFieldError('confirm')
          }}
          error={fieldErrors.confirm}
        />

        <Button type="submit" size="lg" loading={loading} loadingText="Creating account…" className="w-full">
          Create account
        </Button>
      </form>

      <p className="mt-6 text-center text-sm text-ink-500">
        Already have an account?{' '}
        <Link to="/login" className="font-semibold text-brand-700 hover:text-brand-800">
          Sign in
        </Link>
      </p>
    </AuthLayout>
  )
}
