from rest_framework import serializers
from areas.models import Puerta

class PuertaListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Puerta
        fields = ['id', 'nombre', 'descripcion']

class PuertaCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Puerta
        fields = '__all__'

class PuertaUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Puerta
        fields = ['nombre', 'descripcion', 'activo', 'areas']