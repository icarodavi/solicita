from django.forms import ModelForm
from .models import Solicitacao


class SolicitacaoForm(ModelForm):

    class Meta:
        model = Solicitacao
        fields = '__all__'
        exclude = ('usuario', 'qtd_total',)
