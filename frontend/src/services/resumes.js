import api from '../api/client'

export const uploadResume = (file) => {
  const formData = new FormData()
  formData.append('file', file)
  return api.post('/resumes/upload', formData)
}

export const getLatestResume = () => api.get('/resumes/latest')

/**
 * Full parsed resume (education, experience, projects, certifications).
 *
 * NOT CONNECTED YET: the backend does not currently expose these fields
 * through an endpoint. When one exists, point this function at it and the
 * Resume page will populate the corresponding sections automatically.
 */
export const getParsedResumeDetails = () => Promise.resolve(null)
