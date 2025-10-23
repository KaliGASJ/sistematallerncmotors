from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # Ruta para la vista 'home' que creamos en views.py
    # Esta será nuestra página de inicio después de loguearse
    path('', views.home, name='home'),
    
    # Ruta para el Login
    # Usamos la vista LoginView de Django
    # Le decimos que use nuestra plantilla 'login.html'
    # El name='login' coincide con el LOGIN_URL en settings.py
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    
    # Ruta para el Logout
    # Usamos LogoutView de Django. 
    # El name='logout' coincide con el {% url 'logout' %} en base.html
    # Por defecto, redirige a LOGOUT_REDIRECT_URL (que es 'login')
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]