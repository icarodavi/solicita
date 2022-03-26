from django.db import models
from prefeitura.models import Prefeitura
# Create your models here.


class Secretaria(models.Model):
    nome = models.CharField(max_length=100)
    prefeitura = models.ForeignKey(Prefeitura, on_delete=models.CASCADE)
    endereco = models.CharField(max_length=200)
    secretario = models.CharField(max_length=120)
    ativo = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.nome} - {self.prefeitura}'

    def get_nome(self):
        return f'{self.prefeitura} - {self.nome}'

    def get_nome_secretaria(self):
        return f'{self.nome} - {self.prefeitura}'
