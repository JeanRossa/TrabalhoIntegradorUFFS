from django.http import JsonResponse
from apps.login.models import Usuario, Localidade, Nivelfilial
# Create your views here.


def getUsuarios(request):
    # Recupear código passado para o back-end
    coduser = request.GET.get('cod')
    # Procurar usuário com o código
    user = Usuario.objects.get(codusuario=coduser)
    filial = ''
    nv = ''
    # Tratando o retorno para os 3 casos onde filial e nivel podem não estar preenchidos
    if user.tipo == 1:  # ADM
        filial = ''
        nv = ''
    if user.tipo == 2:  # Gerente
        filial = user.filial.codfilial
        nv = ''
    if user.tipo == 3:  # Vendedor
        filial = user.filial.codfilial
        nv = user.nivelvendedor.nivelvendedor

    return JsonResponse({"nome": user.nome, "cpf": user.cpf, "login": user.login, "senha": "*********", "status": user.status, "dtInclusao": user.dtinclusao, "dtencerramento": user.dtencerramento, "tipo": user.tipo, "filial": filial, "nivelvendedor": nv})


def getLocalidades(request):
    codlocal = request.GET.get('cod')
    site = Localidade.objects.get(codlocal=codlocal)
    return JsonResponse({"cidade": site.cidade, 'estado': site.estado})


def getNivelFilial(request):
    nivelfilial = request.GET.get('cod')
    branchLevel = Nivelfilial.objects.get(nivelfilial=nivelfilial)
    return JsonResponse({"nivelfilial": branchLevel.nivelfilial, 'descricao': branchLevel.descricao})
