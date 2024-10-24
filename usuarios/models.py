from django.db import models

# Create your models here.
class Roles(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)
    activo = models.BooleanField(default=False)

    def __str__(self):
        estado = "activo" if self.activo else "inactivo"
        return f"Rol: {self.nombre} está {estado}"
