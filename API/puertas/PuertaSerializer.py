from rest_framework import serializers

from API.areas.AreaSerializer import AreaListSerializer
from areas.models import Puerta, Area


class PuertaListSerializer(serializers.ModelSerializer):
    areas = AreaListSerializer(many=True, read_only=True)  # Aquí, AreaListSerializer sería el serializer que lista las Áreas asociadas

    class Meta:
        model = Puerta
        fields = ['id', 'nombre', 'descripcion', 'activo', 'areas']

class PuertaCreateSerializer(serializers.ModelSerializer):
    areas = serializers.PrimaryKeyRelatedField(queryset=Area.objects.all(), many=True)

    class Meta:
        model = Puerta
        fields = ['id', 'nombre', 'descripcion', 'activo', 'areas']