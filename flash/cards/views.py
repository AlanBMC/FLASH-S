from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth import login as login_django
from django.db import IntegrityError
from .models import Usuario, Pagina
from django.http import JsonResponse
from django.contrib import messages
from django.contrib.auth import logout
import json

# Create your views here.


def cadastro(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        arroba = request.POST.get('arroba')
        senha = request.POST.get('password')
        if User.objects.filter(username=username).exists():
            # Usar mensagens para enviar feedback ao usuário
            return render(request, 'registro.html', {'error_message': 'Nome de usuário já existe. Por favor, escolha outro nome.'})
        else:
            user = User.objects.create_user(
                username=username, email=arroba, password=senha)
            user.save()
            usuario = Usuario(arroba=username)
            usuario.save()
            pagina = Pagina.objects.create(
                titulo='Primeira pagina', pergunta='Perguntas', resposta='Respostas')
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
        pagina = get_object_or_404(Pagina, id=pagina_id)
        return render(request, 'pagina.html', {'paginas': pagina})
    else:
        pagina = usuario.paginas.all().first()
        messages.info(request, "Você tentou acessar uma página que não lhe pertence. Redirecionando para a sua primeira página.")

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


@login_required
def listar_paginas_usuario(request):
    user_arroba = request.user.username  # ajuste conforme sua lógica de autenticação
    try:
        usuario = Usuario.objects.get(arroba=user_arroba)
        paginas = usuario.paginas.all()  # Assumindo que 'paginas' é o nome do campo ManyToMany em Usuario para Pagina
        paginas_data = [{'titulo': pagina.titulo, 'id': pagina.id} for pagina in paginas]
        return JsonResponse({'paginas': paginas_data})
    except Usuario.DoesNotExist:
        return JsonResponse({'erro': 'Usuário não encontrado'}, status=404)
    

@require_POST
@login_required
def excluir_pagina(request, pagina_id):
    user_arroba = request.user.username
    usuario = get_object_or_404(Usuario, arroba=user_arroba)
    pagina = get_object_or_404(Pagina, id=pagina_id)
    pagina.delete()
    return JsonResponse({'mensagem': 'Pagina excluida com sucesso'})