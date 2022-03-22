from django.contrib import admin
from .models import Solicitacao, SolicitacaoItem
# Register your models here.


class SolicitacaoItemInline(admin.TabularInline):
    model = SolicitacaoItem
    extra = 1


class SolicitacaoAdmin(admin.ModelAdmin):
    inlines = [SolicitacaoItemInline]


admin.site.register(Solicitacao, SolicitacaoAdmin)
admin.site.register(SolicitacaoItem)
