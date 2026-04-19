<script setup>
import { ref, watch, onMounted, onUnmounted } from 'vue'
import { useMusicStore } from '@/stores/music'

const musicStore = useMusicStore()
const audio = ref(null)
const progressBar = ref(null)
const isDragging = ref(false)

onMounted(() => {
  audio.value = new Audio()
  audio.value.volume = musicStore.volume

  audio.value.addEventListener('timeupdate', updateProgress)
  audio.value.addEventListener('loadedmetadata', () => {
    musicStore.duration = audio.value.duration
  })
  audio.value.addEventListener('ended', handleEnded)
})

onUnmounted(() => {
  if (audio.value) {
    audio.value.pause()
    audio.value.src = ''
  }
})

watch(() => musicStore.currentTrack, (newTrack) => {
  if (audio.value && newTrack) {
    audio.value.src = newTrack.src
    audio.value.play().catch(() => {})
  }
})

watch(() => musicStore.isPlaying, (playing) => {
  if (audio.value) {
    if (playing) {
      audio.value.play().catch(() => {})
    } else {
      audio.value.pause()
    }
  }
})

watch(() => musicStore.volume, (vol) => {
  if (audio.value) {
    audio.value.volume = vol
  }
})

function updateProgress() {
  if (audio.value && !isDragging.value) {
    musicStore.currentTime = audio.value.currentTime
  }
}

function handleEnded() {
  if (musicStore.repeat === 'one') {
    audio.value.currentTime = 0
    audio.value.play()
  } else if (musicStore.repeat === 'all') {
    musicStore.nextTrack()
  } else {
    musicStore.nextTrack()
  }
}

function seekTo(event) {
  if (progressBar.value && audio.value) {
    const rect = progressBar.value.getBoundingClientRect()
    const percent = (event.clientX - rect.left) / rect.width
    audio.value.currentTime = percent * audio.value.duration
  }
}

function startDrag(event) {
  isDragging.value = true
  seekTo(event)
}

function onDrag(event) {
  if (isDragging.value) {
    seekTo(event)
  }
}

function endDrag() {
  isDragging.value = false
}
</script>

<template>
  <div v-if="musicStore.currentTrack" class="fixed bottom-0 left-0 right-0 z-50 bg-black/90 backdrop-blur-xl border-t border-white/10">
    <div 
      class="h-1 bg-white/20 cursor-pointer group"
      @mousedown="startDrag"
      @mousemove="onDrag"
      @mouseup="endDrag"
      @mouseleave="endDrag"
      ref="progressBar"
    >
      <div 
        class="h-full bg-gradient-to-r from-purple-500 to-violet-500 relative group-hover:h-1.5 transition-all"
        :style="{ width: `${(musicStore.currentTime / musicStore.duration) * 100 || 0}%` }"
      >
        <div class="absolute right-0 top-1/2 -translate-y-1/2 w-3 h-3 bg-white rounded-full opacity-0 group-hover:opacity-100 transition-opacity shadow-lg"></div>
      </div>
    </div>

    <div class="max-w-7xl mx-auto px-4 py-3">
      <div class="flex items-center justify-between gap-4">
        <div class="flex items-center gap-4 min-w-0 flex-1">
          <img
            :src="musicStore.currentTrack.cover"
            :alt="musicStore.currentTrack.title"
            class="w-14 h-14 rounded-lg object-cover shadow-lg"
          />
          <div class="min-w-0">
            <h4 class="text-white font-medium truncate">{{ musicStore.currentTrack.title }}</h4>
            <p class="text-white/60 text-sm truncate">{{ musicStore.currentTrack.artist }}</p>
          </div>
        </div>

        <div class="flex items-center gap-4">
          <button
            @click="musicStore.toggleShuffle"
            class="text-white/60 hover:text-white transition-colors"
            :class="{ 'text-purple-400': musicStore.shuffle }"
          >
            <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 24 24">
              <path d="M10.59 9.17L5.41 4 4 5.41l5.17 5.17 1.42-1.41zM14.5 4l2.04 2.04L4 18.59 5.41 20 17.96 7.46 20 9.5V4h-5.5zm.33 9.41l-1.41 1.41 3.13 3.13L14.5 20H20v-5.5l-2.04 2.04-3.13-3.13z"/>
            </svg>
          </button>

          <button @click="musicStore.prevTrack" class="text-white hover:text-purple-400 transition-colors">
            <svg class="w-8 h-8" fill="currentColor" viewBox="0 0 24 24">
              <path d="M6 6h2v12H6zm3.5 6l8.5 6V6z"/>
            </svg>
          </button>

          <button
            @click="musicStore.togglePlay"
            class="w-12 h-12 rounded-full bg-white flex items-center justify-center hover:scale-110 transition-transform shadow-lg"
          >
            <svg v-if="musicStore.isPlaying" class="w-6 h-6 text-black ml-0.5" fill="currentColor" viewBox="0 0 24 24">
              <path d="M6 19h4V5H6v14zm8-14v14h4V5h-4z"/>
            </svg>
            <svg v-else class="w-6 h-6 text-black ml-1" fill="currentColor" viewBox="0 0 24 24">
              <path d="M8 5v14l11-7z"/>
            </svg>
          </button>

          <button @click="musicStore.nextTrack" class="text-white hover:text-purple-400 transition-colors">
            <svg class="w-8 h-8" fill="currentColor" viewBox="0 0 24 24">
              <path d="M6 18l8.5-6L6 6v12zM16 6v12h2V6h-2z"/>
            </svg>
          </button>

          <button
            @click="musicStore.toggleRepeat"
            class="text-white/60 hover:text-white transition-colors relative"
            :class="{ 'text-purple-400': musicStore.repeat !== 'none' }"
          >
            <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 24 24">
              <path d="M7 7h10v3l4-4-4-4v3H5v6h2V7zm10 10H7v-3l-4 4 4 4v-3h12v-6h-2v4z"/>
            </svg>
            <span v-if="musicStore.repeat === 'one'" class="absolute -top-1 -right-1 text-[8px] font-bold">1</span>
          </button>
        </div>

        <div class="hidden md:flex items-center gap-3 flex-1 justify-end">
          <span class="text-white/60 text-sm min-w-12 text-right">
            {{ musicStore.formatTime(musicStore.currentTime) }}
          </span>
          
          <button @click="musicStore.toggleMute" class="text-white/60 hover:text-white transition-colors">
            <svg v-if="musicStore.isMuted || musicStore.volume === 0" class="w-5 h-5" fill="currentColor" viewBox="0 0 24 24">
              <path d="M16.5 12c0-1.77-1.02-3.29-2.5-4.03v2.21l2.45 2.45c.03-.2.05-.41.05-.63zm2.5 0c0 .94-.2 1.82-.54 2.64l1.51 1.51C20.63 14.91 21 13.5 21 12c0-4.28-2.99-7.86-7-8.77v2.06c2.89.86 5 3.54 5 6.71zM4.27 3L3 4.27 7.73 9H3v6h4l5 5v-6.73l4.25 4.25c-.67.52-1.42.93-2.25 1.18v2.06c1.38-.31 2.63-.95 3.69-1.81L19.73 21 21 19.73l-9-9L4.27 3zM12 4L9.91 6.09 12 8.18V4z"/>
            </svg>
            <svg v-else-if="musicStore.volume < 0.5" class="w-5 h-5" fill="currentColor" viewBox="0 0 24 24">
              <path d="M18.5 12c0-1.77-1.02-3.29-2.5-4.03v8.05c1.48-.73 2.5-2.25 2.5-4.02zM5 9v6h4l5 5V4L9 9H5z"/>
            </svg>
            <svg v-else class="w-5 h-5" fill="currentColor" viewBox="0 0 24 24">
              <path d="M3 9v6h4l5 5V4L7 9H3zm13.5 3c0-1.77-1.02-3.29-2.5-4.03v8.05c1.48-.73 2.5-2.25 2.5-4.02zM14 3.23v2.06c2.89.86 5 3.54 5 6.71s-2.11 5.85-5 6.71v2.06c4.01-.91 7-4.49 7-8.77s-2.99-7.86-7-8.77z"/>
            </svg>
          </button>

          <input
            type="range"
            min="0"
            max="1"
            step="0.01"
            :value="musicStore.isMuted ? 0 : musicStore.volume"
            @input="musicStore.setVolume(parseFloat($event.target.value))"
            class="w-24 h-1 bg-white/20 rounded-full appearance-none cursor-pointer accent-purple-500"
          />

          <span class="text-white/60 text-sm min-w-12">
            {{ musicStore.formatTime(musicStore.duration) }}
          </span>
        </div>
      </div>
    </div>
  </div>
</template>
