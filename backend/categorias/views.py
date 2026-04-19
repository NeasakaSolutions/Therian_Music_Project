# Importaciones
from django.shortcuts import render
from rest_framework.views import APIView
from django.http.response import JsonResponse
from rest_framework.response import Response
from http import HTTPStatus
from django.http import Http404
from django.utils.text import slugify
from categorias.serializers import CategoriaSerializer
from categorias.models import Categoria

# Clase sin argumentos:
class CategoriaLista(APIView):

    # Consultar categorias:
    def get(self, request):
        # Consulta en la base de datos:
        data = Categoria.objects.order_by("-id").all()
        datos_json = CategoriaSerializer(data, many = True)

        return JsonResponse({"data": datos_json.data}, status = HTTPStatus.OK)
    
    # Agregar categoria:
    def post(self, request):
        
        # Validaciones:
        if request.data.get("nombre") == None or not request.data["nombre"]:
            return JsonResponse({
                "estado": "error",
                "mensaje": "El campo de nombre es obligatorio"
            }, status = HTTPStatus.BAD_REQUEST)
        
        # Crear categoria:
        try:
            Categoria.objects.create(nombre = request.data["nombre"])

            return JsonResponse({
                "estado": "ok",
                "mensaje": "Se creo el registro exitosamente"
            }, status = HTTPStatus.CREATED)

        except Exception as e:
            raise Http404
    
# Clase con argumentos:
class CategoriaDetalle(APIView):

    # Consultar categoria
    def get(self, request, id):
        
        try:
            data = Categoria.objects.filter(id = id).get()

            return JsonResponse({"data": {
                "id": data.id,
                "nombre": data.nombre,
                "slug": data.slug
                }}, status = HTTPStatus.OK)
        
        except Categoria.DoesNotExist:
            raise Http404
    
    # Modificar registro:
    def put(self, request, id):
        
        # Validaciones:
        if request.data.get("nombre") == None or not request.data["nombre"]:
            return JsonResponse({
                "estado": "error",
                "mensaje": "El campo de nombre es obligatorio"
            }, status = HTTPStatus.BAD_REQUEST)

        # Modificar registro:
        try:
            data = Categoria.objects.filter(id = id).get()
            Categoria.objects.filter(id = id).update(nombre = request.data.get("nombre"), 
                                                     slug = slugify(request.data.get("nombre")))
            
            return JsonResponse({
                "estado": "ok",
                "mensaje": "Se modifico el registro exitosamente"
            }, status = HTTPStatus.OK)

        except Categoria.DoesNotExist:
            raise Http404
        
    # Eliminar registro:
    def delete(self, request, id):
        
        # Eliminar registro:
        try:
            data = Categoria.objects.filter(id = id).get()
            Categoria.objects.filter(id = id).delete()
            
            return JsonResponse({
                "estado": "ok",
                "mensaje": "Se elimino el registro exitosamente"
            }, status = HTTPStatus.OK)

        except Categoria.DoesNotExist:
            raise Http404