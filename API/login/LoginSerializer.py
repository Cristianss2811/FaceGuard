from rest_framework import serializers
from django.contrib.auth import get_user_model

UserModel = get_user_model()

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    password = serializers.CharField(max_length=128)

    def create(self, validated_data):
        # Crear el usuario con los datos validados
        user = UserModel.objects.create(username=validated_data['username'])
        user.set_password(validated_data['password'])  # Asegurarse de guardar la contraseña de forma segura
        user.save()
        return user