from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from atencion.models import Movimiento


# Create your views here.
@login_required
def movimientos_listar(request):
    movimientos = Movimiento.objects.all()
    return render(request, 'movimientos/movimientos_listar.html', {'movimientos': movimientos})

