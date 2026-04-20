# Importaciones:
from django.urls import path
from artistas.views import ArtistasLista
from artistas.views import ArtistaDetalle

urlpatterns = [
    path("artistas", ArtistasLista.as_view()),
    path("artistas/<int:id>", ArtistaDetalle.as_view()),
]
