from django.shortcuts import render
from testeApp.models import pessoa

def index(request):
    for p in pessoa.objects.raw("SELECT 1 as ID,* FROM CLIENTES"):
        print (p.nome)
    return render(request, 'index.html')

# Create your views here.
