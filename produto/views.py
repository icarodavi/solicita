from pprint import pprint
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import DeleteView, UpdateView
from django.views.generic.list import ListView

from .forms import ProdutoForm
from .models import Produto


class ProdutoList(LoginRequiredMixin, ListView):
    model = Produto
    template_name = 'produto/index.html'
    context_object_name = 'produtos'
    paginate_by = 10

    def get_queryset(self):
        qs = super().get_queryset()
        return qs


class ProdutoCreateView(LoginRequiredMixin, View):
    model = Produto
    template_name = 'produto/form.html'
    fields = '__all__'
    success_url = 'produto:index'

    def get(self, *args, **kwargs):
        form = ProdutoForm()
        return render(self.request, 'produto/form.html', {'form': form})

    def post(self, *args, **kwargs):
        form = ProdutoForm(data=self.request.POST, files=self.request.FILES)
        if form.is_valid():
            form.save()
            return redirect('produto:index')
        else:
            return render(self.request, 'produto/form.html', {'form': form})


class ProdutoEdit(LoginRequiredMixin, UpdateView):
    model = Produto
    template_name = 'produto/edit.html'
    fields = '__all__'
    success_url = reverse_lazy('produto:index')


class ProdutoDeleteView(LoginRequiredMixin, DeleteView):
    model = Produto
    template_name = "produto/delete.html"
    success_url = reverse_lazy('produto:index')


class ProdutoSearch(LoginRequiredMixin, View):
    model = Produto

    def get(self, *args, **kwargs):
        search = self.request.GET['search']
        payload = []
        if search:
            objs: Produto = Produto.objects.filter(nome__icontains=search)
            for item in objs:
                payload.append({
                    'id': item.id,
                    'nome': item.nome,
                    'descricao_curta': item.descricao_curta,
                    'descricao_longa': item.descricao_longa,
                    'imagem': item.imagem.name,
                    'url': item.slug
                })

        return JsonResponse({
            'status': 200,
            'data': payload
        })
