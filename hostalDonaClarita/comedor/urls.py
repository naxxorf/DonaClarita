app_name = 'comedor'

from django.urls import path
from . import views
urlpatterns = [
    path('platos/', views.PlatoListView.as_view(), name='plato_lista'),
    path('platos/crear/', views.PlatoCreateView.as_view(), name='plato_crear'),
    path('platos/<int:pk>/editar/', views.PlatoUpdateView.as_view(), name='plato_editar'),
    path('platos/<int:pk>/eliminar/', views.PlatoDeleteView.as_view(), name='plato_eliminar'),
]