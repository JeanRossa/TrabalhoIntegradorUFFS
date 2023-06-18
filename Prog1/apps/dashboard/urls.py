from django.urls import path
from apps.dashboard.views import DashBoardADM

urlpatterns = [
    path('', DashBoardADM)
]