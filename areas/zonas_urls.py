from django.urls import path
from .views import zonas_listar, zonas_crear, zonas_editar, zonas_eliminar

urlpatterns = [
    path('', zonas_listar, name='zonas_listar'),
    path('crear/', zonas_crear, name='zonas_crear'),
    path('editar/<int:id>/', zonas_editar, name='zonas_editar'),
    path('eliminar/<int:id>/', zonas_eliminar, name='zonas_eliminar'),


    
]
