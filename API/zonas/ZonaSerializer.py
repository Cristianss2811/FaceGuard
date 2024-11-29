from rest_framework import serializers
from areas.models import Zona

class ZonaListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Zona
        fields = ['id', 'nombre', 'descripcion']

class ZonaCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Zona
        fields = '__all__'

class ZonaUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Zona
        fields = ['nombre', 'descripcion', 'activo']