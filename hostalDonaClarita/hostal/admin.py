from django.contrib import admin
from .models import Cliente, Habitacion, OrdenDeCompra, Huesped

# Estos nos permiten ver modelos relacionados dentro de otros modelos.

class OrdenDeCompraInline(admin.TabularInline):
    """
    Permite ver las Órdenes de Compra directamente
    en la vista de detalle de un Cliente.
    """
    model = OrdenDeCompra
    extra = 0  # No mostrar formularios vacíos por defecto
    readonly_fields = ('fecha_emision', 'codigo_orden')
    can_delete = False # Generalmente no querrás borrar OCs desde un cliente
    ordering = ('-fecha_emision',)

class HuespedInline(admin.TabularInline):
    """
    Permite ver los huéspedes (ocupantes) directamente
    en la vista de detalle de una Habitación.
    """
    model = Huesped
    extra = 0
    fields = ('nombre_completo', 'rut', 'empresa') # Campos a mostrar
    readonly_fields = ('nombre_completo', 'rut', 'empresa')
    can_delete = False

# --- ModelAdmins ---
# Aquí personalizamos la apariencia de cada modelo en el admin.

@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    """
    Personalización del admin para el modelo Cliente.
    """
    list_display = ('razon_social', 'rut', 'user')
    search_fields = ('razon_social', 'rut', 'user__username') # Permite buscar por nombre de usuario
    inlines = [OrdenDeCompraInline] # Añade las OCs en la vista del cliente
    raw_id_fields = ('user',)                      # evita dropdown enorme para users
    list_select_related = ('user',)                # mejora rendimiento en list_display

@admin.register(Habitacion)
class HabitacionAdmin(admin.ModelAdmin):
    """
    Personalización del admin para el modelo Habitación.
    """
    list_display = ('numero', 'estado', 'tipo_cama', 'precio')
    search_fields = ('numero',)
    list_filter = ('estado', 'tipo_cama')
    
    # ¡Muy útil! Permite cambiar el estado y precio desde la lista
    list_editable = ('estado', 'precio') 
    
    inlines = [HuespedInline] # Muestra qué huéspedes están en esta habitación
    list_per_page = 50                             # opcional: ajustar según datos

@admin.register(OrdenDeCompra)
class OrdenDeCompraAdmin(admin.ModelAdmin):
    """
    Personalización del admin para Órdenes de Compra.
    """
    list_display = ('codigo_orden', 'cliente', 'fecha_emision', 'lista_huespedes_excel')
    search_fields = ('codigo_orden', 'cliente__razon_social') # Permite buscar por la razón social del cliente
    list_filter = ('cliente', 'fecha_emision')
    readonly_fields = ('fecha_emision',) # Porque es auto_now_add
    
    # Campo de búsqueda en lugar de dropdown (para clientes)
    autocomplete_fields = ['cliente'] 

    # Mejora el rendimiento en list_display
    list_select_related = ('cliente',)             # mejora rendimiento

@admin.register(Huesped)
class HuespedAdmin(admin.ModelAdmin):
    """
    Personalización del admin para Huéspedes.
    """
    list_display = ('nombre_completo', 'rut', 'empresa', 'habitacion', 'orden_de_compra_asociada')
    search_fields = ('nombre_completo', 'rut', 'empresa__razon_social') # Buscar por huésped o empresa
    list_filter = ('empresa', 'habitacion')
    
    # ¡Fundamental! Usa campos de búsqueda en lugar de dropdowns gigantes
    # para seleccionar la empresa, habitación y OC.
    autocomplete_fields = ['empresa', 'habitacion', 'orden_de_compra_asociada']
    list_select_related = ('empresa', 'habitacion', 'orden_de_compra_asociada')