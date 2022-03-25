from django.contrib import admin
from .models import Produto

# Register your models here.


# class VariacaoInLine(admin.TabularInline):
#     model = Variacao
#     extra = 1


class ProdutoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'descricao_curta')
    # inlines = [VariacaoInLine]


admin.site.register(Produto, ProdutoAdmin)
# admin.site.register(Variacao)
