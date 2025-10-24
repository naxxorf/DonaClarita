from django.shortcuts import render
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import (
    ListView, 
    CreateView, 
    UpdateView, 
    DeleteView
)
from .models import Habitacion, Cliente, Huesped

# ===============================================
# Vistas Genéricas (para no repetir plantillas)
# ===============================================
# Usaremos nombres de plantilla genéricos para los formularios
# y así no tener que crear 6 archivos HTML diferentes.
TEMPLATE_FORM = 'hostal/generico_form.html'
TEMPLATE_DELETE = 'hostal/generico_confirm_delete.html'

# ===============================================
# Vistas de HABITACIÓN
# ===============================================

class HabitacionListView(LoginRequiredMixin, ListView):
    model = Habitacion
    template_name = 'hostal/habitacion_lista.html' # Tu plantilla
    context_object_name = 'object_list'

class HabitacionCreateView(LoginRequiredMixin, CreateView):
    model = Habitacion
    template_name = TEMPLATE_FORM
    fields = ['numero', 'estado', 'tipo_cama', 'accesorios', 'precio']
    success_url = reverse_lazy('hostal:habitacion_lista')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = "Crear Nueva Habitación"
        return context

class HabitacionUpdateView(LoginRequiredMixin, UpdateView):
    model = Habitacion
    template_name = TEMPLATE_FORM
    fields = ['numero', 'estado', 'tipo_cama', 'accesorios', 'precio']
    success_url = reverse_lazy('hostal:habitacion_lista')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = f"Editar Habitación: {self.object.numero}"
        return context

class HabitacionDeleteView(LoginRequiredMixin, DeleteView):
    model = Habitacion
    template_name = TEMPLATE_DELETE
    success_url = reverse_lazy('hostal:habitacion_lista')

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
    template_name = 'hostal/cliente_lista.html' # Tu plantilla
    context_object_name = 'object_list'

class ClienteCreateView(LoginRequiredMixin, CreateView):
    model = Cliente
    template_name = TEMPLATE_FORM
    fields = ['user', 'razon_social', 'rut']
    success_url = reverse_lazy('hostal:cliente_lista')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = "Crear Nuevo Cliente (Empresa)"
        return context

class ClienteUpdateView(LoginRequiredMixin, UpdateView):
    model = Cliente
    template_name = TEMPLATE_FORM
    fields = ['user', 'razon_social', 'rut']
    success_url = reverse_lazy('hostal:cliente_lista')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = f"Editar Cliente: {self.object.razon_social}"
        return context

class ClienteDeleteView(LoginRequiredMixin, DeleteView):
    model = Cliente
    template_name = TEMPLATE_DELETE
    success_url = reverse_lazy('hostal:cliente_lista')
    
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
    template_name = 'hostal/huesped_lista.html' # Tu plantilla
    context_object_name = 'object_list'

class HuespedCreateView(LoginRequiredMixin, CreateView):
    model = Huesped
    template_name = TEMPLATE_FORM
    # Seleccionamos los campos para el check-in
    fields = ['nombre_completo', 'rut', 'empresa', 'habitacion', 'orden_de_compra_asociada']
    success_url = reverse_lazy('hostal:huesped_lista')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = "Registrar Check-in de Huésped"
        return context

class HuespedUpdateView(LoginRequiredMixin, UpdateView):
    model = Huesped
    template_name = TEMPLATE_FORM
    fields = ['nombre_completo', 'rut', 'empresa', 'habitacion', 'orden_de_compra_asociada']
    success_url = reverse_lazy('hostal:huesped_lista')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = f"Editar Huésped: {self.object.nombre_completo}"
        return context

class HuespedDeleteView(LoginRequiredMixin, DeleteView):
    model = Huesped
    template_name = TEMPLATE_DELETE
    success_url = reverse_lazy('hostal:huesped_lista')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = f"Eliminar Huésped: {self.object.nombre_completo}"
        context['mensaje_confirmacion'] = f"¿Está seguro de que desea eliminar al huésped {self.object.nombre_completo}?"
        return context