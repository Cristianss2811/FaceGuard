from django.urls import path
from .views import puertas_listar, puertas_crear, puertas_editar, puertas_eliminar, puertas_asignar_roles, \
    eliminar_roles_puertas

urlpatterns = [
    path('', puertas_listar, name='puertas_listar'),
    path('crear/', puertas_crear, name='puertas_crear'),
    path('editar/<int:id>/', puertas_editar, name='puertas_editar'),
    path('eliminar/<int:id>/', puertas_eliminar, name='puertas_eliminar'),
    path('puertas_asignar_roles/<int:id>/', puertas_asignar_roles, name='puertas_asignar_roles'),
    path('eliminar_roles_puertas/<int:id>/', eliminar_roles_puertas, name='eliminar_roles_puertas'),
]
