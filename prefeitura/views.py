from dataclasses import fields
from django.shortcuts import redirect, render
from django.views.generic.list import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.views.generic.edit import UpdateView
from .models import Prefeitura
from .forms import PrefeituraForm

# Create your views here.


class PrefeituraListView(LoginRequiredMixin, ListView):
    model = Prefeitura
    template_name = "prefeitura/index.html"
    context_object_name = 'prefeituras'
    paginate_by = 10


class PrefeituraCreate(LoginRequiredMixin, View):
    model = Prefeitura
    template_name = 'prefeitura/form.html'
    fields = '__all__'
    success_url = 'prefeitura:index'

    def get(self, *args, **kwargs):
        form = PrefeituraForm()

        return render(self.request, 'prefeitura/form.html', {'form': form})

    def post(self, *args, **kwargs):
        data = self.request.POST
        form = PrefeituraForm(data=self.request.POST, files=self.request.FILES)
        if form.is_valid():
            form.save()
            return redirect('prefeitura:index')
        else:
            return render(self.request, 'prefeitura/form.html', {'form': form})


class PrefeituraEdit(LoginRequiredMixin, View):
    model = Prefeitura
    template_name = 'prefeitura/edit.html'
    fields = '__all__'
    success_url = 'prefeitura:index'

    def get(self, *args, **kwargs):
        pk = self.pk
        form = PrefeituraForm()

        return render(self.request, 'prefeitura/edit.html', {'form': form})
