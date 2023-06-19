from django.urls import path
from apps.dashboard.views import DashBoardADM, crud_usuario

urlpatterns = [
    path('', DashBoardADM, name="DashBoardADM"),
    path('crud_usuario/', crud_usuario, name="crud_usuario")
]