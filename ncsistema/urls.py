from django.contrib import admin
from django.urls import path, include  # <-- IMPORTAR include

urlpatterns = [
    path('admin/', admin.site.urls),
    # Añadimos las URLs de la app 'login' a la raíz del proyecto
    path('', include('login.urls')), 
]