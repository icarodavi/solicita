from django import forms
from .models import Prefeitura


class PrefeituraForm(forms.ModelForm):

    class Meta:
        model = Prefeitura
        fields = "__all__"
