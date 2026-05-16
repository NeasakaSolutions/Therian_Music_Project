# Importaciones:
from django.urls import path
from canciones_helper.views import CancionHelperLista
from canciones_helper.views import CancionHelperEditarFoto
from canciones_helper.views import CancionHelperEditarCancion
from canciones_helper.views import CancionHelperEditarVideo
from canciones_helper.views import CancionHelperSlug
from canciones_helper.views import CancionHelperHome
from canciones_helper.views import CancionHelperBuscador

urlpatterns = [
    path("canciones/editar/foto", CancionHelperEditarFoto.as_view()),
    path("canciones/editar/cancion", CancionHelperEditarCancion.as_view()),
    path("canciones/editar/video", CancionHelperEditarVideo.as_view()),
    path("canciones/slug/<str:slug>", CancionHelperSlug.as_view()),
    path("canciones-home", CancionHelperHome.as_view()),
    path("canciones-buscador", CancionHelperBuscador.as_view()),
    path("canciones-panel/<int:id>", CancionHelperLista.as_view()),
]