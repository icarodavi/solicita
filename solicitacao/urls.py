from django.urls import path
from .views import SolicitacaoIndex, SolicitacaoDetailView, SolicitacaoPDF

app_name = 'solicitacao'

urlpatterns = [
    path('', SolicitacaoIndex.as_view(), name='index'),
    path('solicita/<pk>', SolicitacaoDetailView.as_view(), name='solicita'),
    path('pdf/<pk>', SolicitacaoPDF.as_view(), name='pdf'),
]
