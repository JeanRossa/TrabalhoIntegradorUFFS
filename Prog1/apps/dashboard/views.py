from django.shortcuts import render, redirect
from apps.login.models import Usuario, Nivelvendedor, Filial
from apps.dashboard.forms import UsuarioForm
from django.contrib import messages
from django.contrib.auth.models import User

import bcrypt

# Create your views here.

def DashBoardADM(request):
    return render(request, 'DashBoardADM.html')

def crud_usuario(request):

    if request.method == 'POST':
        form = UsuarioForm(request.POST)
        if form.is_valid():
            nome   = form['nome'].value()
            cpf    = form['cpf'].value()
            login  = form['login'].value()
            senha  = form['senha'].value()
            tipo   = form['tipo'].value()
            codfil = form['filial'].value()
            nivel  = form['nivelvendedor'].value()

            senha  = bcrypt.hashpw(senha.encode('utf8'), bcrypt.gensalt(8))

            # Validando CPF
            if not cpf.isnumeric():
                messages.error(request, "o CPF inserido é inválido, por favor, tente novamente (informar CPF sem pontuação)")
                return redirect('crud_usuario')
            
            usuario = Usuario.objects.filter(cpf=cpf)
            if usuario:
                messages.error(request, "o CPF inserido já está cadastrado")
                return redirect('crud_usuario')
            
            # Validando se o Login é único
            usuario = Usuario.objects.filter(login=login)
            if usuario:
                messages.error(request, "o login inserido já está cadastrado, tente novamente")
                return redirect('crud_usuario')

            # Validando os campos opcionais
            if tipo == '1':
                # Administrador - Limpar campo filial e nivel
                codfil = ''
                nivel = ''
            if tipo == '2':
                # Gerente - Limpar campo nivel e verificar filial
                nivel = ''
                if not codfil:
                    messages.error(request, "Para cadastro de Gerentes é necessário informar o campo Filial")
                    return redirect('crud_usuario')
            if tipo == '3':
                # Vendedor - Verificar nivel e filial
                if not nivel:
                    messages.error(request, "Para cadastro de vendedores é necessário informar o campo Nivel")
                    return redirect('crud_usuario')
                if not codfil:
                    messages.error(request, "Para cadastro de Vendedores é necessário informar o campo Filial")
                    return redirect('crud_usuario')
                  
            # Validações realizadas, passar para o salvamento no banco de dados
            form.save()
            usuario = User.objects.create_user(
                username=login,
                password=form['senha'].value(),
            )
            usuario.save()

            messages.success(request, "Tudo certo")
            return redirect('crud_usuario')

        else:
            for field in form:
                if field.errors:
                    print("Field Error:", field.name,  field.errors)
                    messages.error(request, field.errors)
                    return redirect('crud_usuario')
            
        messages.success(request, "Tudo certo")
        return redirect('crud_usuario')
            
    else:
        usuario = Usuario.objects.all()
        form = UsuarioForm
        return render(request, 'crud_usuario.html', {"users":usuario, "form": form})