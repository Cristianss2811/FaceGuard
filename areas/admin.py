from django.contrib import admin
from .models import Area, Puerta

class AreaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'descripcion')  # Muestra estos campos en la lista de zonas
    search_fields = ('nombre',)  # Añade un campo de búsqueda por nombre

class PuertaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'area', 'activo')  # Muestra estos campos en la lista de puertas
    list_filter = ('area', 'activo')  # Añade filtros para zona y estado activo

# Registramos los modelos con personalización
admin.site.register(Area, AreaAdmin)
admin.site.register(Puerta, PuertaAdmin)