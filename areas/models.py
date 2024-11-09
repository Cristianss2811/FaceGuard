from django.db import models

class Zona(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)
    activo = models.BooleanField(default=False)

    def __str__(self):
        return f"Zona: {self.nombre}"

class Area(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)
    activo = models.BooleanField(default=False)
    zonas = models.ManyToManyField(Zona, through='ZonasAreas', related_name='zonas')

    def __str__(self):
        return self.nombre

class Puerta(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)
    activo = models.BooleanField(default=False)
    areas = models.ManyToManyField(Area, through='PuertasAreas', related_name='puertas')

    def __str__(self):
        return f"Puerta: {self.nombre}"

class PuertasAreas(models.Model):
    puerta = models.ForeignKey(Puerta, on_delete=models.CASCADE)
    area = models.ForeignKey(Area, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.puerta.nombre} - {self.area.nombre}"   
    
class ZonasAreas(models.Model):
    zona = models.ForeignKey(Zona, on_delete=models.CASCADE)
    area = models.ForeignKey(Area, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.zona.nombre} - {self.area.nombre}"