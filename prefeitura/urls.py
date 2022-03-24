from django.urls import path
from .views import PrefeituraListView

app_name = 'prefeitura'

urlpatterns = [
    path('', PrefeituraListView.as_view(), name='index'),
]
