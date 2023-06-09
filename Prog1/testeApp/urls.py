from django.urls import path
from testeApp.views import index

urlpatterns = [
    path('', index)
]