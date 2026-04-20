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
from canciones.models import Cancion
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
                    "cancion": f"{os.getenv("BASE_URL")}uploads/canciones/{data.cancion}"
                    }
            }, status = HTTPStatus.OK)

        except Cancion.DoesNotExist:
            raise Http404

