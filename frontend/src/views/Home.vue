<script setup>
import { useThemeStore } from '@/stores/theme'

const themeStore = useThemeStore()
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

    <div class="text-center max-w-2xl">
      <div class="mb-8">
        <div class="w-24 h-24 mx-auto rounded-3xl bg-gradient-to-br from-purple-500 to-violet-600 flex items-center justify-center text-5xl mb-6 shadow-2xl shadow-purple-500/30 animate-pulse">
          🎵
        </div>
        <h1 class="text-6xl font-bold bg-gradient-to-r from-purple-400 via-violet-500 to-purple-600 bg-clip-text text-transparent mb-4">
          Therian Music
        </h1>
        <p class="text-xl text-violet-600 dark:text-violet-400 mb-2">
          Tu música, tu esencia
        </p>
        <p class="text-white/60 max-w-md mx-auto">
          Descubre una nueva forma de experimentar la música. Reproduce, explora y disfruta de tu biblioteca personal.
        </p>
      </div>

      <div class="space-y-4">
        <router-link
          to="/login"
          class="block w-full bg-gradient-to-r from-purple-500 to-violet-600 text-white font-bold py-4 px-8 rounded-2xl hover:from-purple-600 hover:to-violet-700 transition-all transform hover:scale-105 active:scale-95 shadow-lg shadow-purple-500/25"
        >
          Iniciar Sesión
        </router-link>
        
        <router-link
          to="/register"
          class="block w-full bg-white/10 dark:bg-white/5 backdrop-blur-sm border border-white/20 text-white font-semibold py-4 px-8 rounded-2xl hover:bg-white/20 transition-all transform hover:scale-105 active:scale-95"
        >
          Crear Cuenta
        </router-link>
      </div>

      <div class="mt-12">
        <router-link
          to="/inicio"
          class="inline-flex items-center gap-2 text-purple-400 hover:text-purple-300 transition-colors"
        >
          <span>Explorar sin cuenta</span>
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 8l4 4m0 0l-4 4m4-4H3"/>
          </svg>
        </router-link>
      </div>
    </div>
  </div>
</template>
