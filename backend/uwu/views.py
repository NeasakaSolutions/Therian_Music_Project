# Importaciones:
import os
from rest_framework.views import APIView
from django.http import HttpResponse
from django.http import JsonResponse
from http import HTTPStatus
from django.core.files.storage import FileSystemStorage
from datetime import datetime

# Clase de ejemplo:
class Class_Mai(APIView):

    # Consultar informacion:
    def get(self, request):
        # Funciona en esta ruta: http://127.0.0.1:8000/api/mai/ouzuka?id=4
        #return HttpResponse(f"<h1>Metodo Get, id: {request.GET.get("id", None)}</h1>")
        return JsonResponse({"estado": "ok", 
                         "mensaje": f"Metodo GET: Metodo Get, id: {request.GET.get("id", None)}"})

    # Agregar datos:
    def post(self, request):
        #return HttpResponse("<h1>Metodo Post</h1>")

        # Validaciones:
        if request.data.get("correo") == None or request.data.get("password") == None:
            return JsonResponse({
                "estado": "error",
                "mensaje": "Correo o usuario incorrecto"
            }) 

        return JsonResponse({
            "estado": "ok", 
            "mensaje": f"Metodo Post: correo = {request.data.get("correo")} password = {request.data.get("password")}"})
    
    # Modificar datos:
    def put(self, request):
        return HttpResponse("<h1>Metodo Put</h1>")
    
    # Eliminar datos:
    def delete(self, request):
        return HttpResponse("<h1>Metodo Delete</h1>")
    
    # Modificar algunos datos:
    def patch(self, request):
        return HttpResponse("<h1>Metodo Patch</h1>")
    
# Clase con utilizacion de parametros:
class Class_Mai_Parametros(APIView):

    def get(self, request, id):
        # Funciona en esta ruta: http://127.0.0.1:8000/api/mai/ouzuka/4
        return HttpResponse(f"Metodo GET con parametro: {id}")
    
    def post(self, request, id):
        return HttpResponse(f"Metodo POST con parametro: {id}")
    
    def put(self, request, id):
        return HttpResponse(f"Metodo PUT con parametro: {id}")

    def patch(self, request, id):
        return HttpResponse(f"Metodo PATCH con parametro: {id}")
    
    def delete(self, request, id):
        return HttpResponse(f"Metodo DELETE con parametro: {id}")

# Clase para subir archivos:
class Class_Mai_Uploads(APIView):

    def post(self, request):

        # Variables:
        fs = FileSystemStorage()
        fecha =  datetime.now()
        # Cambiar el nombre al archivo y que este no se repita:
        foto = f"{datetime.timestamp(fecha)}{os.path.splitext(str(request.FILES["file"]))[1]}"
        fs.save(f"ouzuka/{foto}", request.FILES["file"]) # Guardar archivo
        fs.url(request.FILES["file"])

        return JsonResponse({
            "estado": "ok",
            "mensaje": "Se subio el archivo"
        })

