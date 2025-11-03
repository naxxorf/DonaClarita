
from django.contrib import admin
from django.urls import path, include
from hostal import views

urlpatterns = [
    # Rutas de inicio de sesión

    #Dashboard
    path('', views.dashboard_view, name='dashboard'),
    # Rutas de administración
    path('administracion/', include('administracion.urls', namespace='administracion')),
    # URLs de Habitacion
    path('hostal/', include('hostal.urls', namespace='hostal')),
    
    # URLs de Cliente
    path('clientes/', views.ClienteListView.as_view(), name='cliente_lista'),
    path('clientes/crear/', views.ClienteCreateView.as_view(), name='cliente_crear'),
    path('clientes/<int:pk>/editar/', views.ClienteUpdateView.as_view(), name='cliente_editar'),
    path('clientes/<int:pk>/eliminar/', views.ClienteDeleteView.as_view(), name='cliente_eliminar'),
    
    # URLs de Huesped
    path('huespedes/', views.HuespedListView.as_view(), name='huesped_lista'),
    path('huespedes/crear/', views.HuespedCreateView.as_view(), name='huesped_crear'),
    path('huespedes/<int:pk>/editar/', views.HuespedUpdateView.as_view(), name='huesped_editar'),
    path('huespedes/<int:pk>/eliminar/', views.HuespedDeleteView.as_view(), name='huesped_eliminar'),

    # URLs de Orden de Compra
    path('ordenes/', views.OrdenDeCompraListView.as_view(), name='orden_lista'),
    path('ordenes/crear/', views.OrdenDeCompraCreateView.as_view(), name='orden_crear'),

    # URLs de la app comedor
    path('comedor/', include('comedor.urls', namespace='comedor')),
    # URLs de Autenticación (Login y Logout)

    path('accounts/', include('django.contrib.auth.urls')),
]
