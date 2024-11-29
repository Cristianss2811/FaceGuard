from django.urls import path
from . import views 

urlpatterns = [
    path('notificaciones/', views.listar_notificaciones, name='listar_notificaciones'),
    path('leer/<int:notificacion_id>', views.leer_notificacion, name='leer_notificacion'),
    path('count/', views.contar_notificaciones, name='contar_notificaciones'), 
]