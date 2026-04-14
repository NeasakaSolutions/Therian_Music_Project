# Importaciones:
from django.contrib import admin
from django.urls import path
from django.urls import include

urlpatterns = [
    path('admin/', admin.site.urls),
    # Rutas de ejemplo/pruebas
    path('', include("home.urls")),
    path('api/mai/', include("uwu.urls")),
]
