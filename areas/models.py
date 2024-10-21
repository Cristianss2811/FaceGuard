from django.db import models

# Create your models here.
class Area(models.Model):
    nombre  = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)
    activo = models.BooleanField(default=False)

    def __str__(self): #Metodo para que en el panel muestre el nombre del area
        return self.nombre
    
class Puerta(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)
    area = models.ForeignKey(Area, on_delete=models.CASCADE)
    activo = models.BooleanField(default=False)

    def __str__(self): #Metodo para que en el panel muestre la descripcion de la puerta
        return f"Puerta:{self.nombre} en el area {self.area.nombre}"