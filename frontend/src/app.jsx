import { BrowserRouter, Navigate, Route, Routes } from 'react-router-dom'

import { ProtectedRoute } from './components/ProtectedRoute'
import { AppShell } from './components/layout/AppShell'

import Landing from './pages/Landing'
import Login from './pages/Login'
import Register from './pages/Register'
import Dashboard from './pages/app/Dashboard'
import Resume from './pages/app/Resume'
import InterviewSetup from './pages/app/InterviewSetup'
import InterviewHistory from './pages/app/InterviewHistory'
import Interview from './pages/app/Interview'
import Results from './pages/app/Results'
import Settings from './pages/app/Settings'

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        {/* Public */}
        <Route path="/" element={<Landing />} />
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />

        {/* Protected application */}
        <Route element={<ProtectedRoute />}>
          <Route element={<AppShell />}>
            <Route path="/app" element={<Navigate to="/app/dashboard" replace />} />
            <Route path="/app/dashboard" element={<Dashboard />} />
            <Route path="/app/resume" element={<Resume />} />
            <Route path="/app/interviews" element={<InterviewHistory />} />
            <Route path="/app/interviews/new" element={<InterviewSetup />} />
            <Route path="/app/interviews/:id/results" element={<Results />} />
            <Route path="/app/settings" element={<Settings />} />
          </Route>

          {/* Focused workspace — no app shell */}
          <Route path="/app/interviews/:id" element={<Interview />} />
        </Route>

        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </BrowserRouter>
  )
}
