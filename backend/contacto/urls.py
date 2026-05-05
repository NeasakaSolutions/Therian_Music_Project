# Importaciones:
from django.urls import path
from contacto.views import ContactoLista
urlpatterns = [
    path("contacto", ContactoLista.as_view()),
]