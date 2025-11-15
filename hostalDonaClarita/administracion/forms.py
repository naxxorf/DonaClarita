from django import forms
from .models import Proveedor, OrdenPedido

class ProveedorForm(forms.ModelForm):
    class Meta:
        model = Proveedor
        fields = ['id_proveedor', 'razon_social', 'rut', 'contacto', 'telefono', 'rubro']

class OrdenPedidoForm(forms.ModelForm):
    class Meta:
        model = OrdenPedido
        fields = ['proveedor', 'estado'] 
        # Nota: El 'solicitante' se asigna automáticamente en la vista