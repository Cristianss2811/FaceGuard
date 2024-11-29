from django.shortcuts import render, redirect, get_object_or_404
from .models import Roles, Profile, User, ProfileRole
from .forms import RolesForm, ProfileForm
from django.contrib.auth.decorators import login_required

# Views Roles
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

"""
VIEWS Profile (usuarios)
"""

@login_required
def profile_listar(request):
    perfiles = Profile.objects.all()
    for perfil in perfiles:
        perfil.roles = perfil.profilerole_set.all()
    return render(request, 'usuarios/usuarios_listar.html', {'usuarios': perfiles})

"""
@login_required
def profile_crear(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST)
        if form.is_valid():
            perfil = form.save(commit=False)
            perfil.user = request.user
            perfil.save()
            return redirect(profile_listar)
    else:
        form = ProfileForm()
    return render(request, 'usuarios/usuarios_crear.html', {'form': form})
"""

@login_required
def profile_editar(request, id):
    perfil = get_object_or_404(Profile, user_id=id)
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=perfil)
        if form.is_valid():
            form.save()
            return redirect(profile_listar)
    else:
        form = ProfileForm(instance=perfil)
    return render(request, 'usuarios/usuarios_editar.html', {'form': form, 'perfil': perfil})


@login_required
def usuarios_asignar_roles(request, id):
    perfil = get_object_or_404(Profile, user_id=id)
    roles = Roles.objects.all()  # Obtener todos los roles disponibles

    if request.method == 'POST':
        # Procesar los roles seleccionados por el usuario
        selected_roles = request.POST.getlist('roles')
        fecha_vencimiento = request.POST.get('fecha_vencimiento')

        # Si la fecha está vacía, asignar None
        if not fecha_vencimiento:
            fecha_vencimiento = None

        for role_id in selected_roles:
            role = get_object_or_404(Roles, id=role_id)
            ProfileRole.objects.create(profile=perfil, role=role, fecha_vencimiento=fecha_vencimiento)
        return redirect('usuarios_listar')  # Redirige a la lista de usuarios

    return render(request, 'usuarios/usuarios_asignar_roles.html', {'perfil': perfil, 'roles': roles})


@login_required
def eliminar_roles_usuario(request, usuario_id):
    usuario = get_object_or_404(Profile, user_id=usuario_id)

    if request.method == 'POST':
        # Obtener los IDs de los roles seleccionados
        roles_a_eliminar = request.POST.getlist('roles')

        if roles_a_eliminar:
            # Eliminar los roles seleccionados
            ProfileRole.objects.filter(id__in=roles_a_eliminar, profile=usuario).delete()

        return redirect(profile_listar)  # Redirigir después de eliminar

    # Para el GET, mostrar los roles actuales del usuario
    roles_asignados = ProfileRole.objects.filter(profile=usuario)

    return render(request, 'usuarios/eliminar_roles_usuario.html', {
        'usuario': usuario,
        'roles_asignados': roles_asignados
    })

@login_required
def profile_completar(request, id):
    perfil = get_object_or_404(User, id=id)
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=perfil)
        if form.is_valid():
            form.save()
            return redirect(profile_listar)
    else:
        form = ProfileForm(instance=perfil)
    return render(request, 'usuarios/usuarios_completar.html', {'form': form, 'perfil': perfil})

@login_required
def profile_eliminar(request, id):
    perfil = get_object_or_404(User, id=id)
    if request.method == 'POST':
        perfil.delete()
        return redirect(profile_listar)
    return render(request, 'usuarios/usuarios_eliminar.html', {'usuarios': perfil})