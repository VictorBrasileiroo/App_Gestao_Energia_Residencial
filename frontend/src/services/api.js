import axios from 'axios'

const API_BASE_URL = 'http://localhost:8000'

// Create axios instance with default config
const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Add token to requests if it exists
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// Handle 401 responses by redirecting to login
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('token')
      window.location.href = '/login'
    }
    return Promise.reject(error)
  }
)

// Auth endpoints
export const authAPI = {
  register: (data) => api.post('/auth/register', null, { params: data }),
  login: (email, password) => {
    const formData = new FormData()
    formData.append('username', email)
    formData.append('password', password)
    return api.post('/auth/login', formData, {
      headers: { 'Content-Type': 'multipart/form-data' }
    })
  },
  getMe: () => api.get('/auth/me'),
}

// Dashboard endpoints
export const dashboardAPI = {
  getSummary: () => api.get('/dashboard/'),
  getMonthlyComparison: () => api.get('/dashboard/monthly-comparison'),
}

// Consumption endpoints
export const consumptionAPI = {
  uploadFile: (file) => {
    const formData = new FormData()
    formData.append('file', file)
    return api.post('/consumption/upload', formData, {
      headers: { 'Content-Type': 'multipart/form-data' }
    })
  },
  getHourlyPattern: () => api.get('/consumption/hourly-pattern'),
}

// Reports endpoints
export const reportsAPI = {
  getMonthly: (year, month) => api.get('/reports/monthly', { params: { year, month } }),
  getSummary: () => api.get('/reports/summary'),
}

// Alerts endpoints
export const alertsAPI = {
  list: () => api.get('/alerts/'),
  evaluate: () => api.post('/alerts/evaluate'),
}

// Predictions endpoints
export const predictionsAPI = {
  getLatest: () => api.get('/predictions/latest'),
  generate: () => api.post('/predictions/generate'),
}

export default api
