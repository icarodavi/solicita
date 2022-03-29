from django.urls import path
from .views import ProdutoList, ProdutoCreateView, ProdutoEdit, ProdutoDeleteView, ProdutoSearch

app_name = 'produto'

urlpatterns = [
    path('',  ProdutoList.as_view(), name='index'),
    path('add/', ProdutoCreateView.as_view(), name='add'),
    path('edit/<pk>', ProdutoEdit.as_view(), name='edit'),
    path('del/<pk>', ProdutoDeleteView.as_view(), name='del'),
    path('search/', ProdutoSearch.as_view(), name='search')
]
