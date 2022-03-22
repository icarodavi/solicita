from django.contrib import admin
from .models import Secretaria


class SecretariaAdmin(admin.ModelAdmin):
    list_display = ['nome', 'prefeitura', 'secretario', 'ativo']
    list_editable = ['ativo']


admin.site.register(Secretaria, SecretariaAdmin)
