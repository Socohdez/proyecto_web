from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authentication import TokenAuthentication
from django.contrib.auth.models import AbstractUser, User
from django.conf import settings

class BearerTokenAuthentication(TokenAuthentication):
    keyword = u"Bearer"


class Profiles(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=False, default=None)
    matricula = models.CharField(max_length=255, null=True, blank=True)
    curp = models.CharField(max_length=255, null=True, blank=True)
    rfc = models.CharField(max_length=255, null=True, blank=True)
    fecha_nacimiento = models.DateTimeField(auto_now_add=False, null=True, blank=True)
    edad = models.IntegerField(null=True, blank=True)
    telefono = models.CharField(max_length=255, null=True, blank=True)
    ocupacion = models.CharField(max_length=255, null=True, blank=True)
    creation = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    update = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return "Perfil del usuario "+self.usuario.first_name+" "+self.usuario.last_name

class Materia(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=False, default=None)
    nrc = models.CharField(max_length=10)
    nombre = models.CharField(max_length=255)
    seccion = models.CharField(max_length=10)
    dias = models.CharField(max_length=50)
    hora_inicio = models.TimeField()
    hora_final = models.TimeField()
    salon = models.CharField(max_length=20)
    programa_educativo = models.CharField(max_length=255)  # Puedes ajustar esto según tus necesidades

    def __str__(self):
        return self.nombre

