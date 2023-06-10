from django.db import models

# Create your models here.
class pessoa(models.Model):
    cpf = models.CharField(max_length=14)
    nome = models.CharField(max_length=100)
    nome_social = models.CharField(max_length=100)
    altura = models.DecimalField(max_digits=2, decimal_places=2)
    massa = models.DecimalField(max_digits=2, decimal_places=2)
    genero = models.CharField(max_length=10)
    idade = models.IntegerField()
    email = models.CharField(max_length=100)
    telefone_celular = models.CharField(max_length=15)
    endereco = models.CharField(max_length=200)