"""solicita URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import include, path
from solicitacao.views import password_reset_request

urlpatterns = [
    path('admin/', admin.site.urls),
    path('perfil/', include('perfil.urls')),
    path('produto/', include('produto.urls')),
    path('prefeitura/', include('prefeitura.urls')),
    path('secretaria/', include('secretaria.urls')),
    # path('accounts/', include('django.contrib.auth.urls')),
    path('password_reset/templates/done/', auth_views.PasswordResetDoneView.as_view(
        template_name='password/templates/password_reset_done.html'), name='password_reset_done'),
    path('password_reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name="password/templates/password_reset_confirm.html"), name='password_reset_confirm'),
    path('password_reset/done/', auth_views.PasswordResetCompleteView.as_view(
        template_name='password/templates/password_reset_complete.html'), name='password_reset_complete'),
    path("password_reset/", password_reset_request, name="password_reset"),
    path('', include('solicitacao.urls'))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
