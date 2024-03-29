from django.db import models
from django.utils import timezone

# Create your models here.
class Pagina(models.Model):
    titulo = models.CharField(max_length=255)
    data_criacao = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.titulo
    

class Usuario(models.Model):
    TIPO_USUARIO_CHOICES = (
        ('professor', 'Professor'),
        ('aluno', 'Aluno'),
    )
    arroba = models.TextField(unique=True)
    paginas = models.ManyToManyField(Pagina, related_name='usuarios')
    tipo_user = models.CharField(max_length=10, choices=TIPO_USUARIO_CHOICES, default='aluno')
    paginas_compartilhadas = models.ManyToManyField(Pagina, related_name='paginas_compartilhadas', blank=True)  # Novo campo adicionado
    foto_perfil = models.ImageField(
        upload_to='perfil/', default='perfil/default.jpg')
    def __str__(self):
        return self.arroba


class Cards(models.Model):
    perguntas = models.TextField()
    respostas = models.TextField()
    pagina = models.ForeignKey(Pagina, related_name='cards', on_delete=models.CASCADE)

class Simulados(models.Model):
    pergunta = models.TextField()
    alternativa_a = models.TextField()
    alternativa_b = models.TextField()
    alternativa_c = models.TextField()
    alternativa_d = models.TextField()
    correta = models.TextField(default='a')
    pagina = models.ForeignKey(Pagina, related_name='simulado', on_delete=models.CASCADE)
