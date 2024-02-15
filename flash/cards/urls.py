from django.urls import path
from . import views

urlpatterns = [
   
    path('paginas/<int:pagina_id>/', views.paginas, name="paginas"),
    path('cadastro/', views.cadastro, name='cadastro'),
    path('login_user/', views.login_user, name='login_user'),
    path('logout/', views.logout_view, name='logout'),
    path('criar_pagina/', views.criar_pagina, name='criar_pagina'),
    path('listar_paginas/', views.listar_paginas_usuario, name='listar_paginas_usuario'),
    path('excluir_pagina/<int:pagina_id>/', views.excluir_pagina, name='excluir_pagina')

]
