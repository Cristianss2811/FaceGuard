from django.shortcuts import render, redirect, get_object_or_404
from .models import Roles
from .forms import RolesForm
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def roles_listar(request):
    roles = Roles.objects.all()
    return render(request, 'roles/roles_listar.html', {'roles': roles})


@login_required
def roles_crear(request):
    if request.method == 'POST':
        form = RolesForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(roles_listar)
    else:
        form = RolesForm()
    return render(request, 'roles/roles_crear.html', {'form': form})


@login_required
def roles_editar(request, id):
    rol = get_object_or_404(Roles, id=id)
    if request.method == 'POST':
        form = RolesForm(request.POST, instance=rol)
        if form.is_valid():
            form.save()  # Actualiza el rol
            return redirect(roles_listar)
    else:
        form = RolesForm(instance=rol)
    return render(request, 'roles/roles_editar.html', {'form': form, 'rol': rol})


@login_required
def roles_eliminar(request, id):
    rol = get_object_or_404(Roles, id=id)
    if request.method == 'POST':
        rol.delete()  # Elimina el rol
        return redirect(roles_listar)
    return render(request, 'roles/roles_eliminar.html', {'rol': rol})