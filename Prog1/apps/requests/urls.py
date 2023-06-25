from django.urls import path
from apps.requests.views import getUsuarios

urlpatterns = [
    path('usuario/', getUsuarios, name="UserRequest"),
]