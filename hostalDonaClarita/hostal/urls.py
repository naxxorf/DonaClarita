from django.urls import path
from . import views

app_name = 'hostal' 

urlpatterns = [
    path('', views.dashboard_view, name='dashboard'), # Esta es la página de inicio
    path('ordenes/', views.OrdenDeCompraListView.as_view(), name='orden_lista'),
    path('ordenes/crear/', views.OrdenDeCompraCreateView.as_view(), name='orden_crear'),
    path('habitaciones/', views.HabitacionListView.as_view(), name='habitacion_lista'),
    path('habitaciones/crear/', views.HabitacionCreateView.as_view(), name='habitacion_crear'),
    path('habitaciones/<int:pk>/editar/', views.HabitacionUpdateView.as_view(), name='habitacion_editar'),
    path('habitaciones/<int:pk>/eliminar/', views.HabitacionDeleteView.as_view(), name='habitacion_eliminar'),
    path('clientes/', views.ClienteListView.as_view(), name='cliente_lista'),
    path('clientes/crear/', views.ClienteCreateView.as_view(), name='cliente_crear'),
    path('clientes/<int:pk>/editar/', views.ClienteUpdateView.as_view(), name='cliente_editar'),
    path('clientes/<int:pk>/eliminar/', views.ClienteDeleteView.as_view(), name='cliente_eliminar'),
    path('huespedes/', views.HuespedListView.as_view(), name='huesped_lista'),
    path('huespedes/crear/', views.HuespedCreateView.as_view(), name='huesped_crear'),
    path('huespedes/<int:pk>/editar/', views.HuespedUpdateView.as_view(), name='huesped_editar'),
    path('huespedes/<int:pk>/eliminar/', views.HuespedDeleteView.as_view(), name='huesped_eliminar'),
]