from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('paginas/<int:pagina_id>/', views.paginas, name="paginas"),
    path('cadastro/', views.cadastro, name='cadastro'),
    path('login_user/', views.login_user, name='login_user'),
    path('logout/', views.logout_view, name='logout'),
    path('criar_pagina/', views.criar_pagina, name='criar_pagina'),
    path('listar_paginas/', views.listar_paginas_usuario, name='listar_paginas_usuario'),
    path('excluir_pagina/<int:pagina_id>/',views.excluir_pagina, name='excluir_pagina'),
    path('conf/', views.conf, name='configurar'),
    path('add_cards/', views.add_cards, name='add_cards'),
    path('delete_card/', views.delete_card, name='delete_card'),
    path('edit_cards/', views.edit_cards, name='edit_cards'),
    path('add_alunos/', views.add_alunos, name='add_alunos'),
    path('paginas_compartilhadas/<int:pagina_compartilhada_id>/', views.paginas_compartilhadas, name='paginas_compartilhadas'),

    #Area de conf
    path('simulado/<int:id_pagina>', views.simulado, name='simulado'),#aqui precisa de ID.
    path('questao_simulado/', views.questao_simulado, name='questao_simulado'),
    path('add_pagina_simulado/', views.add_pagina_simulado, name='add_pagina_simulado'), 
    path('checar_resposta/', views.checa_resposta_simulado, name='checa_resposta'),
    path('delete_questao/', views.delete_simulado, name='delete_questao'),
    path('edit_simulado/', views.edit_simulado, name='edit_simulado'),

    #Area de conf
    path('edit_paginas_conf/', views.edit_paginas_conf, name='edit_paginas_conf'),
    path('edit_titulo_pag_conf/', views.edit_titulo_pag_conf, name='edit_titulo_pag_conf'),
    path('delete_pg_conf/', views.delete_pg_conf, name='delete_pg_conf'),
    path('dash_estatistica/', views.dash_estatistica, name='dash_estatistica')
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
