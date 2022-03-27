from django.urls import path
from .views import SolicitacaoDOCX, SolicitacaoIndex, SolicitacaoDetailView, SolicitacaoPDF

app_name = 'solicitacao'

urlpatterns = [
    path('', SolicitacaoIndex.as_view(), name='index'),
    path('solicita/<pk>', SolicitacaoDetailView.as_view(), name='solicita'),
    path('pdf/<pk>', SolicitacaoPDF.as_view(), name='pdf'),
    path('docx/<pk>', SolicitacaoDOCX.as_view(), name='doc'),
]
