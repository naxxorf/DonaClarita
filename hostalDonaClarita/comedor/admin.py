from django.contrib import admin
from .models import Plato, MinutaDia

@admin.register(Plato)
class PlatoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'tipo')
    list_filter = ('tipo',)
    search_fields = ('nombre',)

@admin.register(MinutaDia)
class MinutaDiaAdmin(admin.ModelAdmin):
    list_display = ('fecha', 'total_platos')
    list_filter = ('fecha',)
    
    # ¡IMPORTANTE! Esto te da una interfaz "mágica" para 
    # seleccionar platos en el admin.
    filter_horizontal = ('platos',) 

    def total_platos(self, obj):
        return obj.platos.count()
    total_platos.short_description = "N° de Platos"