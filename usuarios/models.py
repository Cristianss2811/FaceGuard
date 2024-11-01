from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Roles(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)
    activo = models.BooleanField(default=False)

    def __str__(self):
        estado = "activo" if self.activo else "inactivo"
        return f"Rol: {self.nombre} está {estado}"

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=30, blank=True, null=True)
    apellido_p = models.CharField(max_length=30, blank=True, null=True)
    apellido_m = models.CharField(max_length=30, blank=True, null=True)
    fecha_nacimiento = models.DateField(blank=True, null=True)
    sexo = models.CharField(max_length=10, choices=[('M', 'Masculino'), ('F', 'Femenino')], blank=True, null=True)
    nss = models.CharField(max_length=15, blank=True, null=True)  # Número de Seguro Social
    telefono = models.CharField(max_length=15, blank=True, null=True)
    direccion = models.CharField(max_length=255, blank=True, null=True)
    estado = models.CharField(max_length=50, blank=True, null=True)
    ciudad = models.CharField(max_length=50, blank=True, null=True)
    imagen_id = models.IntegerField(blank=True, null=True)  # ID de la imagen

    def __str__(self):
        return f"{self.user.username}'s Profile"
