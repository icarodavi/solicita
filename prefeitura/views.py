from django.shortcuts import render
from django.views.generic.list import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Prefeitura

# Create your views here.


class PrefeituraListView(LoginRequiredMixin, ListView):
    model = Prefeitura
    template_name = "prefeitura/index.html"
    context_object_name = 'prefeituras'
    paginate_by = 10
