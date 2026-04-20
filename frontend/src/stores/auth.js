import { ref, computed } from 'vue'
import { defineStore } from 'pinia'

export const useAuthStore = defineStore('auth', () => {
  const users = ref([])
  const currentUser = ref(JSON.parse(localStorage.getItem('currentUser')) || null)

  async function initializeUsers() {
    try {
      const response = await fetch('/Usuario.json')
      const data = await response.json()
      users.value = data.usuarios || []
      const storedUsers = JSON.parse(localStorage.getItem('users'))
      if (storedUsers && storedUsers.length > 0) {
        const combined = [...users.value]
        storedUsers.forEach(u => {
          if (!combined.find(existing => existing.email === u.email)) {
            combined.push(u)
          }
        })
        users.value = combined
      }
    } catch (error) {
      users.value = JSON.parse(localStorage.getItem('users')) || []
    }
  }

  initializeUsers()

  const isAuthenticated = computed(() => !!currentUser.value)

  function register(email, password, name) {
    const existingUser = users.value.find(u => u.email === email)
    if (existingUser) {
      return { success: false, message: 'El email ya está registrado' }
    }

    const newUser = { id: Date.now(), email, password, name }
    users.value.push(newUser)
    localStorage.setItem('users', JSON.stringify(users.value))
    
    currentUser.value = { id: newUser.id, email: newUser.email, name: newUser.name }
    localStorage.setItem('currentUser', JSON.stringify(currentUser.value))
    
    return { success: true, message: 'Registro exitoso' }
  }

  function login(email, password) {
    const user = users.value.find(u => u.email === email && u.password === password)
    if (!user) {
      return { success: false, message: 'Email o contraseña incorrectos' }
    }

    currentUser.value = { id: user.id, email: user.email, name: user.name }
    localStorage.setItem('currentUser', JSON.stringify(currentUser.value))
    
    return { success: true, message: 'Login exitoso' }
  }

  function logout() {
    currentUser.value = null
    localStorage.removeItem('currentUser')
  }

  return { users, currentUser, isAuthenticated, register, login, logout, initializeUsers }
})