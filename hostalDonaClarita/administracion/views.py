from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .models import Proveedor, OrdenPedido, Producto, Empleado
from .forms import ProveedorForm, OrdenPedidoForm, EmpleadoRegistroForm, EmpleadoEditarForm
from hostalDonaClarita.mixins import SoloBodegaMixin , SoloAdminMixin


TEMPLATE_FORM = 'administracion/generico_form.html' # Usaremos un template genérico nuevo
TEMPLATE_DELETE = 'administracion/generico_confirm_delete.html'

# ===============================================
# GESTIÓN DE PROVEEDORES
# ===============================================
class ProveedorListView(SoloBodegaMixin,LoginRequiredMixin, ListView):
    model = Proveedor
    template_name = 'administracion/proveedor_lista.html'
    context_object_name = 'proveedores'

class ProveedorCreateView(SoloBodegaMixin,LoginRequiredMixin, CreateView):
    model = Proveedor
    form_class = ProveedorForm
    template_name = TEMPLATE_FORM
    success_url = reverse_lazy('administracion:proveedor_lista')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = "Registrar Nuevo Proveedor"
        context['cancel_url'] = reverse_lazy('administracion:proveedor_lista')
        return context

class ProveedorUpdateView(SoloBodegaMixin,LoginRequiredMixin, UpdateView):
    model = Proveedor
    form_class = ProveedorForm
    template_name = TEMPLATE_FORM
    success_url = reverse_lazy('administracion:proveedor_lista')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = f"Editar Proveedor: {self.object.razon_social}"
        context['cancel_url'] = reverse_lazy('administracion:proveedor_lista')
        return context

class ProveedorDeleteView(SoloBodegaMixin,LoginRequiredMixin, DeleteView):
    model = Proveedor
    template_name = TEMPLATE_DELETE
    success_url = reverse_lazy('administracion:proveedor_lista')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = f"Eliminar Proveedor: {self.object.razon_social}"
        return context

# ===============================================
# GESTIÓN DE PEDIDOS
# ===============================================
class OrdenPedidoListView(SoloBodegaMixin,LoginRequiredMixin, ListView):
    model = OrdenPedido
    template_name = 'administracion/pedido_lista.html'
    context_object_name = 'pedidos'

class OrdenPedidoCreateView(SoloBodegaMixin,LoginRequiredMixin, CreateView):
    model = OrdenPedido
    form_class = OrdenPedidoForm
    template_name = TEMPLATE_FORM
    success_url = reverse_lazy('administracion:pedido_lista')

    def form_valid(self, form):
        form.instance.solicitante = self.request.user # Asigna el usuario actual automáticamente
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = "Generar Orden de Pedido"
        context['cancel_url'] = reverse_lazy('administracion:pedido_lista')
        return context
    
# ===============================================
# GESTIÓN DE EMPLEADOS (Solo Admin)
# ===============================================

class EmpleadoListView(SoloAdminMixin, LoginRequiredMixin, ListView):
    model = Empleado
    template_name = 'administracion/empleado_lista.html'
    context_object_name = 'empleados'

class EmpleadoCreateView(SoloAdminMixin, LoginRequiredMixin, CreateView):
    model = Empleado
    form_class = EmpleadoRegistroForm # Usamos el form especial
    template_name = TEMPLATE_FORM
    success_url = reverse_lazy('administracion:empleado_lista')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = "Registrar Nuevo Empleado"
        context['cancel_url'] = reverse_lazy('administracion:empleado_lista')
        return context

class EmpleadoUpdateView(SoloAdminMixin, LoginRequiredMixin, UpdateView):
    model = Empleado
    form_class = EmpleadoEditarForm # Usamos el form de edición
    template_name = TEMPLATE_FORM
    success_url = reverse_lazy('administracion:empleado_lista')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = f"Editar Empleado: {self.object.user.username}"
        context['cancel_url'] = reverse_lazy('administracion:empleado_lista')
        return context

class EmpleadoDeleteView(SoloAdminMixin, LoginRequiredMixin, DeleteView):
    model = Empleado
    template_name = TEMPLATE_DELETE
    success_url = reverse_lazy('administracion:empleado_lista')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = f"Eliminar Empleado: {self.object.user.username}"
        context['mensaje_confirmacion'] = "¡Advertencia! Esto también eliminará el usuario de acceso al sistema."
        return context