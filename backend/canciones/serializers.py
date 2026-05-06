# Importaciones:
import os
from rest_framework import serializers
from canciones.models import Cancion
from dotenv import load_dotenv

class CancionSerializer(serializers.ModelSerializer):

    # Formatear datos:
    categoria = serializers.ReadOnlyField(source = "categoria.nombre")
    artista = serializers.ReadOnlyField(source = "artista.nombre")
    fecha = serializers.DateTimeField(format = "%d/%m/%Y")
    imagen = serializers.SerializerMethodField()
    cancion = serializers.SerializerMethodField()
    video = serializers.SerializerMethodField()

    class Meta:
        model = Cancion
        fields = ("id", "nombre", "slug", "descripcion", "fecha", "categoria_id", "categoria", 
                  "artista_id", "artista", "imagen", "cancion", "video")

    # Formateo de la imagen:
    def get_imagen(self, obj):
        return f"{os.getenv("BASE_URL")}uploads/canciones/{obj.foto}"

    # Formateo de la cancion:
    def get_cancion(self, obj):
        return f"{os.getenv("BASE_URL")}uploads/canciones/{obj.cancion}"
    
    # Formateo de los videos:
    def get_video(self, obj):
        return f"{os.getenv("BASE_URL")}uploads/canciones/{obj.video}"