from rest_framework import serializers
from areas.models import Roles

class RolesListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Roles
        fields = ['id', 'nombre', 'descripcion', 'activo']

class RolesCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Roles
        fields = '__all__'

class RolesUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Roles
        fields = ['nombre', 'descripcion', 'activo']