<script setup>
import { ref, onMounted, onUnmounted } from 'vue'

const canvas = ref(null)
let animationId = null
let ctx = null
let width = 0
let height = 0

function initCanvas() {
  const canvasEl = canvas.value
  if (!canvasEl) return
  
  ctx = canvasEl.getContext('2d')
  resizeCanvas()
  
  window.addEventListener('resize', resizeCanvas)
  animate()
}

function resizeCanvas() {
  const canvasEl = canvas.value
  if (!canvasEl) return
  
  width = canvasEl.width = window.innerWidth
  height = canvasEl.height = window.innerHeight
}

function animate() {
  if (!ctx) return
  
  ctx.clearRect(0, 0, width, height)
  
  const time = Date.now() * 0.001
  const isDark = document.documentElement.classList.contains('dark')
  
  for (let i = 0; i < 5; i++) {
    ctx.beginPath()
    
    const yOffset = height / 2 + Math.sin(time + i * 0.5) * 50
    const amplitude = 50 + i * 20
    const frequency = 0.01 - i * 0.001
    const opacity = 0.1 - i * 0.015
    
    ctx.moveTo(0, height)
    
    for (let x = 0; x <= width; x += 5) {
      const y = yOffset + Math.sin(x * frequency + time) * amplitude
      ctx.lineTo(x, y)
    }
    
    ctx.lineTo(width, height)
    ctx.closePath()
    
    const gradient = ctx.createLinearGradient(0, 0, width, 0)
    if (isDark) {
      gradient.addColorStop(0, `rgba(168, 85, 247, ${opacity})`)
      gradient.addColorStop(0.5, `rgba(147, 51, 234, ${opacity})`)
      gradient.addColorStop(1, `rgba(126, 34, 206, ${opacity})`)
    } else {
      gradient.addColorStop(0, `rgba(192, 132, 252, ${opacity})`)
      gradient.addColorStop(0.5, `rgba(168, 85, 247, ${opacity})`)
      gradient.addColorStop(1, `rgba(147, 51, 234, ${opacity})`)
    }
    
    ctx.fillStyle = gradient
    ctx.fill()
  }
  
  animationId = requestAnimationFrame(animate)
}

onMounted(() => {
  initCanvas()
})

onUnmounted(() => {
  if (animationId) cancelAnimationFrame(animationId)
  window.removeEventListener('resize', resizeCanvas)
})
</script>

<template>
  <canvas ref="canvas" class="fixed inset-0 w-full h-full pointer-events-none" />
</template>
