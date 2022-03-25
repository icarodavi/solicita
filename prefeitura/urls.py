from django.urls import path
from .views import PrefeituraListView, PrefeituraCreate, PrefeituraEdit

app_name = 'prefeitura'

urlpatterns = [
    path('', PrefeituraListView.as_view(), name='index'),
    path('add/', PrefeituraCreate.as_view(), name='add'),
    path('edit/<pk>', PrefeituraEdit.as_view(), name='edit'),
]
