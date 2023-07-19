from django.http import JsonResponse
from apps.login.models import Usuario, Localidade, Filial, Nivelfilial
# Create your views here.


def getUsuarios(request):
    coduser = request.GET.get('cod')                    # Recupear código passado para o back-end
    user = Usuario.objects.get(codusuario=coduser)      # Procurar usuário com o código
    filial = ''
    nv = ''
    # Tratando o retorno para os 3 casos onde filial e nivel podem não estar preenchidos
    if user.tipo == 1: # ADM
        filial = ''
        nv = ''
    if user.tipo == 2: # Gerente
        filial = user.filial.codfilial
        nv = ''
    if user.tipo == 3: # Vendedor
        filial = user.filial.codfilial
        nv = user.nivelvendedor.nivelvendedor

    return JsonResponse({"nome": user.nome, "cpf": user.cpf, "login": user.login, "senha": "*********", "status": user.status, "dtInclusao": user.dtinclusao, "dtencerramento": user.dtencerramento, "tipo": user.tipo, "filial": filial, "nivelvendedor": nv})


def getLocalidades(request):
    codlocal = request.GET.get('cod')
    site = Localidade.objects.get(codlocal=codlocal)
    return JsonResponse({"cidade": site.cidade, 'estado': site.estado})


def getFiliais(request):
    codfilial = request.GET.get('cod')
    branch = Filial.objects.get(codfilial=codfilial)

    return JsonResponse({"cnpj": branch.cnpj, "dtinclusao": branch.dtinclusao, "dtencerramento": branch.dtencerramento, "status": branch.status, "nivelfilial": branch.nivelfilial.nivelfilial, "codlocal": branch.codlocal.codlocal})


def getNivelFilial(request):
    nivelfilial = request.GET.get('cod')
    branchLevel = Nivelfilial.objects.get(nivelfilial=nivelfilial)
    return JsonResponse({"nivelfilial": branchLevel.nivelfilial, 'descricao': branchLevel.descricao})
