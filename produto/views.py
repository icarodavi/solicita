import copy
import itertools
import json
from pprint import pprint

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import DeleteView, UpdateView
from django.views.generic.list import ListView
from faker import Faker
from solicitacao.models import Solicitacao, SolicitacaoItem

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
                    'produto': item.nome,
                    'descricao_curta': item.descricao_curta,
                    'descricao_longa': item.descricao_longa,
                    'imagem': item.imagem.name,
                    'unidade': item.unidade,
                    'delete': False,
                })

        return JsonResponse({
            'status': 200,
            'data': payload
        })


class Buscador(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        solicitacao = Solicitacao.objects.filter(pk=kwargs.get(
            'pk')).first()
        items = SolicitacaoItem.objects.filter(
            solicitacao=solicitacao).values()
        if items:
            contexto = {'solicitacao': solicitacao,
                        'items': json.dumps(list(items))}
        else:
            contexto = {'solicitacao': solicitacao}
        return render(self.request, 'produto/busca.html', context=contexto)

    def post(self, *args, **kwargs):

        data = json.loads(self.request.POST.get('objProdutos'))
        # produtos = {'produtos': data}
        solicitacao = Solicitacao.objects.filter(
            pk=kwargs.get('pk')).first()
        list_data = [SolicitacaoItem(
            solicitacao=solicitacao,
            produto=v['produto'],
            produto_id=v['id'],
            qtd=v['qtd'],
            imagem=v['imagem'],
        ) for v in data]
        solicitacao.solicitacaoitem_set.all().delete()
        solicitacao.solicitacaoitem_set.set(list_data, bulk=False, clear=True)

        # return render(self.request, 'produto/blank.html', context=produtos)
        return redirect('solicitacao:edit', solicitacao.id)


class Blank(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        return render(self.request, 'produto/blank.html')

    def post(self, *args, **kwargs):
        produtos = {'produtos': json.loads(
            self.request.POST.get('objProdutos'))}
        return render(self.request, 'produto/blank.html', context=produtos)


def generate_data(request):
    faker: Faker = Faker('pt_BR')
    for i in range(0, 10):
        Produto.objects.create(
            nome=faker.company(),
            descricao_curta=faker.paragraphs(nb=1),
            descricao_longa=faker.paragraphs(nb=5),
        )
    return JsonResponse({
        'status': 200
    })
