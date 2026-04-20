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

const activeTab = ref('overview')

function logout() {
  authStore.logout()
  router.push('/')
}

const stats = [
  { icon: '🎵', label: 'Canciones reproducidas', value: '127' },
  { icon: '⏱', label: 'Horas escuchadas', value: '48' },
  { icon: '❤️', label: 'Me gusta', value: '23' },
  { icon: '📋', label: 'Playlists', value: '5' }
]

const recentActivity = [
  { type: 'played', track: 'Midnight Dreams', artist: 'Luna Eclipse', time: 'Hace 5 min' },
  { type: 'liked', track: 'Electric Pulse', artist: 'Neon Waves', time: 'Hace 1 hora' },
  { type: 'playlist', track: 'Mis Favoritos', artist: '', time: 'Ayer' },
  { type: 'played', track: 'Starlight Serenade', artist: 'Cosmic Echo', time: 'Ayer' }
]

const playlists = [
  { name: 'Mis Favoritos', count: 23, cover: 'https://picsum.photos/seed/playlist1/300/300' },
  { name: 'Para Gimnasio', count: 15, cover: 'https://picsum.photos/seed/playlist2/300/300' },
  { name: 'Lo-Fi Chill', count: 42, cover: 'https://picsum.photos/seed/playlist3/300/300' },
  { name: 'Viaje', count: 30, cover: 'https://picsum.photos/seed/playlist4/300/300' }
]
</script>

<template>
  <div class="pt-20 pb-32 min-h-screen">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="bg-gradient-to-br from-purple-900/50 via-violet-800/30 to-transparent rounded-3xl p-8 mb-8">
        <div class="flex flex-col md:flex-row items-center gap-6">
          <div class="w-32 h-32 rounded-full bg-gradient-to-br from-purple-500 to-violet-600 flex items-center justify-center text-5xl font-bold text-white shadow-2xl">
            {{ authStore.currentUser?.name?.charAt(0).toUpperCase() }}
          </div>
          <div class="flex-1 text-center md:text-left">
            <p class="text-purple-400 text-sm font-medium mb-1">PERFIL</p>
            <h1 class="text-4xl font-bold text-white mb-2">{{ authStore.currentUser?.name }}</h1>
            <p class="text-white/60 mb-4">{{ authStore.currentUser?.email }}</p>
            <div class="flex flex-wrap justify-center md:justify-start gap-4">
              <span class="bg-white/10 px-4 py-2 rounded-full text-white/80 text-sm">
                🎵 {{ stats[0].value }} canciones
              </span>
              <span class="bg-white/10 px-4 py-2 rounded-full text-white/80 text-sm">
                ⏱ {{ stats[1].value }} horas
              </span>
            </div>
          </div>
          <div class="flex gap-3">
            <button
              @click="themeStore.toggleTheme"
              class="w-12 h-12 rounded-full bg-white/10 hover:bg-white/20 flex items-center justify-center transition-all hover:scale-110"
            >
              <span v-if="themeStore.isDark" class="text-xl">☀️</span>
              <span v-else class="text-xl">🌙</span>
            </button>
            <button
              @click="logout"
              class="bg-red-500/20 text-red-400 px-6 py-3 rounded-full hover:bg-red-500/30 transition-colors flex items-center gap-2"
            >
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1"/>
              </svg>
              <span>Cerrar Sesión</span>
            </button>
          </div>
        </div>
      </div>

      <div class="flex gap-2 mb-8 overflow-x-auto pb-2">
        <button
          @click="activeTab = 'overview'"
          class="px-6 py-3 rounded-full font-medium transition-all whitespace-nowrap"
          :class="activeTab === 'overview' ? 'bg-purple-500 text-white' : 'bg-white/5 text-white/60 hover:text-white'"
        >
          Resumen
        </button>
        <button
          @click="activeTab = 'playlists'"
          class="px-6 py-3 rounded-full font-medium transition-all whitespace-nowrap"
          :class="activeTab === 'playlists' ? 'bg-purple-500 text-white' : 'bg-white/5 text-white/60 hover:text-white'"
        >
          Playlists
        </button>
        <button
          @click="activeTab = 'favorites'"
          class="px-6 py-3 rounded-full font-medium transition-all whitespace-nowrap"
          :class="activeTab === 'favorites' ? 'bg-purple-500 text-white' : 'bg-white/5 text-white/60 hover:text-white'"
        >
          Favoritos
        </button>
        <button
          @click="activeTab = 'history'"
          class="px-6 py-3 rounded-full font-medium transition-all whitespace-nowrap"
          :class="activeTab === 'history' ? 'bg-purple-500 text-white' : 'bg-white/5 text-white/60 hover:text-white'"
        >
          Historial
        </button>
        <button
          @click="activeTab = 'settings'"
          class="px-6 py-3 rounded-full font-medium transition-all whitespace-nowrap"
          :class="activeTab === 'settings' ? 'bg-purple-500 text-white' : 'bg-white/5 text-white/60 hover:text-white'"
        >
          Configuración
        </button>
      </div>

      <div v-if="activeTab === 'overview'" class="space-y-8">
        <section>
          <h3 class="text-xl font-bold text-white mb-4">Estadísticas</h3>
          <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
            <div
              v-for="stat in stats"
              :key="stat.label"
              class="bg-white/5 backdrop-blur-sm rounded-2xl p-6 border border-white/10 hover:border-purple-500/50 transition-colors"
            >
              <span class="text-3xl mb-2 block">{{ stat.icon }}</span>
              <p class="text-3xl font-bold text-white mb-1">{{ stat.value }}</p>
              <p class="text-white/50 text-sm">{{ stat.label }}</p>
            </div>
          </div>
        </section>

        <section>
          <h3 class="text-xl font-bold text-white mb-4">Actividad Reciente</h3>
          <div class="bg-white/5 backdrop-blur-sm rounded-2xl border border-white/10 overflow-hidden">
            <div
              v-for="(activity, index) in recentActivity"
              :key="index"
              class="flex items-center gap-4 p-4 border-b border-white/5 last:border-0"
            >
              <div class="w-12 h-12 rounded-xl bg-gradient-to-br from-purple-500 to-violet-600 flex items-center justify-center text-xl">
                <span v-if="activity.type === 'played'">🎵</span>
                <span v-else-if="activity.type === 'liked'">❤️</span>
                <span v-else>📋</span>
              </div>
              <div class="flex-1 min-w-0">
                <p class="text-white font-medium truncate">{{ activity.track }}</p>
                <p v-if="activity.artist" class="text-white/50 text-sm truncate">{{ activity.artist }}</p>
              </div>
              <span class="text-white/40 text-sm">{{ activity.time }}</span>
            </div>
          </div>
        </section>

        <section>
          <div class="flex items-center justify-between mb-4">
            <h3 class="text-xl font-bold text-white">Tus Playlists</h3>
            <button class="text-purple-400 hover:text-purple-300 text-sm">Ver todas</button>
          </div>
          <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
            <div
              v-for="playlist in playlists"
              :key="playlist.name"
              class="group cursor-pointer"
            >
              <div class="relative aspect-square rounded-xl overflow-hidden mb-3 shadow-lg group-hover:shadow-xl transition-shadow">
                <img
                  :src="playlist.cover"
                  :alt="playlist.name"
                  class="w-full h-full object-cover group-hover:scale-110 transition-transform duration-500"
                />
                <div class="absolute inset-0 bg-black/40 opacity-0 group-hover:opacity-100 transition-opacity flex items-center justify-center">
                  <div class="w-14 h-14 rounded-full bg-purple-500 flex items-center justify-center shadow-lg">
                    <svg class="w-7 h-7 text-white" fill="currentColor" viewBox="0 0 24 24">
                      <path d="M8 5v14l11-7z"/>
                    </svg>
                  </div>
                </div>
              </div>
              <h4 class="text-white font-medium truncate group-hover:text-purple-400 transition-colors">
                {{ playlist.name }}
              </h4>
              <p class="text-white/50 text-sm">{{ playlist.count }} canciones</p>
            </div>
          </div>
        </section>
      </div>

      <div v-else-if="activeTab === 'playlists'" class="space-y-6">
        <div class="flex items-center justify-between">
          <h3 class="text-xl font-bold text-white">Tus Playlists</h3>
          <button class="bg-purple-500 text-white px-4 py-2 rounded-full hover:bg-purple-600 transition-colors flex items-center gap-2">
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4"/>
            </svg>
            Nueva Playlist
          </button>
        </div>
        <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
          <div
            v-for="playlist in playlists"
            :key="playlist.name"
            class="group cursor-pointer"
          >
            <div class="relative aspect-square rounded-xl overflow-hidden mb-3 shadow-lg">
              <img
                :src="playlist.cover"
                :alt="playlist.name"
                class="w-full h-full object-cover group-hover:scale-110 transition-transform duration-500"
              />
            </div>
            <h4 class="text-white font-medium truncate">{{ playlist.name }}</h4>
            <p class="text-white/50 text-sm">{{ playlist.count }} canciones</p>
          </div>
        </div>
      </div>

      <div v-else-if="activeTab === 'favorites'" class="space-y-6">
        <div class="flex items-center justify-between">
          <h3 class="text-xl font-bold text-white">Tus Favoritos</h3>
        </div>
        <div class="bg-white/5 backdrop-blur-sm rounded-2xl border border-white/10 overflow-hidden">
          <div class="divide-y divide-white/5">
            <div
              v-for="track in musicStore.playlist.slice(0, 5)"
              :key="track.id"
              @click="musicStore.playTrack(track)"
              class="flex items-center gap-4 p-4 hover:bg-white/5 cursor-pointer transition-colors"
            >
              <img :src="track.cover" :alt="track.title" class="w-12 h-12 rounded-lg object-cover" />
              <div class="flex-1 min-w-0">
                <p class="text-white font-medium truncate">{{ track.title }}</p>
                <p class="text-white/50 text-sm truncate">{{ track.artist }}</p>
              </div>
              <span class="text-white/40 text-sm">{{ musicStore.formatTime(track.duration) }}</span>
              <button class="text-purple-400">
                <svg class="w-6 h-6" fill="currentColor" viewBox="0 0 24 24">
                  <path d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z"/>
                </svg>
              </button>
            </div>
          </div>
        </div>
      </div>

      <div v-else-if="activeTab === 'history'" class="space-y-6">
        <div class="flex items-center justify-between">
          <h3 class="text-xl font-bold text-white">Historial</h3>
          <button class="text-purple-400 hover:text-purple-300 text-sm">Limpiar historial</button>
        </div>
        <div class="bg-white/5 backdrop-blur-sm rounded-2xl border border-white/10 overflow-hidden">
          <div class="divide-y divide-white/5">
            <div
              v-for="activity in recentActivity"
              :key="activity.time"
              class="flex items-center gap-4 p-4"
            >
              <div class="w-10 h-10 rounded-lg bg-gradient-to-br from-purple-500 to-violet-600 flex items-center justify-center">
                🎵
              </div>
              <div class="flex-1 min-w-0">
                <p class="text-white font-medium truncate">{{ activity.track }}</p>
                <p class="text-white/50 text-sm truncate">{{ activity.artist }}</p>
              </div>
              <span class="text-white/40 text-sm">{{ activity.time }}</span>
            </div>
          </div>
        </div>
      </div>

      <div v-else-if="activeTab === 'settings'" class="space-y-6">
        <div class="bg-white/5 backdrop-blur-sm rounded-2xl border border-white/10 p-6">
          <h3 class="text-xl font-bold text-white mb-6">Configuración de Cuenta</h3>
          
          <div class="space-y-6">
            <div>
              <label class="block text-white/60 text-sm mb-2">Nombre</label>
              <input
                :value="authStore.currentUser?.name"
                type="text"
                class="w-full bg-white/5 border border-white/10 rounded-xl px-4 py-3 text-white focus:outline-none focus:ring-2 focus:ring-purple-500"
              />
            </div>
            
            <div>
              <label class="block text-white/60 text-sm mb-2">Email</label>
              <input
                :value="authStore.currentUser?.email"
                type="email"
                class="w-full bg-white/5 border border-white/10 rounded-xl px-4 py-3 text-white focus:outline-none focus:ring-2 focus:ring-purple-500"
                disabled
              />
            </div>

            <div>
              <label class="block text-white/60 text-sm mb-2">Tema</label>
              <button
                @click="themeStore.toggleTheme"
                class="flex items-center gap-3 bg-white/5 border border-white/10 rounded-xl px-4 py-3 hover:border-purple-500/50 transition-colors"
              >
                <span v-if="themeStore.isDark" class="text-xl">☀️</span>
                <span v-else class="text-xl">🌙</span>
                <span class="text-white">{{ themeStore.isDark ? 'Modo Oscuro' : 'Modo Claro' }}</span>
              </button>
            </div>

            <button class="bg-purple-500 text-white px-6 py-3 rounded-xl hover:bg-purple-600 transition-colors">
              Guardar Cambios
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>