# Importaciones:
from django.urls import path
from seguridad.views import Clase_Registro
urlpatterns = [
    path("seguridad/registro", Clase_Registro.as_view()),
]