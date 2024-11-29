from django.contrib import admin

from notificaciones.models import Notificacion


# Register your models here.
class NotificacionAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'mensaje','leida', 'fecha_creacion')  # Muestra estos campos en la lista de zonas
    
admin.site.register(Notificacion, NotificacionAdmin)