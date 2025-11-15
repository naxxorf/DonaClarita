from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .models import Proveedor, OrdenPedido, Producto
from .forms import ProveedorForm, OrdenPedidoForm 
from hostalDonaClarita.mixins import SoloBodegaMixin

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