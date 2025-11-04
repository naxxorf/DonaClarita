from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('administracion/', include('administracion.urls', namespace='administracion')),
    path('comedor/', include('comedor.urls', namespace='comedor')),
    path('', include('hostal.urls', namespace='hostal')),
]