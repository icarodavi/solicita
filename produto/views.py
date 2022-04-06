import copy
import itertools
import json
from pprint import pprint
from tkinter.tix import Tree

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

# from pprint import pprint


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


class Buscador(View):
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
        # pprint(data)
        data_final = copy.deepcopy(data)
        produtos = {'produtos': data}
        solicitacao = Solicitacao.objects.filter(
            pk=kwargs.get('pk')).first()
        solicitacao_itens = solicitacao.solicitacaoitem_set.all()
        atualizar_itens = set([])
        deletar_itens = set([])
        criar_itens = set([])
        for solicitacao_item in solicitacao_itens:
            for data_item in data:
                # print(data_item)
                if data_item.get('delete'):
                    deletar_itens.add(solicitacao_item)
                    # print('delete')
                else:
                    if not solicitacao_item.get_nome() in list(data_item.values()):
                        # if solicitacao_item.get_nome()
                        # deletar_itens.add(solicitacao_item)
                        pass
                    else:
                        atualizar_itens.add(data_item)
                        index_data = data_final.index(data_item)
                        data_final.pop(index_data)

        criar_itens = [item for item in data_final]
        atualizar_itens = [item for item in atualizar_itens]
        deletar_itens = [item for item in deletar_itens]
        pprint(criar_itens)
        print('-'*100)
        pprint(atualizar_itens)
        print('-'*100)
        pprint(deletar_itens)
        print('-'*100)
        # if deletar_itens:
        #     # apagar = [SolicitacaoItem(id=item['id']) for item in deletar_itens]
        #     SolicitacaoItem.delete(deletar_itens)
        #     print('deletar_itens', deletar_itens)
        #     # print(apagar)
        #     pass

        # if criar_itens:
        #     SolicitacaoItem.objects.bulk_create(
        #         [SolicitacaoItem(
        #             solicitacao=solicitacao,
        #             produto=v['produto'],
        #             produto_id=v['id'],
        #             quantidade=v['quantidade'],
        #             imagem=v['imagem'],
        #         ) for v in criar_itens]
        #     )
        # if atualizar_itens:
        #     upds = SolicitacaoItem.objects.bulk_update(
        #         [SolicitacaoItem(
        #             id=v['id'],
        #             quantidade=v['quantidade']
        #         ) for v in atualizar_itens], ['quantidade'])
        #     print(upds)
        return render(self.request, 'produto/blank.html', context=produtos)

    def verifica_deletados(self, lista_deletados, lista_banco, *args, **kwargs):
        deletados = [{'id': x.__dict__['id'],
                      'solicitacao_id': x.__dict__['solicitacao_id'],
                      'produto': x.__dict__['produto'],
                      'produto_id': x.__dict__['produto_id'],
                      'quantidade': x.__dict__['quantidade'],
                      'imagem': x.__dict__['imagem'],
                      } for x in lista_deletados]

        return deletados


class Blank(View):
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
