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
            'orden_de_compra_asociada'
        ]
        
    def clean(self):
        cleaned_data = super().clean()
        habitacion = cleaned_data.get('habitacion')
        
        if habitacion:
            # 1. Validar Estado (Mantenimiento/Limpieza) - Igual que antes
            if habitacion.estado in ['M', 'L']:
                self.add_error('habitacion', f"La habitación {habitacion.numero} no está disponible (Estado: {habitacion.get_estado_display()}).")
                return cleaned_data

            # 2. NUEVA VALIDACIÓN: EL CANDADO DE BLOQUEO
            # Si estamos agregando a alguien nuevo (no editando al mismo)
            es_nuevo_ingreso = True
            if self.instance.pk and self.instance.habitacion == habitacion:
                es_nuevo_ingreso = False 

            if es_nuevo_ingreso and habitacion.bloqueada_ingreso:
                # AQUÍ ESTÁ TU MENSAJE PERSONALIZADO
                self.add_error('habitacion', f"Habitación {habitacion.numero} ocupada y bloqueada para agregar huéspedes. Desbloquéela en 'Editar Habitación' si desea agregar más personas.")
                return cleaned_data

            # 3. Validación de Capacidad Real (Respaldo final)
            ocupantes_actuales = habitacion.ocupantes.all()
            cantidad_actual = ocupantes_actuales.count()
            
            if self.instance.pk and self.instance in ocupantes_actuales:
                cantidad_actual -= 1
            
            if cantidad_actual >= habitacion.capacidad:
                self.add_error('habitacion', f"La habitación {habitacion.numero} está llena al 100% ({habitacion.capacidad} personas).")

        return cleaned_data
    
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
            'capacidad',
            'bloqueada_ingreso',
            'tipo_cama',
            'accesorios',
            'precio'
        ]
        widgets = {'bloqueada_ingreso': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }