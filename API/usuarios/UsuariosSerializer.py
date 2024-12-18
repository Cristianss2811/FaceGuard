from rest_framework import serializers

from usuarios.models import Profile, ProfileRole, Roles


class ProfileListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['id', 'nombre', 'apellido_p', 'apellido_m', 'fecha_nacimiento', 'sexo', 'nss', 'telefono', 'direccion', 'estado', 'ciudad', 'user_id']

class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Roles
        fields = ['id', 'nombre', 'descripcion', 'activo']

class ProfileRoleSerializer(serializers.ModelSerializer):
    role = RoleSerializer()

    class Meta:
        model = ProfileRole
        fields = ['profile', 'role', 'fecha_vencimiento']

class ProfileSerializer(serializers.ModelSerializer):
    roles = RoleSerializer(many=True, read_only=True)

    class Meta:
        model = Profile
        fields = ['user', 'nombre', 'apellido_p', 'apellido_m', 'telefono', 'direccion', 'estado', 'ciudad', 'roles']