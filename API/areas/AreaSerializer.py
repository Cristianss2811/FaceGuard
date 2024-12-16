from rest_framework import serializers
from areas.models import Area

class AreaListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Area
        fields = ['id', 'nombre', 'descripcion', 'activo']

class AreaCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Area
        fields = '__all__'

class AreaUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Area
        fields = ['nombre', 'descripcion', 'activo', 'zonas']