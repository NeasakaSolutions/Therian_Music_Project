# Importaciones:
from django.db import models
from autoslug import AutoSlugField


# Create your models here.
class Artista(models.Model):
    nombre = models.CharField(max_length = 100, null = False)
    slug = AutoSlugField(populate_from = "nombre")

    def __str__(self):
        return self.nombre

    class Meta:
        db_table = "artistas"
        verbose_name = "Artista"
        verbose_name_plural = "Artistas"
