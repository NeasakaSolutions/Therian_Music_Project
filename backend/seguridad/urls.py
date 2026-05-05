# Importaciones:
from django.urls import path
from seguridad.views import Clase_Registro
from seguridad.views import Clase_Verificacion
from seguridad.views import Clase3

urlpatterns = [
    path("seguridad/registro", Clase_Registro.as_view()),
    path("seguridad/verificacion/<str:token>", Clase_Verificacion.as_view()),
    path("seguridad/login", Clase3.as_view()),
]