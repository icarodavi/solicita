from django.contrib import admin
from .models import Produto, Variacao

# Register your models here.


class VariacaoInLine(admin.TabularInline):
    model = Variacao
    extra = 1


class ProdutoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'tipo')
    inlines = [VariacaoInLine]


admin.site.register(Produto, ProdutoAdmin)
admin.site.register(Variacao)
