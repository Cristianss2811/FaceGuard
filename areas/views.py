from django.shortcuts import render, redirect, get_object_or_404

from usuarios.models import Roles
from .models import Area, Puerta, Zona, PuertasRoles
from .forms import AreaForm, PuertaForm, ZonaForm
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

def puertas_asignar_roles(request, id):
    puerta = get_object_or_404(Puerta, pk=id)
    puertas_roles = PuertasRoles.objects.filter(puerta=puerta)
    roles = Roles.objects.exclude(
        id__in=puertas_roles.values_list('rol_id', flat=True)
    )

    if request.method == 'POST':
        #Procesar los roles seleccionados
        selected_roles = request.POST.getlist('roles')

        for role_id in selected_roles:
            role = get_object_or_404(Roles, pk=role_id)
            PuertasRoles.objects.create(puerta=puerta, rol=role)
        return redirect('puertas_listar')
    return render(request, 'puertas/puertas_asignar_roles.html', {'puerta': puerta, 'roles': roles})

@login_required
def eliminar_roles_puertas(request, id):
    puerta = get_object_or_404(Puerta, id=id)

    if request.method == 'POST':
        # Obtener los IDs de los roles seleccionados
        roles_a_eliminar = request.POST.getlist('roles')

        if roles_a_eliminar:
            # Eliminar los roles seleccionados
            PuertasRoles.objects.filter(id__in=roles_a_eliminar, puerta = puerta).delete()

        return redirect('puertas_listar')  # Redirigir después de eliminar

    # Para el GET, mostrar los roles actuales del usuario
    roles_asignados = PuertasRoles.objects.filter(puerta = puerta)

    return render(request, 'puertas/eliminar_roles_puertas.html', {
        'puerta': puerta,
        'roles_asignados': roles_asignados
    })
#-------------------------------------------------------------------------------------------------


#Views Zonas ------------------------------------------------------------------------
@login_required
def zonas_listar(request):
    zonas = Zona.objects.all()
    return render(request, 'zonas/zonas_listar.html', {'zonas': zonas})

@login_required
def zonas_crear(request):
    if request.method == 'POST':
        form = ZonaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(zonas_listar)
    else:
        form = ZonaForm()
    return render(request, 'zonas/zonas_crear.html', {'form': form})

@login_required
def zonas_editar(request, id):
    zona = get_object_or_404(Zona, id=id)
    if request.method == 'POST':
        form = ZonaForm(request.POST, instance=zona)
        if form.is_valid():
            form.save()
            return redirect('zonas_listar')
    else:
        form = ZonaForm(instance=zona)
    return render(request, 'zonas/zonas_editar.html', {'form': form, 'zona': zona})

@login_required
def zonas_eliminar(request, id):
    zona = get_object_or_404(Zona, pk=id)
    if request.method == 'POST':
        zona.delete()
        return redirect(zonas_listar)
    return render(request, 'zonas/zonas_eliminar.html', {'zona': zona})


#-------------------------------------------------------------------------------------------------
