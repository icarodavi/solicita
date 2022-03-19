from django.db import models

# Create your models here.


class Prefeitura(models.Model):
    nome = models.CharField(max_length=80)
    site = models.CharField(max_length=100, blank=True, null=True)
    ativo = models.BooleanField()
