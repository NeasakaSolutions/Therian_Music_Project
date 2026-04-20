<script setup>
import { ref, onMounted, onUnmounted, computed } from 'vue'

const props = defineProps({
  items: {
    type: Array,
    required: true
  }
})

const emit = defineEmits(['select'])

const container = ref(null)
const currentIndex = ref(0)
const itemsPerView = ref(4)
let autoplayInterval = null

function updateItemsPerView() {
  if (window.innerWidth < 640) itemsPerView.value = 2
  else if (window.innerWidth < 768) itemsPerView.value = 3
  else if (window.innerWidth < 1024) itemsPerView.value = 4
  else if (window.innerWidth < 1280) itemsPerView.value = 5
  else itemsPerView.value = 6
}

const maxIndex = computed(() => props.items.length - itemsPerView.value)

function next() {
  if (maxIndex.value <= 0) return
  currentIndex.value = currentIndex.value >= maxIndex.value ? 0 : currentIndex.value + 1
}

function prev() {
  if (maxIndex.value <= 0) return
  currentIndex.value = currentIndex.value <= 0 ? maxIndex.value : currentIndex.value - 1
}

function goTo(index) {
  currentIndex.value = index
}

function startAutoplay() {
  stopAutoplay()
  autoplayInterval = setInterval(next, 3000)
}

function stopAutoplay() {
  if (autoplayInterval) {
    clearInterval(autoplayInterval)
    autoplayInterval = null
  }
}

onMounted(() => {
  updateItemsPerView()
  window.addEventListener('resize', updateItemsPerView)
  startAutoplay()
})

onUnmounted(() => {
  window.removeEventListener('resize', updateItemsPerView)
  stopAutoplay()
})
</script>

<template>
  <div 
    class="relative"
    @mouseenter="stopAutoplay"
    @mouseleave="startAutoplay"
  >
    <div class="overflow-hidden" ref="container">
      <div 
        class="flex transition-transform duration-500 ease-out"
        :style="{ transform: `translateX(-${currentIndex * (100 / itemsPerView)}%)` }"
      >
        <div
          v-for="item in items"
          :key="item.id"
          class="flex-shrink-0 px-2"
          :style="{ width: `${100 / itemsPerView}%` }"
          @click="emit('select', item)"
        >
          <slot :item="item" />
        </div>
      </div>
    </div>

    <button
      v-if="maxIndex > 0"
      @click="prev"
      class="absolute left-0 top-1/2 -translate-y-1/2 -translate-x-2 w-10 h-10 rounded-full bg-black/50 backdrop-blur-sm flex items-center justify-center opacity-0 hover:opacity-100 transition-opacity z-10"
    >
      <svg class="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7"/>
      </svg>
    </button>

    <button
      v-if="maxIndex > 0"
      @click="next"
      class="absolute right-0 top-1/2 -translate-y-1/2 translate-x-2 w-10 h-10 rounded-full bg-black/50 backdrop-blur-sm flex items-center justify-center opacity-0 hover:opacity-100 transition-opacity z-10"
    >
      <svg class="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"/>
      </svg>
    </button>

    <div v-if="maxIndex > 0" class="flex justify-center gap-2 mt-4">
      <button
        v-for="(_, index) in items.slice(0, maxIndex + 1)"
        :key="index"
        @click="goTo(index)"
        class="w-2 h-2 rounded-full transition-all"
        :class="index === currentIndex ? 'bg-purple-500 w-6' : 'bg-white/30 hover:bg-white/50'"
      />
    </div>
  </div>
</template>