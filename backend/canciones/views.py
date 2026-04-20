# Importaciones
from django.shortcuts import render
from rest_framework.views import APIView
from django.http.response import JsonResponse
from rest_framework.response import Response
from http import HTTPStatus
from django.http import Http404
from django.utils.text import slugify

# Clase sin argumentos:
class CancionesLista(APIView):

    def get(self, request):
        pass

