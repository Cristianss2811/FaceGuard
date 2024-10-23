from django.shortcuts import render, redirect, get_object_or_404
from .models import Area, Puerta
from .forms import AreaForm, PuertaForm
from django.contrib.auth.decorators import login_required

# Create your views here.

#Views Areas ------------------------------------------------------------------------
@login_required
def areas_listar(request):
    areas = Area.objects.all()
    return render(request, 'areas/areas_listar.html', {'areas': areas})

@login_required
def areas_crear(request):
    if request.method == 'POST':
        form = AreaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(areas_listar)
    else:
        form = AreaForm()
    return render(request, 'areas/areas_crear.html', {'form': form})

@login_required
def areas_editar(request, id):
    area = get_object_or_404(Area, id=id)
    if request.method == 'POST':
        form = AreaForm(request.POST, instance=area)
        if form.is_valid():
            form.save()
            return redirect('areas_listar')
    else:
        form = AreaForm(instance=area)
    return render(request, 'areas/areas_editar.html', {'form': form, 'area': area})

@login_required
def areas_eliminar(request, id):
    area = get_object_or_404(Area, pk=id)
    if request.method == 'POST':
        area.delete()
        return redirect(areas_listar)
    return render(request, 'areas/areas_eliminar.html', {'area': area})


#-------------------------------------------------------------------------------------------------


# Views Puertas -----------------------------------------------------------------------------------
@login_required
def puertas_listar(request):
    puertas = Puerta.objects.all()
    return render(request, 'puertas/puertas_listar.html', {'puertas': puertas})

@login_required
def puertas_crear(request):
    if request.method == 'POST':
        form = PuertaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(puertas_listar)
    else:
        form = PuertaForm()
    return render(request, 'puertas/puertas_crear.html', {'form': form})

@login_required
def puertas_editar(request, id):
    puerta = get_object_or_404(Puerta, id=id)
    if request.method == 'POST':
        form = PuertaForm(request.POST, instance=puerta)
        if form.is_valid():
            form.save()
            return redirect('puertas_listar')
    else:
        form = PuertaForm(instance=puerta)
    return render(request, 'puertas/puertas_editar.html', {'form': form, 'puerta': puerta})

@login_required
def puertas_eliminar(request, id):
    puerta = get_object_or_404(Puerta, pk=id)
    if request.method == 'POST':
        puerta.delete()
        return redirect(puertas_listar)
    return render(request, 'puertas/puertas_eliminar.html', {'puerta': puerta})