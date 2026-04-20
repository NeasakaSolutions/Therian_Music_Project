# Importaciones:
from django.urls import path
from canciones.views import CancionesLista
from canciones.views import CancionDetalle

urlpatterns = [
    path("canciones", CancionesLista.as_view()),
    path("canciones/<int:id>", CancionDetalle.as_view()),
]
