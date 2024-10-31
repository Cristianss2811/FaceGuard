from django.db import models
from datetime import datetime

class Movimiento(models.Model):
    tipo  = models.CharField(max_length=40)
    hora = models.TimeField(default = datetime.now().strftime("%H:%M:%S"))
    fecha = models.DateField(default= datetime.now().strftime("%Y-%m-%d"))

    def __str__(self): #Metodo para que en el panel muestre el nombre del area
        return f"Tipo de movimiento: {self.tipo} Hora: {self.hora} Fecha: {self.fecha}"