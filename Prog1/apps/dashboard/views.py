from django.shortcuts import render, redirect
from apps.login.models import Usuario, Nivelvendedor, Filial
from apps.dashboard.forms import UsuarioForm
from django.contrib import messages
from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import login_required
from datetime import datetime
import bcrypt

# Create your views here.

def DashBoardADM(request):
    return render(request, 'DashBoardADM.html')

@login_required # Redireciona paga a pagina de login caso o usuário não esteja autenticado
def crud_usuario(request):
    # Verifica se o usuário logado tem permissão (está no grupo de administrador) para acessar a pagina
    if not request.user.groups.filter(name='Administrador').exists() and request.user.is_superuser == False:
        messages.error(request, "Você não tem permissão para acessar esta página")
        return redirect('DashBoardADM')
    # Verificar se a função está sendo chamada por um método POST (Ou seja: se está sendo feito um submit de formulário do front-end para o back-end)
    if request.method == 'POST':
        # Le o cookie "Operation" que informa qual tipo de operação o usuário esta fazendo
        operation = request.COOKIES.get('operation') # 1 = Incluir, # 2 = Visualizar, # 3 = Editar, # 4 = Deletar
        # Recupera o formulário enviado e salva na variavel FORM
        form = UsuarioForm(request.POST)
        # Operações para incluir o usuário
        if operation == '1':
            if form.is_valid(): # Realiza as validações configuradaos no forms.py e models.py
                # Le as informações do formulário
                cpf    = form['cpf'].value()
                login  = form['login'].value()
                senha  = form['senha'].value()
                tipo   = form['tipo'].value()
                codfil = form['filial'].value()
                nivel  = form['nivelvendedor'].value()

                senha  = bcrypt.hashpw(senha.encode('utf8'), bcrypt.gensalt(8)) # Criptografar a senha

                # Validando CPF
                if not cpf.isnumeric():
                    messages.error(request, "o CPF inserido é inválido, por favor, tente novamente (informar CPF sem pontuação)") # Retorna uma mensagem para o front-end
                    return redirect('crud_usuario') # Redireciona/atualiza a pagina

                usuario = Usuario.objects.filter(cpf=cpf, dtencerramento=None) # Realiza a busca de um usuário com os filtros passados
                if usuario: # Se encontrou
                    messages.error(request, "o CPF inserido já está cadastrado")
                    return redirect('crud_usuario')

                # Validando se o Login é único
                usuario = Usuario.objects.filter(login=login) # Realiza a busca de um usuário com os filtros passados
                if usuario: # Se encontrou
                    messages.error(request, "o login inserido já está cadastrado, tente novamente")
                    return redirect('crud_usuario')

                newUsuario = form.save(commit=False)    # Salva o formulário em um novo objeto de usuário, é feito isso para podermos editar as informações que o usuário colocou
                newUsuario.dtinclusao = datetime.now()  # Preenchendo data de inclusão

                # Realizando tratativas para os tipos de usuário, salvar um campo como "None" significa Nulo
                if tipo == '1':
                    newUsuario.filial = None
                    newUsuario.nivelvendedor = None

                if tipo == '2':
                    newUsuario.nivelvendedor = None
                    if not codfil:
                        messages.error(request, "Para cadastro de Gerentes é necessário informar o campo Filial")
                        return redirect('crud_usuario')

                if tipo == '3':
                    if not nivel:
                        messages.error(request, "Para cadastro de vendedores é necessário informar o campo Nivel")
                        return redirect('crud_usuario')
                    if not codfil:
                        messages.error(request, "Para cadastro de Vendedores é necessário informar o campo Filial")
                        return redirect('crud_usuario')

                newUsuario.save()   # Salvar instancia temporária, isso vai atualizar o objeto forms com os dados do newUsuario
                form.save_m2m()     # Salva o formulário no banco de dados, nesse momento é feito um novo registro na tabela

                # Criar um usuário no sistema de login do Django
                usuario = User.objects.create_user(
                    username=login,
                    password=form['senha'].value(),
                )
                # Setando o grupo de permissões com base no tipo preenchido
                group = Group.objects.get(name=Usuario.OPC_TIPO[int(tipo)-1][1])
                usuario.groups.add(group)
                usuario.save()
                # Redireciona para a tela com mensagem de sucesso
                messages.success(request, "Usuário Incluido")
                return redirect('crud_usuario')

            else:
                # Ocorreram erros nas validações de campo, retornar para o front-end os erros
                for field in form:
                    if field.errors:
                        print("Field Error:", field.name,  field.errors)
                        messages.error(request, field.errors)
                        return redirect('crud_usuario')

        # Operações para editar o usuário
        if operation == '3':
            cpf    = form['cpf'].value()
            nome   = form['nome'].value()
            tipo   = form['tipo'].value()
            status = form['status'].value()
            codfil = form['filial'].value()
            nivel  = form['nivelvendedor'].value()

            usuario = Usuario.objects.get(cpf=cpf, dtencerramento=None)
            usuario.nome = nome # Atualizar nome

            if usuario.status == 2: # Não deixa editar registros já inativos
                messages.error(request, "Não é permitida a edição de registros inativos")
                return redirect('crud_usuario')

            # Expressões regulares, Variavel = ValorSeVerdadeiro if Condição else ValorSeFalso ----- Exemplo abaixo
            # maiorDeIdade = True if idade >= 18 else False
            codfil = int(codfil) if codfil != '' else ''
            codfil_atual = usuario.filial.codfilial if (not usuario.filial == None) else ''
            nivel_atual = usuario.nivelvendedor.nivelvendedor if (not usuario.nivelvendedor == None) else ''

            # Mudanças que serão necessárias um novo registro para não perder os dados antigos
            if (codfil != codfil_atual and int(tipo) != 1) or (nivel != nivel_atual and int(tipo) == 3) or (int(tipo) != usuario.tipo):
                # Validar ajustes
                if tipo == '1':
                    codfil = None
                    nivel = None

                if tipo == '2':
                    nivel = None
                    if not codfil:
                        messages.error(request, "Para cadastro de Gerentes é necessário informar o campo Filial")
                        return redirect('crud_usuario')
                    else:
                        codfil = Filial.objects.get(codfilial=codfil) # Para salvar no banco um dado de uma FK, é necessário salvar a instancia e não a PK

                if tipo == '3':
                    if not nivel:
                        messages.error(request, "Para cadastro de vendedores é necessário informar o campo Nivel")
                        return redirect('crud_usuario')
                    else:
                        nivel = Nivelvendedor.objects.get(nivelvendedor=nivel)
                    if not codfil:
                        messages.error(request, "Para cadastro de Vendedores é necessário informar o campo Filial")
                        return redirect('crud_usuario')
                    else:
                        codfil = Filial.objects.get(codfilial=codfil)

                # Encerrar o registro atual
                usuario.status = 2
                usuario.dtencerramento = datetime.now()

                try:
                    usuario.save()
                except:
                    messages.error(request, "Ocorreu um erro ao editar o usuário, não é possível editar o mesmo CPF duas vezes ao dia")
                    return redirect('crud_usuario')

                # Criar novo registro com os dados novos
                usuario.codusuario      = None
                usuario.status          = 1
                usuario.dtinclusao      = datetime.now()
                usuario.dtencerramento  = None
                usuario.tipo            = tipo
                usuario.filial          = codfil
                usuario.nivelvendedor   = nivel
                # Salvando na base de dados
                usuario.save()

                # Atualizando grupo do usuário
                group = Group.objects.get(name=usuario.OPC_TIPO[int(tipo)-1][1])
                SysUser = User.objects.get(username=usuario.login.strip())
                SysUser.groups.clear()
                SysUser.groups.add(group)
                SysUser.save()

            # Alterando Status do usuário
            elif int(status) != usuario.status:
                SysUser = User.objects.get(username=usuario.login.strip())
                SysUser.is_active = False
                SysUser.save()
                usuario.status = int(status)
                usuario.save()
            else:
                usuario.save()

            messages.success(request, "Edição Concluída")
            return redirect('crud_usuario')

        # Operações para excluir o usuário
        if operation == '4':
            cpf    = form['cpf'].value()

            usuario = Usuario.objects.get(cpf=cpf, dtencerramento=None)
            usuario.dtencerramento = datetime.now()
            usuario.status = 2

            try:
                usuario.save()
            except:
                messages.error(request, "Ocorreu um erro ao editar o usuário, não é possível editar o mesmo CPF duas vezes ao dia")
                return redirect('crud_usuario')

            SysUser = User.objects.get(username=usuario.login.strip())
            SysUser.is_active = False
            SysUser.save()

            messages.success(request, "Exclusão Concluída")
            return redirect('crud_usuario')

    else:
        usuario = Usuario.objects.all().order_by('cpf')                                     # Busca dos dados que irão ser listados na tela
        form = UsuarioForm                                                                  # Instancia o formulário criado no forms.py
        return render(request, 'crud_usuario.html', {"users":usuario, "form": form})        # Passa para o front-end a pagina crud_usuario.html com os dados de usuário e o formulário