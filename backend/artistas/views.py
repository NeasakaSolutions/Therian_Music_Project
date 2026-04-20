# Importaciones
from django.shortcuts import render
from rest_framework.views import APIView
from django.http.response import JsonResponse
from rest_framework.response import Response
from http import HTTPStatus
from django.http import Http404
from django.utils.text import slugify
from artistas.serializers import ArtistaSerializer
from artistas.models import Artista

# Clase sin argumentos:
class ArtistasLista(APIView):

    # Consultar artistas:
    def get(self, request):
        
        # Variables:
        data = Artista.objects.order_by("-id").all()
        datos_json = ArtistaSerializer(data, many = True)

        return JsonResponse({
            "data": datos_json.data
        }, status = HTTPStatus.OK)
    
    # Agregar artista:
    def post(self, request):

        # Validaciones:
        if request.data.get("nombre") == None or not request.data["nombre"]:

            return JsonResponse({
                "estado": "error",
                "mensaje": "El campo nombre es obligatorio"
            }, status = HTTPStatus.BAD_REQUEST)
        
        # Crear campo:
        try:
            Artista.objects.create(nombre = request.data["nombre"])

            return JsonResponse({
                "estado": "ok",
                "mensaje": "Campo creado correctamente"
            }, status = HTTPStatus.CREATED)
        
        except Exception as e:
            raise Http404
        
# Clase con argumentos:
class ArtistaDetalle(APIView):

    # Consultar artista:
    def get(self, request, id):
        
        try:
            data = Artista.objects.filter(id = id).get()

            return JsonResponse({
                "data": {
                    "id": data.id,
                    "nombre": data.nombre,
                    "slug": data.slug
                }
            }, status = HTTPStatus.OK)
        
        except Artista.DoesNotExist:

            raise Http404
        
    # Modificar registro:
    def put(self, request, id):

        # Validaciones:
        if request.data.get("nombre") == None or not request.data.get("nombre"):

            return JsonResponse({
                "estado": "error",
                "mensaje": "El campo nombre es obligatorio"
            }, status = HTTPStatus.BAD_REQUEST)
        
        # Modificar registro:
        try:
            data = Artista.objects.filter(id = id).get()
            Artista.objects.filter(id = id).update(
                nombre = request.data.get("nombre"),
                slug = slugify(request.data.get("nombre"))
            )

            return JsonResponse({
                "estado": "ok",
                "mensaje": "Se modifico correctamente"
            }, status = HTTPStatus.OK)
        
        except Artista.DoesNotExist:
            raise Http404
        
    # ELiminar registro:
    def delete(self, request, id):

        # Eliminar registro
        try:
            data = Artista.objects.filter(id = id).get()
            Artista.objects.filter(id = id).delete()

            return JsonResponse({
                "estado": "ok",
                "mensaje": "Se elimino correctamente"
            }, status = HTTPStatus.OK)
        
        except Artista.DoesNotExist:
            raise Http404



