from django.contrib import admin
from .models import Prefeitura
# Register your models here.


class PrefeituraAdmin(admin.ModelAdmin):
    list_display = ['nome', 'site', 'ativo']
    list_editable = ['ativo']


admin.site.register(Prefeitura, PrefeituraAdmin)
