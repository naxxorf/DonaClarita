app_name = 'administracion'
from django.contrib import admin
from django.urls import path
from . import views
urlpatterns = [
    path('admin/', admin.site.urls),
    # Proveedores
    path('proveedores/', views.ProveedorListView.as_view(), name='proveedor_lista'),
    path('proveedores/crear/', views.ProveedorCreateView.as_view(), name='proveedor_crear'),
    path('proveedores/<int:pk>/editar/', views.ProveedorUpdateView.as_view(), name='proveedor_editar'),
    path('proveedores/<int:pk>/eliminar/', views.ProveedorDeleteView.as_view(), name='proveedor_eliminar'),

    # Pedidos
    path('pedidos/', views.OrdenPedidoListView.as_view(), name='pedido_lista'),
    path('pedidos/crear/', views.OrdenPedidoCreateView.as_view(), name='pedido_crear'),
]