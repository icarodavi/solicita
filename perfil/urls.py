from django.urls import path
from .views import Login
app_name = 'perfil'

urlpatterns = [
    path('', Login.as_view(), name='index')
]
