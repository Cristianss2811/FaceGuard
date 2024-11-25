from django.contrib.auth.management.commands.changepassword import UserModel
from django.db import models
from datetime import datetime

from areas.models import Puerta


class Movimiento(models.Model):
    tipo  = models.CharField(max_length=40)
    hora = models.TimeField(default = datetime.now().strftime("%H:%M:%S"))
    fecha = models.DateField(default= datetime.now().strftime("%Y-%m-%d"))

    def __str__(self): #Metodo para que en el panel muestre el nombre del area
        return f"Tipo de movimiento: {self.tipo} Hora: {self.hora} Fecha: {self.fecha}"

class UsuarioMovimiento(models.Model):
    usuario = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    movimiento = models.ForeignKey(Movimiento, on_delete=models.CASCADE)

class PuertaMovimiento(models.Model):
    puerta = models.ForeignKey(Puerta, on_delete=models.CASCADE)
    movimiento = models.ForeignKey(Movimiento, on_delete=models.CASCADE)