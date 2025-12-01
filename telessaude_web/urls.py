"""projeto URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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

from django.urls import path, re_path, include
from django.views.static import serve
from django.contrib.auth import views as auth_views
from django.conf import settings
from . import views, htmx_views
from rest_framework.routers import DefaultRouter
from .views import ProfissionalSaudeViewSet, FuncionarioViewSet, PacienteViewSet, ConsultaViewSet


router = DefaultRouter()
router.register(r'profissionais', ProfissionalSaudeViewSet)
router.register(r'funcionarios', FuncionarioViewSet)
router.register(r'pacientes', PacienteViewSet)
router.register(r'consultas', ConsultaViewSet)

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('consultas/', views.consultas, name='consultas'),
    path('sala/<int:pk>/', views.sala, name='sala'),
    path('enviarmsg/<int:pk>/', views.enviarmensagem, name='enviarmensagem'),
    path('deletarconsulta/<int:id>/', views.deleteConsulta, name='deletarconsulta'),
    path('register/', views.register, name='cadastro'),
    path('profile/', views.perfil, name='perfil'),
    path('recover_password/', views.recuperarsenha, name='recuperarsenha'),
    path('api/', include(router.urls)),
    path('get_msg/<int:pk>/', htmx_views.getMensagem),
    path('get_token/', views.getToken, name='get_token'),
    path('get_user/', views.getUser),
    path('logout/', views.sair, name='sair'),
    re_path(r'^media/(?P<path>.*)$', serve,{'document_root': settings.MEDIA_ROOT}),
    re_path(r'^static/(?P<path>.*)$', serve,{'document_root': settings.STATIC_ROOT}),
]






"""path('form/', views.form, name = 'form'),
path('create/', views.create, name = 'create'),
path('read/<int:pk>/', views.read, name = 'read'),
path('edit/<int:pk>/', views.edit, name = 'edit'),
path('update/<int:pk>/', views.update, name = 'update')"""
