# Importaciones:
from django.urls import path
from categorias.views import CategoriaLista
from categorias.views import CategoriaDetalle

urlpatterns = [
    path("categorias", CategoriaLista.as_view()),
    path("categorias/<int:id>", CategoriaDetalle.as_view()),
]
