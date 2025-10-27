from django.db import models

# Create your models here.
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