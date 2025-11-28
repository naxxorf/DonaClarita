from django.contrib import admin
from .models import Proveedor, FamiliaProducto, Producto, OrdenPedido, DetallePedido, Empleado, Factura


class DetallePedidoInline(admin.TabularInline):
    model = DetallePedido
    extra = 1

@admin.register(OrdenPedido)
class OrdenPedidoAdmin(admin.ModelAdmin):
    list_display = ('id', 'proveedor', 'fecha_emision', 'estado')
    inlines = [DetallePedidoInline]

@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'codigo_generado', 'stock_actual', 'proveedor')
    list_filter = ('familia', 'proveedor')
    readonly_fields = ('codigo_generado',)

admin.site.register(Proveedor)
admin.site.register(FamiliaProducto)

@admin.register(Empleado)
class EmpleadoAdmin(admin.ModelAdmin):
    list_display = ('user', 'rut', 'rol', 'telefono')
    list_filter = ('rol',)
    search_fields = ('user__username', 'rut')
    
@admin.register(Factura)
class FacturaAdmin(admin.ModelAdmin):
    list_display = ('id', 'cliente', 'fecha_emision', 'total', 'estado')
    list_filter = ('estado', 'fecha_emision')
    search_fields = ('cliente__razon_social', 'id')
    list_editable = ('estado',)
    autocomplete_fields = ['cliente']