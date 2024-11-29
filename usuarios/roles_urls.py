from django.urls import path
from .views import roles_listar, roles_crear, roles_editar,roles_eliminar

urlpatterns = [
    path('', roles_listar, name='roles_listar'),
    path('crear/', roles_crear, name='roles_crear'),
    path('editar/<int:id>/', roles_editar, name='roles_editar'),
    path('eliminar/<int:id>/', roles_eliminar, name='roles_eliminar'),
]