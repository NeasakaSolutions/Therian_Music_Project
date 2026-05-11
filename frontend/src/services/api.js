import axios from 'axios'

const API_URL = 'http://127.0.0.1:8000/api/mai'

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

export async function registerUser(data) {
  const response = await api.post('/seguridad/registro', {
    nombre: data.name,
    correo: data.email,
    password: data.password,
  })
  return response.data
}

export async function loginUser(data) {
  const response = await api.post('/seguridad/login', {
    correo: data.email,
    password: data.password,
  })
  return response.data
}

export async function verifyUser(token) {
  const response = await api.get(`/seguridad/verificacion/${token}`)
  return response.data
}

export default api
