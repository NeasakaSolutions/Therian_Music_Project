import { ref, computed } from 'vue'
import { defineStore } from 'pinia'

export const useMusicStore = defineStore('music', () => {
  const currentTrack = ref(null)
  const isPlaying = ref(false)
  const currentTime = ref(0)
  const duration = ref(0)
  const volume = ref(0.7)
  const isMuted = ref(false)
  const repeat = ref('none')
  const shuffle = ref(false)

  const playlist = ref([
    {
      id: 1,
      title: 'Midnight Dreams',
      artist: 'Luna Eclipse',
      album: 'Nocturnal',
      duration: 234,
      cover: 'https://picsum.photos/seed/music1/300/300',
      src: 'https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3'
    },
    {
      id: 2,
      title: 'Electric Pulse',
      artist: 'Neon Waves',
      album: 'Synthwave',
      duration: 198,
      cover: 'https://picsum.photos/seed/music2/300/300',
      src: 'https://www.soundhelix.com/examples/mp3/SoundHelix-Song-2.mp3'
    },
    {
      id: 3,
      title: 'Starlight Serenade',
      artist: 'Cosmic Echo',
      album: 'Galaxy',
      duration: 267,
      cover: 'https://picsum.photos/seed/music3/300/300',
      src: 'https://www.soundhelix.com/examples/mp3/SoundHelix-Song-3.mp3'
    },
    {
      id: 4,
      title: 'Ocean Breeze',
      artist: 'Wave Rider',
      album: 'Tropical',
      duration: 212,
      cover: 'https://picsum.photos/seed/music4/300/300',
      src: 'https://www.soundhelix.com/examples/mp3/SoundHelix-Song-4.mp3'
    },
    {
      id: 5,
      title: 'Urban Jungle',
      artist: 'City Lights',
      album: 'Metropolis',
      duration: 245,
      cover: 'https://picsum.photos/seed/music5/300/300',
      src: 'https://www.soundhelix.com/examples/mp3/SoundHelix-Song-5.mp3'
    },
    {
      id: 6,
      title: 'Crystal Cascade',
      artist: 'Aurora Sound',
      album: 'Ethereal',
      duration: 189,
      cover: 'https://picsum.photos/seed/music6/300/300',
      src: 'https://www.soundhelix.com/examples/mp3/SoundHelix-Song-6.mp3'
    },
    {
      id: 7,
      title: 'Neon Nights',
      artist: 'Synth Masters',
      album: 'Retro',
      duration: 256,
      cover: 'https://picsum.photos/seed/music7/300/300',
      src: 'https://www.soundhelix.com/examples/mp3/SoundHelix-Song-7.mp3'
    },
    {
      id: 8,
      title: 'Sunset Boulevard',
      artist: 'Golden Hour',
      album: 'Sunrise',
      duration: 203,
      cover: 'https://picsum.photos/seed/music8/300/300',
      src: 'https://www.soundhelix.com/examples/mp3/SoundHelix-Song-8.mp3'
    },
    {
      id: 9,
      title: 'Digital Dreams',
      artist: 'Cyber Orchestra',
      album: 'Digital',
      duration: 278,
      cover: 'https://picsum.photos/seed/music9/300/300',
      src: 'https://www.soundhelix.com/examples/mp3/SoundHelix-Song-9.mp3'
    },
    {
      id: 10,
      title: 'Rainbow Sky',
      artist: 'Prism',
      album: 'Colors',
      duration: 221,
      cover: 'https://picsum.photos/seed/music10/300/300',
      src: 'https://www.soundhelix.com/examples/mp3/SoundHelix-Song-10.mp3'
    },
    {
      id: 11,
      title: 'Deep Forest',
      artist: 'Nature Sounds',
      album: 'Forest',
      duration: 289,
      cover: 'https://picsum.photos/seed/music11/300/300',
      src: 'https://www.soundhelix.com/examples/mp3/SoundHelix-Song-11.mp3'
    },
    {
      id: 12,
      title: 'Mountain Echo',
      artist: 'Alpine',
      album: 'Peaks',
      duration: 245,
      cover: 'https://picsum.photos/seed/music12/300/300',
      src: 'https://www.soundhelix.com/examples/mp3/SoundHelix-Song-12.mp3'
    }
  ])

  const searchQuery = ref('')

  const filteredPlaylist = computed(() => {
    if (!searchQuery.value) return playlist.value
    const query = searchQuery.value.toLowerCase()
    return playlist.value.filter(
      track => track.title.toLowerCase().includes(query) ||
               track.artist.toLowerCase().includes(query) ||
               track.album.toLowerCase().includes(query)
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
    const currentIndex = playlist.value.findIndex(t => t.id === currentTrack.value.id)
    const nextIndex = (currentIndex + 1) % playlist.value.length
    playTrack(playlist.value[nextIndex])
  }

  function prevTrack() {
    if (!currentTrack.value) return
    const currentIndex = playlist.value.findIndex(t => t.id === currentTrack.value.id)
    const prevIndex = (currentIndex - 1 + playlist.value.length) % playlist.value.length
    playTrack(playlist.value[prevIndex])
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
    playTrack,
    togglePlay,
    nextTrack,
    prevTrack,
    setVolume,
    toggleMute,
    toggleShuffle,
    toggleRepeat,
    formatTime
  }
})