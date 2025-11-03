from django.db import models

# ===============================================
# MODELO: PLATO
# ===============================================

class Plato(models.Model):
    """ 
    Representa un plato individual que se puede servir (Entrada, Fondo, etc.)
    """
    TIPO_CHOICES = [
        ('entrada', 'Entrada'),
        ('fondo', 'Plato de Fondo'),
        ('postre', 'Postre'),
        ('bebida', 'Bebida'),
    ]
    
    nombre = models.CharField(max_length=200, unique=True)
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)
    descripcion = models.TextField(blank=True, help_text="Ingredientes o detalles")

    class Meta:
        ordering = ['tipo', 'nombre']

    def __str__(self):
        # Esto devuelve, por ejemplo: "Plato de Fondo: Lomo Saltado"
        return f"{self.get_tipo_display()}: {self.nombre}"

# ===============================================
# MODELO: MINUTA DEL DÍA
# ===============================================

class MinutaDia(models.Model):
    """ 
    Define el menú o 'minuta' para una fecha específica.
    Se conecta con el modelo Plato.
    """
    fecha = models.DateField(unique=True, help_text="Fecha para la que aplica este menú")
    
    # Esta es la conexión clave:
    platos = models.ManyToManyField(
        Plato, 
        related_name="minutas",
        help_text="Seleccione los platos disponibles para este día"
    )

    class Meta:
        ordering = ['-fecha'] # Muestra las fechas más nuevas primero

    def __str__(self):
        return f"Minuta del {self.fecha.strftime('%d-%m-%Y')}"