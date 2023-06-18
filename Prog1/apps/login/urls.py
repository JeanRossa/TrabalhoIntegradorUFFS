from django.urls import path
from apps.login.views import logar

urlpatterns = [
    path('', logar, name="logar")
]