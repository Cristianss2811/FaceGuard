from datetime import datetime

import requests
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from tensorflow.python.ops.logging_ops import Print

from areas.views import puertas_listar
from atencion.models import Movimiento, MovimientoUsuario, MovimientoPuerta
from .models import Roles, Profile, User, ProfileRole
from areas.models import Puerta, PuertasRoles
from .forms import RolesForm, ProfileForm
from django.contrib.auth.decorators import login_required
from notificaciones.models import Notificacion

from .utils.registro_facial import consultar_imagen_usuario, login_captura_facial


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
    perf = Profile.objects.filter(user=request.user).first()
    for perfil in perfiles:
        perfil.roles = perfil.profilerole_set.all()
    if perf:
        perf.roles = list(perf.profilerole_set.all())
    else:
        perf = None
    return render(request, 'usuarios/usuarios_listar.html', {'usuarios': perfiles, "usuari": perf})

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
    roles_asignados = ProfileRole.objects.filter(profile=perfil).values_list('role', flat=True)
    roles = Roles.objects.exclude(id__in=roles_asignados)

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
    from tasks.views import tasks
    perfil = get_object_or_404(Profile, user_id=id)
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=perfil)
        if form.is_valid():
            form.save()
            return redirect(tasks)
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

def notificar_a_staff(mensaje):
    staff_users = User.objects.filter(is_staff=True)
    for staff_user in staff_users:
        Notificacion.objects.create(
            usuario=staff_user,
            mensaje=mensaje,
            leida=False,
        )

def registrar_movimiento(tipo, usuario, puerta):
    """
    Registra un movimiento en las tablas Movimiento, MovimientoUsuario y MovimientoPuerta.

    :param tipo: Tipo de movimiento ("acceso" o "acceso denegado").
    :param usuario: Instancia del usuario relacionado con el movimiento.
    :param puerta: Instancia de la puerta relacionada con el movimiento.
    """
    # Crear el registro en la tabla principal Movimiento
    movimiento = Movimiento.objects.create(
        tipo=tipo,
        hora=datetime.now().time(),
        fecha=datetime.now().date(),
    )

    # Crear los registros en las tablas intermedias
    MovimientoUsuario.objects.create(movimiento=movimiento, usuario=usuario.user)
    MovimientoPuerta.objects.create(movimiento=movimiento, puerta=puerta)

def verificar_acceso(request, puerta_id):
    # Obtener la puerta
    puerta = get_object_or_404(Puerta, id=puerta_id)

    # Obtener el perfil del usuario actual
    perfil = request.user.profile

    # Obtener los roles del perfil del usuario
    roles_usuario = ProfileRole.objects.filter(profile=perfil).values_list('role', flat=True)

    # Obtener los roles asignados a la puerta
    roles_puerta = PuertasRoles.objects.filter(puerta=puerta).values_list('rol', flat=True)

    # Determinar si hay intersección entre los roles del usuario y los roles de la puerta
    acceso = any(rol in roles_puerta for rol in roles_usuario)

    context = {
        'puerta': puerta,
        'acceso': acceso
    }
    return render(request, 'usuarios/verificar_acceso.html', context)

@login_required
def verificar_rostro_acceso(request, puerta_id):
    print("Metodo de verificar")

    # Obtener los datos de la imagen enviados desde el formulario
    photo_data = request.POST.get("photo")

    if not photo_data:
        print("No se encontró foto en el formulario")
        messages.error(request, "No se encontró foto en el formulario.")
        return redirect(puertas_listar)

    profile = request.user.profile
    puerta = get_object_or_404(Puerta, id=puerta_id)
    perfil = request.user.profile

    if not profile or not profile.imagen_id:
        print("Perfil de usuario inválido o sin imagen registrada")
        messages.error(request, "Perfil de usuario inválido o sin imagen registrada.")
        return redirect(puertas_listar)

    # Consultar la imagen del usuario registrada
    img_profile = profile.imagen_id
    user_face = consultar_imagen_usuario(imagen_id=img_profile)

    if user_face is False:
        print("El usuario no tiene rostro registrado")
        messages.error(request, "El usuario no tiene rostro registrado.")
        return redirect(puertas_listar)

    if user_face is None:
        print("Error al recuperar la imagen del perfil")
        messages.error(request, "Error al recuperar la imagen del perfil.")
        return redirect(puertas_listar)

    # Comparar el rostro registrado con el rostro capturado
    resultado = login_captura_facial(user_face, photo_data)

    if resultado is True:
        # Obtener los roles del perfil del usuario
        roles_usuario = ProfileRole.objects.filter(profile=profile).values_list('role', flat=True)

        # Obtener los roles asignados a la puerta
        roles_puerta = PuertasRoles.objects.filter(puerta=puerta).values_list('rol', flat=True)

        # Determinar si hay intersección entre los roles del usuario y los roles de la puerta
        acceso = any(rol in roles_puerta for rol in roles_usuario)

        if acceso:
            print("acceso es true")
            print(f"Registrar movimiento correcto | perfil {perfil}, puerta {puerta}")
            registrar_movimiento("Acceso", profile, puerta)
            print("Notificacion a staff")
            mensaje = ("Acceso concedido\n"
                       f"Usuario: {perfil.user}\n")
            notificar_a_staff(mensaje)
            print("Notificacion a staff correctamente")
        else:
            print("acceso es false")
            print(f"Registrar movimiento false | perfil {perfil.user_id}, puerta {puerta.pk}")
            registrar_movimiento("Acceso denegado", profile, puerta)
            print("movimiento registrado correctamente")
            print("Notificacion a staff")
            mensaje = ("Acceso denegado\n"
                       f"Usuario: {perfil.user}\n")
            notificar_a_staff(mensaje)
            print("Notificacion a staff correctamente")

        context = {
            'puerta': puerta,
            'acceso': acceso
        }
        return render(request, 'usuarios/verificar_acceso.html', context)

    elif resultado is False:
        print("Rostros no coinciden")
        messages.error(request, "No coinciden lo suficiente los rostros.")
        return redirect(puertas_listar)
    elif resultado == -100:
        print("Error al decodificar la imagen")
        messages.error(request, "Error al decodificar la imagen.")
        return redirect(puertas_listar)
    elif resultado == -200:
        print("No se detectaron rostros en la imagen")
        messages.error(request, "No se detectaron rostros en la imagen.")
        return redirect(puertas_listar)
    else:
        print("Error desconocido al procesar la imagen")
        messages.error(request, "Error desconocido al procesar la imagen.")
        return redirect(puertas_listar)

    """
    try:
        # Obtener foto | Necesaria para API
        photo = request.POST["photo"]

        # Obtener perfil y puerta
        profile = request.user
        perfil = request.user.profile
        puerta = get_object_or_404(Puerta, id=puerta_id)

        # Obtener nombre de usuario | Necesario para API
        usuario = profile.username

        print("Antes de realizar la solicitud"
              f"Usuario: {usuario}"
              f"Foto: {photo}")
        # Realizar la solicitud asincrónica a la API
        response = requests.post(
            "https://microservicio-fr.onrender.com/login/",
            data={"usuario": usuario, "photo": photo},
        )

        response.raise_for_status()

        api_response = response.json()

        if not api_response.get("success"):
            error_message = api_response.get("error") or api_response.get("detail", "Error")
            messages.error(request, error_message)
            print("redireccion en api not success")
            return redirect(puertas_listar)


        if api_response.get("success"):
            print("success True")
            roles_usuario = ProfileRole.objects.filter(profile=perfil).values_list('role', flat=True)
            print(f"Roles del usuario: {perfil}: {roles_usuario}")
            roles_puerta = PuertasRoles.objects.filter(puerta=puerta).values_list('rol', flat=True)
            print(f"Roles de la puerta: {puerta}: {roles_puerta}")
            acceso = any(rol in roles_puerta for rol in roles_usuario)
            print(f"resultado de acceso: {acceso}")
            if acceso:
                print("acceso es true")
                print(f"Registrar movimiento correcto | perfil {perfil}, puerta {puerta}")
                registrar_movimiento("Acceso", profile, puerta)
                print("Notificacion a staff")
                mensaje = ("Acceso concedido\n"
                           f"Usuario: {perfil.user}\n")
                notificar_a_staff(mensaje)
                print("Notificacion a staff correctamente")
            else:
                print("acceso es false")
                print(f"Registrar movimiento false | perfil {perfil.user_id}, puerta {puerta.pk}")
                registrar_movimiento("Acceso denegado", profile, puerta)
                print("movimiento registrado correctamente")
                print("Notificacion a staff")
                mensaje = ("Acceso denegado\n"
                           f"Usuario: {perfil.user}\n")
                notificar_a_staff(mensaje)
                print("Notificacion a staff correctamente")
            context = {
                'puerta': puerta,
                'acceso': acceso
            }
            return render(request, 'usuarios/verificar_acceso.html', context)
        else:
            print("success False")
            messages.error(request, "Acceso denegado")
            print("redireccion en Acceso denegado")
            return redirect(puertas_listar)

    except requests.exceptions.RequestException as e:
        messages.error(request, f"Error al comunicarse con la API: {str(e)}")
        print("redireccion en RequestException", str(e))
        return redirect(puertas_listar)

    except Exception as e:
        messages.error(request, f"Error inesperado: {str(e)}")
        print("redireccion en Exception")
        return redirect(puertas_listar)
    """