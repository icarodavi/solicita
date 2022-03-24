from django.urls import path
from .views import ProdutoList

app_name = 'produto'

urlpatterns = [
    path('',  ProdutoList.as_view(), name='index'),
]
