"""
URL configuration for hostalDonaClarita project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from hostal import views

urlpatterns = [
    # Rutas de inicio de sesión

    #Dashboard
    path('', views.dashboard_view, name='dashboard'),
    # Rutas de administración
    path("administracion/", admin.site.urls),
    # URLs de Habitacion
    path('habitaciones/', views.HabitacionListView.as_view(), name='habitacion_lista'),
    path('habitaciones/crear/', views.HabitacionCreateView.as_view(), name='habitacion_crear'),
    path('habitaciones/<int:pk>/editar/', views.HabitacionUpdateView.as_view(), name='habitacion_editar'),
    path('habitaciones/<int:pk>/eliminar/', views.HabitacionDeleteView.as_view(), name='habitacion_eliminar'),
    
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
]
