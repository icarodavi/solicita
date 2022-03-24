from django.db import models

# Create your models here.


class Prefeitura(models.Model):
    nome = models.CharField(max_length=80)
    site = models.CharField(max_length=100, blank=True, null=True)
    logotipo = models.ImageField('Logotipo', blank=True, null=True)
    ativo = models.BooleanField()

    def __str__(self):
        return f'Prefeitura de {self.nome}'

    def get_prefeitura(self):
        return f'Prefeitura de {self.nome}'
