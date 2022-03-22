from django.urls import path
from .views import Login
from django.contrib.auth.views import LoginView, LogoutView

app_name = 'perfil'

urlpatterns = [
    path('', LoginView.as_view(template_name='perfil/index.html'), name='index'),
    path('login/', LoginView.as_view(
        template_name='perfil/index.html'
    ), name='login'),
    path('logout/', LogoutView.as_view(), name='logout')
]
