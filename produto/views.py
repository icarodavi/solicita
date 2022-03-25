from django.shortcuts import render
from django.views.generic.list import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Produto
# Create your views here.


class ProdutoList(LoginRequiredMixin, ListView):
    model = Produto
    template_name = 'produto/index.html'
    context_object_name = 'produtos'
    paginate_by = 10

    def get_queryset(self):
        qs = super().get_queryset()
        # qs = qs.select_related('variacao')
        return qs
