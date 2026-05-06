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
from seguridad.decorators import logueado
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
    @logueado()
    def post(self, request):

        # validaciones de campos
        if not request.data.get("nombre"):
            return JsonResponse({
                "estado": "error",
                "mensaje": "El campo nombre es obligatorio"
            }, status=HTTPStatus.BAD_REQUEST)

        if not request.data.get("descripcion"):
            return JsonResponse({
                "estado": "error",
                "mensaje": "El campo descripcion es obligatorio"
            }, status=HTTPStatus.BAD_REQUEST)

        if not request.data.get("categoria_id"):
            return JsonResponse({
                "estado": "error",
                "mensaje": "El campo categoria es obligatorio"
            }, status=HTTPStatus.BAD_REQUEST)

        if not request.data.get("artista_id"):
            return JsonResponse({
                "estado": "error",
                "mensaje": "El campo artista es obligatorio"
            }, status=HTTPStatus.BAD_REQUEST)

        if not request.FILES.get("foto"):
            return JsonResponse({
                "estado": "error",
                "mensaje": "El campo foto es obligatorio"
            }, status=HTTPStatus.BAD_REQUEST)

        if not request.FILES.get("cancion"):
            return JsonResponse({
                "estado": "error",
                "mensaje": "El campo cancion es obligatorio"
            }, status=HTTPStatus.BAD_REQUEST)


        # validar existencia
        try:
            categoria = Categoria.objects.get(id=request.data.get("categoria_id"))
        except Categoria.DoesNotExist:
            return JsonResponse({
                "estado": "error",
                "mensaje": "La categoria no existe"
            }, status=HTTPStatus.BAD_REQUEST)

        try:
            artista = Artista.objects.get(id=request.data.get("artista_id"))
        except Artista.DoesNotExist:
            return JsonResponse({
                "estado": "error",
                "mensaje": "El artista no existe"
            }, status=HTTPStatus.BAD_REQUEST)


        # validar duplicado
        if Cancion.objects.filter(nombre=request.data.get("nombre")).exists():
            return JsonResponse({
                "estado": "error",
                "mensaje": "La cancion ya existe"
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

        # subir cancion
        cancion_file = request.FILES["cancion"]

        if cancion_file.content_type not in ["audio/mpeg", "audio/wav", "audio/ogg", "audio/mp4"]:
            return JsonResponse({
                "estado": "error",
                "mensaje": "Formato de audio no valido"
            }, status=HTTPStatus.BAD_REQUEST)

        try:
            ext = os.path.splitext(cancion_file.name)[1]
            cancion = f"{datetime.timestamp(datetime.now())}{ext}"
            fs.save(f"canciones/{cancion}", cancion_file)
        except Exception:
            return JsonResponse({
                "estado": "error",
                "mensaje": "Error al subir la cancion"
            }, status=HTTPStatus.BAD_REQUEST)


        # subir video (opcional)
        video_file = request.FILES.get("video")
        video = None

        if video_file:
            if video_file.content_type not in ["video/mp4", "video/webm", "video/ogg"]:
                return JsonResponse({
                    "estado": "error",
                    "mensaje": "Formato de video no valido"
                }, status=HTTPStatus.BAD_REQUEST)

            try:
                ext = os.path.splitext(video_file.name)[1]
                video = f"{datetime.timestamp(datetime.now())}{ext}"
                fs.save(f"canciones/{video}", video_file)
            except Exception:
                return JsonResponse({
                    "estado": "error",
                    "mensaje": "Error al subir el video"
                }, status=HTTPStatus.BAD_REQUEST)

        # crear registro
        try:
            Cancion.objects.create(
                nombre=request.data.get("nombre"),
                descripcion=request.data.get("descripcion"),
                categoria=categoria,
                artista=artista,
                fecha=datetime.now(),
                foto=foto,
                cancion=cancion,
                video=video
            )

            return JsonResponse({
                "estado": "ok",
                "mensaje": "Se creo el registro correctamente"
            }, status=HTTPStatus.CREATED)

        except Exception:
            return JsonResponse({
                "estado": "error",
                "mensaje": "Error al guardar en la base de datos"
            }, status=HTTPStatus.INTERNAL_SERVER_ERROR)
    
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

    # Modificar un registro:
    @logueado()
    def put(self, request, id):
        
        try:
            data = Cancion.objects.filter(id = id).get()

        except Cancion.DoesNotExist:
            return JsonResponse({
                "estado": "error",
                "mensaje": "Ocurrio un error"
            }, status = HTTPStatus.NOT_FOUND)
        
        # validaciones de campos
        if not request.data.get("nombre"):
            return JsonResponse({
                "estado": "error",
                "mensaje": "El campo nombre es obligatorio"
            }, status=HTTPStatus.BAD_REQUEST)

        if not request.data.get("descripcion"):
            return JsonResponse({
                "estado": "error",
                "mensaje": "El campo descripcion es obligatorio"
            }, status=HTTPStatus.BAD_REQUEST)

        if not request.data.get("categoria_id"):
            return JsonResponse({
                "estado": "error",
                "mensaje": "El campo categoria es obligatorio"
            }, status=HTTPStatus.BAD_REQUEST)

        if not request.data.get("artista_id"):
            return JsonResponse({
                "estado": "error",
                "mensaje": "El campo artista es obligatorio"
            }, status=HTTPStatus.BAD_REQUEST)

        try:
            Cancion.objects.filter(id = id).update(
                nombre = request.data.get("nombre"),
                slug = slugify(request.data["nombre"]),
                descripcion = request.data.get("descripcion"),
                categoria = Categoria.objects.get(id=request.data.get("categoria_id")),
                artista = Artista.objects.get(id=request.data.get("artista_id")),
            )

            return JsonResponse({
                "estado": "ok",
                "mensaje": "Se modifico el registro correctamente"
            }, status = HTTPStatus.OK)

        except:
            return JsonResponse({
                "estado": "error",
                "mensaje": "Ocurrio un error"
            }, status = HTTPStatus.BAD_REQUEST)

    # Eliminar un registro:
    @logueado()
    def delete(self, request, id):

        try:
            data = Cancion.objects.get(id=id)
        except Cancion.DoesNotExist:
            return JsonResponse({
                "estado": "error",
                "mensaje": "Registro no encontrado"
            }, status=HTTPStatus.NOT_FOUND)

        base_path = "./uploads/canciones/"

        # foto
        path_foto = base_path + str(data.foto)
        if os.path.exists(path_foto):
            os.remove(path_foto)

        # cancion
        path_cancion = base_path + str(data.cancion)
        if os.path.exists(path_cancion):
            os.remove(path_cancion)

        # video
        if data.video:
            path_video = base_path + str(data.video)
            if os.path.exists(path_video):
                os.remove(path_video)

        # eliminar registro
        Cancion.objects.filter(id = id).delete()

        return JsonResponse({
            "estado": "ok",
            "mensaje": "Registro eliminado correctamente"
        }, status=HTTPStatus.OK)

