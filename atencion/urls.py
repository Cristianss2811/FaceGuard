from django.urls import path
from .views import movimientos_listar

urlpatterns = [
    path('', movimientos_listar, name='movimientos_listar'),
]
