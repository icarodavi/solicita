from django.db import models
from django.utils.text import slugify

# from utils.resize import resize_image


class Produto(models.Model):
    nome = models.CharField(max_length=255)
    descricao_curta = models.TextField(max_length=255)
    descricao_longa = models.TextField()
    unidade = models.CharField(max_length=30, default='UN')
    imagem = models.ImageField(
        upload_to='produto_imagens/%Y/%m', blank=True, null=True)
    slug = models.SlugField(blank=True, null=True)

    def __str__(self):
        return f'{self.nome}'

    def save(self, *args, **kwargs):
        # max_img_size = 800
        if not self.slug:
            slug = slugify(self.nome)
            self.slug = slug
        super().save(*args, **kwargs)
        # if self.imagem:
        #     resize_image(self.imagem, max_img_size)
