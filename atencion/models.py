from django.contrib.auth import get_user_model
from django.db import models
from datetime import datetime
from areas.models import Puerta

UserModel = get_user_model()  # Obtiene el modelo de usuario configurado en settings.AUTH_USER_MODEL

class Movimiento(models.Model):
    tipo = models.CharField(max_length=40)
    hora = models.TimeField(default=datetime.now)
    fecha = models.DateField(default=datetime.now)

    def __str__(self):
        return f"Tipo de movimiento: {self.tipo} Hora: {self.hora} Fecha: {self.fecha}"


class MovimientoUsuario(models.Model):  # Renombrado para mayor claridad
    usuario = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    movimiento = models.ForeignKey(Movimiento, on_delete=models.CASCADE)


class MovimientoPuerta(models.Model):  # Renombrado para mayor claridad
    puerta = models.ForeignKey(Puerta, on_delete=models.CASCADE)
    movimiento = models.ForeignKey(Movimiento, on_delete=models.CASCADE)