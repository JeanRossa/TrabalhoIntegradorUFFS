from django.shortcuts import render, redirect

# Create your views here.

def DashBoardADM(request):
    return render(request, 'DashBoardADM.html')
