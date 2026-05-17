# Importaciones:
import os
from rest_framework.views import APIView
from django.http.response import JsonResponse
from http import HTTPStatus
from django.http import Http404
from dotenv import load_dotenv
from datetime import datetime
from django.utils.dateformat import DateFormat
from django.core.files.storage import FileSystemStorage
from seguridad.decorators import logueado
from utilidades.utilidades import paginar
from django.contrib.auth.models import User
from canciones.serializers import CancionSerializer
from canciones.models import Cancion

# Create your views here.
class CancionHelperEditarFoto(APIView):
    
    @logueado()
    def post(self, request):
        
        # validaciones de campos
        if not request.data.get("id"):
            return JsonResponse({
                "estado": "error",
                "mensaje": "El campo id es obligatorio"
            }, status=HTTPStatus.BAD_REQUEST)
        
        try: 
            existe = Cancion.objects.filter(id = request.data["id"]).get()
            anterior = existe.foto
        
        except Cancion.DoesNotExist:
            return JsonResponse({
                "estado": "error",
                "mensaje": "La cancion seleccionada no existe"
            }, status=HTTPStatus.BAD_REQUEST)
        
        fs = FileSystemStorage()

        # subir imagen
        foto_file = request.FILES["foto"]

        if foto_file.content_type not in ["image/jpeg", "image/png", "image/webp"]:
            return JsonResponse({
                "estado": "error",
                "mensaje": "Formato de imagen no valido"
            }, status=HTTPStatus.BAD_REQUEST)

        try:
            ext = os.path.splitext(foto_file.name)[1]
            foto = f"{datetime.timestamp(datetime.now())}{ext}"
            fs.save(f"canciones/{foto}", foto_file)
        except Exception:
            return JsonResponse({
                "estado": "error",
                "mensaje": "Error al subir la imagen"
            }, status=HTTPStatus.BAD_REQUEST)
        
        try:
            Cancion.objects.filter(id = request.data["id"]).update(foto = foto)

            # Elaiminar archivo anterior:
            path = f"./uploads/canciones/{anterior}"

            if os.path.exists(path):
                os.remove(path)

            return JsonResponse({
                "estado": "ok",
                "mensaje": "Se actualizo correctamente"
            }, status=HTTPStatus.OK)

        except Exception as e:
            return JsonResponse({
                "estado": "error",
                "mensaje": "Ocurrio un error inesperado"
            }, status=HTTPStatus.BAD_REQUEST)
        
# Editar cancion
class CancionHelperEditarCancion(APIView):

    @logueado()
    def post(self, request):

        # validar id
        if not request.data.get("id"):
            return JsonResponse({
                "estado": "error",
                "mensaje": "El campo id es obligatorio"
            }, status=HTTPStatus.BAD_REQUEST)

        # validar archivo
        if not request.FILES.get("cancion"):
            return JsonResponse({
                "estado": "error",
                "mensaje": "El campo cancion es obligatorio"
            }, status=HTTPStatus.BAD_REQUEST)

        # validar existencia
        try:
            existe = Cancion.objects.filter(id=request.data["id"]).get()
            anterior = existe.cancion

        except Cancion.DoesNotExist:
            return JsonResponse({
                "estado": "error",
                "mensaje": "La cancion seleccionada no existe"
            }, status=HTTPStatus.BAD_REQUEST)

        fs = FileSystemStorage()

        # obtener archivo
        cancion_file = request.FILES["cancion"]

        # validar formato
        if cancion_file.content_type not in [
            "audio/mpeg",
            "audio/wav",
            "audio/ogg",
            "audio/mp4"
        ]:
            return JsonResponse({
                "estado": "error",
                "mensaje": "Formato de audio no valido"
            }, status=HTTPStatus.BAD_REQUEST)

        # subir archivo
        try:
            ext = os.path.splitext(cancion_file.name)[1]
            cancion = f"{datetime.timestamp(datetime.now())}{ext}"

            fs.save(f"canciones/{cancion}", cancion_file)

        except Exception:
            return JsonResponse({
                "estado": "error",
                "mensaje": "Error al subir la cancion"
            }, status=HTTPStatus.BAD_REQUEST)

        # actualizar registro
        try:
            Cancion.objects.filter(id=request.data["id"]).update(
                cancion=cancion
            )

            # eliminar anterior
            path = f"./uploads/canciones/{anterior}"

            if os.path.exists(path):
                os.remove(path)

            return JsonResponse({
                "estado": "ok",
                "mensaje": "Se actualizo correctamente"
            }, status=HTTPStatus.OK)

        except Exception:
            return JsonResponse({
                "estado": "error",
                "mensaje": "Ocurrio un error inesperado"
            }, status=HTTPStatus.BAD_REQUEST)
        
# Editar video
class CancionHelperEditarVideo(APIView):

    @logueado()
    def post(self, request):

        # validar id
        if not request.data.get("id"):
            return JsonResponse({
                "estado": "error",
                "mensaje": "El campo id es obligatorio"
            }, status=HTTPStatus.BAD_REQUEST)

        # validar archivo
        if not request.FILES.get("video"):
            return JsonResponse({
                "estado": "error",
                "mensaje": "El campo video es obligatorio"
            }, status=HTTPStatus.BAD_REQUEST)

        # validar existencia
        try:
            existe = Cancion.objects.filter(id=request.data["id"]).get()
            anterior = existe.video

        except Cancion.DoesNotExist:
            return JsonResponse({
                "estado": "error",
                "mensaje": "La cancion seleccionada no existe"
            }, status=HTTPStatus.BAD_REQUEST)

        fs = FileSystemStorage()

        # obtener archivo
        video_file = request.FILES["video"]

        # validar formato
        if video_file.content_type not in [
            "video/mp4",
            "video/webm",
            "video/ogg"
        ]:
            return JsonResponse({
                "estado": "error",
                "mensaje": "Formato de video no valido"
            }, status=HTTPStatus.BAD_REQUEST)

        # subir archivo
        try:
            ext = os.path.splitext(video_file.name)[1]
            video = f"{datetime.timestamp(datetime.now())}{ext}"

            fs.save(f"canciones/{video}", video_file)

        except Exception:
            return JsonResponse({
                "estado": "error",
                "mensaje": "Error al subir el video"
            }, status=HTTPStatus.BAD_REQUEST)

        # actualizar registro
        try:
            Cancion.objects.filter(id=request.data["id"]).update(
                video=video
            )

            # eliminar anterior si existe
            if anterior:
                path = f"./uploads/canciones/{anterior}"

                if os.path.exists(path):
                    os.remove(path)

            return JsonResponse({
                "estado": "ok",
                "mensaje": "Se actualizo correctamente"
            }, status=HTTPStatus.OK)

        except Exception:
            return JsonResponse({
                "estado": "error",
                "mensaje": "Ocurrio un error inesperado"
            }, status=HTTPStatus.BAD_REQUEST)

# Buscador por medio de slug:
class CancionHelperSlug(APIView):

    # Consultar un registro:
    def get(self, request, slug):
        
        try:
            data = Cancion.objects.filter(slug = slug).get()
            
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
                    "video": f"{os.getenv("BASE_URL")}uploads/canciones/{data.video}" if data.video else None,
                    "user_id": data.user_id,
                    "user": data.user.first_name
                    }
            }, status = HTTPStatus.OK)

        except Cancion.DoesNotExist:
            raise Http404

# Canciones aleatorias:
class CancionHelperHome(APIView):

    def get(self, request):
        data = Cancion.objects.order_by("?").all()[:3] # SELECT * FROM canciopnes ORDER BY rand()  LIMIT 3
        datos_json = CancionSerializer(data, many = True)
        return JsonResponse({
            "data": datos_json.data
        }, status = HTTPStatus.OK)

# Buscador por categoria:
class CancionHelperBuscador(APIView):

    def get(self, request):
        if request.GET.get("categoria_id") == None or not request.GET.get("categoria_id"):
            return JsonResponse({
                "estado": "error",
                "mensaje": "Categoria no valida"
            }, status = HTTPStatus.BAD_REQUEST)

        data = Cancion.objects.filter(categoria_id = request.GET.get("categoria_id")).filter(nombre__icontains = request.GET.get("search")).order_by("?").all()[:3] # SELECT * FROM canciopnes WHERE categoria_id
        datos_json = CancionSerializer(data, many = True)
        return JsonResponse({
            "data": datos_json.data
        }, status = HTTPStatus.OK)

# Listar canciones por usuario:
class CancionHelperLista(APIView):

    @logueado()
    def get(self, request, id):

        try:
            User.objects.filter(id=id).get()

        except User.DoesNotExist:
            return JsonResponse({
                "estado": "error",
                "mensaje": "Ocurrio un error"
            }, status=HTTPStatus.BAD_REQUEST)

        data = Cancion.objects.filter(
            user_id=id
        ).order_by('-id')

        paginado = paginar(request, data, 10)

        datos_json = CancionSerializer(
            paginado["data"],
            many=True
        )

        return JsonResponse({
            "data": datos_json.data,
            "pagina_actual": paginado["pagina_actual"],
            "total_paginas": paginado["total_paginas"],
            "total_registros": paginado["total_registros"],
            "hay_siguiente": paginado["hay_siguiente"],
            "hay_anterior": paginado["hay_anterior"]
        }, status=HTTPStatus.OK)