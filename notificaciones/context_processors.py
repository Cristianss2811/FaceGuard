from .models import Notificacion

def notificaciones(request):
    if request.user.is_authenticated:
        notificaciones = request.user.notificaciones.all()
        notificaciones_no_leidas = notificaciones.filter(leida=False).count()
        return {'notificaciones': notificaciones, 'notificaciones_no_leidas': notificaciones_no_leidas}
    return {'notificaciones': [], 'notificaciones_no_leidas': 0}