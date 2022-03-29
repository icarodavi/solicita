import tempfile
import requests
import shutil
from django.db import models
from decouple import config
from utils.resize import resize_image
from utils.s3urls import create_presigned_url
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

    def get_logo(self):
        tempdir = tempfile.mkdtemp()
        url = create_presigned_url(
            config('AWS_STORAGE_BUCKET_NAME'), 'media/public/'+self.logotipo.name)
        file = requests.get(url, stream=True)
        with open(tempdir+self.logotipo.name, "wb") as f:
            file.raw.decode_content = True
            shutil.copyfileobj(file.raw, f)
            logo = f
        return logo
