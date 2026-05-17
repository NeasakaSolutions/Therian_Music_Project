import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import { fetchCancionesHome, fetchCanciones } from '@/services/api'

export const useMusicStore = defineStore('music', () => {
  const currentTrack = ref(null)
  const isPlaying = ref(false)
  const currentTime = ref(0)
  const duration = ref(0)
  const volume = ref(0.7)
  const isMuted = ref(false)
  const repeat = ref('none')
  const shuffle = ref(false)

  const playlist = ref([])
  const homeTracks = ref([])
  const loading = ref(false)

  const searchQuery = ref('')

  async function loadHomeTracks() {
    try {
      const data = await fetchCancionesHome()
      homeTracks.value = data.data.map(mapTrack)
    } catch {
      homeTracks.value = []
    }
  }

  async function loadPlaylist() {
    loading.value = true
    try {
      const data = await fetchCanciones(1, 20)
      playlist.value = data.data.map(mapTrack)
    } catch {
      useMockPlaylist()
    }
    loading.value = false
  }

  function mapTrack(item) {
    return {
      id: item.id,
      title: item.nombre,
      artist: item.artista,
      album: item.categoria,
      duration: 200,
      cover: item.imagen || `https://picsum.photos/seed/music${item.id}/300/300`,
      src: item.cancion || '',
      slug: item.slug,
      description: item.descripcion,
      date: item.fecha,
      userId: item.user_id,
    }
  }

  function useMockPlaylist() {
    playlist.value = [
      { id: 1, title: 'Midnight Dreams', artist: 'Luna Eclipse', album: 'Nocturnal', duration: 234, cover: 'https://picsum.photos/seed/music1/300/300', src: 'https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3' },
      { id: 2, title: 'Electric Pulse', artist: 'Neon Waves', album: 'Synthwave', duration: 198, cover: 'https://picsum.photos/seed/music2/300/300', src: 'https://www.soundhelix.com/examples/mp3/SoundHelix-Song-2.mp3' },
      { id: 3, title: 'Starlight Serenade', artist: 'Cosmic Echo', album: 'Galaxy', duration: 267, cover: 'https://picsum.photos/seed/music3/300/300', src: 'https://www.soundhelix.com/examples/mp3/SoundHelix-Song-3.mp3' },
      { id: 4, title: 'Ocean Breeze', artist: 'Wave Rider', album: 'Tropical', duration: 212, cover: 'https://picsum.photos/seed/music4/300/300', src: 'https://www.soundhelix.com/examples/mp3/SoundHelix-Song-4.mp3' },
      { id: 5, title: 'Urban Jungle', artist: 'City Lights', album: 'Metropolis', duration: 245, cover: 'https://picsum.photos/seed/music5/300/300', src: 'https://www.soundhelix.com/examples/mp3/SoundHelix-Song-5.mp3' },
      { id: 6, title: 'Crystal Cascade', artist: 'Aurora Sound', album: 'Ethereal', duration: 189, cover: 'https://picsum.photos/seed/music6/300/300', src: 'https://www.soundhelix.com/examples/mp3/SoundHelix-Song-6.mp3' },
      { id: 7, title: 'Neon Nights', artist: 'Synth Masters', album: 'Retro', duration: 256, cover: 'https://picsum.photos/seed/music7/300/300', src: 'https://www.soundhelix.com/examples/mp3/SoundHelix-Song-7.mp3' },
      { id: 8, title: 'Sunset Boulevard', artist: 'Golden Hour', album: 'Sunrise', duration: 203, cover: 'https://picsum.photos/seed/music8/300/300', src: 'https://www.soundhelix.com/examples/mp3/SoundHelix-Song-8.mp3' },
      { id: 9, title: 'Digital Dreams', artist: 'Cyber Orchestra', album: 'Digital', duration: 278, cover: 'https://picsum.photos/seed/music9/300/300', src: 'https://www.soundhelix.com/examples/mp3/SoundHelix-Song-9.mp3' },
      { id: 10, title: 'Rainbow Sky', artist: 'Prism', album: 'Colors', duration: 221, cover: 'https://picsum.photos/seed/music10/300/300', src: 'https://www.soundhelix.com/examples/mp3/SoundHelix-Song-10.mp3' },
      { id: 11, title: 'Deep Forest', artist: 'Nature Sounds', album: 'Forest', duration: 289, cover: 'https://picsum.photos/seed/music11/300/300', src: 'https://www.soundhelix.com/examples/mp3/SoundHelix-Song-11.mp3' },
      { id: 12, title: 'Mountain Echo', artist: 'Alpine', album: 'Peaks', duration: 245, cover: 'https://picsum.photos/seed/music12/300/300', src: 'https://www.soundhelix.com/examples/mp3/SoundHelix-Song-12.mp3' },
    ]
  }

  const filteredPlaylist = computed(() => {
    if (!searchQuery.value) return playlist.value.length ? playlist.value : homeTracks.value
    const query = searchQuery.value.toLowerCase()
    const source = playlist.value.length ? playlist.value : homeTracks.value
    return source.filter(
      track => track.title?.toLowerCase().includes(query) ||
               track.artist?.toLowerCase().includes(query) ||
               track.album?.toLowerCase().includes(query)
    )
  })

  function playTrack(track) {
    currentTrack.value = track
    isPlaying.value = true
    currentTime.value = 0
  }

  function togglePlay() {
    isPlaying.value = !isPlaying.value
  }

  function nextTrack() {
    if (!currentTrack.value) return
    const source = playlist.value.length ? playlist.value : homeTracks.value
    const currentIndex = source.findIndex(t => t.id === currentTrack.value.id)
    const nextIndex = (currentIndex + 1) % source.length
    playTrack(source[nextIndex])
  }

  function prevTrack() {
    if (!currentTrack.value) return
    const source = playlist.value.length ? playlist.value : homeTracks.value
    const currentIndex = source.findIndex(t => t.id === currentTrack.value.id)
    const prevIndex = (currentIndex - 1 + source.length) % source.length
    playTrack(source[prevIndex])
  }

  function setVolume(value) {
    volume.value = value
    isMuted.value = value === 0
  }

  function toggleMute() {
    isMuted.value = !isMuted.value
  }

  function toggleShuffle() {
    shuffle.value = !shuffle.value
  }

  function toggleRepeat() {
    const modes = ['none', 'one', 'all']
    const currentIndex = modes.indexOf(repeat.value)
    repeat.value = modes[(currentIndex + 1) % modes.length]
  }

  function formatTime(seconds) {
    const mins = Math.floor(seconds / 60)
    const secs = Math.floor(seconds % 60)
    return `${mins}:${secs.toString().padStart(2, '0')}`
  }

  return {
    playlist,
    homeTracks,
    currentTrack,
    isPlaying,
    currentTime,
    duration,
    volume,
    isMuted,
    repeat,
    shuffle,
    searchQuery,
    filteredPlaylist,
    loading,
    loadHomeTracks,
    loadPlaylist,
    playTrack,
    togglePlay,
    nextTrack,
    prevTrack,
    setVolume,
    toggleMute,
    toggleShuffle,
    toggleRepeat,
    formatTime,
  }
})