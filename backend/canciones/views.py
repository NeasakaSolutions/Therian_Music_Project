# Importaciones
import os
from dotenv import load_dotenv
from django.shortcuts import render
from rest_framework.views import APIView
from django.http.response import JsonResponse
from rest_framework.response import Response
from http import HTTPStatus
from django.http import Http404
from django.utils.text import slugify
from django.utils.dateformat import DateFormat
from datetime import datetime
from django.core.files.storage import FileSystemStorage
from canciones.models import Cancion
from categorias.models import Categoria
from artistas.models import Artista
from canciones.serializers import CancionSerializer

# Clase sin argumentos:
class CancionesLista(APIView):

    # COnsultar registros:
    def get(self, request):
        data = Cancion.objects.order_by("-id").all()
        datos_json = CancionSerializer(data, many = True)

        return JsonResponse({
            "data": datos_json.data
        })
    
    # Agregar campo
    def post(self, request):

        # Validaciones:
        if request.data.get("nombre") == None or not request.data.get("nombre"):
            return JsonResponse({
                "estado": "error",
                "mensaje": "El campo nombre es obligatorio"
            }, status = HTTPStatus.BAD_REQUEST)
        
        if request.data.get("descripcion") == None or not request.data.get("descripcion"):
            return JsonResponse({
                "estado": "error",
                "mensaje": "El campo descripcion es obligatorio"
            }, status = HTTPStatus.BAD_REQUEST)
        
        if request.data.get("categoria_id") == None or not request.data.get("categoria_id"):
            return JsonResponse({
                "estado": "error",
                "mensaje": "El campo categoria es obligatorio"
            }, status = HTTPStatus.BAD_REQUEST)
        
        if request.data.get("artista_id") == None or not request.data.get("artista_id"):
            return JsonResponse({
                "estado": "error",
                "mensaje": "El campo artista es obligatorio"
            }, status = HTTPStatus.BAD_REQUEST)
        
        # Validar que exista la categoria:
        try:
            categoria = Categoria.objects.filter(id = request.data["categoria_id"]).get()

        except Categoria.DoesNotExist:
            return JsonResponse({
                "estado": "error",
                "mensaje": "La categoria ingresada no existe"
            }, status = HTTPStatus.BAD_REQUEST)
        
        # Validar que exista el artista:
        try:
            artista = Artista.objects.filter(id = request.data["artista_id"]).get()

        except Artista.DoesNotExist:
            return JsonResponse({
                "estado": "error",
                "mensaje": "El artista ingresado no existe"
            }, status = HTTPStatus.BAD_REQUEST)

        # Validar que el nombre de la cancion no se repita:
        if Cancion.objects.filter(nombre = request.data.get("nombre")).exists():
            return JsonResponse({
                "estado": "error",
                "mensaje": "El nombre de la cancion ya existe"
            }, status = HTTPStatus.BAD_REQUEST)

        # Crear campo
        try:
            Cancion.objects.create(
                nombre = request.data.get("nombre"),
                descripcion = request.data.get("descripcion"),
                categoria_id = request.data.get("categoria_id"),
                artista_id = request.data.get("artista_id"),
                fecha = datetime.now(),
                foto = "sss",
                cancion = "ssss",
                video = "ssssssss"
            )

            return JsonResponse({
                "estado": "ok",
                "mensaje": "Se creo el registro correctamente"
            }, status = HTTPStatus.CREATED)

        except Exception as e:
            raise Http404
    
# Clase con  argumentos:
class CancionDetalle(APIView):

    # Consultar un registro:
    def get(self, request, id):
        
        try:
            data = Cancion.objects.filter(id = id).get()
            
            return JsonResponse({
                "data": {
                    "id": data.id,
                    "nombre": data.nombre,
                    "slug": data.slug,
                    "descripcion": data.descripcion,
                    "fecha": DateFormat(data.fecha).format("d/m/Y"),
                    "categoria_id": data.categoria_id,
                    "categoria": data.categoria.nombre,
                    "imagen": f"{os.getenv("BASE_URL")}uploads/canciones/{data.foto}",
                    "cancion": f"{os.getenv("BASE_URL")}uploads/canciones/{data.cancion}",
                    "video": f"{os.getenv("BASE_URL")}uploads/canciones/{data.video}"
                    }
            }, status = HTTPStatus.OK)

        except Cancion.DoesNotExist:
            raise Http404

