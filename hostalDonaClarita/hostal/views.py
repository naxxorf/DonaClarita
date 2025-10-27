from django.shortcuts import render
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import (
    ListView, 
    CreateView, 
    UpdateView, 
    DeleteView
)
from .models import Habitacion, Cliente, Huesped, OrdenDeCompra
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