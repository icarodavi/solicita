from django.urls import path
from .views import ProdutoList, ProdutoCreateView, ProdutoEdit
from .views import ProdutoDeleteView, ProdutoSearch, generate_data, Buscador
from .views import Blank

app_name = 'produto'

urlpatterns = [
    path('',  ProdutoList.as_view(), name='index'),
    path('add/', ProdutoCreateView.as_view(), name='add'),
    path('edit/<pk>', ProdutoEdit.as_view(), name='edit'),
    path('del/<pk>', ProdutoDeleteView.as_view(), name='del'),
    path('search/', ProdutoSearch.as_view(), name='search'),
    path('busca/', Buscador.as_view(), name='buscador'),
    path('blank', Blank.as_view(), name='blank'),
    # path('gera/', generate_data, name='gera')
]
