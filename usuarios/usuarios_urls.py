from django.urls import path
from .views import profile_listar, profile_editar, profile_eliminar, profile_completar, \
    usuarios_asignar_roles, eliminar_roles_usuario, verificar_acceso, verificar_rostro_acceso  # , profile_crear

urlpatterns = [
    path('', profile_listar, name='usuarios_listar'),
    #path('crear/', profile_crear, name='usuarios_crear'),
    path('editar/<int:id>/', profile_editar, name='usuarios_editar'),
    path('eliminar/<int:id>/', profile_eliminar, name='usuarios_eliminar'),
    path('completar/<int:id>/', profile_completar, name='usuarios_completar'),
    path('usuarios_asignar_roles/<int:id>/', usuarios_asignar_roles, name='usuarios_asignar_roles'),#
    path('eliminar_roles_usuario/<int:usuario_id>/', eliminar_roles_usuario, name='eliminar_roles_usuario'),
    path('verificar_acceso/<int:puerta_id>/', verificar_acceso, name='verificar_acceso'),
    path('verificar_rostro_acceso/<int:puerta_id>/', verificar_rostro_acceso, name='verificar_rostro_acceso')
]