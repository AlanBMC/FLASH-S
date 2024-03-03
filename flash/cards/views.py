from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth import login as login_django
from django.db import IntegrityError
from .models import Usuario, Pagina, Cards, Simulados
from django.http import JsonResponse
from django.contrib import messages
from django.contrib.auth import logout
import json
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
# Create your views here.


def cadastro(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        arroba = request.POST.get('arroba')
        senha = request.POST.get('password')
        tipo_user = request.POST.get('tipo_user')
        img = request.FILES.get('imagem_de_perfil', None)
        if User.objects.filter(username=username).exists():
            # Usar mensagens para enviar feedback ao usuário
            return render(request, 'registro.html', {'error_message': 'Nome de usuário já existe. Por favor, escolha outro nome.'})
        else:
            user = User.objects.create_user(
                username=username, email=arroba, password=senha)
            user.save()
            usuario = Usuario(arroba=username, tipo_user=tipo_user)
            if img:
                usuario.foto_perfil = img
            else:
                messages.error(request, 'Coloque uma foto de perfil')
                return redirect('cadastro')
            usuario.save()
            # retirar perguntas e respostas.
            pagina = Pagina.objects.create(
                titulo='Home')
            usuario.paginas.add(pagina)
            return redirect('login_user')
    else:
        return render(request, 'registro.html')


def login_user(request):
    if request.method == 'POST':
        nome = request.POST.get('username')
        senha = request.POST.get('password')
        user = authenticate(username=nome, password=senha)
        if user:
            login_django(request, user)
            try:
                usuario = Usuario.objects.get(arroba=nome)
                pagina = usuario.paginas.all().first()
                if pagina:
                    return redirect('paginas', pagina_id=pagina.id)
                else:
                    return redirect('login_user')
            except Usuario.DoesNotExist:

                return render(request, 'login_user', {'erro': 'Usuário ou Senha Incorreto'})

        else:
            return render(request, 'login1.html', {'erro': 'Usuário ou Senha Incorreto'})
    else:
        return render(request, 'login1.html')


@login_required(login_url="/user/login_user/")
def paginas(request, pagina_id):
    user_arroba = request.user.username
    usuario = get_object_or_404(Usuario, arroba=user_arroba)

    if usuario.paginas.filter(id=pagina_id).exists():
        cards = Cards.objects.filter(pagina_id=pagina_id)
        # instancia do objeto(classe) pagina, com a condição vai me retorna todos os objetos paginas que tem o id que passei como parametro
        pagina = get_object_or_404(Pagina, id=pagina_id)
        paginas_compartilhadas = usuario.paginas_compartilhadas.all()
        paginas_cards2 = Pagina.objects.filter(
            cards__isnull=False, usuarios=usuario).distinct()
        paginas_com_simulados = Pagina.objects.filter(
            simulado__isnull=False).distinct()
        print(paginas_com_simulados)
        conteudo = {'paginas': pagina,
                    'cards': cards,
                    'paginas_com_card': paginas_cards2,
                    'paginas_simulado': paginas_com_simulados,
                    'tipo_user': usuario.tipo_user,
                    'paginas_compartilhadas': paginas_compartilhadas,
                    'foto_perfil': usuario.foto_perfil.url}

        if usuario.tipo_user == 'professor':
            return render(request, 'professor.html', conteudo)
        else:
            return render(request, 'aluno.html', conteudo)

    else:
        pagina = usuario.paginas.all().first()
        messages.info(
            request, " ")

        return redirect('paginas', pagina_id=pagina.id)


def logout_view(request):
    logout(request)
    return redirect('login_user')


@csrf_exempt
def criar_pagina(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        titulo = data.get('titulo')
        user_arroba = request.user.username
        print(request.user.username)
        try:
            usuario = Usuario.objects.get(arroba=user_arroba)
            nova_pagina = Pagina.objects.create(titulo=titulo)
            usuario.paginas.add(nova_pagina)

            url_pagina = f'/user/paginas/{nova_pagina.id}/'
            return JsonResponse({'mensagem': 'Pagina criada com sucesso!', 'urlPagina': url_pagina}, status=201)
        except Usuario.DoesNotExist:
            return JsonResponse({"error": "Você não tem permissão para isso."}, status=404)
    else:
        return JsonResponse({'erro': 'Metodo Post nao requirido'}, status=405)


# colocar aqui tbm para colocar os cards em paginas correspondente.
@login_required
def listar_paginas_usuario(request):
    user_arroba = request.user.username  # ajuste conforme sua lógica de autenticação
    try:
        usuario = Usuario.objects.get(arroba=user_arroba)
        # Assumindo que 'paginas' é o nome do campo ManyToMany em Usuario para Pagina
        paginas = usuario.paginas.all()
        paginas_data = [{'titulo': pagina.titulo, 'id': pagina.id}
                        for pagina in paginas]
        return JsonResponse({'paginas': paginas_data})
    except Usuario.DoesNotExist:
        return JsonResponse({'erro': 'Usuário não encontrado'}, status=404)


@login_required
def conf(request):
    if request.method == 'POST':
        pass
    else:
        # assim que pega o ID atual do usuario logado
        user_arroba = request.user.username
        usuario = Usuario.objects.get(arroba=user_arroba)
        pagina = usuario.paginas.all().first()
        PG = usuario.paginas.all()
        # fim do bloco (id atual)
        print(pagina, pagina.id, pagina.titulo)

        return render(request, 'conf.html', {'paginas': pagina, 'pg_titulos': PG, 'tipo_user': usuario.tipo_user})


@require_POST
@login_required
def excluir_pagina(request, pagina_id):
    user_arroba = request.user.username
    usuario = get_object_or_404(Usuario, arroba=user_arroba)
    pagina = get_object_or_404(Pagina, id=pagina_id)
    pagina.delete()
    return JsonResponse({'mensagem': 'Pagina excluida com sucesso'})


# ----------- area de cards -----------------------
@require_POST
def add_cards(request):
    if request.method == 'POST':
        pergunta = request.POST.get('question')
        resposta = request.POST.get('answer')
        pagina_id = request.POST.get('pagina_id')
        pagina = Pagina.objects.get(id=pagina_id)
        Cards.objects.create(perguntas=pergunta,
                             respostas=resposta, pagina=pagina)

        return redirect('paginas', pagina_id=pagina_id)
    else:
        return HttpResponse('nao postou')


@require_POST
def delete_card(request):
    if request.method == 'POST':
        card_id = request.POST.get('card_id')
        pagina_id = request.POST.get('pagina_id')
        card = get_object_or_404(Cards, id=card_id)
        card.delete()
        return redirect('paginas', pagina_id=pagina_id)


@login_required
@require_POST
def edit_cards(request):
    if request.method == 'POST':
        card_id = request.POST.get('card_id')
        pagina_id = request.POST.get('pagina_id')
        pergunta_card = request.POST.get('pergunta_editada')
        resposta_card = request.POST.get('resposta_editada')

        # atualiza a pergunta e a resposta da carta no banco de dados
        Cards.objects.filter(id=card_id).update(
            perguntas=pergunta_card, respostas=resposta_card)
        # redireciona para a página das cartas dessa página
        return redirect('paginas', pagina_id=pagina_id)

# -------------------- fim area cards --------------------

# ------------ area professor x aluno -----------------


@login_required
def add_alunos(request):
    user_arroba_atual = request.user.username
    usuario_atual = Usuario.objects.get(arroba=user_arroba_atual)
    PG = usuario_atual.paginas.all()
    primeira_pagina = usuario_atual.paginas.all().first()

    if request.method == 'POST':
        nome_usuario_aluno = request.POST.get('arroba_aluno')
        paginas_ids = request.POST.getlist('paginas_compartilhadas')
        usuario_aluno = Usuario.objects.get(
            arroba=nome_usuario_aluno, tipo_user='aluno')
        try:
            usuario_aluno = Usuario.objects.get(
                arroba=nome_usuario_aluno, tipo_user='aluno')
            for pagina_id in paginas_ids:
                pagina = Pagina.objects.get(id=pagina_id)

                usuario_aluno.paginas_compartilhadas.add(pagina)
            messages.success(request, 'Páginas compartilhadas com sucesso.')
            return render(request, 'add_aluno.html', {'paginas': primeira_pagina, 'paginas_titulos': PG, 'tipo_user': usuario_atual.tipo_user, 'foto_perfil': usuario_atual.foto_perfil.url})
        except ObjectDoesNotExist:
            messages.error(request, 'O aluno especificado não existe.')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
    else:

        return render(request, 'add_aluno.html', {'paginas': primeira_pagina, 'paginas_titulos': PG, 'tipo_user': usuario_atual.tipo_user, 'foto_perfil': usuario_atual.foto_perfil.url})


@login_required
def paginas_compartilhadas(request, pagina_compartilhada_id):
    user_arroba_atual = request.user.username
    usuario_atual = Usuario.objects.get(arroba=user_arroba_atual)
    pagina_principal = usuario_atual.paginas.all().first()
    todas_paginas_usuario = usuario_atual.paginas.all()
    paginas_compartilhadas = usuario_atual.paginas_compartilhadas.all()
    cards_compartilhados = Cards.objects.filter(
        pagina_id=pagina_compartilhada_id)

    return render(request, 'paginas_compartilhadas.html', {'tipo_user': usuario_atual.tipo_user,
                                                           'pagina_principal': pagina_principal,
                                                           'paginas_compartilhadas': paginas_compartilhadas,
                                                           'cards': cards_compartilhados,
                                                           'pg': todas_paginas_usuario,
                                                           'foto_perfil': usuario_atual.foto_perfil.url})


# -------------------------- AREA DOS SIMULADOS --------------------------------
@login_required
def simulado(request, id_pagina):

    user_atual = request.user.username
    usuario_atual = Usuario.objects.get(arroba=user_atual)
    pagina_principal = usuario_atual.paginas.all().first()
    todas_paginas = usuario_atual.paginas.all().first()
    paginas_compartilhadas = usuario_atual.paginas_compartilhadas.all()
    paginas_cards2 = Pagina.objects.filter(
        cards__isnull=False, usuarios=usuario_atual).distinct()
    paginas_com_simulados = Pagina.objects.filter(
        simulado__isnull=False).distinct()

    contexto = {'tipo_user': usuario_atual.tipo_user,
                'pagina_princiapal': pagina_principal,
                'pg': paginas_cards2,
                'paginass': id_pagina,
                'paginas_simulados': paginas_com_simulados,
                'paginas_compartilhadas': paginas_compartilhadas,
                'foto_perfil': usuario_atual.foto_perfil.url}

    return render(request, 'simulado.html', contexto)


@login_required
@require_POST
def questao_simulado(request):
    if request.method == 'POST':

        pergunta_simulado = request.POST.get('pergunta_simulado')
        alternativa_a = request.POST.get('alternativa_a_simulado')
        alternativa_b = request.POST.get('alternativa_b_simulado')
        alternativa_c = request.POST.get('alternativa_c_simulado')
        alternativa_d = request.POST.get('alternativa_d_simulado')
        alternativa_correta = request.POST.get('alternativa_correta')
        id_pagina = request.POST.get('id_pagina')
        pagina = Pagina.objects.get(id=id_pagina)
        simulado = Simulados.objects.create(pergunta=pergunta_simulado, alternativa_a=alternativa_a,
                                            alternativa_b=alternativa_b, alternativa_c=alternativa_c,
                                            alternativa_d=alternativa_d, correta=alternativa_correta, pagina=pagina)

        simulado.save()
        return redirect('simulado', id_pagina)
    else:
        return redirect('simulado', id_pagina)


@login_required
@require_POST
def add_pagina_simulado(request):
    if request.method == 'POST':
        titulo = request.POST.get('titulo_pagina_simulado')
        nova_pagina = Pagina.objects.create(titulo=titulo)
        Simulados.objects.create(pergunta=titulo, alternativa_a=titulo,
                                 alternativa_b=titulo, alternativa_c=titulo,
                                 alternativa_d=titulo, correta=titulo, pagina=nova_pagina)
        usuario_atual = request.user.username
        usuario = Usuario.objects.get(arroba=usuario_atual)
        usuario.paginas.add(nova_pagina)
        id_pagina = nova_pagina.id
        return redirect('simulado', id_pagina)
    else:
        return redirect('simulado', id_pagina)


@login_required
def checa_resposta_simulado(request):
    if request.method == 'POST':
       pass

@require_POST
@login_required
def delete_simulado(request):
    if request.method == 'POST':
        id_questao = request.POST.get('id_questao')
        id_pagina = request.POST.get('id_pagina')
        simulado = get_object_or_404(Simulados, id=id_questao)
        simulado.delete()
        return redirect('simulado', id_pagina)


@login_required
@require_POST
def edit_simulado(request):
    if request.method == 'POST':
        pergunta_simulado = request.POST.get('pergunta_simulado')
        alternativa_a = request.POST.get('alternativa_a_simulado')
        alternativa_b = request.POST.get('alternativa_b_simulado')
        alternativa_c = request.POST.get('alternativa_c_simulado')
        alternativa_d = request.POST.get('alternativa_d_simulado')
        alternativa_correta = request.POST.get('alternativa_correta')
        id_pagina = request.POST.get('id_pagina')
        id_questao = request.POST.get('id_questao')

        Simulados.objects.filter(id=id_questao).update(pergunta=pergunta_simulado,
                                                       alternativa_a=alternativa_a,
                                                       alternativa_b=alternativa_b,
                                                       alternativa_c=alternativa_c,
                                                       alternativa_d=alternativa_d,
                                                       correta=alternativa_correta)

        return redirect('simulado', id_pagina)

# -------------------------- FIM AREA DOS SIMULADOS --------------------------------
