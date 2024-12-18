from rest_framework import serializers
from  atencion.models import Movimiento, MovimientoUsuario, MovimientoPuerta

class MovimientoUsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = MovimientoUsuario
        fields = ['usuario']

class MovimientoPuertaSerializer(serializers.ModelSerializer):
    class Meta:
        model = MovimientoPuerta
        fields = ['puerta']

class MovimientoSerializer(serializers.ModelSerializer):
    usuario = serializers.SerializerMethodField()
    puerta = serializers.SerializerMethodField()

    class Meta:
        model = Movimiento
        fields = ['tipo', 'hora', 'fecha', 'usuario', 'puerta']

    def get_usuario(self, obj):
        usuario = MovimientoUsuario.objects.filter(movimiento=obj).first()
        return {
            "id": usuario.usuario.id,
            "nombre": usuario.usuario.first_name
        } if usuario else None

    def get_puerta(self, obj):
        puerta = MovimientoPuerta.objects.filter(movimiento=obj).first()
        return {
            "id": puerta.puerta.id,
            "nombre": puerta.puerta.nombre
        } if puerta else None
