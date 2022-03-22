from django.urls import path
from .views import SolicitacaoIndex

app_name = 'solicitacao'

urlpatterns = [
    path('', SolicitacaoIndex.as_view(), name='index')
]
