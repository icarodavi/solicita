from django.shortcuts import render
from django.http.response import HttpResponse
from django.views.generic import View
# Create your views here.


class SolicitacaoIndex(View):
    def get(self, *args, **kwargs):
        return HttpResponse('SOLICITAÇÃO!')
