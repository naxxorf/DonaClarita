from django import forms
from .models import Proveedor, OrdenPedido, Empleado
from django.contrib.auth.models import User

class ProveedorForm(forms.ModelForm):
    class Meta:
        model = Proveedor
        fields = ['id_proveedor', 'razon_social', 'rut', 'contacto', 'telefono', 'rubro']

class OrdenPedidoForm(forms.ModelForm):
    class Meta:
        model = OrdenPedido
        fields = ['proveedor', 'estado'] 
        # Nota: El 'solicitante' se asigna automáticamente en la vista

class EmpleadoRegistroForm(forms.ModelForm):
    # Campos extra para crear el Usuario
    username = forms.CharField(label="Nombre de Usuario", max_length=150)
    email = forms.EmailField(label="Correo Electrónico")
    password = forms.CharField(label="Contraseña", widget=forms.PasswordInput)
    first_name = forms.CharField(label="Nombre")
    last_name = forms.CharField(label="Apellido")

    class Meta:
        model = Empleado
        fields = ['rut', 'telefono', 'rol'] # Campos del Empleado
        
    def save(self, commit=True):
        # 1. Creamos primero el Usuario
        user = User.objects.create_user(
            username=self.cleaned_data['username'],
            email=self.cleaned_data['email'],
            password=self.cleaned_data['password'],
            first_name=self.cleaned_data['first_name'],
            last_name=self.cleaned_data['last_name']
        )
        
        # 2. Creamos el Empleado y lo vinculamos
        empleado = super().save(commit=False)
        empleado.user = user
        
        if commit:
            empleado.save()
        return empleado

class EmpleadoEditarForm(forms.ModelForm):
    # Formulario más simple solo para editar datos del empleado (sin tocar password)
    first_name = forms.CharField(label="Nombre")
    last_name = forms.CharField(label="Apellido")
    email = forms.EmailField(label="Correo")

    class Meta:
        model = Empleado
        fields = ['rut', 'telefono', 'rol']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Pre-llenamos los datos del usuario
        if self.instance.pk:
            self.fields['first_name'].initial = self.instance.user.first_name
            self.fields['last_name'].initial = self.instance.user.last_name
            self.fields['email'].initial = self.instance.user.email

    def save(self, commit=True):
        empleado = super().save(commit=False)
        
        # Actualizamos también el Usuario vinculado
        user = empleado.user
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']
        user.save()

        if commit:
            empleado.save()
        return empleado