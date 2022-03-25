from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic.list import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.views.generic.edit import UpdateView, DeleteView
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
        form = PrefeituraForm(data=self.request.POST, files=self.request.FILES)
        if form.is_valid():
            form.save()
            return redirect('prefeitura:index')
        else:
            return render(self.request, 'prefeitura/form.html', {'form': form})


class PrefeituraEdit(LoginRequiredMixin, UpdateView):
    model = Prefeitura
    template_name = 'prefeitura/edit.html'
    fields = '__all__'
    success_url = reverse_lazy('prefeitura:index')


# def post(self, *args, **kwargs):
#     data = self.request.POST
#     form = PrefeituraForm(data=self.request.POST, files=self.request.FILES)
#     if form.is_valid():
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
