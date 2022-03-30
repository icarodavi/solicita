from django import forms
from .models import Prefeitura
from utils.resize import resize_uploaded_image


class PrefeituraForm(forms.ModelForm):

    class Meta:
        model = Prefeitura
        fields = "__all__"

    # def clean(self, *args, **kwargs):
    #     data = self.data
    #     logotipo = self.clean_image(self.logotipo)
    #     super().clean()

    # def clean_image(self, image_name):
    #     image = image_name
    #     image = resize_uploaded_image(image_name, 800)
    #     return image
