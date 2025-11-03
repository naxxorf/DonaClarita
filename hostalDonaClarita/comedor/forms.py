from django import forms
from .models import Plato, MinutaDia

class PlatoForm(forms.ModelForm):
    class Meta:
        model = Plato
        fields = ['nombre', 'tipo', 'descripcion']

class MinutaDiaForm(forms.ModelForm):
    class Meta:
        model = MinutaDia
        fields = ['fecha', 'platos']
        
        # Widgets para mejorar la experiencia
        widgets = {
            # Usamos un selector de fecha nativo del navegador
            'fecha': forms.DateInput(attrs={'type': 'date'}),
            
            # ¡IMPORTANTE! Esto es mucho mejor que la lista fea
            # de selección múltiple.
            'platos': forms.CheckboxSelectMultiple, 
        }