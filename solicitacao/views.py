import django
from django.shortcuts import render
from django.http.response import HttpResponse
from django.views.generic import View
from django.views.generic.list import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Solicitacao, SolicitacaoItem
# Create your views here.


class SolicitacaoIndex(LoginRequiredMixin, ListView):
    model = Solicitacao
    template_name = 'solicitacao/index.html'
    context_object_name = 'solicitacoes'
    paginate_by = 10

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.select_related('secretaria')
        return qs
