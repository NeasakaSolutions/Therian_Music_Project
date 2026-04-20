<script setup>
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { useThemeStore } from '@/stores/theme'
import { useMusicStore } from '@/stores/music'
import TrackCard from '@/components/TrackCard.vue'
import Carousel from '@/components/Carousel.vue'

const router = useRouter()
const authStore = useAuthStore()
const themeStore = useThemeStore()
const musicStore = useMusicStore()

function handleTrackSelect(track) {
  musicStore.playTrack(track)
}
</script>

<template>
  <div class="pt-20 pb-32 min-h-screen">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="mb-8 flex items-center justify-between">
        <div>
          <h2 class="text-3xl font-bold bg-gradient-to-r from-purple-400 to-violet-500 bg-clip-text text-transparent mb-2">
            {{ authStore.isAuthenticated ? `¡Hola, ${authStore.currentUser?.name}!` : 'Explora la música' }}
          </h2>
          <p class="text-white/60">
            {{ authStore.isAuthenticated ? 'Aquí está tu biblioteca musical' : 'Disfruta de las mejores canciones' }}
          </p>
        </div>
        
        <router-link
          v-if="!authStore.isAuthenticated"
          to="/login"
          class="hidden sm:flex items-center gap-2 bg-purple-500/20 text-purple-400 px-4 py-2 rounded-full hover:bg-purple-500/30 transition-colors"
        >
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"/>
          </svg>
          <span>Iniciar Sesión</span>
        </router-link>
      </div>

      <div v-if="musicStore.searchQuery" class="mb-8">
        <h3 class="text-xl font-semibold text-white mb-2">
          Resultados para "{{ musicStore.searchQuery }}"
        </h3>
        <p class="text-white/50">
          {{ musicStore.filteredPlaylist.length }} canciones encontradas
        </p>
      </div>

      <div v-if="musicStore.filteredPlaylist.length === 0 && musicStore.searchQuery" class="text-center py-16">
        <div class="w-20 h-20 mx-auto mb-4 rounded-full bg-white/5 flex items-center justify-center">
          <svg class="w-10 h-10 text-white/30" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19V6l12-3v13M9 19c0 1.105-1.343 2-3 2s-3-.895-3-2 1.343-2 3-2 3 .895 3 2zm12-3c0 1.105-1.343 2-3 2s-3-.895-3-2 1.343-2 3-2 3 .895 3 2zM9 10l12-3"/>
          </svg>
        </div>
        <h3 class="text-xl font-medium text-white mb-2">No se encontraron canciones</h3>
        <p class="text-white/50">Intenta con otro término de búsqueda</p>
      </div>

      <div v-else class="space-y-8">
        <section>
          <h3 class="text-xl font-bold text-white mb-4 flex items-center gap-2">
            <span class="w-8 h-8 rounded-lg bg-gradient-to-br from-purple-500 to-violet-600 flex items-center justify-center text-sm">🔥</span>
            Tendencias
          </h3>
          <div class="bg-white/5 backdrop-blur-sm rounded-2xl border border-white/10 overflow-hidden">
            <div class="grid grid-cols-[auto_1fr_auto] gap-4 p-4 text-white/40 text-sm border-b border-white/10">
              <span class="w-14"></span>
              <span>TÍTULO</span>
              <span class="hidden sm:block">ÁLBUM</span>
              <span class="text-right pr-8">��</span>
            </div>
            
            <div class="divide-y divide-white/5">
              <TrackCard
                v-for="track in musicStore.filteredPlaylist.slice(0, 3)"
                :key="track.id"
                :track="track"
              />
            </div>
          </div>
        </section>

        <section>
          <h3 class="text-xl font-bold text-white mb-4 flex items-center gap-2">
            <span class="w-8 h-8 rounded-lg bg-gradient-to-br from-pink-500 to-rose-600 flex items-center justify-center text-sm">✨</span>
            Recomendados para ti
          </h3>
          <Carousel :items="musicStore.playlist" @select="handleTrackSelect">
            <template #default="{ item }">
              <div class="group cursor-pointer">
                <div class="relative aspect-square rounded-xl overflow-hidden mb-2 shadow-lg group-hover:shadow-xl transition-shadow">
                  <img
                    :src="item.cover"
                    :alt="item.title"
                    class="w-full h-full object-cover group-hover:scale-110 transition-transform duration-500"
                  />
                  <div class="absolute inset-0 bg-black/40 opacity-0 group-hover:opacity-100 transition-opacity flex items-center justify-center">
                    <div class="w-12 h-12 rounded-full bg-purple-500 flex items-center justify-center shadow-lg transform scale-90 group-hover:scale-100 transition-transform">
                      <svg class="w-6 h-6 text-white ml-1" fill="currentColor" viewBox="0 0 24 24">
                        <path d="M8 5v14l11-7z"/>
                      </svg>
                    </div>
                  </div>
                </div>
                <h4 class="text-white font-medium truncate group-hover:text-purple-400 transition-colors">
                  {{ item.title }}
                </h4>
                <p class="text-white/50 text-sm truncate">{{ item.artist }}</p>
              </div>
            </template>
          </Carousel>
        </section>

        <section>
          <h3 class="text-xl font-bold text-white mb-4 flex items-center gap-2">
            <span class="w-8 h-8 rounded-lg bg-gradient-to-br from-amber-500 to-orange-600 flex items-center justify-center text-sm">🎧</span>
            Todas las canciones
          </h3>
          <div class="bg-white/5 backdrop-blur-sm rounded-2xl border border-white/10 overflow-hidden">
            <div class="divide-y divide-white/5">
              <TrackCard
                v-for="track in musicStore.filteredPlaylist"
                :key="track.id"
                :track="track"
              />
            </div>
          </div>
        </section>
      </div>
    </div>
  </div>
</template>