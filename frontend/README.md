# Therian Music - Frontend

Frontend de la aplicación Therian Music, una plataforma de streaming de música.

## Stack Tecnológico

- **Vue 3** (Composition API)
- **Vite** - Bundler y servidor de desarrollo
- **Pinia** - Gestión de estado
- **Vue Router** - Enrutamiento
- **Tailwind CSS** - Estilos
- **ESLint + Oxlint** - Linting

## Estructura del Proyecto

```
frontend/
├── src/
│   ├── components/       # Componentes reutilizables
│   │   ├── Navbar.vue      # Barra de navegación
│   │   ├── MusicPlayer.vue # Reproductor de música
│   │   ├── TrackCard.vue   # Tarjeta de canción
│   │   ├── Carousel.vue   # Carrusel automático
│   │   └── WavesBackground.vue # Fondo animado
│   ├── pages/             # Páginas principales
│   │   ├── Inicio.vue     # Página principal (música)
│   │   └── Dashboard.vue  # Panel de usuario
│   ├── views/             # Vistas de autenticación
│   │   ├── Home.vue      # Landing page
│   │   ├── Login.vue    # Formulario de login
│   │   └── Register.vue # Formulario de registro
│   ├── stores/            # Pinia stores
│   │   ├── auth.js       # Autenticación
│   │   ├── music.js     # Reproductor de música
│   │   └── theme.js    # Tema (oscuro/claro)
│   ├── router/           # Configuración de rutas
│   ├── App.vue          # Componente raíz
│   ├── main.js         # Entry point
│   └── style.css      # Estilos globales
└── package.json
```

## Rutas

| Ruta | Componente | Descripción |
|------|------------|-------------|
| `/` | Home | Landing con login/register |
| `/inicio` | Inicio | Página principal con música |
| `/login` | Login | Formulario de autenticación |
| `/register` | Register | Formulario de registro |
| `/dashboard` | Dashboard | Panel del usuario |

## Instalación

```bash
npm install
```

## Desarrollo

```bash
npm run dev
```

## Build

```bash
npm run build
```

## Linting

```bash
npm run lint
```

## Características

- 🎵 Reproductor de música con controles
- 🌊 Animación de ondas de fondo
- 🌓 Tema oscuro/claro
- 🔍 Buscador de canciones
- 🎠 Carrusel de recomendaciones
- 📊 Dashboard de usuario
- 📱 Diseño responsive

## Notas

- Datos mock (sin backend)
- Almacenamiento en localStorage
- Audio de SoundHelix para pruebas