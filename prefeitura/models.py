from django.db import models
from utils.resize import resize_image
# Create your models here.


class Prefeitura(models.Model):
    nome = models.CharField(max_length=80)
    site = models.CharField(max_length=100, blank=True, null=True)
    logotipo = models.ImageField(
        'Logotipo', upload_to='prefeitura/%Y/%m', blank=True, null=True)
    ativo = models.BooleanField(default=True)

    def __str__(self):
        return f'Prefeitura de {self.nome}'

    def get_prefeitura(self):
        return f'Prefeitura de {self.nome}'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        max_img_size = 800
        if self.logotipo:
            resize_image(self.logotipo, max_img_size)
