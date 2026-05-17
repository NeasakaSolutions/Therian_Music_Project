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

export async function fetchCancionesHome() {
  const response = await api.get('/canciones-home')
  return response.data
}

export async function fetchCanciones(page = 1, perPage = 10) {
  const response = await api.get(`/canciones?page=${page}&per_page=${perPage}`)
  return response.data
}

export async function fetchCancionById(id) {
  const response = await api.get(`/canciones/${id}`)
  return response.data
}

export async function fetchCancionBySlug(slug) {
  const response = await api.get(`/canciones/slug/${slug}`)
  return response.data
}

export async function searchCanciones(categoriaId, search) {
  const response = await api.get(`/canciones-buscador?categoria_id=${categoriaId}&search=${search}`)
  return response.data
}

export async function fetchArtistas() {
  const response = await api.get('/artistas')
  return response.data
}

export async function fetchCategorias() {
  const response = await api.get('/categorias')
  return response.data
}

export async function crearArtista(data) {
  const response = await api.post('/artistas', { nombre: data.nombre })
  return response.data
}

export async function crearCategoria(data) {
  const response = await api.post('/categorias', { nombre: data.nombre })
  return response.data
}

export async function uploadSong(formData) {
  const response = await api.post('/canciones', formData, {
    headers: { 'Content-Type': 'multipart/form-data' },
  })
  return response.data
}

export async function submitContacto(data) {
  const response = await api.post('/contacto', {
    nombre: data.nombre,
    correo: data.correo,
    telefono: data.telefono,
    mensaje: data.mensaje,
  })
  return response.data
}

export async function fetchCancionesPanel(id) {
  const response = await api.get(`/canciones-panel/${id}`)
  return response.data
}

export default api
