from django.urls import path
from apps.dashboard.views import DashBoardADM, crud_usuario, crud_localidade, crud_filial, crud_nivelfilial

urlpatterns = [
    path('', DashBoardADM, name="DashBoardADM"),
    path('crud_usuario/', crud_usuario, name="crud_usuario"),
    path('crud_localidade/', crud_localidade, name="crud_localidade"),
    path('crud_filial/', crud_filial, name="crud_filial"),
    path('crud_nivelfilial/', crud_nivelfilial, name="crud_nivelfilial")
]
