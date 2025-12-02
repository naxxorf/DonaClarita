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
        
# ==========================================
# PRUEBA DE VISTA: Dashboard (Lógica y Contexto)
# ==========================================
class DashboardViewTest(TestCase):
    def setUp(self):
        # Usuario y Cliente
        self.user = User.objects.create_user(username='recep_dash', password='123')
        # Asignamos rol de recepción para que entre al dashboard logueado
        # Nota: Dependiendo de tu mixin, quizas baste con estar logueado, 
        # pero es mejor ser explícito si usas perfiles.
        
        # Creamos habitaciones para probar la matemática
        # 2 Ocupadas, 1 Disponible = 3 Totales. Ocupación esperada: 66%
        Habitacion.objects.create(numero="101", estado='O', precio=100, capacidad=1) # Ocupada
        Habitacion.objects.create(numero="102", estado='A', precio=100, capacidad=1) # Asignada (cuenta como ocupada)
        Habitacion.objects.create(numero="103", estado='D', precio=100, capacidad=1) # Disponible

    def test_dashboard_contexto_logueado(self):
        """
        Prueba que el dashboard calcule bien el porcentaje de ocupación
        y entregue las variables correctas al template.
        """
        self.client.force_login(self.user)
        response = self.client.get(reverse('hostal:dashboard'))
        
        self.assertEqual(response.status_code, 200)
        
        # Verificamos los cálculos matemáticos que hace tu vista
        contexto = response.context
        
        # 2 ocupadas de 3 totales = 66.666... -> int(66.66) -> 66
        # Nota: Ajusta esto según cómo redondees en tu vista (int o float)
        self.assertEqual(contexto['total_habitaciones'], 3)
        
        # Verificamos que 'porcentaje_ocupacion' sea un número razonable (aprox 66)
        # Usamos assertAlmostEqual por si hay decimales
        self.assertAlmostEqual(contexto['porcentaje_ocupacion'], 66.6, delta=1.0)
        
        # Verificamos el conteo por estado
        conteo = contexto['conteo_estados']
        self.assertEqual(conteo['O']['total'], 1) # 1 Ocupada
        self.assertEqual(conteo['A']['total'], 1) # 1 Asignada
        self.assertEqual(conteo['D']['total'], 1) # 1 Disponible

    def test_dashboard_anonimo(self):
        """
        Prueba que el usuario anónimo vea la versión pública (public_home)
        y NO vea los datos de gestión interna.
        """
        response = self.client.get(reverse('hostal:dashboard'))
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'hostal/public_home.html')
        
        # El contexto NO debe tener datos sensibles
        self.assertNotIn('porcentaje_ocupacion', response.context)
        self.assertNotIn('habitaciones_lista', response.context)
        
# ==========================================
# PRUEBA DE VISTAS: CRUD de Clientes (Empresas)
# ==========================================
class ClienteCRUDViewTest(TestCase):
    def setUp(self):
        # Usuario Recepcionista
        self.user = User.objects.create_user(username='recep_cliente', password='123')
        # Si usas perfiles, aquí deberías asignar el rol, pero el mixin de prueba
        # a veces pasa si es superuser. Para ser estricto:
        self.user.is_superuser = True 
        self.user.save()
        
        # Cliente base para editar/borrar
        self.cliente = Cliente.objects.create(
            user=self.user,
            razon_social="Empresa Base",
            rut="55555555-5"
        )

    def test_crear_cliente_view(self):
        """Prueba la vista de creación de clientes (POST)"""
        self.client.force_login(self.user)
        
        # Necesitamos un usuario NUEVO para el nuevo cliente (relación 1 a 1)
        otro_user = User.objects.create_user(username='nuevo_cliente_user', password='123')
        
        data = {
            'user': otro_user.id,
            'razon_social': 'Nueva Empresa SPA',
            'rut': '66666666-6'
        }
        
        url = reverse('hostal:cliente_crear')
        response = self.client.post(url, data)
        
        # Debería redirigir a la lista tras éxito
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Cliente.objects.count(), 2)

    def test_editar_cliente_view(self):
        """Prueba la vista de edición (POST)"""
        self.client.force_login(self.user)
        
        url = reverse('hostal:cliente_editar', args=[self.cliente.pk])
        
        # Cambiamos la razón social
        data = {
            'user': self.user.id,
            'razon_social': 'Empresa Editada',
            'rut': '55555555-5' # Mismo rut
        }
        
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
        
        self.cliente.refresh_from_db()
        self.assertEqual(self.cliente.razon_social, 'Empresa Editada')
        
# ==========================================
# PRUEBA DE VISTAS: Órdenes de Compra
# ==========================================
class OrdenCompraViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_superuser(username='recep_oc', password='123')
        self.cliente = Cliente.objects.create(user=self.user, razon_social="Cliente OC", rut="77777777-7")

    def test_crear_orden_view(self):
        """Prueba que se pueda cargar una Orden de Compra desde la vista"""
        self.client.force_login(self.user)
        
        url = reverse('hostal:orden_crear')
        data = {
            'cliente': self.cliente.id,
            'codigo_orden': 'OC-2025-001',
            # 'lista_huespedes_excel': (Opcional, se puede omitir para prueba simple)
        }
        
        response = self.client.post(url, data)
        
        # Redirección exitosa
        self.assertEqual(response.status_code, 302)
        self.assertTrue(OrdenDeCompra.objects.filter(codigo_orden='OC-2025-001').exists())

    def test_listar_ordenes(self):
        """Prueba simple de que la lista carga"""
        self.client.force_login(self.user)
        OrdenDeCompra.objects.create(cliente=self.cliente, codigo_orden="OC-TEST-LIST")
        
        response = self.client.get(reverse('hostal:orden_lista'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "OC-TEST-LIST")
        
# ==========================================
# PRUEBA FINAL: Cobertura Total de Vistas (Habitación y Huésped)
# ==========================================
class CoberturaTotalViewsTest(TestCase):
    def setUp(self):
        # Usuario con permisos
        self.user = User.objects.create_superuser(username='super_tester', password='123')
        self.client.force_login(self.user)
        
        # Datos base
        self.habitacion = Habitacion.objects.create(numero="999", precio=1000, estado='D')
        self.cliente_empresa = Cliente.objects.create(user=self.user, razon_social="Empresa X", rut="11111111-1")
        self.huesped = Huesped.objects.create(
            empresa=self.cliente_empresa, 
            rut="22222222-2", 
            nombre_completo="Juanito", 
            habitacion=self.habitacion
        )

    # --- HABITACIONES (Faltaba probar Create/Update/Delete) ---

    def test_habitacion_create_get(self):
        """Prueba que la página de crear habitación cargue con su contexto correcto"""
        resp = self.client.get(reverse('hostal:habitacion_crear'))
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.context['titulo'], "Crear Nueva Habitación")

    def test_habitacion_update_get(self):
        """Prueba que la página de editar habitación cargue"""
        resp = self.client.get(reverse('hostal:habitacion_editar', args=[self.habitacion.pk]))
        self.assertEqual(resp.status_code, 200)
        # Verifica que el título dinámico (con el número) se genere bien
        self.assertIn(f"Editar Habitación: {self.habitacion.numero}", resp.context['titulo'])

    def test_habitacion_delete(self):
        """Prueba la vista de confirmación (GET) y la eliminación real (POST)"""
        # 1. GET: Ver la página de confirmación
        resp_get = self.client.get(reverse('hostal:habitacion_eliminar', args=[self.habitacion.pk]))
        self.assertEqual(resp_get.status_code, 200)
        self.assertIn("Eliminar Habitación:", resp_get.context['titulo'])
        
        # 2. POST: Eliminarla
        resp_post = self.client.post(reverse('hostal:habitacion_eliminar', args=[self.habitacion.pk]))
        self.assertEqual(resp_post.status_code, 302) # Redirección
        self.assertFalse(Habitacion.objects.filter(pk=self.habitacion.pk).exists())

    # --- HUÉSPEDES (Faltaba probar Create/Update/Delete) ---

    def test_huesped_create_get(self):
        """Visitar formulario de crear huésped"""
        resp = self.client.get(reverse('hostal:huesped_crear'))
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.context['titulo'], "Registrar Check-in de Huésped")

    def test_huesped_update_get(self):
        """Visitar formulario de editar huésped"""
        resp = self.client.get(reverse('hostal:huesped_editar', args=[self.huesped.pk]))
        self.assertEqual(resp.status_code, 200)
        self.assertIn(f"Editar Huésped: {self.huesped.nombre_completo}", resp.context['titulo'])

    def test_huesped_delete(self):
        """Borrar un huésped"""
        # GET
        resp_get = self.client.get(reverse('hostal:huesped_eliminar', args=[self.huesped.pk]))
        self.assertEqual(resp_get.status_code, 200)
        
        # POST
        resp_post = self.client.post(reverse('hostal:huesped_eliminar', args=[self.huesped.pk]))
        self.assertEqual(resp_post.status_code, 302)
        self.assertFalse(Huesped.objects.filter(pk=self.huesped.pk).exists())

    # --- CLIENTES (Faltaba probar Delete) ---
    
    def test_cliente_delete(self):
        """Borrar un cliente"""
        # Creamos uno extra para borrar
        cliente_borrar = Cliente.objects.create(
            user=User.objects.create_user('borrar', 'b@b.cl', '123'), 
            razon_social="Borrar SPA", 
            rut="33333333-3"
        )
        
        # GET (Confirmación)
        resp_get = self.client.get(reverse('hostal:cliente_eliminar', args=[cliente_borrar.pk]))
        self.assertEqual(resp_get.status_code, 200)
        self.assertIn("Eliminar Cliente:", resp_get.context['titulo'])

        # POST (Acción)
        resp_post = self.client.post(reverse('hostal:cliente_eliminar', args=[cliente_borrar.pk]))
        self.assertEqual(resp_post.status_code, 302)
        self.assertFalse(Cliente.objects.filter(pk=cliente_borrar.pk).exists())