from django.shortcuts import render
from django.views import View
from .models import Perfil
# Create your views here.


class Login(View):
    template_name = 'perfil/index.html'
    model = Perfil

    def get(self, *args, **kwargs):
        return render(self.request, 'perfil/index.html')
