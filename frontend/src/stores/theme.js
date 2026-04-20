import { ref } from 'vue'
import { defineStore } from 'pinia'

export const useThemeStore = defineStore('theme', () => {
  const stored = localStorage.getItem('theme')
  const defaultIsDark = stored === null ? true : JSON.parse(stored)
  
  const isDark = ref(defaultIsDark)
  
  function toggleTheme() {
    isDark.value = !isDark.value
    localStorage.setItem('theme', JSON.stringify(isDark.value))
    applyTheme()
  }

  function applyTheme() {
    if (isDark.value) {
      document.documentElement.classList.add('dark')
      document.documentElement.classList.remove('light')
    } else {
      document.documentElement.classList.add('light')
      document.documentElement.classList.remove('dark')
    }
  }

  applyTheme()

  return { isDark, toggleTheme, applyTheme }
})