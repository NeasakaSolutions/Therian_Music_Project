import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import { registerUser, loginUser } from '@/services/api'

export const useAuthStore = defineStore('auth', () => {
  const currentUser = ref(JSON.parse(localStorage.getItem('currentUser')) || null)
  const token = ref(localStorage.getItem('token') || null)
  const loading = ref(false)
  const error = ref(null)

  const isAuthenticated = computed(() => !!token.value)

  async function register(name, email, password) {
    loading.value = true
    error.value = null

    try {
      const response = await registerUser({ name, email, password })
      loading.value = false
      return { success: true, message: response.mensaje }
    } catch (err) {
      loading.value = false
      error.value = err.response?.data?.mensaje || 'Error al registrar'
      return { success: false, message: error.value }
    }
  }

  async function login(email, password) {
    loading.value = true
    error.value = null

    try {
      const response = await loginUser({ email, password })
      token.value = response.token
      currentUser.value = {
        id: response.id,
        name: response.nombre,
        email: email,
      }

      localStorage.setItem('token', response.token)
      localStorage.setItem('currentUser', JSON.stringify(currentUser.value))

      loading.value = false
      return { success: true, message: 'Login exitoso' }
    } catch (err) {
      loading.value = false
      error.value = err.response?.data?.mensaje || 'Error al iniciar sesión'
      return { success: false, message: error.value }
    }
  }

  function logout() {
    currentUser.value = null
    token.value = null
    localStorage.removeItem('currentUser')
    localStorage.removeItem('token')
  }

  return { currentUser, token, loading, error, isAuthenticated, register, login, logout }
})