from django.urls import path
from . import views

# ¡IMPORTANTE! Esto nos permite usar 'comedor:plato_lista'
app_name = 'comedor' 

urlpatterns = [
    # URLs de Platos
    path('platos/', views.PlatoListView.as_view(), name='plato_lista'),
    path('platos/crear/', views.PlatoCreateView.as_view(), name='plato_crear'),
    path('platos/<int:pk>/editar/', views.PlatoUpdateView.as_view(), name='plato_editar'),
    path('platos/<int:pk>/eliminar/', views.PlatoDeleteView.as_view(), name='plato_eliminar'),
    
    # URLs de Minutas
    path('minutas/', views.MinutaDiaListView.as_view(), name='minuta_lista'),
    path('minutas/crear/', views.MinutaDiaCreateView.as_view(), name='minuta_crear'),
    path('minutas/<int:pk>/editar/', views.MinutaDiaUpdateView.as_view(), name='minuta_editar'),
    path('minutas/<int:pk>/eliminar/', views.MinutaDiaDeleteView.as_view(), name='minuta_eliminar'),
]