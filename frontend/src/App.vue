<script setup>
import { useThemeStore } from '@/stores/theme'
import WavesBackground from '@/components/WavesBackground.vue'
import Navbar from '@/components/Navbar.vue'
import MusicPlayer from '@/components/MusicPlayer.vue'

const themeStore = useThemeStore()
</script>

<template>
  <div :class="{ 'dark': themeStore.isDark }" class="min-h-screen transition-colors duration-300">
    <WavesBackground />
    <Navbar />
    <router-view />
    <MusicPlayer />
  </div>
</template>

<style scoped>
.dark {
  color-scheme: dark;
}
</style>
