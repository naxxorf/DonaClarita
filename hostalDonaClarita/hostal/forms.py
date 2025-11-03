from django import forms
from hostal.models import OrdenDeCompra, Huesped, Cliente, Habitacion

class OrdenDeCompraForm(forms.ModelForm):
    class Meta:
        model = OrdenDeCompra
        # Campos que pides al crear una OC:
        fields = ['cliente', 'codigo_orden', 'lista_huespedes_excel']

class HuespedForm(forms.ModelForm):
    class Meta:
        model = Huesped
        # Campos que pides al crear un Huésped:
        fields = [
            'empresa', 
            'rut', 
            'nombre_completo', 
            'habitacion', 
            'orden_de_compra_asociada'  # <-- El campo clave de validación
        ]

class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        # Campos que pides al crear un Cliente:
        fields = [
            'user',
            'razon_social',
            'rut'
        ]

class HabitacionForm(forms.ModelForm):
    class Meta:
        model = Habitacion
        # Campos que pides al crear una Habitación:
        fields = [
            'numero',
            'estado',
            'tipo_cama',
            'accesorios',
            'precio'
        ]