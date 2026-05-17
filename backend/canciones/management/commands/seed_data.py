import os
import requests
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from artistas.models import Artista
from categorias.models import Categoria
from canciones.models import Cancion

SONGS = [
    {"nombre": "Midnight Dreams", "artista": "Luna Eclipse", "categoria": "Nocturnal", "descripcion": "A dreamy nocturnal journey"},
    {"nombre": "Electric Pulse", "artista": "Neon Waves", "categoria": "Synthwave", "descripcion": "Pulsating electronic beats"},
    {"nombre": "Starlight Serenade", "artista": "Cosmic Echo", "categoria": "Galaxy", "descripcion": "A serenade under the stars"},
    {"nombre": "Ocean Breeze", "artista": "Wave Rider", "categoria": "Tropical", "descripcion": "Gentle waves and summer vibes"},
    {"nombre": "Urban Jungle", "artista": "City Lights", "categoria": "Metropolis", "descripcion": "The rhythm of the city"},
    {"nombre": "Crystal Cascade", "artista": "Aurora Sound", "categoria": "Ethereal", "descripcion": "Pure crystalline sounds"},
    {"nombre": "Neon Nights", "artista": "Luna Eclipse", "categoria": "Synthwave", "descripcion": "Neon-lit night drive"},
    {"nombre": "Sunset Boulevard", "artista": "Wave Rider", "categoria": "Tropical", "descripcion": "Golden hour melodies"},
    {"nombre": "Digital Dreams", "artista": "Neon Waves", "categoria": "Metropolis", "descripcion": "Binary sunset echoes"},
    {"nombre": "Rainbow Sky", "artista": "Aurora Sound", "categoria": "Ethereal", "descripcion": "Colors of the sky"},
    {"nombre": "Deep Forest", "artista": "Cosmic Echo", "categoria": "Nocturnal", "descripcion": "Mysterious forest sounds"},
    {"nombre": "Mountain Echo", "artista": "City Lights", "categoria": "Galaxy", "descripcion": "Echoes from the peaks"},
]

SOUNDHELIX_URLS = [
    "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3",
    "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-2.mp3",
    "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-3.mp3",
    "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-4.mp3",
    "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-5.mp3",
    "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-6.mp3",
    "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-7.mp3",
    "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-8.mp3",
    "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-9.mp3",
    "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-10.mp3",
    "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-11.mp3",
    "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-12.mp3",
]


def get_or_create_artist(nombre):
    obj, _ = Artista.objects.get_or_create(nombre=nombre)
    return obj


def get_or_create_categoria(nombre):
    obj, _ = Categoria.objects.get_or_create(nombre=nombre)
    return obj


def download_file(url, dest):
    if os.path.exists(dest):
        return True
    try:
        r = requests.get(url, timeout=30)
        r.raise_for_status()
        with open(dest, "wb") as f:
            f.write(r.content)
        return True
    except Exception:
        return False


class Command(BaseCommand):
    help = "Seed database with sample artists, categories, user and songs"

    def handle(self, *args, **options):
        upload_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))), "uploads", "canciones")
        os.makedirs(upload_dir, exist_ok=True)

        self.stdout.write("Seeding artists...")
        artist_names = set(s["artista"] for s in SONGS)
        for name in artist_names:
            get_or_create_artist(name)
        self.stdout.write(self.style.SUCCESS(f"Created {len(artist_names)} artists"))

        self.stdout.write("Seeding categories...")
        cat_names = set(s["categoria"] for s in SONGS)
        for name in cat_names:
            get_or_create_categoria(name)
        self.stdout.write(self.style.SUCCESS(f"Created {len(cat_names)} categories"))

        test_email = "test@test.com"
        if not User.objects.filter(email=test_email).exists():
            user = User.objects.create_user(
                username=test_email,
                email=test_email,
                password="Test1234!",
                first_name="Test",
                is_active=1,
            )
            self.stdout.write(self.style.SUCCESS(f"Created test user: {test_email} / Test1234!"))
        else:
            user = User.objects.get(email=test_email)
            self.stdout.write(f"Test user already exists: {test_email}")

        self.stdout.write("Downloading audio files...")
        downloaded = 0
        for i, url in enumerate(SOUNDHELIX_URLS):
            ext = os.path.splitext(url.split("/")[-1])[1]
            filename = f"soundhelix_{i+1}{ext}"
            dest = os.path.join(upload_dir, filename)
            if download_file(url, dest):
                downloaded += 1
                self.stdout.write(f"  Downloaded {i+1}/{len(SOUNDHELIX_URLS)}: {filename}")
            else:
                self.stdout.write(self.style.WARNING(f"  Failed to download {i+1}/{len(SOUNDHELIX_URLS)}: {url}"))

        self.stdout.write(f"Downloaded {downloaded}/{len(SOUNDHELIX_URLS)} audio files")

        self.stdout.write("Seeding songs...")
        created = 0
        for i, song in enumerate(SONGS):
            if Cancion.objects.filter(nombre=song["nombre"]).exists():
                continue
            artista = Artista.objects.get(nombre=song["artista"])
            categoria = Categoria.objects.get(nombre=song["categoria"])
            filename = f"soundhelix_{i+1}.mp3"
            Cancion.objects.create(
                nombre=song["nombre"],
                descripcion=song["descripcion"],
                artista=artista,
                categoria=categoria,
                user=user,
                foto="placeholder.jpg",
                cancion=filename,
            )
            created += 1
        self.stdout.write(self.style.SUCCESS(f"Created {created} songs"))

        placeholder_img = os.path.join(upload_dir, "placeholder.jpg")
        if not os.path.exists(placeholder_img):
            try:
                img_data = requests.get("https://picsum.photos/seed/music/300/300", timeout=15).content
                with open(placeholder_img, "wb") as f:
                    f.write(img_data)
                self.stdout.write(self.style.SUCCESS("Created placeholder image"))
            except Exception:
                self.stdout.write(self.style.WARNING("Could not download placeholder image"))

        self.stdout.write(self.style.SUCCESS("Seed complete!"))
