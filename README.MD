# Therian Music Project

Plataforma de música interactiva con frontend moderno (Vue 3) y backend robusto (Django REST Framework + JWT). Los usuarios pueden registrarse, explorar canciones, reproducir música en un reproductor integrado y gestionar su panel personal.

---

## Tecnologías

### Frontend
- **Vue 3** (Composition API + `<script setup>`)
- **Vite** (bundler y dev server)
- **Pinia** (gestión de estado)
- **Vue Router** (SPA con rutas protegidas)
- **Axios** (cliente HTTP con interceptor JWT)
- **Tailwind CSS** (estilos utilitarios)
- Tema oscuro/claro (predeterminado: oscuro)

### Backend
- **Django 6.0.4** + **Django REST Framework**
- **MySQL** (`therian_music_project`, charset `utf8mb4`)
- **JWT** (python-jose, algoritmo HS512)
- **CORS** habilitado para `localhost:5173`
- **Mailtrap SMTP** (verificación de correo en registro)

---

## Estructura del proyecto

```
Therian_Music_Project/
├── backend/
│   ├── backend/              # Configuración Django (settings, urls, wsgi)
│   ├── artistas/             # CRUD de artistas
│   ├── canciones/            # CRUD de canciones
│   ├── canciones_helper/     # Endpoints auxiliares (home, búsqueda, panel)
│   ├── categorias/           # CRUD de categorías
│   ├── contacto/             # Formulario de contacto
│   ├── seguridad/            # Registro, login, verificación JWT
│   ├── utilidades/           # Utilidades (paginación, envío de correos)
│   ├── uploads/canciones/    # Archivos de audio e imágenes
│   ├── .env.local            # Variables de entorno
│   ├── manage.py
│   └── ApisTherianMusic.json # Colección Postman (16 endpoints)
├── frontend/
│   ├── src/
│   │   ├── components/       # Navbar, MusicPlayer, Carousel, TrackCard, WavesBackground
│   │   ├── pages/            # Inicio (exploración), Dashboard
│   │   ├── views/            # Home (landing), Login, Register
│   │   ├── stores/           # auth, music, theme (Pinia)
│   │   ├── services/         # api.js (axios con interceptor)
│   │   └── router/           # Configuración de rutas
│   └── package.json
└── README.MD
```

---

## Configuración del backend

### 1. Base de datos (MySQL)

Crea la base de datos:

```sql
CREATE DATABASE therian_music_project CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

### 2. Variables de entorno

Edita `backend/.env.local`:

```

### 3. Instalar dependencias

```bash
cd backend
pip install -r requirements.txt
```

### 4. Migraciones

```bash
python manage.py migrate
```

### 5. Poblar datos de prueba

```bash
python manage.py seed_data
```

Esto crea:
- 6 artistas (Luna Eclipse, Neon Waves, Cosmic Echo, etc.)
- 6 categorías (Nocturnal, Synthwave, Galaxy, etc.)
- 12 canciones con archivos de audio reales (SoundHelix MP3)
- Usuario de prueba: `test@test.com` / `Test1234!`

### 6. Iniciar servidor

```bash
python manage.py runserver 127.0.0.1:8000
```

---

## Configuración del frontend

```bash
cd frontend
npm install
npm run dev
```

El frontend se sirve en `http://localhost:5173`.

### Dependencias adicionales del frontend

- `music-metadata-browser` — Extracción de metadatos ID3 (título, artista, carátula) de archivos de audio en el navegador

---

## Endpoints de la API

Todas las rutas están bajo el prefijo `/api/mai/`.

### Autenticación
| Método | Ruta | Descripción |
|--------|------|-------------|
| POST | `/seguridad/registro` | Registro de usuario (requiere verificación por email) |
| GET | `/seguridad/verificacion/<token>` | Verifica y activa la cuenta |
| POST | `/seguridad/login` | Inicio de sesión, devuelve JWT |

### Canciones
| Método | Ruta | Descripción |
|--------|------|-------------|
| GET | `/canciones` | Lista paginada de canciones |
| GET | `/canciones/<id>` | Detalle de una canción |
| POST | `/canciones` | Crear canción (requiere autenticación, multipart) |
| PUT | `/canciones/<id>` | Actualizar canción |
| DELETE | `/canciones/<id>` | Eliminar canción |

### Helper (auxiliares)
| Método | Ruta | Descripción |
|--------|------|-------------|
| GET | `/canciones-home` | 3 canciones aleatorias para la página principal |
| GET | `/canciones-buscador?categoria_id=&search=` | Búsqueda por categoría y texto |
| GET | `/canciones-panel/<id>` | Canciones del usuario (requiere auth) |
| GET | `/canciones/slug/<slug>` | Detalle por slug |

### Artistas y Categorías
| Método | Ruta | Descripción |
|--------|------|-------------|
| GET | `/artistas` | Lista de artistas |
| POST | `/artistas` | Crear artista |
| GET | `/categorias` | Lista de categorías |
| POST | `/categorias` | Crear categoría |

### Contacto
| Método | Ruta | Descripción |
|--------|------|-------------|
| POST | `/contacto` | Enviar mensaje de contacto |

---

## Funcionalidades implementadas

### Frontend
- **Landing page** (`/`) — Página de bienvenida con diseño morado y ondas animadas
- **Exploración** (`/inicio`) — Lista de canciones, carrusel de recomendados, búsqueda en vivo
- **Reproductor** — Barra inferior fija con control de reproducción, progreso, volumen, aleatorio y repetición
- **Autenticación** — Registro con verificación por email, login con JWT, protección de rutas
- **Dashboard** (`/dashboard`) — Estadísticas de usuario, playlists, actividad reciente, configuración
- **Subida de música** — Formulario en el Dashboard para subir canciones con:
  - Extracción automática de metadatos ID3 (título, artista, carátula) al seleccionar el archivo de audio
  - Si el archivo no tiene metadatos, se usa el nombre del archivo como título
  - Creación de nuevos artistas y categorías inline sin recargar la página
  - Previsualización de audio, imagen y video antes de subir
  - Soporte para audio (MP3, WAV, OGG, MP4), imagen (JPG, PNG, WebP) y video (MP4, WebM, OGG) opcional
- **Tema oscuro/claro** — Persistencia en localStorage, predeterminado oscuro
- **Ondas animadas** — Fondo canvas interactivo con ondas color morado

### Backend
- **JWT** — Tokens con expiración de 1 día, algoritmo HS512
- **CORS** — Configurado para permitir peticiones desde el frontend
- **Paginación** — Paginación personalizada en listados
- **Archivos multimedia** — Subida y servido de imágenes, audio y video
- **Verificación por email** — Enlace de activación enviado al registrarse
- **Seed data** — Comando `seed_data` que descarga canciones reales y crea datos de prueba
- **Validación de formatos** — Los endpoints de subida validan tipos MIME para audio, imagen y video

---

## Flujo completo de usuario

1. El usuario se registra en `/register`
2. Recibe un correo de verificación (Mailtrap SMTP)
3. Hace clic en el enlace → cuenta activada → redirigido al frontend
4. Inicia sesión en `/login` → obtiene JWT
5. Explora canciones en `/inicio` (12 canciones con audio real)
6. Reproduce canciones con el reproductor inferior
7. Busca por título, artista o álbum
8. Accede al Dashboard en `/dashboard` para ver estadísticas
9. Sube su propia música desde la pestaña "Subir" del Dashboard:
   - Selecciona archivo de audio (MP3, WAV, OGG, MP4)
   - Los metadatos ID3 se extraen automáticamente (título, artista, carátula)
   - Selecciona imagen opcional y video opcional
   - Crea nuevo artista o categoría si no existen en el sistema
   - Envía el formulario y la canción aparece en su panel y en la lista general

---

## Notas adicionales

- El campo `video` en la respuesta de canciones retorna `null` cuando no hay video (en lugar de la cadena `"None"`)
- Las estadísticas del Dashboard se calculan reactivamente con `computed()` para reflejar datos asíncronos
- El reproductor usa archivos de SoundHelix con licencia Creative Commons como contenido de demostración
- La búsqueda en el frontend es client-side sobre la lista actual de canciones
- La extracción de metadatos ID3 se realiza en el navegador con `music-metadata-browser` antes de enviar el formulario
- Después de subir una canción, la lista de canciones se refresca automáticamente en el panel y en la página de inicio
