from django.contrib import admin
from .models import Proveedor, FamiliaProducto, Producto, OrdenPedido, DetallePedido

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