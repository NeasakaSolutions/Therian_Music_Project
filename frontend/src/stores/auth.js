import { ref, computed } from 'vue'
import { defineStore } from 'pinia'

export const useAuthStore = defineStore('auth', () => {
  const users = ref(JSON.parse(localStorage.getItem('users')) || [])
  const currentUser = ref(JSON.parse(localStorage.getItem('currentUser')) || null)

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

  return { users, currentUser, isAuthenticated, register, login, logout }
})
