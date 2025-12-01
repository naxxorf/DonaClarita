from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import redirect
from django.contrib import messages

class SoloRecepcionMixin(UserPassesTestMixin):
    """ Solo permite acceso a Recepcionistas y Administradores """
    def test_func(self):
        user = self.request.user
        if not user.is_authenticated: return False
        # Si es superusuario, pasa. Si tiene perfil de empleado y es RECEPCION o ADMIN, pasa.
        return user.is_superuser or (hasattr(user, 'empleado_profile') and user.empleado_profile.rol in ['RECEPCION', 'ADMIN'])

    def handle_no_permission(self):
        if not self.request.user.is_authenticated:
            return super().handle_no_permission()
        messages.error(self.request, "No tienes permisos de Recepción para ver esta página.")
        return redirect('hostal:dashboard')
        
class SoloCocinaMixin(UserPassesTestMixin):
    """ Solo permite acceso a Cocina y Administradores """
    def test_func(self):
        user = self.request.user
        if not user.is_authenticated: return False
        return user.is_superuser or (hasattr(user, 'empleado_profile') and user.empleado_profile.rol in ['COCINA', 'ADMIN'])

    def handle_no_permission(self):
        if not self.request.user.is_authenticated:
            return super().handle_no_permission()
        messages.error(self.request, "Acceso denegado. Área exclusiva de Cocina.")
        return redirect('hostal:dashboard')
    
class SoloBodegaMixin(UserPassesTestMixin):
    """ Solo permite acceso a Bodega/Administración """
    def test_func(self):
        user = self.request.user
        if not user.is_authenticated: return False
        return user.is_superuser or (hasattr(user, 'empleado_profile') and user.empleado_profile.rol in ['BODEGA', 'ADMIN'])

    def handle_no_permission(self):
        if not self.request.user.is_authenticated:
            return super().handle_no_permission()
        messages.error(self.request, "No tienes permisos de Bodega para ver esta página.")
        return redirect('hostal:dashboard')
    
class SoloAdminMixin(UserPassesTestMixin):
    """ Solo permite acceso a Administradores Generales y Superusuarios """
    def test_func(self):
        u = self.request.user
        if not u.is_authenticated: return False
        # Pasa si es Superuser O si su rol es 'ADMIN'
        return u.is_active and (u.is_superuser or (hasattr(u, 'empleado_profile') and u.empleado_profile.rol == 'ADMIN'))
    
    def handle_no_permission(self):
        if not self.request.user.is_authenticated:
            return super().handle_no_permission()
        messages.error(self.request, "Acceso denegado. Área exclusiva de Administración.")
        return redirect('hostal:dashboard')