<script setup>
import { useMusicStore } from '@/stores/music'

const props = defineProps({
  track: {
    type: Object,
    required: true
  }
})

const musicStore = useMusicStore()

function playTrack() {
  musicStore.playTrack(props.track)
}
</script>

<template>
  <div
    @click="playTrack"
    class="group flex items-center gap-4 p-3 rounded-xl hover:bg-white/10 dark:hover:bg-white/5 cursor-pointer transition-all"
    :class="{ 'bg-purple-500/20': musicStore.currentTrack?.id === track.id }"
  >
    <div class="relative flex-shrink-0">
      <img
        :src="track.cover"
        :alt="track.title"
        class="w-14 h-14 rounded-lg object-cover shadow-md group-hover:shadow-lg transition-shadow"
      />
      <div class="absolute inset-0 bg-black/40 rounded-lg opacity-0 group-hover:opacity-100 transition-opacity flex items-center justify-center">
        <div v-if="musicStore.currentTrack?.id === track.id && musicStore.isPlaying" class="flex gap-0.5">
          <span class="w-1 h-4 bg-purple-400 rounded-full animate-pulse"></span>
          <span class="w-1 h-6 bg-purple-400 rounded-full animate-pulse" style="animation-delay: 0.1s"></span>
          <span class="w-1 h-3 bg-purple-400 rounded-full animate-pulse" style="animation-delay: 0.2s"></span>
        </div>
        <svg v-else class="w-6 h-6 text-white" fill="currentColor" viewBox="0 0 24 24">
          <path d="M8 5v14l11-7z"/>
        </svg>
      </div>
    </div>

    <div class="min-w-0 flex-1">
      <h4 class="text-white font-medium truncate group-hover:text-purple-400 transition-colors">
        {{ track.title }}
      </h4>
      <p class="text-white/50 text-sm truncate">{{ track.artist }}</p>
    </div>

    <div class="flex items-center gap-4">
      <span class="text-white/40 text-sm hidden sm:block">{{ track.album }}</span>
      <span class="text-white/60 text-sm">{{ musicStore.formatTime(track.duration) }}</span>
      <button class="p-2 rounded-full hover:bg-white/10 opacity-0 group-hover:opacity-100 transition-all">
        <svg class="w-5 h-5 text-white/60 hover:text-purple-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z"/>
        </svg>
      </button>
    </div>
  </div>
</template>
