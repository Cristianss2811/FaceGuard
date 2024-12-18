from rest_framework import serializers

from API.zonas.ZonaSerializer import ZonaListSerializer
from areas.models import Area
from areas.models import Zona


class AreaListSerializer(serializers.ModelSerializer):
    zonas = ZonaListSerializer(many=True, read_only=True)

    class Meta:
        model = Area
        fields = ['id', 'nombre', 'descripcion', 'activo', 'zonas']


class AreaCreateSerializer(serializers.ModelSerializer):
    zonas = serializers.PrimaryKeyRelatedField(queryset=Zona.objects.all(), many=True)

    class Meta:
        model = Area
        fields = ['id', 'nombre', 'descripcion', 'activo', 'zonas']