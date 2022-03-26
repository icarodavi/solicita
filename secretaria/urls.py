from django.urls import path
from .views import SecretariaListView, SecretariaCreateView, SecretariaEdit, SecretariaDeleteView

app_name = 'secretaria'

urlpatterns = [
    path('', SecretariaListView.as_view(), name='index'),
    path('add/', SecretariaCreateView.as_view(), name='add'),
    path('edit/<pk>', SecretariaEdit.as_view(), name='edit'),
    path('del/<pk>', SecretariaDeleteView.as_view(), name='del'),
]
