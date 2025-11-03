from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .models import Plato, MinutaDia
from .forms import PlatoForm, MinutaDiaForm

# Definimos las plantillas genéricas
TEMPLATE_FORM = 'comedor/generico_form.html'
TEMPLATE_DELETE = 'comedor/generico_confirm_delete.html'

# ===============================================
# Vistas de PLATO
# ===============================================

class PlatoListView(LoginRequiredMixin, ListView):
    model = Plato
    template_name = 'comedor/plato_lista.html'
    context_object_name = 'platos'

class PlatoCreateView(LoginRequiredMixin, CreateView):
    model = Plato
    form_class = PlatoForm
    template_name = TEMPLATE_FORM
    success_url = reverse_lazy('comedor:plato_lista')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = "Crear Nuevo Plato"
        context['cancel_url'] = reverse_lazy('comedor:plato_lista')
        return context

class PlatoUpdateView(LoginRequiredMixin, UpdateView):
    model = Plato
    form_class = PlatoForm
    template_name = TEMPLATE_FORM
    success_url = reverse_lazy('comedor:plato_lista')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = f"Editar Plato: {self.object.nombre}"
        context['cancel_url'] = reverse_lazy('comedor:plato_lista')
        return context

class PlatoDeleteView(LoginRequiredMixin, DeleteView):
    model = Plato
    template_name = TEMPLATE_DELETE
    success_url = reverse_lazy('comedor:plato_lista')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = f"Eliminar Plato: {self.object.nombre}"
        return context

# ===============================================
# Vistas de MINUTA (Menú del Día)
# ===============================================

class MinutaDiaListView(LoginRequiredMixin, ListView):
    model = MinutaDia
    template_name = 'comedor/minuta_lista.html'
    context_object_name = 'minutas'

class MinutaDiaCreateView(LoginRequiredMixin, CreateView):
    model = MinutaDia
    form_class = MinutaDiaForm
    template_name = TEMPLATE_FORM
    success_url = reverse_lazy('comedor:minuta_lista')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = "Crear Minuta del Día"
        context['cancel_url'] = reverse_lazy('comedor:minuta_lista')
        return context

class MinutaDiaUpdateView(LoginRequiredMixin, UpdateView):
    model = MinutaDia
    form_class = MinutaDiaForm
    template_name = TEMPLATE_FORM
    success_url = reverse_lazy('comedor:minuta_lista')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = f"Editar Minuta del {self.object.fecha}"
        context['cancel_url'] = reverse_lazy('comedor:minuta_lista')
        return context

class MinutaDiaDeleteView(LoginRequiredMixin, DeleteView):
    model = MinutaDia
    template_name = TEMPLATE_DELETE
    success_url = reverse_lazy('comedor:minuta_lista')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = f"Eliminar Minuta del {self.object.fecha}"
        return context