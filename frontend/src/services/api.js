import axios from 'axios'

const api = axios.create({
  baseURL: '/api/v1',
  timeout: 120_000,
})

api.interceptors.response.use(
  res => res,
  err => {
    const message = err.response?.data?.detail || err.message || 'An error occurred'
    return Promise.reject(new Error(message))
  }
)

export default api
