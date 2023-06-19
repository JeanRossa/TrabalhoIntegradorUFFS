from django.shortcuts import render, redirect
from apps.login.forms import LoginForms
from django.contrib import auth, messages
# Create your views here.

def logar (request):
    form = LoginForms()

    if request.method == 'POST':
        form = LoginForms(request.POST)
        if form.is_valid():
            nome  = form['nome_login'].value()
            senha = form['senha'].value()

        usuario = auth.authenticate(
            request,
            username = nome,
            password = senha,
        )

        if usuario is not None:
            auth.login(request, usuario)
            return redirect('DashBoardADM')
        else:
            messages.error(request, "Login ou senha incorretos!")
            return redirect('logar')


    return render(request, 'login.html', {"form": form})