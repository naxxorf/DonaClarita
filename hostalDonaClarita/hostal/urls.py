from django.urls import path
from . import views

# ¡IMPORTANTE! Esto nos permite usar 'comedor:plato_lista'
app_name = 'hostal' 

urlpatterns = [
    path('habitaciones/', views.HabitacionListView.as_view(), name='habitacion_lista'),
    path('habitaciones/crear/', views.HabitacionCreateView.as_view(), name='habitacion_crear'),
    path('habitaciones/<int:pk>/editar/', views.HabitacionUpdateView.as_view(), name='habitacion_editar'),
    path('habitaciones/<int:pk>/eliminar/', views.HabitacionDeleteView.as_view(), name='habitacion_eliminar'),
   
]
    