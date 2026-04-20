<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { useThemeStore } from '@/stores/theme'
import { useMusicStore } from '@/stores/music'

const router = useRouter()
const authStore = useAuthStore()
const themeStore = useThemeStore()
const musicStore = useMusicStore()

function handleAuth() {
  router.push('/login')
}

function goHome() {
  router.push('/inicio')
}

function goToDashboard() {
  router.push('/dashboard')
}
</script>

<template>
  <nav class="fixed top-0 left-0 right-0 z-50 bg-white/10 dark:bg-black/40 backdrop-blur-xl border-b border-white/10">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="flex items-center justify-between h-16">
        <div class="flex items-center gap-8">
          <div @click="goHome" class="flex items-center gap-3 cursor-pointer group">
            <div class="w-10 h-10 rounded-xl bg-gradient-to-br from-purple-500 to-violet-600 flex items-center justify-center text-xl group-hover:scale-110 transition-transform">
              🎵
            </div>
            <span class="text-xl font-bold bg-gradient-to-r from-purple-400 to-violet-500 bg-clip-text text-transparent hidden sm:block">
              Therian Music
            </span>
          </div>
        </div>

        <div class="hidden md:flex flex-1 max-w-md mx-8">
          <div class="relative w-full">
            <input
              v-model="musicStore.searchQuery"
              type="text"
              placeholder="Buscar canciones, artistas..."
              class="w-full bg-white/5 dark:bg-white/5 border border-white/10 rounded-full py-2.5 pl-11 pr-4 text-sm text-white placeholder:text-white/50 focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-transparent transition-all"
            />
            <svg class="absolute left-4 top-1/2 -translate-y-1/2 w-4 h-4 text-white/50" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"/>
            </svg>
          </div>
        </div>

        <div class="flex items-center gap-3">
          <button
            @click="themeStore.toggleTheme"
            class="w-10 h-10 rounded-full bg-white/10 hover:bg-white/20 flex items-center justify-center transition-all hover:scale-110"
          >
            <span v-if="themeStore.isDark" class="text-lg">☀️</span>
            <span v-else class="text-lg">🌙</span>
          </button>

          <template v-if="authStore.isAuthenticated">
            <button
              @click="goToDashboard"
              class="flex items-center gap-3 bg-white/10 hover:bg-white/20 rounded-full pr-4 transition-colors"
            >
              <div class="w-10 h-10 rounded-full bg-gradient-to-br from-purple-500 to-violet-600 flex items-center justify-center text-white font-bold">
                {{ authStore.currentUser?.name?.charAt(0).toUpperCase() }}
              </div>
              <span class="text-white text-sm hidden sm:block">Mi Perfil</span>
            </button>
          </template>

          <template v-else>
            <button
              @click="handleAuth"
              class="bg-gradient-to-r from-purple-500 to-violet-600 text-white px-5 py-2.5 rounded-full font-medium text-sm hover:from-purple-600 hover:to-violet-700 transition-all transform hover:scale-105 shadow-lg shadow-purple-500/25"
            >
              Iniciar Sesión
            </button>
          </template>
        </div>
      </div>
    </div>

    <div class="md:hidden px-4 pb-3">
      <div class="relative">
        <input
          v-model="musicStore.searchQuery"
          type="text"
          placeholder="Buscar..."
          class="w-full bg-white/5 border border-white/10 rounded-full py-2 pl-11 pr-4 text-sm text-white placeholder:text-white/50 focus:outline-none focus:ring-2 focus:ring-purple-500"
        />
        <svg class="absolute left-4 top-1/2 -translate-y-1/2 w-4 h-4 text-white/50" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"/>
        </svg>
      </div>
    </div>
  </nav>
</template>