from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Task(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True)
    datecompleted = models.DateTimeField(null=True, blank=True)
    importnat = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE) #El cascade es para eliminación en cascada si se borra el usuario se borran sus tareas

    def __str__(self): #Metodo para que en el panel muestre el nombre de la tarea
        return self.title + '- by ' + self.user.username