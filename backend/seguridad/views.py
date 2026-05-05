# IMportaciones:
import uuid
import os
from dotenv import  load_dotenv
from django.shortcuts import render
from rest_framework.views import APIView
from django.http.response import JsonResponse
from django.http import Http404
from http import HTTPStatus
from django.contrib.auth.models import User
from seguridad.models import UsersMetadata

# Create your views here.
class Clase_Registro(APIView):

    def post(self, request):
        
        # Validacion nombre:
        if request.data.get("nombre") == None or not request.data.get("nombre"):
            return JsonResponse({
                "estado": "error",
                "mensaje": "El campo nombre es obligatorio"
            }, status =  HTTPStatus.BAD_REQUEST)
        
        # Validacion correo:
        if request.data.get("correo") == None or not request.data.get("correo"):
            return JsonResponse({
                "estado": "error",
                "mensaje": "El campo correo es obligatorio"
            }, status =  HTTPStatus.BAD_REQUEST)
        
        # Validacion password:
        if request.data.get("password") == None or not request.data.get("password"):
            return JsonResponse({
                "estado": "error",
                "mensaje": "El campo password es obligatorio"
            }, status =  HTTPStatus.BAD_REQUEST)
        
        #  Correo repetido
        if User.objects.filter(email = request.data["correo"]).exists():
            return JsonResponse({
                "estado": "error",
                "mensaje": "El correo ingresado no esta disponible"
            }, status =  HTTPStatus.BAD_REQUEST)
        
        token = uuid.uuid4()
        url = f'{os.getenv("BASE_URL")}api/mai/seguridad/verificacion/{token}'
        
        try:
            u = User.objects.create_user(
                username = request.data["correo"],
                password = request.data["password"],
                email = request.data["correo"],
                first_name = request.data["nombre"],
                last_name = "",
                is_active = 0
            )
            UsersMetadata.objects.create(token = token, user_id = u.id)

            html = f"""
            <h3>Verificacion de cuenta</h3>
            Hola {request.data["nombre"]} te haz registrado exitosamente. Para activar tu cuenta ingresa al link:
            <a href="{url}">aqui</a>
            </br>
            """

        except Exception as e:
            return JsonResponse({
                "estado": "error",
                "mensaje": "Ocurrio un error inesperado"
            }, status =  HTTPStatus.BAD_REQUEST)

        return JsonResponse({
                "estado": "ok",
                "mensaje": "Se creo el registro"
            }, status =  HTTPStatus.CREATED)