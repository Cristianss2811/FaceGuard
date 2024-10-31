from django.contrib import admin

from atencion.models import Movimiento


# Register your models here.
class MovimientoAdmin(admin.ModelAdmin):
    list_display = ('tipo', 'hora', 'fecha')  # Muestra estos campos en la lista de zonas
    search_fields = ('tipo',)

admin.site.register(Movimiento, MovimientoAdmin)