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
    sexo = models.CharField(max_length=10, choices=[('M', 'Masculino'), ('F', 'Femenino'), ('O', 'Otro')], blank=True, null=True)
    nss = models.CharField(max_length=15, blank=True, null=True)
    telefono = models.CharField(max_length=15, blank=True, null=True)
    direccion = models.CharField(max_length=255, blank=True, null=True)
    estado = models.CharField(max_length=50, blank=True, null=True)
    ciudad = models.CharField(max_length=50, blank=True, null=True)
    imagen_id = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"

class ProfileRole(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    role = models.ForeignKey(Roles, on_delete=models.CASCADE)
    fecha_vencimiento = models.DateField(null=True, blank=True)

    class Meta:
        unique_together = ('profile', 'role')

    def __str__(self):
        return f"{self.profile.user.username} - {self.role.nombre} (Vence: {self.fecha_vencimiento})"