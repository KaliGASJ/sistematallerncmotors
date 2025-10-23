from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Protegemos esta vista para que solo usuarios logueados puedan acceder
@login_required
def home(request):
    """
    Vista para la página de inicio que se muestra después del login.
    """
    # Simplemente renderiza la plantilla 'home.html'
    return render(request, 'home.html')