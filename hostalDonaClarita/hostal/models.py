from django.conf import settings
from django.db import models
from django.core.validators import RegexValidator

RUT_VALIDATOR = RegexValidator(r'^\d{7,8}-[0-9kK]$', 'Formato RUT inválido. Ej: 12345678-9')

# REQUERIMIENTO: REGISTRO DE CLIENTES [cite: 12]
class Cliente(models.Model):
    """
    Representa a la Empresa (cliente) que contrata los servicios.
    Se vincula 1 a 1 con un Usuario de Django para el login.
    """
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='cliente_profile', help_text="Usuario de la empresa para iniciar sesión")
    razon_social = models.CharField(max_length=255, unique=True, help_text="Datos de la empresa.")
    rut = models.CharField(max_length=12, unique=True, validators=[RUT_VALIDATOR], db_index=True)
    
    class Meta:
        ordering = ['razon_social']
        indexes = [models.Index(fields=['rut']),]

    def __str__(self):
        return self.razon_social

# REQUERIMIENTO: REGISTRO DE HABITACIÓN 
class Habitacion(models.Model):
    """
    Representa una habitación del hostal y su estado.
    """
    ESTADO_CHOICES = [
        ('D', 'Disponible'),
        ('A', 'Asignada a empresa'),
        ('M', 'En mantenimiento'),
        ('O', 'Ocupada'),
        ('L', 'Para Limpieza'),
    ]
    
    numero = models.CharField(max_length=10, unique=True, db_index=True)
    estado = models.CharField(max_length=1, choices=ESTADO_CHOICES, default='D', help_text="Estado de disponibilidad de la habitación")
    tipo_cama = models.CharField(max_length=100, help_text="Datos propios de la habitación")
    accesorios = models.TextField(blank=True, help_text="Accesorios de la habitación")
    precio = models.DecimalField(max_digits=10, decimal_places=2, help_text="Precio de la habitación")

    class Meta:
        ordering = ['numero']

    def __str__(self):
        return f"Habitación {self.numero} ({self.get_estado_display()})"

# REQUERIMIENTO: REGISTROS DE ORDEN DE COMPRA (CLIENTE)
class OrdenDeCompra(models.Model):
    """
    Registra la orden de compra enviada por la empresa cliente.
    """
    cliente = models.ForeignKey(Cliente, on_delete=models.PROTECT, related_name='ordenes', help_text="Cliente que emite la orden")
    codigo_orden = models.CharField(max_length=100, unique=True, help_text="Código de la orden de compra", db_index=True)
    fecha_emision = models.DateField(auto_now_add=True)
    lista_huespedes_excel = models.FileField(upload_to='listas_excel/', blank=True, null=True, help_text="Permite registrar la lista de huéspedes por planilla.")

    class Meta:
        ordering = ['-fecha_emision']
        indexes = [models.Index(fields=['codigo_orden']),]

    def __str__(self):
        return f"OC {self.codigo_orden} - {self.cliente.razon_social}"

# REQUERIMIENTO: REGISTRO DE HUÉSPEDES
class Huesped(models.Model):
    """
    Ficha del huésped (trabajador de la empresa).
    """
    empresa = models.ForeignKey(Cliente, on_delete=models.PROTECT, related_name='huespedes', help_text="Empresa de procedencia.")
    orden_de_compra_asociada = models.ForeignKey(OrdenDeCompra, on_delete=models.SET_NULL, null=True, blank=True, help_text="Orden de compra que valida su estadía")
    habitacion = models.ForeignKey(Habitacion, on_delete=models.SET_NULL, null=True, blank=True, related_name='ocupantes', help_text="Habitación asignada.")
    rut = models.CharField(max_length=12, unique=True, validators=[RUT_VALIDATOR], db_index=True)
    nombre_completo = models.CharField(max_length=255)

    class Meta:
        ordering = ['nombre_completo']
        indexes = [models.Index(fields=['rut']),]

    def __str__(self):
        return f"{self.nombre_completo} ({self.empresa.razon_social})"
    
    @property
    def esta_autorizado(self):
        # La validación es simple: ¿Tiene una OC asignada?
        return self.orden_de_compra_asociada is not None

    @property
    def estado_autorizacion_texto(self):
        if self.esta_autorizado:
            return f"✅ Validado (OC: {self.orden_de_compra_asociada.codigo_orden})"

        return "❌ Sin Autorización"
    
    def save(self, *args, **kwargs):
        
        # 1. Obtenemos la habitación "antigua" (la que estaba en la BBDD)
        old_habitacion = None
        if self.pk: # Si el huésped ya existe (es una edición)
            try:
                # Buscamos el estado anterior del huésped
                old_huesped = Huesped.objects.get(pk=self.pk)
                old_habitacion = old_huesped.habitacion
            except Huesped.DoesNotExist:
                pass # No debería pasar, pero por si acaso

        # 2. Obtenemos la habitación "nueva" (la que se está asignando ahora)
        new_habitacion = self.habitacion

        # 3. Guardamos al huésped PRIMERO
        super().save(*args, **kwargs)

        # 4. Comparamos si la habitación cambió
        if new_habitacion != old_habitacion:
            
            # 4a. Si hay una HABITACIÓN NUEVA, marcarla como Ocupada
            if new_habitacion:
                new_habitacion.estado = 'O'  # 'O' = Ocupada
                new_habitacion.save(update_fields=['estado'])

            # 4b. Si había una HABITACIÓN ANTIGUA, marcarla para Limpieza
            if old_habitacion:
                # Revisamos si la habitación antigua quedó 100% vacía
                # Usamos el related_name='ocupantes' que ya tenías
                if not old_habitacion.ocupantes.exists():
                    old_habitacion.estado = 'L'  # 'L' = Para Limpieza
                    old_habitacion.save(update_fields=['estado'])

# --- MODELOS PARA EL COMEDOR ---

class Plato(models.Model):
    """ Representa un plato individual que se puede servir. """
    TIPO_CHOICES = [
        ('entrada', 'Entrada'),
        ('fondo', 'Plato de Fondo'),
        ('postre', 'Postre'),
        ('bebida', 'Bebida'),
    ]
    nombre = models.CharField(max_length=200)
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)
    descripcion = models.TextField(blank=True, help_text="Ingredientes o detalles")

    class Meta:
        ordering = ['tipo', 'nombre']

    def __str__(self):
        return f"{self.get_tipo_display()}: {self.nombre}"

class MinutaDia(models.Model):
    """ Define el menú o 'minuta' para una fecha específica. """
    fecha = models.DateField(unique=True, help_text="Fecha para la que aplica este menú")
    platos = models.ManyToManyField(
        Plato, 
        related_name="minutas",
        help_text="Platos disponibles para este día"
    )

    class Meta:
        ordering = ['-fecha']

    def __str__(self):
        return f"Minuta del {self.fecha.strftime('%d-%m-%Y')}"