<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { useThemeStore } from '@/stores/theme'

const router = useRouter()
const authStore = useAuthStore()
const themeStore = useThemeStore()

const name = ref('')
const email = ref('')
const password = ref('')
const confirmPassword = ref('')
const error = ref('')
const loading = ref(false)

async function handleRegister() {
  error.value = ''

  if (!name.value || !email.value || !password.value || !confirmPassword.value) {
    error.value = 'Completa todos los campos'
    return
  }

  if (password.value !== confirmPassword.value) {
    error.value = 'Las contraseñas no coinciden'
    return
  }

  if (password.value.length < 6) {
    error.value = 'La contraseña debe tener al menos 6 caracteres'
    return
  }

  loading.value = true
  await new Promise(r => setTimeout(r, 500))

  const result = authStore.register(email.value, password.value, name.value)
  loading.value = false

  if (result.success) {
    router.push('/inicio')
  } else {
    error.value = result.message
  }
}
</script>

<template>
  <div class="min-h-screen flex items-center justify-center px-4 relative">
    <button
      @click="themeStore.toggleTheme"
      class="absolute top-6 right-6 w-12 h-12 rounded-full bg-white/10 dark:bg-white/10 backdrop-blur-sm flex items-center justify-center hover:scale-110 transition-transform"
    >
      <span v-if="themeStore.isDark" class="text-2xl">☀️</span>
      <span v-else class="text-2xl">🌙</span>
    </button>

    <router-link
      to="/inicio"
      class="absolute top-6 left-6 flex items-center gap-2 text-white/60 hover:text-white transition-colors"
    >
      <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 19l-7-7m0 0l7-7m-7 7h18"/>
      </svg>
      <span>Volver al inicio</span>
    </router-link>

    <div class="w-full max-w-md bg-white/10 dark:bg-white/5 backdrop-blur-xl rounded-3xl p-8 shadow-2xl border border-white/10">
      <div class="text-center mb-8">
        <h1 class="text-4xl font-bold bg-gradient-to-r from-purple-400 via-violet-500 to-purple-600 bg-clip-text text-transparent mb-2">
          Therian Music
        </h1>
        <p class="text-violet-500 dark:text-violet-400 text-sm">Tu música, tu esencia</p>
      </div>
      
      <h2 class="text-2xl font-semibold text-center mb-6 text-violet-900 dark:text-violet-100">
        Crear Cuenta
      </h2>
      
      <form @submit.prevent="handleRegister" class="space-y-5">
        <div class="relative">
          <input
            v-model="name"
            type="text"
            placeholder="Nombre"
            class="w-full bg-violet-100 dark:bg-white/5 text-violet-900 dark:text-white rounded-xl px-5 py-4 outline-none focus:ring-2 focus:ring-violet-500 border border-transparent focus:border-violet-500 transition-all"
          />
        </div>

        <div class="relative">
          <input
            v-model="email"
            type="email"
            placeholder="Email"
            class="w-full bg-violet-100 dark:bg-white/5 text-violet-900 dark:text-white rounded-xl px-5 py-4 outline-none focus:ring-2 focus:ring-violet-500 border border-transparent focus:border-violet-500 transition-all"
          />
        </div>
        
        <div class="relative">
          <input
            v-model="password"
            type="password"
            placeholder="Contraseña"
            class="w-full bg-violet-100 dark:bg-white/5 text-violet-900 dark:text-white rounded-xl px-5 py-4 outline-none focus:ring-2 focus:ring-violet-500 border border-transparent focus:border-violet-500 transition-all"
          />
        </div>

        <div class="relative">
          <input
            v-model="confirmPassword"
            type="password"
            placeholder="Confirmar Contraseña"
            class="w-full bg-violet-100 dark:bg-white/5 text-violet-900 dark:text-white rounded-xl px-5 py-4 outline-none focus:ring-2 focus:ring-violet-500 border border-transparent focus:border-violet-500 transition-all"
          />
        </div>

        <p v-if="error" class="text-red-500 text-sm text-center bg-red-500/10 py-2 rounded-lg">
          {{ error }}
        </p>

        <button
          type="submit"
          :disabled="loading"
          class="w-full bg-gradient-to-r from-purple-500 to-violet-600 text-white font-bold py-4 rounded-xl hover:from-purple-600 hover:to-violet-700 transition-all transform hover:scale-[1.02] active:scale-[0.98] disabled:opacity-50 disabled:hover:scale-100 shadow-lg shadow-purple-500/25"
        >
          {{ loading ? 'Cargando...' : 'Registrarse' }}
        </button>
      </form>

      <p class="text-center mt-6 text-violet-700 dark:text-violet-300">
        ¿Ya tienes cuenta?
        <router-link to="/login" class="font-semibold hover:underline ml-1">
          Inicia Sesión
        </router-link>
      </p>
    </div>
  </div>
</template>
