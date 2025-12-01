from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Habitacion
from .forms import HuespedForm
from .models import Cliente, Habitacion, OrdenDeCompra, Huesped

# ==========================================
# PRUEBA DE MODELO: Habitacion
# ==========================================
class HabitacionModelTest(TestCase):
    
    def setUp(self):
        # Creamos una habitación de prueba antes de cada test
        self.habitacion = Habitacion.objects.create(
            numero="101",
            tipo_cama="Matrimonial",
            precio=50000,
            capacidad=2,
            estado='D' # Disponible
        )

    def test_creacion_habitacion(self):
        """Prueba que la habitación se guarda con los datos correctos"""
        h = Habitacion.objects.get(numero="101")
        self.assertEqual(h.tipo_cama, "Matrimonial")
        self.assertEqual(h.precio, 50000)
        # Verificamos que el default de 'bloqueada_ingreso' sea False (según tu modelo)
        self.assertFalse(h.bloqueada_ingreso)

    def test_str_habitacion(self):
        """Prueba que el método __str__ funciona como definiste: 'Habitación 101 (Disponible)'"""
        # Tu modelo define __str__ como: f"Habitación {self.numero} ({self.get_estado_display()})"
        esperado = "Habitación 101 (Disponible)"
        self.assertEqual(str(self.habitacion), esperado)


# ==========================================
# PRUEBA DE VISTA: Listado de Habitaciones
# ==========================================
class HabitacionViewTest(TestCase):

    def setUp(self):
        # 1. Crear un Usuario (Necesario porque tus vistas usan LoginRequiredMixin)
        # Usamos create_superuser para pasar automáticamente el 'SoloRecepcionMixin'
        self.user = User.objects.create_superuser(
            username='admin_test',
            password='password123',
            email='admin@test.com'
        )
        
        # 2. Crear datos para mostrar en la lista
        Habitacion.objects.create(numero="201", precio=30000, tipo_cama="Single")
        Habitacion.objects.create(numero="202", precio=30000, tipo_cama="Single")

    def test_vista_protegida_para_anonimos(self):
        """Si NO estoy logueado, debería redirigirme al login (Status 302)"""
        url = reverse('hostal:habitacion_lista')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302) # Redirección
        self.assertIn('/accounts/login/', response.url)

    def test_vista_accesible_para_admin(self):
        """Si estoy logueado como Admin, debería ver la lista (Status 200)"""
        # Simulamos el login
        self.client.force_login(self.user)
        
        url = reverse('hostal:habitacion_lista')
        response = self.client.get(url)
        
        # Verificamos que cargó bien
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'hostal/habitacion_lista.html')
        
        # Verificamos que las habitaciones creadas aparecen en el HTML
        self.assertContains(response, "201")
        self.assertContains(response, "202")
        
# ==========================================
# PRUEBA DE FORMULARIO: HuespedForm (Lógica de Negocio)
# ==========================================
class HuespedFormTest(TestCase):

    def setUp(self):
        # 1. Necesitamos una Empresa (Cliente) y un Usuario para esa empresa
        self.user = User.objects.create_user(username='empresa_test', password='123')
        self.cliente = Cliente.objects.create(
            user=self.user, 
            razon_social="Empresa Minera SPA", 
            rut="76111222-3"
        )
        
        # 2. Una habitación DISPONIBLE y con capacidad para 2
        self.habitacion = Habitacion.objects.create(
            numero="505", 
            estado='D', 
            precio=45000, 
            capacidad=2,
            bloqueada_ingreso=False
        )

    def test_form_valido(self):
        """Caso Feliz: Debería permitir registrar si todo está bien."""
        data = {
            'empresa': self.cliente.id,
            'rut': '18111222-3',
            'nombre_completo': 'Juan Pérez',
            'habitacion': self.habitacion.id,
            # 'orden_de_compra_asociada': ... (opcional según tu modelo)
        }
        form = HuespedForm(data=data)
        self.assertTrue(form.is_valid(), f"El formulario debería ser válido. Errores: {form.errors}")

    def test_habitacion_en_mantenimiento(self):
        """Caso Triste: No debería permitir asignar habitación en Mantenimiento ('M')."""
        # Ponemos la habitación en mantención
        self.habitacion.estado = 'M'
        self.habitacion.save()

        data = {
            'empresa': self.cliente.id,
            'rut': '18111222-3',
            'nombre_completo': 'Juan Pérez',
            'habitacion': self.habitacion.id
        }
        form = HuespedForm(data=data)
        
        # Verificamos que NO sea válido
        self.assertFalse(form.is_valid())
        # Verificamos que el error sea sobre la habitación
        self.assertIn('habitacion', form.errors)
        # Opcional: Verificar el mensaje de error exacto
        self.assertIn('no está disponible', form.errors['habitacion'][0])

    def test_habitacion_bloqueada(self):
        """Caso Triste: No debería permitir entrar si tiene el candado puesto (bloqueada_ingreso=True)."""
        self.habitacion.bloqueada_ingreso = True
        self.habitacion.save()

        data = {
            'empresa': self.cliente.id,
            'rut': '19222333-K',
            'nombre_completo': 'Ana Gómez',
            'habitacion': self.habitacion.id
        }
        form = HuespedForm(data=data)
        
        self.assertFalse(form.is_valid())
        self.assertIn('bloqueada para agregar huéspedes', form.errors['habitacion'][0])
        
# ==========================================
# PRUEBA DE AUTOMATIZACIÓN: Efectos Secundarios (Signals/Save)
# ==========================================
class HuespedAutomationTest(TestCase):

    def setUp(self):
        # 1. Crear Usuario y Cliente
        self.user = User.objects.create_user(username='empresa_auto', password='123')
        self.cliente = Cliente.objects.create(user=self.user, razon_social="Auto Test SPA", rut="88888888-8")
        
        # 2. Crear Habitación DISPONIBLE
        self.habitacion = Habitacion.objects.create(
            numero="707", 
            estado='D', # Disponible
            precio=10000, 
            bloqueada_ingreso=False
        )

    def test_cambio_estado_al_ingresar(self):
        """Al crear un huésped, la habitación debe pasar automáticamente a OCUPADA ('O')"""
        
        # Estado inicial
        self.assertEqual(self.habitacion.estado, 'D')

        # Creamos el huésped (Esto dispara el método .save() personalizado)
        Huesped.objects.create(
            empresa=self.cliente,
            rut="11222333-4",
            nombre_completo="Test Automático",
            habitacion=self.habitacion
        )

        # Recargamos la habitación desde la base de datos para ver los cambios
        self.habitacion.refresh_from_db()

        # Verificamos
        self.assertEqual(self.habitacion.estado, 'O', "La habitación debería haber cambiado a Ocupada")

    def test_cambio_estado_al_salir(self):
        """Al quitar al último huésped, la habitación debe pasar a LIMPIEZA ('L')"""
        
        # 1. Llenamos la habitación primero
        huesped = Huesped.objects.create(
            empresa=self.cliente,
            rut="11222333-4",
            nombre_completo="Test Salida",
            habitacion=self.habitacion
        )
        self.habitacion.refresh_from_db()
        self.assertEqual(self.habitacion.estado, 'O') # Confirmamos que está ocupada

        # 2. Simulamos que el huésped se va (Lo movemos a None o lo borramos)
        # En tu lógica 'save', detecta cambios. Vamos a asignarle habitación None (Check-out)
        huesped.habitacion = None
        huesped.save()

        # 3. Verificamos el efecto en la habitación vieja
        self.habitacion.refresh_from_db()
        
        self.assertEqual(self.habitacion.estado, 'L', "La habitación vacía debería pasar a Limpieza ('L')")
        self.assertFalse(self.habitacion.bloqueada_ingreso, "El bloqueo de ingreso debería desactivarse")