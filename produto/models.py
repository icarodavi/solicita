import os
from utils import utils
from PIL import Image
from django.conf import settings
from django.db import models
from django.utils.text import slugify


class Produto(models.Model):
    nome = models.CharField(max_length=255)
    descricao_curta = models.TextField(max_length=255)
    descricao_longa = models.TextField()
    imagem = models.ImageField(
        upload_to='produto_imagens/%Y/%m', blank=True, null=True)
    slug = models.SlugField(unique=True, blank=True, null=True)
    tipo = models.CharField(default='V',
                            max_length=1,
                            choices=((('V', 'Variação'), ('S', 'Simples'))))

    def __str__(self):
        return self.nome

    def save(self, *args, **kwargs):
        max_img_size = 800
        if not self.slug:
            slug = slugify(self.nome)
            self.slug = slug
        super().save(*args, **kwargs)

        if self.imagem:
            self.resize_image(self.imagem, max_img_size)

    @staticmethod
    def resize_image(image_name, new_width=800):
        image_path = os.path.join(settings.MEDIA_ROOT, str(image_name))
        image = Image.open(image_path)
        width, height = image.size
        new_height = round((new_width * height) / width)
        if width <= new_width:
            image.close()
            return None

        new_image = image.resize((new_width, new_height), Image.LANCZOS)
        new_image.save(
            image_path,
            optimize=True,
            quality=50
        )

    def get_preco_format(self):
        return utils.formata_preco(self.preco_marketing)
    get_preco_format.short_description = 'Preço'

    def get_preco_promocional_format(self):
        return utils.formata_preco(self.preco_marketing_promocional)
    get_preco_promocional_format.short_description = 'Preço promocional'


class Variacao(models.Model):
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    nome = models.CharField(max_length=60, blank=True, null=True)

    def __str__(self):
        return self.nome or self.produto.nome

    class Meta:
        verbose_name = 'Variação'
        verbose_name_plural = 'Variações'
