import api from '../api/client'

export const startInterview = (role) => api.post('/interviews/start', { role })

export const listInterviews = () => api.get('/interviews')

export const getInterviewQuestions = (interviewId) =>
  api.get(`/interviews/${interviewId}/questions`)

export const submitAnswer = (interviewId, questionId, answer) =>
  api.post(`/interviews/${interviewId}/answer`, {
    question_id: questionId,
    answer,
  })

export const completeInterview = (interviewId) =>
  api.post(`/interviews/${interviewId}/complete`)

export const getResult = (interviewId) =>
  api.get(`/interviews/${interviewId}/result`)
