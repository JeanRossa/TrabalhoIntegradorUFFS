from django.urls import path
from dashboard.views import DashBoardADM

urlpatterns = [
    path('', DashBoardADM)
]