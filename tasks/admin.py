from django.contrib import admin
from .models import Task

class TaskAdmin(admin.ModelAdmin): #Este metodo hereda de admin y solo se utiliza para ver mas campos en el panel
    readonly_fields = ("created", )

# Register your models here.
admin.site.register(Task, TaskAdmin) #Agregamos la tabla al panel de administrador de django