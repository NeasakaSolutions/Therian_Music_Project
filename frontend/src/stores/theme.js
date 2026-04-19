import { ref, watch } from 'vue'
import { defineStore } from 'pinia'

export const useThemeStore = defineStore('theme', () => {
  const isDark = ref(JSON.parse(localStorage.getItem('theme')) ?? true)
  
  function toggleTheme() {
    isDark.value = !isDark.value
    localStorage.setItem('theme', JSON.stringify(isDark.value))
  }

  watch(isDark, (value) => {
    document.documentElement.classList.toggle('dark', value)
  }, { immediate: true })

  return { isDark, toggleTheme }
})
