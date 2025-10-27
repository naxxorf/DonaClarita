from django.shortcuts import render
from django.utils import timezone
from django.db.models import Q,Count
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import (
    ListView, 
    CreateView, 
    UpdateView, 
    DeleteView
)
from django.contrib.auth.decorators import login_required
from .models import Habitacion, Cliente, Huesped, OrdenDeCompra, MinutaDia
from .forms import OrdenDeCompraForm, HuespedForm, ClienteForm, HabitacionForm

# ===============================================
# Vistas Genéricas (para no repetir plantillas)
# ===============================================

TEMPLATE_FORM = 'hostal/generico_form.html'
TEMPLATE_DELETE = 'hostal/generico_confirm_delete.html'

# ===============================================
# Vistas de HABITACIÓN
# ===============================================

class HabitacionListView(LoginRequiredMixin, ListView):
    model = Habitacion
    template_name = 'hostal/habitacion_lista.html' 
    context_object_name = 'object_list'

class HabitacionCreateView(LoginRequiredMixin, CreateView):
    model = Habitacion
    template_name = TEMPLATE_FORM
    form_class = HabitacionForm
    success_url = reverse_lazy('habitacion_lista')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = "Crear Nueva Habitación"
        context['cancel_url'] = reverse_lazy('habitacion_lista')
        return context

class HabitacionUpdateView(LoginRequiredMixin, UpdateView):
    model = Habitacion
    template_name = TEMPLATE_FORM
    form_class = HabitacionForm
    success_url = reverse_lazy('habitacion_lista')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = f"Editar Habitación: {self.object.numero}"
        context['cancel_url'] = reverse_lazy('habitacion_lista')
        return context

class HabitacionDeleteView(LoginRequiredMixin, DeleteView):
    model = Habitacion
    template_name = TEMPLATE_DELETE
    success_url = reverse_lazy('habitacion_lista')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = f"Eliminar Habitación: {self.object.numero}"
        context['mensaje_confirmacion'] = f"¿Está seguro de que desea eliminar la habitación {self.object.numero}?"
        return context

# ===============================================
# Vistas de CLIENTE (Empresa)
# ===============================================

class ClienteListView(LoginRequiredMixin, ListView):
    model = Cliente
    template_name = 'hostal/cliente_lista.html' 
    context_object_name = 'object_list'

class ClienteCreateView(LoginRequiredMixin, CreateView):
    model = Cliente
    template_name = TEMPLATE_FORM
    form_class = ClienteForm
    success_url = reverse_lazy('cliente_lista')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = "Crear Nuevo Cliente (Empresa)"
        context['cancel_url'] = reverse_lazy('cliente_lista')
        return context

class ClienteUpdateView(LoginRequiredMixin, UpdateView):
    model = Cliente
    template_name = TEMPLATE_FORM
    form_class = ClienteForm
    success_url = reverse_lazy('cliente_lista')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = f"Editar Cliente: {self.object.razon_social}"
        context['cancel_url'] = reverse_lazy('cliente_lista')
        return context

class ClienteDeleteView(LoginRequiredMixin, DeleteView):
    model = Cliente
    template_name = TEMPLATE_DELETE
    success_url = reverse_lazy('cliente_lista')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = f"Eliminar Cliente: {self.object.razon_social}"
        context['mensaje_confirmacion'] = f"¿Está seguro de que desea eliminar al cliente {self.object.razon_social}?"
        return context

# ===============================================
# Vistas de HUÉSPED
# ===============================================

class HuespedListView(LoginRequiredMixin, ListView):
    model = Huesped
    template_name = 'hostal/huesped_lista.html'
    context_object_name = 'object_list'

class HuespedCreateView(LoginRequiredMixin, CreateView):
    model = Huesped
    template_name = TEMPLATE_FORM
    form_class = HuespedForm
    success_url = reverse_lazy('huesped_lista')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = "Registrar Check-in de Huésped"
        context['cancel_url'] = reverse_lazy('huesped_lista')
        return context

class HuespedUpdateView(LoginRequiredMixin, UpdateView):
    model = Huesped
    template_name = TEMPLATE_FORM
    form_class = HuespedForm
    success_url = reverse_lazy('huesped_lista')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = f"Editar Huésped: {self.object.nombre_completo}"
        context['cancel_url'] = reverse_lazy('huesped_lista')
        return context

class HuespedDeleteView(LoginRequiredMixin, DeleteView):
    model = Huesped
    template_name = TEMPLATE_DELETE
    success_url = reverse_lazy('huesped_lista')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = f"Eliminar Huésped: {self.object.nombre_completo}"
        context['mensaje_confirmacion'] = f"¿Está seguro de que desea eliminar al huésped {self.object.nombre_completo}?"
        context['cancel_url'] = reverse_lazy('huesped_lista')
        return context
    
    # ===============================================
    # Vistas de ORDEN DE COMPRA
    # ===============================================

class OrdenDeCompraListView(ListView):
    model = OrdenDeCompra
    template_name = 'hostal/orden_lista.html' # Tendrás que crear esta plantilla
    context_object_name = 'ordenes'

class OrdenDeCompraCreateView(CreateView):
    model = OrdenDeCompra
    form_class = OrdenDeCompraForm
    template_name = 'hostal/generico_form.html' 
    success_url = reverse_lazy('orden_lista')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Cargar Nueva Orden de Compra'
        context['cancel_url'] = reverse_lazy('orden_lista')
        return context
    
# ===============================================
# Vista del DASHBOARD
# ===============================================   
@login_required
def dashboard_view(request):
    """
    Vista principal que reúne todas las estadísticas clave 
    para el dashboard.
    """
    
    # 1. Estado de Habitaciones (Conteo y lista)
    habitaciones_lista = Habitacion.objects.all().order_by('numero')
    
    # Usamos .aggregate() para un conteo eficiente por estado
    conteo_estados = Habitacion.objects.values('estado').annotate(
        total=Count('estado')
    ).order_by() # El order_by() vacío es para limpiar ordenamientos por defecto

    # Convertimos la lista de diccionarios a un diccionario fácil de usar
    # ej: {'D': 5, 'O': 3, 'L': 2}
    # Y lo inicializamos con ceros para todos los estados
    status_choices = dict(Habitacion.ESTADO_CHOICES)
    counts = {key: {'label': label, 'total': 0} for key, label in status_choices.items()}
    
    for item in conteo_estados:
        key = item['estado']
        if key in counts:
            counts[key]['total'] = item['total']

    # 2. Porcentaje de Ocupación
    total_habitaciones = habitaciones_lista.count()
    # "Ocupación" incluye Ocupada ('O') y Asignada ('A')
    habitaciones_ocupadas = counts['O']['total'] + counts['A']['total']
    
    porcentaje_ocupacion = 0
    if total_habitaciones > 0:
        porcentaje_ocupacion = (habitaciones_ocupadas * 100) / total_habitaciones

    # 3. Minuta de Platos del Día
    today = timezone.now().date()
    minuta_hoy = MinutaDia.objects.filter(fecha=today).first()
    platos_del_dia = None
    if minuta_hoy:
        platos_del_dia = minuta_hoy.platos.all().order_by('tipo')

    # 4. Compilar el contexto
    context = {
        'habitaciones_lista': habitaciones_lista,
        'conteo_estados': counts, # Pasamos el diccionario de conteos
        'total_habitaciones': total_habitaciones,
        'porcentaje_ocupacion': porcentaje_ocupacion,
        'platos_del_dia': platos_del_dia,
        'fecha_hoy': today,
    }
    
    return render(request, 'hostal/dashboard.html', context)