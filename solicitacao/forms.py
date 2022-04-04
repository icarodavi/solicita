from django.contrib.auth.models import User
from django.forms import DateField, DateInput, ModelForm
from tempus_dominus.widgets import DatePicker

from .models import Solicitacao


class SolicitacaoForm(ModelForm):

    data = DateField(
        input_formats=['%d/%m/%Y'],
        widget=DatePicker(
            attrs={
                # 'class': 'form-control datetimepicker-input',
                # 'data-target': '#id_data'
                'append': 'fa fa-calendar',
                'icon_toggle': True
            },
        ),
        required=False)

    class Meta:
        model = Solicitacao
        fields = '__all__'
        exclude = ('usuario', 'qtd_total',)


class PasswordResetForm(ModelForm):

    class Meta:
        model = User
        fields = ('email',)
        # exclude = ('password', 'las_login')
