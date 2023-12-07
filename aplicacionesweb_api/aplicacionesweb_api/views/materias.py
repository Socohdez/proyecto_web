# users.py o materias.py
from django.shortcuts import render
from django.db.models import *
from django.db import transaction
from aplicacionesweb_api.serializers import *
from aplicacionesweb_api.models import *
from rest_framework.authentication import BasicAuthentication, SessionAuthentication, TokenAuthentication
from rest_framework.generics import CreateAPIView, DestroyAPIView, UpdateAPIView
from rest_framework import permissions
from rest_framework import generics
from rest_framework import status
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.reverse import reverse
from rest_framework import viewsets
from django.shortcuts import get_object_or_404
from django.core import serializers
from django.utils.html import strip_tags
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model
from django_filters.rest_framework import DjangoFilterBackend
from django_filters import rest_framework as filters
from datetime import datetime
from django.conf import settings
from django.template.loader import render_to_string
import string
import random
import json

class MateriasAll(generics.ListAPIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        # Obtener la lista de materias asociadas al usuario actual
        materias = Materia.objects.filter(usuario=request.user)
        lista = MateriaSerializer(materias, many=True).data
        return Response(lista, 200)

class MateriaDetailsView(generics.RetrieveAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    queryset = Materia.objects.all()
    serializer_class = MateriaSerializer

    def get(self, request, *args, **kwargs):
        # Obtener el ID de la materia desde la consulta
        materia_id = request.GET.get('id')

        # Verificar si el usuario actual es propietario de la materia
        materia = get_object_or_404(Materia, id=materia_id, usuario=request.user)

        # Serializar y devolver los detalles de la materia
        serializer = self.get_serializer(materia)
        return Response(serializer.data, status=status.HTTP_200_OK)

class MateriasView(generics.CreateAPIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        serializer = MateriaSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            # Asociar la materia al usuario actual
            serializer.validated_data['usuario'] = request.user
            materia = serializer.save()
            return Response({"materia_created_id": materia.id}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class MateriasViewEdit(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    queryset = Materia.objects.all()
    serializer_class = MateriaSerializer
    
    def put(self, request, *args, **kwargs):
        # Obtener la materia y verificar si pertenece al usuario actual
        
        #materia = self.get_object()
        materia_id = request.GET.get('id')
        
        # Verificar si el usuario actual es propietario de la materia
        materia = get_object_or_404(Materia, id=materia_id, usuario=request.user)
        if materia.usuario == request.user:
            serializer = self.get_serializer(materia, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({"details": "No tienes permisos para editar esta materia"}, status=status.HTTP_403_FORBIDDEN)

    def delete(self, request, *args, **kwargs):
        # Obtener el ID de la materia desde la consulta
        materia_id = request.GET.get('id')

        # Verificar si el usuario actual es propietario de la materia
        materia = get_object_or_404(Materia, id=materia_id, usuario=request.user)

        # Eliminar la materia
        materia.delete()

        return Response({"details": "Materia eliminada"}, status=status.HTTP_200_OK)

    