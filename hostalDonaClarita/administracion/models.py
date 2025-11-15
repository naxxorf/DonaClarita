from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

# ===============================================
# 1. PROVEEDORES
# ===============================================
class Proveedor(models.Model):
    id_proveedor = models.CharField(max_length=3, unique=True, help_text="ID de 3 dígitos")
    razon_social = models.CharField(max_length=255, unique=True)
    rut = models.CharField(max_length=12, unique=True)
    contacto = models.CharField(max_length=255, help_text="Nombre del contacto")
    telefono = models.CharField(max_length=20)
    rubro = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = "Proveedores"

    def __str__(self):
        return f"{self.razon_social} ({self.rubro})"

# ===============================================
# 2. PRODUCTOS (Para abastecimiento)
# ===============================================
class FamiliaProducto(models.Model):
    """ Ej: Abarrotes, Limpieza, Perecibles """
    codigo = models.CharField(max_length=3, unique=True, help_text="Código de 3 dígitos")
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre

class Producto(models.Model):
    proveedor = models.ForeignKey(Proveedor, on_delete=models.PROTECT, related_name='productos')
    familia = models.ForeignKey(FamiliaProducto, on_delete=models.PROTECT)
    nombre = models.CharField(max_length=255)
    sku_secuencial = models.CharField(max_length=3, help_text="Secuencial de 3 dígitos")
    precio_costo = models.DecimalField(max_digits=10, decimal_places=2)
    stock_actual = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.nombre}"

    @property
    def codigo_generado(self):
        # Requisito del PDF: ID Prov + ID Familia + Secuencial
        return f"{self.proveedor.id_proveedor}{self.familia.codigo}{self.sku_secuencial}"

# ===============================================
# 3. ÓRDENES DE PEDIDO (A Proveedores)
# ===============================================
class OrdenPedido(models.Model):
    ESTADOS = [('P', 'Pendiente'), ('R', 'Recibido'), ('C', 'Cancelado')]
    
    proveedor = models.ForeignKey(Proveedor, on_delete=models.PROTECT)
    solicitante = models.ForeignKey(User, on_delete=models.PROTECT)
    fecha_emision = models.DateTimeField(auto_now_add=True)
    estado = models.CharField(max_length=1, choices=ESTADOS, default='P')

    def __str__(self):
        return f"Pedido #{self.id} - {self.proveedor.razon_social}"

class DetallePedido(models.Model):
    orden = models.ForeignKey(OrdenPedido, on_delete=models.CASCADE, related_name='detalles')
    producto = models.ForeignKey(Producto, on_delete=models.PROTECT)
    cantidad = models.PositiveIntegerField()
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)

    @property
    def subtotal(self):
        return self.cantidad * self.precio_unitario
    
# ===============================================
# 4. GESTIÓN DE PERSONAL (EMPLEADOS)
# ===============================================
class Empleado(models.Model):
    """
    Extiende el usuario de Django para asignarle un ROL específico
    que limitará su acceso en el sistema.
    """
    ROLES = [
        ('ADMIN', 'Administrador General'),      # Acceso total
        ('RECEPCION', 'Recepcionista'),          # Acceso solo a Hostal (Check-in, Habitaciones)
        ('COCINA', 'Encargado de Cocina'),       # Acceso solo a Comedor (Platos, Minutas)
        ('BODEGA', 'Encargado de Bodega'),       # Acceso solo a Administración (Pedidos, Proveedores)
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='empleado_profile')
    rut = models.CharField(max_length=12, unique=True, help_text="RUT del empleado")
    telefono = models.CharField(max_length=20, blank=True)
    rol = models.CharField(max_length=20, choices=ROLES, default='RECEPCION')

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name} ({self.get_rol_display()})"    