import django
from django.urls import reverse_lazy
from django.views.generic.list import ListView
from django.views import View
from django.views.generic import UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render
from .models import Secretaria
from .forms import SecretariaForm


class SecretariaListView(LoginRequiredMixin, ListView):
    model = Secretaria
    template_name = "secretaria/index.html"
    context_object_name = 'secretarias'
    paginate_by = 10

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.select_related('prefeitura')
        return qs


class SecretariaCreateView(LoginRequiredMixin, View):
    model = Secretaria
    template_name = 'secretaria/form.html'
    fields = '__all__'
    success_url = 'secretaria:index'

    def get(self, *args, **kwargs):
        form = SecretariaForm()
        return render(self.request, 'secretaria/form.html', {'form': form})

    def post(self, *args, **kwargs):
        form = SecretariaForm(data=self.request.POST, files=self.request.FILES)
        if form.is_valid():
            form.save()
            return redirect('secretaria:index')
        else:
            return render(self.request, 'secretaria/form.html', {'form': form})


class SecretariaEdit(LoginRequiredMixin, UpdateView):
    model = Secretaria
    template_name = 'secretaria/edit.html'
    fields = '__all__'
    success_url = reverse_lazy('secretaria:index')


class SecretariaDeleteView(LoginRequiredMixin, DeleteView):
    model = Secretaria
    template_name = "secretaria/delete.html"
    success_url = reverse_lazy('secretaria:index')
