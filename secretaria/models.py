from tkinter import CASCADE
from django.db import models
from prefeitura.models import Prefeitura
# Create your models here.


class Secretaria(models.Model):
    nome = models.CharField(max_length=100)
    prefeitura = models.ForeignKey(Prefeitura, on_delete=models.CASCADE)
    endereco = models.CharField(max_length=200)
    secretario = models.CharField(max_length=120)
    ativo = models.BooleanField()
