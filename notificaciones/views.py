from django.shortcuts import render, get_object_or_404, redirect

# Create your views here.
from django.http import JsonResponse
from .models import Notificacion
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt


@login_required
def listar_notificaciones(request):
    notificaciones = request.user.notificaciones.all()
    notificaciones_no_leidas = notificaciones.filter(leida=False).count()
    return render(request, 'base.html', {
        'notificaciones': notificaciones,
        'notificaciones_no_leidas': notificaciones_no_leidas
    })

@login_required
def leer_notificacion(request, notificacion_id):
    notificacion = get_object_or_404(Notificacion, id=notificacion_id, usuario=request.user)
    notificacion.leida = True
    notificacion.save()
    return redirect('listar_notificaciones')

@login_required
def contar_notificaciones(request):
    """Devuelve el conteo de notificaciones no leídas para el usuario autenticado."""
    notificaciones_no_leidas = request.user.notificaciones.filter(leida=False).count()
    return JsonResponse({'count': notificaciones_no_leidas})