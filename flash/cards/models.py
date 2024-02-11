from django.db import models

# Create your models here.
class Pagina(models.Model):
    titulo = models.CharField(max_length=255)
    pergunta = models.TextField()
    resposta = models.TextField()
    data_criacao = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.titulo
    

class Usuario(models.Model):
    email = models.EmailField(unique=True)
    paginas = models.ManyToManyField(Pagina, related_name='usuarios')
    def __str__(self):
        return self.username
