from django.test import TestCase
from django.contrib.auth.models import User
from .models import Empleado
from .forms import EmpleadoRegistroForm, EmpleadoEditarForm

class EmpleadoFormTest(TestCase):

    def test_registro_empleado_crea_usuario(self):
        """
        Prueba que el formulario 'mágico' cree tanto el Empleado 
        como el Usuario de Django asociado.
        """
        data = {
            'username': 'nuevo_recep',
            'email': 'recep@hostal.cl',
            'password': 'password123',
            'first_name': 'Roberto',
            'last_name': 'Gómez',
            'rut': '15555666-7',
            'telefono': '912345678',
            'rol': 'RECEPCION'
        }
        
        form = EmpleadoRegistroForm(data=data)
        
        # 1. Validar que el form sea válido
        self.assertTrue(form.is_valid(), f"Errores: {form.errors}")
        
        # 2. Guardar (esto ejecuta tu método save() personalizado)
        empleado = form.save()
        
        # 3. Verificar que se creó el Empleado
        self.assertEqual(empleado.rut, '15555666-7')
        
        # 4. Verificar que se creó el Usuario y se vinculó
        self.assertIsNotNone(empleado.user)
        self.assertEqual(empleado.user.username, 'nuevo_recep')
        
        # 5. Verificar que la contraseña funciona (está hasheada)
        self.assertTrue(empleado.user.check_password('password123'))

    def test_edicion_empleado_actualiza_usuario(self):
        """
        Prueba que el formulario de edición actualice datos del usuario
        (nombre, email) reflejándolos en el modelo User.
        """
        # Setup: Crear un empleado existente
        user = User.objects.create_user('admin_viejo', 'a@a.cl', 'pass')
        empleado = Empleado.objects.create(user=user, rut='9999999-9', rol='ADMIN')

        data = {
            'first_name': 'Administrador', # Cambiamos nombre
            'last_name': 'Supremo',       # Cambiamos apellido
            'email': 'nuevo@admin.cl',    # Cambiamos email
            'rut': '9999999-9',           # Mismo rut
            'telefono': '123123123',
            'rol': 'ADMIN'
        }

        # Pasamos la instancia ('instance=empleado') para editar, no crear
        form = EmpleadoEditarForm(data=data, instance=empleado)
        
        self.assertTrue(form.is_valid(), f"Errores: {form.errors}")
        empleado_actualizado = form.save()

        # Verificar que los cambios pasaron al modelo User
        empleado_actualizado.user.refresh_from_db()
        self.assertEqual(empleado_actualizado.user.first_name, 'Administrador')
        self.assertEqual(empleado_actualizado.user.email, 'nuevo@admin.cl')