from django.urls import path
from . import views

urlpatterns = [
   
    path('', views.home, name="home"),
    path('registro/', views.registro, name="registro"),
    path('configuracao/', views.configuracao, name="configuracao"),
    path('login/', views.login, name='login'),
]
