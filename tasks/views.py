import requests
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from usuarios.utils.registro_facial import registro_facial, consultar_imagen_usuario, login_captura_facial
from usuarios.views import profile_completar
from .forms import TaskForm
from .models import Task
from notificaciones.models import Notificacion
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from usuarios.models import Profile

# Create your views here.


def home(request):
    return render(request, "home.html")


def signup(request):
    if request.method == "GET":
        return render(request, "signup.html", {"form": UserCreationForm})
    else:
        if not request.POST["username"]:
            return render(request, "signup.html", {
                "form": UserCreationForm,
                "error": "Coloca el campo username"
            })
        if not request.POST["password1"] or not request.POST["password2"]:
            return render(request, "signup.html", {
                "form": UserCreationForm,
                "error": "Coloca el password"
            })
        if request.POST["password1"] == request.POST["password2"]:
            try:
                photo_data = request.POST.get("photo")
                if not photo_data:
                    print("No se encontró foto en el formulario")
                    return render(request, "signup.html", {
                        "form": UserCreationForm,
                        "error": "No se encontró foto en el formulario"
                    })

                """
                response = requests.post(
                    "https://microservicio-fr.onrender.com/registro/",
                    data={"usuario": request.POST["username"], "photo": photo_data},
                )

                response.raise_for_status()

                api_response = response.json()

                if not api_response.get("success"):
                    return render(request, "signup.html", {
                        "form": UserCreationForm(),
                        "error": api_response.get("error"),
                    })

                img_id = api_response.get("img_id")
                """

                img_id = registro_facial(request.POST["username"], photo_data)

                if img_id is None:
                    print("No se detectaron rostros")
                    return render(request, "signup.html", {
                        "form": UserCreationForm(),
                        "error": "No se detectaron rostros"
                    })

                if img_id is False:
                    print("Error al decodificar la imagen")
                    return render(request, "signup.html", {
                        "form": UserCreationForm(),
                        "error": "Error al decodificar la imagen"
                    })

                # Registrar Usuario
                user = User.objects.create_user(
                    username=request.POST["username"],
                    password=request.POST["password1"],
                )
                user.save()

                # Crear el perfil asociado al usuario
                profile = Profile.objects.create(
                    user=user,
                    imagen_id=img_id,
                )
                profile.save()
                print("Perfil creado exitosamente")

                login(request, user)  # Creo la cookie para que el navegador sepa que hay un usuario logeado

                return redirect(profile_completar, id=profile.user_id)
            except IntegrityError:
                return render(  # Aqui retornamos a la misma vista y el mismo formulario
                    request,
                    "signup.html",  # Vista
                    {
                        "form": UserCreationForm,
                        "error": "El usuario ya existe",
                    },  # Aqui esta el formulario y tambien creamos el error
                )
            except requests.exceptions.RequestException as e:
                return render(  # Aqui retornamos a la misma vista y el mismo formulario
                    request,
                    "signup.html",  # Vista
                    {
                        "form": UserCreationForm,
                        "error": "Error de comunicación",
                    },  # Aqui esta el formulario y tambien creamos el error
                )

            except Exception as e:
                return render(  # Aqui retornamos a la misma vista y el mismo formulario
                    request,
                    "signup.html",  # Vista
                    {
                        "form": UserCreationForm,
                        "error": "Error inesperado",
                    },  # Aqui esta el formulario y tambien creamos el error
                )
        return render(
            request,
            "signup.html",
            {"form": UserCreationForm, "error": "las contraseñas no coinciden"},
        )

@login_required
def tasks(request):
    tasks = Task.objects.filter(user = request.user, datecompleted__isnull=True)
    return render(request, "tasks.html", {
        "tasks":tasks
    })

@login_required
def tasks_completed(request):
    tasks = Task.objects.filter(user = request.user, datecompleted__isnull=False).order_by('-datecompleted')
    return render(request, "tasks.html", {
        "tasks":tasks
    })

@login_required
def  create_task(request): #Renderizar la vista create_task
    if request.method == 'GET':
      return render(request, "create_task.html",{
           "form" : TaskForm
       })
    else:
        try:
            form = TaskForm(request.POST)
            new_task = form.save(commit=False)
            new_task.user = request.user
            new_task.save()
            return redirect('tasks')
        except ValueError:
            return render(request, "create_task.html", {
                "form": TaskForm,
                "error":"Ingresa datos válidos"
            })

@login_required
def task_detail(request, task_id):
    if request.method == "GET":
        task = get_object_or_404(Task, pk=task_id, user=request.user)#filtramos que solo muestre las tareas del usuario logeado
        form = TaskForm(instance=task) #Llena el formulario con la tarea
        return render(request, "task_detail.html",{
            "task":task,
            "form":form
        })
    else:
        try:
            task = get_object_or_404(Task, pk=task_id, user=request.user)
            form = TaskForm(request.POST, instance=task)
            form.save()
            return redirect("tasks")
        except ValueError:
             return render(request, "task_detail.html",{
            "task":task,
            "form":form,
            "error":"Error actualizando la tarea"
        })

@login_required
def complete_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id, user = request.user)
    if request.method == 'POST':
        task.datecompleted = timezone.now()
        task.save()
        return redirect('tasks')

@login_required
def delete_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id, user = request.user)
    if request.method == 'POST':
        task.delete()
        return redirect('tasks')

@login_required
def signout(request):
    logout(request)
    return redirect("home")

def notificar_a_staff(mensaje):
    staff_users = User.objects.filter(is_staff=True)
    for staff_user in staff_users:
        Notificacion.objects.create(
            usuario=staff_user,
            mensaje=mensaje,
            leida=False,
        )



def signin(request):  # Metodo para login
    if request.method == "GET":
        return render(request, "signin.html", {"form": AuthenticationForm})
    else:
        user = authenticate(  # Si el usuario es válido lo devuelve, si no regresa vacío
            request,
            username=request.POST["username"],
            password=request.POST["password"],
        )
        if user is None:
            mensaje = f"Intento fallido de ingreso, usuario: {request.POST.get('username')}"
            notificar_a_staff(mensaje)
            return render(
                request,
                "signin.html",
                {
                    "form": AuthenticationForm,
                    "error": "Usuario o contraseña incorrecta",
                },
            )

        login(request, user)  # Guardamos la cookie ya que el usuario si existe
        return redirect("tasks")
        """
        photo_data = request.POST.get("photo")

        if not photo_data:
            print("No se encontró foto en el formulario")
            return render(request, "signin.html", {
                "form": AuthenticationForm,
                "error": "No se encontró foto en el formulario"
            })

        else:
            profile = Profile.objects.get(user=user)
            if profile and profile.imagen_id:
                img_profile = profile.imagen_id
                user_face = consultar_imagen_usuario(imagen_id=img_profile)

                if user_face is False:
                    mensaje = "Intento fallido: usuario no reconocido por el sistema de reconocimiento facial."
                    notificar_a_staff(mensaje)
                    print("El usuario no existe")
                    return render(request, "signin.html", {
                        "form": AuthenticationForm,
                        "error": "El usuario no existe"
                    })
                if user_face is None:
                    print("Error al recuperar la imagen")
                    return render(request, "signin.html", {
                        "form": AuthenticationForm,
                        "error": "Error al recuperar la imagen"
                    })

                result = login_captura_facial(user_face, photo_data)
                if result is True:
                    login(request, user) #Guardamos la cookie ya que el usuario si existe
                    return redirect("tasks")
                if result is False:
                    mensaje = "No coinciden lo suficiente los rostros"
                    notificar_a_staff(f"Intento fallido: {mensaje}")
                    print("No coinciden los rostros")
                    return render(request, "signin.html", {
                        "form": AuthenticationForm,
                        "error": "No coinciden lo suficiente los rostros"
                    })
                if result == -100:
                    print("Error al decodificar la imagen")
                    return render(request, "signin.html", {
                        "form": UserCreationForm(),
                        "error": "Error al decodificar la imagen"
                    })
                if result == -200:
                    mensaje = "Alguien intento ingresar pero no se encontraron rostros"
                    notificar_a_staff(f"Intento fallido: {mensaje}")
                    print("No se detectaron rostros")
                    return render(request, "signin.html", {
                        "form": UserCreationForm(),
                        "error": "No se detectaron rostros"
                    })
        """

