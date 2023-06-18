from django.urls import path
from login.views import logar

urlpatterns = [
    path('', logar, name="logar")
]