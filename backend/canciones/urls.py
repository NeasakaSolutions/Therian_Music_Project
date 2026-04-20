# Importaciones:
from django.urls import path
from canciones.views import CancionesLista
#from canciones.views import CategoriaDetalle

urlpatterns = [
    path("canciones", CancionesLista.as_view()),
    #path("canciones/<int:id>", CategoriaDetalle.as_view()),
]
