from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth import login as login_django
from django.db import IntegrityError

# Create your views here.



@login_required
def home(request):
    return render(request, 'principal.html')



def login(request):
    if  request.method=='POST':
        username = request.POST.get('username')
        senha = request.POST.get('password')
        user = authenticate(username=username, password=senha)
        if user:
            login_django(request, user)
            return render(request, 'principal.html')
        else:
            return render(request, 'registration/login.html')
    else:
        return render(request, 'registration/login.html')
    


def registro(request):
    if request.method == 'POST':
        nome = request.POST.get('username')
        arroba = request.POST.get('arroba')
        pas = request.POST.get('password')
        try:
            # Tenta criar o usuário
            user = User.objects.create_user(username=nome, email=arroba, password=pas)
            #criar uma classe ususario para guarda arroba tbm
            user.save()
            login_django(request, user)
            return redirect('home')
        except IntegrityError as e:
            if 'UNIQUE constraint failed: auth_user.username' in str(e):
                # Nome de usuário já existe
                return render(request, 'registration/login.html', {'error_message': 'Nome de usuário já existe. Por favor, escolha outro nome.'})

            else:
                # Outro erro de integridade
                return HttpResponse('Erro ao cadastrar usuário. Por favor, tente novamente mais tarde.')
    else:
        return render(request, 'registration/registro.html')


def configuracao(request):
    return render(request , 'conf.html')