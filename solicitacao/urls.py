from django.urls import path

from .views import (SolicitacaoCreateView, SolicitacaoDeleteView,
                    SolicitacaoDetailView, SolicitacaoDOCX, SolicitacaoEdit,
                    SolicitacaoIndex, SolicitacaoPDF)

app_name = 'solicitacao'

urlpatterns = [
    path('', SolicitacaoIndex.as_view(), name='index'),
    path('solicita/<pk>', SolicitacaoDetailView.as_view(), name='solicita'),
    path('pdf/<pk>', SolicitacaoPDF.as_view(), name='pdf'),
    path('docx/<pk>', SolicitacaoDOCX.as_view(), name='doc'),
    path('add/', SolicitacaoCreateView.as_view(), name='add'),
    path('edit/<pk>', SolicitacaoEdit.as_view(), name='edit'),
    path('del/<pk>', SolicitacaoDeleteView.as_view(), name='del'),
]
