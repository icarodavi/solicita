from django.contrib import admin

from .models import Solicitacao, SolicitacaoItem

# Register your models here.


class SolicitacaoItemInline(admin.TabularInline):
    model = SolicitacaoItem
    extra = 1
    # autocomplete_fields = ['solicitacao_item']


class SolicitacaoAdmin(admin.ModelAdmin):
    inlines = [SolicitacaoItemInline]
    search = ['secretaria ']


admin.site.register(Solicitacao, SolicitacaoAdmin)
admin.site.register(SolicitacaoItem)
