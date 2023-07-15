from django.urls import path
from apps.requests.views import getUsuarios, getLocalidades

urlpatterns = [
    path('usuario/', getUsuarios, name="UserRequest"),
    path('localidade/', getLocalidades, name="SiteRequest")
]
