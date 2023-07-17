from django.shortcuts import render, redirect
from apps.login.models import Usuario, Nivelvendedor, Filial, Localidade, Filial, Nivelfilial
from apps.dashboard.forms import UsuarioForm, LocalidadeForm, FilialForm, NivelFilialForm
from django.contrib import messages
from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import login_required
from datetime import datetime
import bcrypt

# Create your views here.


def DashBoardADM(request):
    return render(request, 'DashBoardADM.html')


@login_required  # Redireciona paga a pagina de login caso o usuário não esteja autenticado
def crud_usuario(request):
    # Verifica se o usuário logado tem permissão (está no grupo de administrador) para acessar a pagina
    if not request.user.groups.filter(name='Administrador').exists() and request.user.is_superuser == False:
        messages.error(
            request, "Você não tem permissão para acessar esta página")
        return redirect('DashBoardADM')
    # Verificar se a função está sendo chamada por um método POST (Ou seja: se está sendo feito um submit de formulário do front-end para o back-end)
    if request.method == 'POST':
        # Le o cookie "Operation" que informa qual tipo de operação o usuário esta fazendo
        # 1 = Incluir, # 2 = Visualizar, # 3 = Editar, # 4 = Deletar
        operation = request.COOKIES.get('operation')
        # Recupera o formulário enviado e salva na variavel FORM
        form = UsuarioForm(request.POST)
        # Operações para incluir o usuário
        if operation == '1':
            if form.is_valid():  # Realiza as validações configuradaos no forms.py e models.py
                # Le as informações do formulário
                cpf = form['cpf'].value()
                login = form['login'].value()
                senha = form['senha'].value()
                tipo = form['tipo'].value()
                codfil = form['filial'].value()
                nivel = form['nivelvendedor'].value()

                # Criptografar a senha
                senha = bcrypt.hashpw(senha.encode('utf8'), bcrypt.gensalt(8))

                # Validando CPF
                if not cpf.isnumeric():
                    # Retorna uma mensagem para o front-end
                    messages.error(
                        request, "o CPF inserido é inválido, por favor, tente novamente (informar CPF sem pontuação)")
                    # Redireciona/atualiza a pagina
                    return redirect('crud_usuario')

                # Realiza a busca de um usuário com os filtros passados
                usuario = Usuario.objects.filter(cpf=cpf, dtencerramento=None)
                if usuario:  # Se encontrou
                    messages.error(
                        request, "o CPF inserido já está cadastrado")
                    return redirect('crud_usuario')

                # Validando se o Login é único
                # Realiza a busca de um usuário com os filtros passados
                usuario = Usuario.objects.filter(login=login)
                if usuario:  # Se encontrou
                    messages.error(
                        request, "o login inserido já está cadastrado, tente novamente")
                    return redirect('crud_usuario')

                # Salva o formulário em um novo objeto de usuário, é feito isso para podermos editar as informações que o usuário colocou
                newUsuario = form.save(commit=False)
                newUsuario.dtinclusao = datetime.now()  # Preenchendo data de inclusão

                # Realizando tratativas para os tipos de usuário, salvar um campo como "None" significa Nulo
                if tipo == '1':
                    newUsuario.filial = None
                    newUsuario.nivelvendedor = None

                if tipo == '2':
                    newUsuario.nivelvendedor = None
                    if not codfil:
                        messages.error(
                            request, "Para cadastro de Gerentes é necessário informar o campo Filial")
                        return redirect('crud_usuario')

                if tipo == '3':
                    if not nivel:
                        messages.error(
                            request, "Para cadastro de vendedores é necessário informar o campo Nivel")
                        return redirect('crud_usuario')
                    if not codfil:
                        messages.error(
                            request, "Para cadastro de Vendedores é necessário informar o campo Filial")
                        return redirect('crud_usuario')

                # Salvar instancia temporária, isso vai atualizar o objeto forms com os dados do newUsuario
                newUsuario.save()
                # Salva o formulário no banco de dados, nesse momento é feito um novo registro na tabela
                form.save_m2m()

                # Criar um usuário no sistema de login do Django
                usuario = User.objects.create_user(
                    username=login,
                    password=form['senha'].value(),
                )
                # Setando o grupo de permissões com base no tipo preenchido
                group = Group.objects.get(
                    name=Usuario.OPC_TIPO[int(tipo)-1][1])
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
            cpf = form['cpf'].value()
            nome = form['nome'].value()
            tipo = form['tipo'].value()
            status = form['status'].value()
            codfil = form['filial'].value()
            nivel = form['nivelvendedor'].value()

            usuario = Usuario.objects.get(cpf=cpf, dtencerramento=None)
            usuario.nome = nome  # Atualizar nome

            if usuario.status == 2:  # Não deixa editar registros já inativos
                messages.error(
                    request, "Não é permitida a edição de registros inativos")
                return redirect('crud_usuario')

            # Expressões regulares, Variavel = ValorSeVerdadeiro if Condição else ValorSeFalso ----- Exemplo abaixo
            # maiorDeIdade = True if idade >= 18 else False
            codfil = int(codfil) if codfil != '' else ''
            codfil_atual = usuario.filial.codfilial if (
                not usuario.filial == None) else ''
            nivel_atual = usuario.nivelvendedor.nivelvendedor if (
                not usuario.nivelvendedor == None) else ''

            # Mudanças que serão necessárias um novo registro para não perder os dados antigos
            if (codfil != codfil_atual and int(tipo) != 1) or (nivel != nivel_atual and int(tipo) == 3) or (int(tipo) != usuario.tipo):
                # Validar ajustes
                if tipo == '1':
                    codfil = None
                    nivel = None

                if tipo == '2':
                    nivel = None
                    if not codfil:
                        messages.error(
                            request, "Para cadastro de Gerentes é necessário informar o campo Filial")
                        return redirect('crud_usuario')
                    else:
                        # Para salvar no banco um dado de uma FK, é necessário salvar a instancia e não a PK
                        codfil = Filial.objects.get(codfilial=codfil)

                if tipo == '3':
                    if not nivel:
                        messages.error(
                            request, "Para cadastro de vendedores é necessário informar o campo Nivel")
                        return redirect('crud_usuario')
                    else:
                        nivel = Nivelvendedor.objects.get(nivelvendedor=nivel)
                    if not codfil:
                        messages.error(
                            request, "Para cadastro de Vendedores é necessário informar o campo Filial")
                        return redirect('crud_usuario')
                    else:
                        codfil = Filial.objects.get(codfilial=codfil)

                # Encerrar o registro atual
                usuario.status = 2
                usuario.dtencerramento = datetime.now()

                try:
                    usuario.save()
                except:
                    messages.error(
                        request, "Ocorreu um erro ao editar o usuário, não é possível editar o mesmo CPF duas vezes ao dia")
                    return redirect('crud_usuario')

                # Criar novo registro com os dados novos
                usuario.codusuario = None
                usuario.status = 1
                usuario.dtinclusao = datetime.now()
                usuario.dtencerramento = None
                usuario.tipo = tipo
                usuario.filial = codfil
                usuario.nivelvendedor = nivel
                # Salvando na base de dados
                usuario.save()

                # Atualizando grupo do usuário
                group = Group.objects.get(
                    name=usuario.OPC_TIPO[int(tipo)-1][1])
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
            cpf = form['cpf'].value()

            usuario = Usuario.objects.get(cpf=cpf, dtencerramento=None)
            usuario.dtencerramento = datetime.now()
            usuario.status = 2

            try:
                usuario.save()
            except:
                messages.error(
                    request, "Ocorreu um erro ao editar o usuário, não é possível editar o mesmo CPF duas vezes ao dia")
                return redirect('crud_usuario')

            SysUser = User.objects.get(username=usuario.login.strip())
            SysUser.is_active = False
            SysUser.save()

            messages.success(request, "Exclusão Concluída")
            return redirect('crud_usuario')

    else:
        # Busca dos dados que irão ser listados na tela
        usuario = Usuario.objects.all().order_by('cpf')
        # Instancia o formulário criado no forms.py
        form = UsuarioForm
        # Passa para o front-end a pagina crud_usuario.html com os dados de usuário e o formulário
        return render(request, 'crud_usuario.html', {"users": usuario, "form": form})


@login_required
def crud_localidade(request):

    if not request.user.groups.filter(name='Administrador').exists() and request.user.is_superuser == False:
        messages.error(
            request, "Você não tem permissão para acessar esta página")
        return redirect('DashBoardADM')

    if request.method == 'POST':
        operation = request.COOKIES.get('operation')
        form = LocalidadeForm(request.POST)

        if operation == '4':
            cidade = form['cidade'].value()
            estado = form['estado'].value()

            localidade = Localidade.objects.get(
                cidade=cidade, estado=estado)
            try:
                filial = Filial.objects.get(codlocal=localidade.codlocal)
            except:
                filial = None

            if filial:
                messages.error(
                    request, "Exclusão não realizada a localidade está sendo usada pela filial " + str(filial.codfilial))
                return redirect('crud_localidade')
            try:
                localidade.delete()
            except:
                messages.error(request, "Ocorreu um erro")
                return redirect('crud_localidade')
            messages.success(request, "Exclusão realizada com sucesso.")
            return redirect('crud_localidade')

        if form.is_valid():
            if operation == '1':
                try:
                    form.save()
                except:
                    messages.error(
                        request, "Ocorreu um erro ao criar a localidade, não é possível incluir a mesma cidade e estado duas vezes")
                    return redirect('crud_localidade')
                messages.success(request, "Localidade incluida com sucesso")
                return redirect('crud_localidade')

            if operation == '3':
                codlocal = request.COOKIES.get('codlocal')
                cidade2 = form['cidade'].value()
                estado2 = form['estado'].value()

                localidade = Localidade.objects.get(codlocal=codlocal)

                localidade.cidade = cidade2
                localidade.estado = estado2

                try:
                    localidade.save()
                except:
                    messages.error(
                        request, "Ocorreu um erro ao editar a localidade")
                    return redirect('crud_localidade')
                messages.success(request, "Localidade editada com sucesso")
                return redirect('crud_localidade')
        else:
            # Ocorreram erros nas validações de campo, retornar para o front-end os erros
            for field in form:
                if field.errors:
                    print("Field Error:", field.name,  field.errors)
                    messages.error(request, field.errors)
                    return redirect('crud_localidade')

    else:
        localidade = Localidade.objects.all()
        form = LocalidadeForm
        return render(request, 'crud_localidade.html', {"sites": localidade, "form": form})


@login_required
def crud_filial(request):
    if not request.user.groups.filter(name='Administrador').exists() and request.user.is_superuser == False:
        messages.error(
            request, "Você não tem permissão para acessar esta página")
        return redirect('DashBoardADM')

    if request.method == 'POST':
        # Le o cookie "Operation" que informa qual tipo de operação o usuário esta fazendo
        # 1 = Incluir, # 2 = Visualizar, # 3 = Editar, # 4 = Deletar
        operation = request.COOKIES.get('operation')
        form = FilialForm(request.POST)
        if operation == '1':
            if form.is_valid():
                # Le as informações do formulário
                cnpj = form['cnpj'].value()

                if not cnpj.isnumeric():
                    # Retorna uma mensagem para o front-end
                    messages.error(
                        request, "o CNPJ inserido é inválido, por favor, tente novamente (informar CNPJ sem pontuação)")
                    # Redireciona/atualiza a pagina
                    return redirect('crud_filial')
                    # Realiza a busca de um CNPJ com os filtros passados
                filial = Filial.objects.filter(cnpj=cnpj, dtencerramento=None)
                if filial:  # Se encontrou
                    messages.error(
                        request, "O CNPJ inserido já está cadastrado")
                    return redirect('crud_filial')

                newFilial = form.save(commit=False)
                newFilial.dtinclusao = datetime.now()  # Preenchendo data de inclusão
                newFilial.save()
                form.save()

                messages.success(request, "Filial incluida com sucesso")
                return redirect('crud_filial')

            # Ocorreram erros nas validações de campo, retornar para o front-end os erros
            else:
                for field in form:
                    if field.errors:
                        print("Field Error:", field.name,  field.errors)
                        messages.error(request, field.errors)
                        return redirect('crud_filial')

        if operation == '3':
            codfilial = request.COOKIES.get('codfilial')
            cnpj = form['cnpj'].value()
            status = form['status'].value()
            nivelfilial = form['nivelfilial'].value()
            codlocal = form['codlocal'].value()

            print(codfilial, cnpj, status, nivelfilial, codlocal)

            filial = Filial.objects.get(
                codfilial=codfilial, dtencerramento=None)
            filial.cnpj = cnpj

            if filial.status == 2:
                messages.error(
                    request, "Não é permitida a edição de registros inativos")
                return redirect('crud_filial')

            filial.status = status
            filial.nivelfilial = Nivelfilial.objects.get(
                nivelfilial=nivelfilial)
            filial.codlocal = Localidade.objects.get(codlocal=codlocal)

            try:
                filial.save()
            except:
                messages.error(request, "Ocorreu um erro ao editar a filial")
                return redirect('crud_filial')
            messages.success(request, "Filial editada com sucesso")
            return redirect('crud_filial')

        if operation == '4':
            codfilial = request.COOKIES.get('codfilial')

            filial = Filial.objects.get(codfilial=codfilial)

            try:
                usuario = Usuario.objects.get(filial=filial.codfilial)
            except:
                usuario = None

            if usuario:
                messages.error(
                    request, "Exclusão não realizada a filial está sendo usada pelo usuário " + str(usuario.nome))
                return redirect('crud_filial')
            try:
                filial.delete()
            except:
                messages.error(request, "Ocorreu um erro")
                return redirect('crud_filial')
            messages.success(request, "Exclusão realizada com sucesso.")

    else:
        filial = Filial.objects.all().order_by('cnpj')
        form = FilialForm
        # else:
        return render(request, 'crud_filial.html', {"branches": filial, "form": form})


@login_required
def crud_filial(request):
    if not request.user.groups.filter(name='Administrador').exists() and request.user.is_superuser == False:
        messages.error(
            request, "Você não tem permissão para acessar esta página")
        return redirect('DashBoardADM')

    if request.method == 'POST':
        # Le o cookie "Operation" que informa qual tipo de operação o usuário esta fazendo
        # 1 = Incluir, # 2 = Visualizar, # 3 = Editar, # 4 = Deletar
        operation = request.COOKIES.get('operation')
        form = FilialForm(request.POST)
        if operation == '1':
            if form.is_valid():
                # Le as informações do formulário
                cnpj = form['cnpj'].value()

                if not cnpj.isnumeric():
                    # Retorna uma mensagem para o front-end
                    messages.error(
                        request, "o CNPJ inserido é inválido, por favor, tente novamente (informar CNPJ sem pontuação)")
                    # Redireciona/atualiza a pagina
                    return redirect('crud_filial')
                    # Realiza a busca de um CNPJ com os filtros passados
                filial = Filial.objects.filter(cnpj=cnpj, dtencerramento=None)
                if filial:  # Se encontrou
                    messages.error(
                        request, "O CNPJ inserido já está cadastrado")
                    return redirect('crud_filial')

                newFilial = form.save(commit=False)
                newFilial.dtinclusao = datetime.now()  # Preenchendo data de inclusão
                newFilial.save()
                form.save()

                messages.success(request, "Filial incluida com sucesso")
                return redirect('crud_filial')

            # Ocorreram erros nas validações de campo, retornar para o front-end os erros
            else:
                for field in form:
                    if field.errors:
                        print("Field Error:", field.name,  field.errors)
                        messages.error(request, field.errors)
                        return redirect('crud_filial')

        if operation == '3':
            codfilial = request.COOKIES.get('codfilial')
            cnpj = form['cnpj'].value()
            status = form['status'].value()
            nivelfilial = form['nivelfilial'].value()
            codlocal = form['codlocal'].value()

            print(codfilial, cnpj, status, nivelfilial, codlocal)

            filial = Filial.objects.get(
                codfilial=codfilial, dtencerramento=None)
            filial.cnpj = cnpj

            if filial.status == 2:
                messages.error(
                    request, "Não é permitida a edição de registros inativos")
                return redirect('crud_filial')

            filial.status = status
            filial.nivelfilial = Nivelfilial.objects.get(
                nivelfilial=nivelfilial)
            filial.codlocal = Localidade.objects.get(codlocal=codlocal)

            try:
                filial.save()
            except:
                messages.error(request, "Ocorreu um erro ao editar a filial")
                return redirect('crud_filial')
            messages.success(request, "Filial editada com sucesso")
            return redirect('crud_filial')

        if operation == '4':
            codfilial = request.COOKIES.get('codfilial')

            filial = Filial.objects.get(codfilial=codfilial)

            try:
                usuario = Usuario.objects.get(filial=filial.codfilial)
            except:
                usuario = None

            if usuario:
                messages.error(
                    request, "Exclusão não realizada a filial está sendo usada pelo usuário " + str(usuario.nome))
                return redirect('crud_filial')
            try:
                filial.delete()
            except:
                messages.error(request, "Ocorreu um erro")
                return redirect('crud_filial')
            messages.success(request, "Exclusão realizada com sucesso.")

    else:
        filial = Filial.objects.all().order_by('cnpj')
        form = FilialForm
        # else:
        return render(request, 'crud_filial.html', {"branches": filial, "form": form})


def crud_nivelfilial(request):

    if not request.user.groups.filter(name='Administrador').exists() and request.user.is_superuser == False:
        messages.error(
            request, "Você não tem permissão para acessar esta página")
        return redirect('DashBoardADM')

    if request.method == 'POST':
        operation = request.COOKIES.get('operation')
        form = NivelFilialForm(request.POST)

        if form.is_valid():
            if operation == '1':

                nv = form['nivelfilial'].value()

                nivelfilial = Nivelfilial.objects.filter(nivelfilial=nv)

                if nivelfilial:
                    messages.error(request, "O nível de filial já existe")
                    return redirect('crud_nivelfilial')
                newNivelFilial = form.save(commit=False)
                newNivelFilial.save()
                form.save()

                messages.success(
                    request, "Nível de filial incluido com sucesso")
                return redirect('crud_nivelfilial')

    else:

        nivelFilial = Nivelfilial.objects.all()
        form = NivelFilialForm
        return render(request, 'crud_nivelfilial.html', {"branchLevels": nivelFilial, "form": form})
