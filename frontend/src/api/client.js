import axios from 'axios'

import { useAuthStore } from '../store/authStore'

// In development Vite proxies /api -> http://localhost:8000.
// In production set VITE_API_URL to the deployed backend.
const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || '/api/v1',
})

api.interceptors.request.use((config) => {
  const token = useAuthStore.getState().token
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      const wasAuthed = Boolean(useAuthStore.getState().token)
      useAuthStore.getState().logout()

      if (window.location.pathname !== '/login') {
        // Tell the login page to show a "session expired" notice.
        if (wasAuthed) sessionStorage.setItem('session_expired', '1')
        window.location.href = '/login'
      }
    }
    return Promise.reject(error)
  },
)

export default api
