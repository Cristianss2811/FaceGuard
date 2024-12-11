from rest_framework import serializers
from notificaciones.models import Notificacion

class NotificacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notificacion
        fields = ['id', 'usuario', 'mensaje', 'leida', 'fecha_creacion']
        read_only_fields = ['id', 'usuario', 'fecha_creacion']