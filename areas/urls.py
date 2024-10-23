from django.urls import path
from .views import areas_listar, areas_crear, areas_editar, areas_eliminar

urlpatterns = [
    path('', areas_listar, name='areas_listar'),
    path('crear/', areas_crear, name='areas_crear'),
    path('editar/<int:id>/', areas_editar, name='areas_editar'),
    path('eliminar/<int:id>/', areas_eliminar, name='areas_eliminar'),


    
]
