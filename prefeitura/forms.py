from pprint import pprint

from django import forms
from utils.resize import resize_image

from .models import Prefeitura


class PrefeituraForm(forms.ModelForm):

    class Meta:
        model = Prefeitura
        fields = "__all__"

    def clean(self, *args, **kwargs):
        # logotipo = self.cleaned_data.get('logotipo')
        # logotipo.image = resize_image(self.cleaned_data.get('logotipo')))
        # pprint(dir(data.cleaned_data))
        # pprint(self.cleaned_data)
        # logotipo = self.clean_image(self.logotipo)
        super().clean()

    # def clean_image(self, image_name):
    #     image = image_name
    #     image = resize_uploaded_image(image_name, 800)
    #     return image
