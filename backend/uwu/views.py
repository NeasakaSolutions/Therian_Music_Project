# Importaciones:
from rest_framework.views import APIView
from django.http import HttpResponse

# Clase de ejemplo:
class Class_Mai(APIView):

    # Consultar informacion:
    def get(self, request):
        return HttpResponse("<h1>Metodo Get</h1>")

    # Agregar datos:
    def post(self, request):
        return HttpResponse("<h1>Metodo Post</h1>")
    
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
        return HttpResponse(f"Metodo GET con parametro: {id}")
    
    def post(self, request, id):
        return HttpResponse(f"Metodo POST con parametro: {id}")
    
    def put(self, request, id):
        return HttpResponse(f"Metodo PUT con parametro: {id}")

    def patch(self, request, id):
        return HttpResponse(f"Metodo PATCH con parametro: {id}")
    
    def delete(self, request, id):
        return HttpResponse(f"Metodo DELETE con parametro: {id}")
