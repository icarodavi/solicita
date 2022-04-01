import os
import tempfile
from io import BytesIO
from pathlib import Path
from pprint import pprint

import requests
from decouple import config
from django.core.files import File
from django.db import models
from PIL import Image
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
        print(self.logotipo._file)

    def get_logo(self):
        tempdir = tempfile.mkdtemp()
        logo = ''
        url = create_presigned_url(
            config('AWS_STORAGE_BUCKET_NAME'), 'media/public/'+self.logotipo.name)
        file = requests.get(url, stream=True)
        if file.status_code == 200:
            filename, filext = os.path.splitext(self.logotipo.name)
            with open(os.path.join(tempdir, 'logotipo'+filext), "wb") as f:
                f.write(file.content)
                logo = f
        return logo.name

    @staticmethod
    def resize_image(image_name: models.ImageField, new_width, *args, **kwargs):
        img = Image.open(image_name)
        width, height = img.size
        new_height = round((new_width * height) / width)
        size = (new_width, new_height)
        # img_filename = Path(image_name.file.name).name
        if width > new_width:
            pass
        img.resize(size, Image.LANCZOS)
        filename, filext = os.path.splitext(image_name._file.name)
        buffer = BytesIO()
        # image_path = os.path.join(tempfile.mkdtemp(), str(image_name))
        file_object = File(buffer)
        img.save(file_object, format=img.format)
        img.close()
        print('------------')
        pprint(dir(file_object))
        image_name._file = Image.open(file_object)
        # img._committed = False
        # img.name = img_filename
        # img.file = image_name.file
        # x = Image.open(file_object)

        # image_name
        pprint(vars(image_name.field))
        # img.close()
        # image_name.save(img_filename, file_object)
        return image_name
