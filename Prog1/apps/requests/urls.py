from django.urls import path
from apps.requests.views import getUsuarios, getLocalidades, getNivelFilial

urlpatterns = [
    path('usuario/', getUsuarios, name="UserRequest"),
    path('localidade/', getLocalidades, name="SiteRequest"),
    
    path('nivelfilial/', getNivelFilial, name='NivelFilialRequest'),
]
