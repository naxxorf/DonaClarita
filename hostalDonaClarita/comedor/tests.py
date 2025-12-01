from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from administracion.models import Empleado  # Importamos Empleado para asignar roles
from .models import Plato, MinutaDia

class ComedorModelTest(TestCase):
    def test_crear_plato(self):
        """Verifica que un plato se crea correctamente con su tipo"""
        plato = Plato.objects.create(
            nombre="Cazuela de Ave",
            tipo="fondo",
            descripcion="Con chuchoca"
        )
        self.assertEqual(str(plato), "Plato de Fondo: Cazuela de Ave")

class ComedorPermisosTest(TestCase):
    def setUp(self):
        # 1. Usuario Cocinero (Debe poder entrar)
        self.user_cocina = User.objects.create_user(username='chef', password='123')
        Empleado.objects.create(user=self.user_cocina, rut='11111111-1', rol='COCINA')

        # 2. Usuario Recepcionista (NO debe poder entrar al comedor)
        self.user_recepcion = User.objects.create_user(username='recep', password='123')
        Empleado.objects.create(user=self.user_recepcion, rut='22222222-2', rol='RECEPCION')

    def test_acceso_cocinero(self):
        """El cocinero DEBE ver la lista de platos"""
        self.client.force_login(self.user_cocina)
        response = self.client.get(reverse('comedor:plato_lista'))
        self.assertEqual(response.status_code, 200)

    def test_acceso_denegado_recepcionista(self):
        """El recepcionista NO debe ver la lista de platos (Redirección al dashboard)"""
        self.client.force_login(self.user_recepcion)
        response = self.client.get(reverse('comedor:plato_lista'))
        
        # Debe redirigir (302) al dashboard porque no tiene permiso
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('hostal:dashboard'))