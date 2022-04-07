from pprint import pprint

from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic.edit import DeleteView, UpdateView
from django.views.generic.list import ListView
from utils.resize import resize_image

from .forms import PrefeituraForm
from .models import Prefeitura

# Create your views here.


class PrefeituraListView(LoginRequiredMixin, ListView):
    model = Prefeitura
    template_name = "prefeitura/index.html"
    context_object_name = 'prefeituras'
    paginate_by = 10


class PrefeituraCreate(LoginRequiredMixin, View):
    model = Prefeitura
    template_name = 'prefeitura/form.html'
    # fields = '__all__'
    success_url = 'prefeitura:index'
    form_class = PrefeituraForm

    def get(self, *args, **kwargs):
        form = PrefeituraForm()

        return render(self.request, 'prefeitura/form.html', {'form': form})

    def post(self, *args, **kwargs):
        form = PrefeituraForm(data=self.request.POST, files=self.request.FILES)
        if form.is_valid():
            form.save(commit=False)
            # x = resize_image(form.files.get('logotipo'), 800)
            x = False
            if x:
                form.files.logotipo = x
                form.save()
            else:
                form.save()
            # self.logotipo.save(
            #     name=Path(self.logotipo.file.name).name, content=x)
            return redirect('prefeitura:index')
        else:
            return render(self.request, 'prefeitura/form.html', {'form': form})


class PrefeituraEdit(LoginRequiredMixin, UpdateView):
    model = Prefeitura
    template_name = 'prefeitura/edit.html'
    # fields = '__all__'
    success_url = reverse_lazy('prefeitura:index')
    form_class = PrefeituraForm


# def post(self, *args, **kwargs):
#     # super().post(self.request, *args, **kwargs)
#     form = PrefeituraForm(data=self.request.POST, files=self.request.FILES)
#     nome = form.cleaned_data.get('nome')
#     site = form.cleaned_data.get('site')
#     logotipo = form.cleaned_data.get('logotipo')
#     prefeitura = get_object_or_404(Prefeitura, pk=kwargs.get('pk'))
#     if form.is_valid():

#         self.request.FILES['logotipo'] = resize_image(
#             self.request.FILES.get('logotipo'), 800)
#         form.save()
#         return redirect('prefeitura:index')
#     else:
#         return render(self.request, 'prefeitura/form.html', {'form': form})
    # def get(self, *args, **kwargs):
    #     pk = int(kwargs.get('pk'))
    #     prefeitura = Prefeitura.objects.filter(pk=pk)
    #     print(prefeitura.__dict__)
    #     prefeitura_comp = {
    #         'id': prefeitura['id'],
    #         'nome': prefeitura['nome'],
    #         'site': prefeitura['site'],
    #         'logotipo': prefeitura['logotipo'],
    #         'ativo': prefeitura['ativo']
    #     }
    #     form = PrefeituraForm(prefeitura_comp)

    #     return render(self.request, 'prefeitura/edit.html', {'form': form})

# class PrefeituraDelete(LoginRequiredMixin, View):
#     def get(self, *args, **kwargs):
#         pass


class PrefeituraDeleteView(LoginRequiredMixin, DeleteView):
    model = Prefeitura
    template_name = "prefeitura/delete.html"
    success_url = reverse_lazy('prefeitura:index')
