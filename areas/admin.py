from django.contrib import admin
from .models import Area, Puerta, Zona

class AreaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'descripcion', 'mostrar_zonas', 'activo')  # Muestra estos campos en la lista de zonas
    search_fields = ('nombre',)  # Añade un campo de búsqueda por nombre

    def mostrar_zonas(self, obj):
        # Mostrar las áreas asociadas a la puerta como una lista de nombres
        return ", ".join([zona.nombre for zona in obj.zonas.all()])
    mostrar_zonas.short_description = 'Zonas'  # Personaliza el nombre de la columna

class PuertaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'mostrar_areas', 'activo')  # Muestra estos campos en la lista de puertas
    list_filter = ('areas', 'activo')  # Añade filtros para zona y estado activo

    def mostrar_areas(self, obj):
        # Mostrar las áreas asociadas a la puerta como una lista de nombres
        return ", ".join([area.nombre for area in obj.areas.all()])
    mostrar_areas.short_description = 'Áreas'  # Personaliza el nombre de la columna

class ZonaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'descripcion', 'activo')  # Muestra estos campos en la lista de zonas
    search_fields = ('nombre',)  # Añade un campo de búsqueda por nombre


    

# Registramos los modelos con personalización
admin.site.register(Area, AreaAdmin)
admin.site.register(Puerta, PuertaAdmin)
admin.site.register(Zona, ZonaAdmin)