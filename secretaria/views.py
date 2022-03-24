from django.views.generic.list import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Secretaria
# Create your views here.


class SecretariaListView(LoginRequiredMixin, ListView):
    model = Secretaria
    template_name = "secretaria/index.html"
    context_object_name = 'secretarias'
    paginate_by = 10

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.select_related('prefeitura')
        return qs
