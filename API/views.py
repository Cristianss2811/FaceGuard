from django.contrib.auth.models import User
from django.db import IntegrityError
from rest_framework.authentication import TokenAuthentication
from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveAPIView, DestroyAPIView, UpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework import status, permissions
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from tutorial.quickstart.serializers import UserSerializer

from API.areas.AreaSerializer import AreaListSerializer, AreaCreateSerializer
from API.login.LoginSerializer import LoginSerializer
from API.moviminetos.MovimientoSeralizer import MovimientoSerializer
from API.notificaciones.NotificacionSerializer import NotificacionSerializer
from API.puertas.PuertaSerializer import PuertaListSerializer, PuertaCreateSerializer
from API.usuarios.UsuariosSerializer import ProfileListSerializer, RoleSerializer
from API.zonas.ZonaSerializer import ZonaListSerializer, ZonaCreateSerializer, ZonaUpdateSerializer
from API.roles.RolesSerializer import RolesListSerializer, RolesCreateSerializer, RolesUpdateSerializer
from areas.models import Area, Zona, Puerta, Roles, PuertasRoles
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404

from atencion.models import Movimiento
from notificaciones.models import Notificacion
from usuarios.models import Profile, ProfileRole
from usuarios.utils.registro_facial import login_captura_facial, consultar_imagen_usuario, registro_facial
from usuarios.views import notificar_a_staff, registrar_movimiento

UserModel = get_user_model()

'''
API's de la tabla Area
'''


@authentication_classes([TokenAuthentication])  # Utilizada para autenticarse
@permission_classes([IsAuthenticated])  # Si la ruta está protegida
class AreaListAPIView(ListAPIView):
    queryset = Area.objects.prefetch_related('zonas')  # Optimiza la consulta
    serializer_class = AreaListSerializer


@authentication_classes([TokenAuthentication])  # Utilizada para autenticarse
@permission_classes([IsAuthenticated])  # Si la ruta está protegida
class AreaCreateAPIView(CreateAPIView):
    serializer_class = AreaCreateSerializer


@authentication_classes([TokenAuthentication])  # Utilizada para autenticarse
@permission_classes([IsAuthenticated])  # Si la ruta está protegida
class AreaRetrieveAPIView(RetrieveAPIView):
    serializer_class = AreaCreateSerializer
    queryset = Area.objects.all()


@authentication_classes([TokenAuthentication])  # Utilizada para autenticarse
@permission_classes([IsAuthenticated])  # Si la ruta está protegida
class AreaDestroyAPIView(DestroyAPIView):
    serializer_class = AreaCreateSerializer
    queryset = Area.objects.all()


@authentication_classes([TokenAuthentication])  # Utilizada para autenticarse
@permission_classes([IsAuthenticated])  # Si la ruta está protegida
class AreaUpdateAPIView(UpdateAPIView):
    serializer_class = AreaCreateSerializer
    queryset = Area.objects.all()


'''
API's de la tabla Zonas
'''


@authentication_classes([TokenAuthentication])  # Utilizada para autenticarse
@permission_classes([IsAuthenticated])  # Si la ruta está protegida
class ZonaListAPIView(ListAPIView):
    def get_queryset(self):
        return Zona.objects.all()

    serializer_class = AreaListSerializer


@authentication_classes([TokenAuthentication])  # Utilizada para autenticarse
@permission_classes([IsAuthenticated])  # Si la ruta está protegida
class ZonaCreateAPIView(CreateAPIView):
    serializer_class = ZonaListSerializer


@authentication_classes([TokenAuthentication])  # Utilizada para autenticarse
@permission_classes([IsAuthenticated])  # Si la ruta está protegida
class ZonaRetrieveAPIView(RetrieveAPIView):
    serializer_class = ZonaCreateSerializer
    queryset = Zona.objects.all()


@authentication_classes([TokenAuthentication])  # Utilizada para autenticarse
@permission_classes([IsAuthenticated])  # Si la ruta está protegida
class ZonaDestroyAPIView(DestroyAPIView):
    serializer_class = ZonaCreateSerializer
    queryset = Zona.objects.all()


@authentication_classes([TokenAuthentication])  # Utilizada para autenticarse
@permission_classes([IsAuthenticated])  # Si la ruta está protegida
class ZonaUpdateAPIView(UpdateAPIView):
    serializer_class = ZonaUpdateSerializer
    queryset = Zona.objects.all()


'''
API's de la tabla Puertas
'''


@authentication_classes([TokenAuthentication])  # Utilizada para autenticarse
@permission_classes([IsAuthenticated])  # Si la ruta está protegida
class PuertaListAPIView(ListAPIView):
    queryset = Puerta.objects.prefetch_related('areas')  # Optimiza la consulta
    serializer_class = PuertaListSerializer

@authentication_classes([TokenAuthentication])  # Utilizada para autenticarse
@permission_classes([IsAuthenticated])  # Si la ruta está protegida
class PuertaCreateAPIView(CreateAPIView):
    serializer_class = PuertaCreateSerializer

@authentication_classes([TokenAuthentication])  # Utilizada para autenticarse
@permission_classes([IsAuthenticated])  # Si la ruta está protegida
class PuertaRetrieveAPIView(RetrieveAPIView):
    serializer_class = PuertaCreateSerializer
    queryset = Puerta.objects.all()

@authentication_classes([TokenAuthentication])  # Utilizada para autenticarse
@permission_classes([IsAuthenticated])  # Si la ruta está protegida
class PuertaDestroyAPIView(DestroyAPIView):
    serializer_class = PuertaCreateSerializer
    queryset = Puerta.objects.all()

@authentication_classes([TokenAuthentication])  # Utilizada para autenticarse
@permission_classes([IsAuthenticated])  # Si la ruta está protegida
class PuertaUpdateAPIView(UpdateAPIView):
    serializer_class = PuertaCreateSerializer
    queryset = Puerta.objects.all()


'''
API's del login
'''


@api_view(['POST'])
def login(request):
    user = get_object_or_404(UserModel, username=request.data['username'])
    if not user.check_password(request.data['password']):
        return Response({"Error": "Password no válida"}, status=status.HTTP_400_BAD_REQUEST)

    token, created = Token.objects.get_or_create(user=user)
    serializer = LoginSerializer(instance=user)

    return Response({"token": token.key, "username": serializer.data['username']}, status=status.HTTP_200_OK)


class SignupAPI(APIView):
    def post(self, request, *args, **kwargs):
        try:
            #print(request)
            # Validar que se envíen los datos necesarios
            username = request.data.get("username")
            password1 = request.data.get("password")
            photo_data = request.data.get("photo")

            if not username:
                return Response({"error": "Coloca el campo username"}, status=status.HTTP_400_BAD_REQUEST)

            if not password1:
                return Response({"error": "Coloca el campo password"}, status=status.HTTP_400_BAD_REQUEST)

            if not photo_data:
                return Response({"error": "No se encontró foto en el formulario"}, status=status.HTTP_400_BAD_REQUEST)

            # Procesar la foto con el sistema de reconocimiento facial
            img_id = registro_facial(username, photo_data)

            if img_id is None:
                return Response({"error": "No se detectaron rostros"}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

            if img_id is False:
                return Response({"error": "Error al decodificar la imagen"},
                                status=status.HTTP_422_UNPROCESSABLE_ENTITY)

            # Registrar usuario
            try:
                user = User.objects.create_user(username=username, password=password1)
                user.save()

                # Crear el perfil asociado al usuario
                profile = Profile.objects.create(user=user, imagen_id=img_id)
                profile.save()

                token = Token.objects.create(user=user)
                return Response(
                    {'token': token.key, "username": user.username},
                    status=status.HTTP_201_CREATED)

            except IntegrityError:
                return Response({"error": "El usuario ya existe"}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({"error": f"Error inesperado: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
def register(request):
    serializer = LoginSerializer(data=request.data)

    if serializer.is_valid():
        if not not UserModel.objects.filter(username=serializer.validated_data['username']).exists():
            return Response({"Error": 'El usuario ya se encuentra creado'}, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()

        user = UserModel.objects.get(username=serializer.data['username'])
        # user.set_password(serializer.data['password'])
        user.save()

        token = Token.objects.create(user=user)
        return Response(
            {'token': token.key, "user": serializer.data},
            status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@authentication_classes([TokenAuthentication])  # Utilizada para autenticarse
@permission_classes([IsAuthenticated])  # Si la ruta está protegida
# Esta consulta debe enviar un HEADER de Authentication con la propiedad Token
def profile(request):
    print(request.data)

    return Response({"username": request.user.username, "is_staff": request.user.is_staff}, status=status.HTTP_200_OK)


'''
API's de la tabla Roles
'''


@authentication_classes([TokenAuthentication])  # Utilizada para autenticarse
@permission_classes([IsAuthenticated])  # Si la ruta está protegida
class RolesListAPIView(ListAPIView):
    def get_queryset(self):
        return Roles.objects.all()

    serializer_class = RolesListSerializer


@authentication_classes([TokenAuthentication])  # Utilizada para autenticarse
@permission_classes([IsAuthenticated])  # Si la ruta está protegida
class RolesCreateAPIView(CreateAPIView):
    serializer_class = RolesListSerializer


@authentication_classes([TokenAuthentication])  # Utilizada para autenticarse
@permission_classes([IsAuthenticated])  # Si la ruta está protegida
class RolesRetrieveAPIView(RetrieveAPIView):
    serializer_class = RolesCreateSerializer
    queryset = Roles.objects.all()


@authentication_classes([TokenAuthentication])  # Utilizada para autenticarse
@permission_classes([IsAuthenticated])  # Si la ruta está protegida
class RolesDestroyAPIView(DestroyAPIView):
    serializer_class = RolesCreateSerializer
    queryset = Roles.objects.all()


@authentication_classes([TokenAuthentication])  # Utilizada para autenticarse
@permission_classes([IsAuthenticated])  # Si la ruta está protegida
class RolesUpdateAPIView(UpdateAPIView):
    serializer_class = RolesUpdateSerializer
    queryset = Roles.objects.all()


"""
API's de Notificaciones
"""


@authentication_classes([TokenAuthentication])  # Utilizada para autenticarse
@permission_classes([IsAuthenticated])
class NotificacionListAPIView(ListAPIView):
    serializer_class = NotificacionSerializer

    def get_queryset(self):
        # Retorna solo las notificaciones del usuario autenticado
        return Notificacion.objects.filter(usuario=self.request.user).order_by('-fecha_creacion')


@authentication_classes([TokenAuthentication])  # Utilizada para autenticarse
@permission_classes([IsAuthenticated])
class NotificacionMarkAsReadAPIView(APIView):

    def patch(self, request, pk):
        try:
            # Busca la notificación del usuario autenticado
            notificacion = Notificacion.objects.get(pk=pk, usuario=request.user)
            notificacion.leida = True
            notificacion.save()
            return Response({'status': 'Notificación marcada como leída'})
        except Notificacion.DoesNotExist:
            return Response({'error': 'Notificación no encontrada'}, status=404)


"""
API´s Usuarios
"""


@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class ProfileListAPIView(ListAPIView):
    serializer_class = ProfileListSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Profile.objects.all()
        return Profile.objects.filter(user=user)


@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class ProfileUpdateAPIView(UpdateAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileListSerializer


@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class UnassignedRolesView(APIView):
    def get(self, request, profile_id):
        try:
            # Obtener el perfil del usuario
            profile = Profile.objects.get(id=profile_id)

            # Obtener roles que no están asignados al perfil
            assigned_roles = ProfileRole.objects.filter(profile=profile).values_list('role', flat=True)
            unassigned_roles = Roles.objects.exclude(id__in=assigned_roles, activo=True)

            # Serializar los roles disponibles
            serializer = RoleSerializer(unassigned_roles, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Profile.DoesNotExist:
            return Response({"error": "Perfil no encontrado"}, status=status.HTTP_404_NOT_FOUND)


@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class AssignRoleView(APIView):
    def post(self, request, profile_id):
        try:
            # Obtener el perfil y los datos del rol desde la solicitud
            profile = Profile.objects.get(id=profile_id)
            role_id = request.data.get('role_id')
            fecha_vencimiento = request.data.get('fecha_vencimiento')

            # Verificar si el rol ya está asignado
            if ProfileRole.objects.filter(profile=profile, role_id=role_id).exists():
                return Response({"error": "El rol ya está asignado a este perfil."}, status=status.HTTP_400_BAD_REQUEST)

            # Asignar el rol
            role = Roles.objects.get(id=role_id)
            profile_role = ProfileRole(profile=profile, role=role, fecha_vencimiento=fecha_vencimiento)
            profile_role.save()

            return Response({"message": "Rol asignado correctamente"}, status=status.HTTP_201_CREATED)

        except Profile.DoesNotExist:
            return Response({"error": "Perfil no encontrado"}, status=status.HTTP_404_NOT_FOUND)
        except Roles.DoesNotExist:
            return Response({"error": "Rol no encontrado"}, status=status.HTTP_404_NOT_FOUND)


@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class DeleteRoleAssignmentView(APIView):
    def delete(self, request, profile_id, role_id):
        try:
            # Obtener el perfil y el rol
            profile = Profile.objects.get(id=profile_id)
            role = Roles.objects.get(id=role_id)

            # Filtrar roles asignados a este perfil
            profile_roles = ProfileRole.objects.filter(profile=profile)

            # Verificar si el rol está asignado al perfil
            if not profile_roles.filter(role=role).exists():
                return Response({"error": "El rol no está asignado a este perfil."}, status=status.HTTP_400_BAD_REQUEST)

            # Eliminar la asignación de rol
            profile_role = profile_roles.get(role=role)
            profile_role.delete()

            return Response({"message": "Rol eliminado correctamente del perfil."}, status=status.HTTP_200_OK)

        except Profile.DoesNotExist:
            return Response({"error": "Perfil no encontrado"}, status=status.HTTP_404_NOT_FOUND)
        except Roles.DoesNotExist:
            return Response({"error": "Rol no encontrado"}, status=status.HTTP_404_NOT_FOUND)


"""
class VerificarRostroAccesoView(APIView):
    #permission_classes = [IsAuthenticated]

    def post(self, request, puerta_id):
        photo_data = request.data.get("photo")

        if not photo_data:
            return Response({"detail": "No se encontró foto en la solicitud."}, status=status.HTTP_400_BAD_REQUEST)

        profile = request.user.profile
        puerta = get_object_or_404(Puerta, id=puerta_id)

        if not profile or not profile.imagen_id:
            return Response({"detail": "Perfil de usuario inválido o sin imagen registrada."}, status=status.HTTP_400_BAD_REQUEST)

        # Consultar la imagen del usuario registrada
        img_profile = profile.imagen_id
        user_face = consultar_imagen_usuario(imagen_id=img_profile)

        if user_face is False:
            return Response({"detail": "El usuario no tiene rostro registrado."}, status=status.HTTP_400_BAD_REQUEST)
        if user_face is None:
            return Response({"detail": "Error al recuperar la imagen del perfil."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # Comparar el rostro registrado con el rostro capturado
        resultado = login_captura_facial(user_face, photo_data)

        if resultado is True:
            # Verificar los roles del usuario y de la puerta
            roles_usuario = ProfileRole.objects.filter(profile=profile).values_list('role', flat=True)
            roles_puerta = PuertasRoles.objects.filter(puerta=puerta).values_list('rol', flat=True)
            acceso = any(rol in roles_puerta for rol in roles_usuario)

            # Registrar el movimiento
            accion = "Acceso" if acceso else "Acceso denegado"
            registrar_movimiento(accion, profile, puerta)

            # Notificar al staff
            mensaje = (
                f"{accion} concedido\n"
                f"Usuario: {profile.user}\n"
            )
            notificar_a_staff(mensaje)

            return Response({"puerta": puerta.id, "acceso": acceso}, status=status.HTTP_200_OK)

        elif resultado is False:
            return Response({"detail": "No coinciden lo suficiente los rostros."}, status=status.HTTP_400_BAD_REQUEST)
        elif resultado == -100:
            return Response({"detail": "Error al decodificar la imagen."}, status=status.HTTP_400_BAD_REQUEST)
        elif resultado == -200:
            return Response({"detail": "No se detectaron rostros en la imagen."}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"detail": "Error desconocido al procesar la imagen."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
"""


class VerificarRostroAccesoView(APIView):
    # permission_classes = [IsAuthenticated]  # Si quieres mantener la autenticación, descomenta esta línea

    def post(self, request, puerta_id):
        # Obtener la imagen y el nombre de usuario desde la solicitud
        photo_data = request.data.get("photo")
        username = request.data.get("username")

        # Validar que se haya enviado la foto y el nombre de usuario
        if not photo_data:
            return Response({"detail": "No se encontró foto en la solicitud."}, status=status.HTTP_400_BAD_REQUEST)

        if not username:
            return Response({"detail": "No se proporcionó el nombre de usuario."}, status=status.HTTP_400_BAD_REQUEST)

        # Buscar el perfil asociado con el nombre de usuario proporcionado
        try:
            user = get_object_or_404(User, username=username)
            profile = user.profile
        except:
            return Response({"detail": "Usuario no encontrado."}, status=status.HTTP_404_NOT_FOUND)

        puerta = get_object_or_404(Puerta, id=puerta_id)

        # Validar que el perfil tenga una imagen registrada
        if not profile or not profile.imagen_id:
            return Response({"detail": "Perfil de usuario inválido o sin imagen registrada."},
                            status=status.HTTP_400_BAD_REQUEST)

        # Consultar la imagen del usuario registrada
        img_profile = profile.imagen_id
        user_face = consultar_imagen_usuario(imagen_id=img_profile)

        if user_face is False:
            return Response({"detail": "El usuario no tiene rostro registrado."}, status=status.HTTP_400_BAD_REQUEST)

        if user_face is None:
            return Response({"detail": "Error al recuperar la imagen del perfil."},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # Comparar el rostro registrado con el rostro capturado
        resultado = login_captura_facial(user_face, photo_data)

        if resultado is True:
            # Verificar los roles del usuario y de la puerta
            roles_usuario = ProfileRole.objects.filter(profile=profile).values_list('role', flat=True)
            roles_puerta = PuertasRoles.objects.filter(puerta=puerta).values_list('rol', flat=True)
            acceso = any(rol in roles_puerta for rol in roles_usuario)

            # Registrar el movimiento
            accion = "Acceso" if acceso else "Acceso denegado"
            registrar_movimiento(accion, profile, puerta)

            # Notificar al staff
            mensaje = (
                f"{accion} concedido\n"
                f"Usuario: {profile.user}\n"
            )
            notificar_a_staff(mensaje)

            return Response({"puerta": puerta.id, "acceso": acceso}, status=status.HTTP_200_OK)

        elif resultado is False:
            return Response({"detail": "No coinciden lo suficiente los rostros."}, status=status.HTTP_400_BAD_REQUEST)
        elif resultado == -100:
            return Response({"detail": "Error al decodificar la imagen."}, status=status.HTTP_400_BAD_REQUEST)
        elif resultado == -200:
            return Response({"detail": "No se detectaron rostros en la imagen."}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"detail": "Error desconocido al procesar la imagen."},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)


"""
API's de Movimientos
"""


@authentication_classes([TokenAuthentication])  # Utilizada para autenticarse
@permission_classes([IsAuthenticated])
class MovimientoListView(ListAPIView):
    queryset = Movimiento.objects.all()
    serializer_class = MovimientoSerializer


"""
API's de Reconocimiento
"""
