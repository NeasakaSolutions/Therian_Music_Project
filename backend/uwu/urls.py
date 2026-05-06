# Importaciones:
from django.urls import path
from uwu.views import Class_Mai
from uwu.views import Class_Mai_Parametros
from uwu.views import Class_Mai_Uploads

urlpatterns = [
    path('ouzuka', Class_Mai.as_view()),
    path('ouzuka/<int:id>', Class_Mai_Parametros.as_view()),
    path('ouzuka-upload', Class_Mai_Uploads.as_view()),
]
