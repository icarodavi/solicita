from django.urls import path
from .views import SecretariaListView

app_name = 'secretaria'

urlpatterns = [
    path('', SecretariaListView.as_view(), name='index'),
]
