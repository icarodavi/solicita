from django.urls import path
from .views import PrefeituraListView, PrefeituraCreate, PrefeituraEdit, PrefeituraDeleteView

app_name = 'prefeitura'

urlpatterns = [
    path('', PrefeituraListView.as_view(), name='index'),
    path('add/', PrefeituraCreate.as_view(), name='add'),
    path('edit/<pk>', PrefeituraEdit.as_view(), name='edit'),
    path('del/<pk>', PrefeituraDeleteView.as_view(), name='del'),
]
