from rest_framework.authentication import TokenAuthentication
from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveAPIView, DestroyAPIView, UpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework import status, permissions
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from tutorial.quickstart.serializers import UserSerializer

from API.areas.AreaSerializer import AreaListSerializer, AreaCreateSerializer, AreaUpdateSerializer
from API.login.LoginSerializer import LoginSerializer
from API.notificaciones.NotificacionSerializer import NotificacionSerializer
from API.puertas.PuertaSerializer import PuertaListSerializer, PuertaCreateSerializer, PuertaUpdateSerializer
from API.zonas.ZonaSerializer import ZonaListSerializer, ZonaCreateSerializer, ZonaUpdateSerializer
from API.roles.RolesSerializer import RolesListSerializer, RolesCreateSerializer, RolesUpdateSerializer
from areas.models import Area, Zona, Puerta, Roles
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404

from notificaciones.models import Notificacion

UserModel = get_user_model()

'''
API's de la tabla Area
'''

@authentication_classes([TokenAuthentication]) #Utilizada para autenticarse
@permission_classes([IsAuthenticated]) #Si la ruta está protegida
class AreaListAPIView(ListAPIView):
    def get_queryset(self):
        return Area.objects.all()

    serializer_class = AreaListSerializer

@authentication_classes([TokenAuthentication]) #Utilizada para autenticarse
@permission_classes([IsAuthenticated]) #Si la ruta está protegida
class AreaCreateAPIView(CreateAPIView):
    serializer_class = AreaCreateSerializer

@authentication_classes([TokenAuthentication]) #Utilizada para autenticarse
@permission_classes([IsAuthenticated]) #Si la ruta está protegida
class AreaRetrieveAPIView(RetrieveAPIView):
    serializer_class = AreaCreateSerializer
    queryset = Area.objects.all()

@authentication_classes([TokenAuthentication]) #Utilizada para autenticarse
@permission_classes([IsAuthenticated]) #Si la ruta está protegida
class AreaDestroyAPIView(DestroyAPIView):
    serializer_class = AreaCreateSerializer
    queryset = Area.objects.all()

@authentication_classes([TokenAuthentication]) #Utilizada para autenticarse
@permission_classes([IsAuthenticated]) #Si la ruta está protegida
class AreaUpdateAPIView(UpdateAPIView):
    serializer_class = AreaUpdateSerializer
    queryset = Area.objects.all()


'''
API's de la tabla Zonas
'''

@authentication_classes([TokenAuthentication]) #Utilizada para autenticarse
@permission_classes([IsAuthenticated]) #Si la ruta está protegida
class ZonaListAPIView(ListAPIView):
    def get_queryset(self):
        return Zona.objects.all()

    serializer_class = AreaListSerializer

@authentication_classes([TokenAuthentication]) #Utilizada para autenticarse
@permission_classes([IsAuthenticated]) #Si la ruta está protegida
class ZonaCreateAPIView(CreateAPIView):
    serializer_class = ZonaListSerializer

@authentication_classes([TokenAuthentication]) #Utilizada para autenticarse
@permission_classes([IsAuthenticated]) #Si la ruta está protegida
class ZonaRetrieveAPIView(RetrieveAPIView):
    serializer_class = ZonaCreateSerializer
    queryset = Zona.objects.all()

@authentication_classes([TokenAuthentication]) #Utilizada para autenticarse
@permission_classes([IsAuthenticated]) #Si la ruta está protegida
class ZonaDestroyAPIView(DestroyAPIView):
    serializer_class = ZonaCreateSerializer
    queryset = Zona.objects.all()

@authentication_classes([TokenAuthentication]) #Utilizada para autenticarse
@permission_classes([IsAuthenticated]) #Si la ruta está protegida
class ZonaUpdateAPIView(UpdateAPIView):
    serializer_class = ZonaUpdateSerializer
    queryset = Zona.objects.all()


'''
API's de la tabla Puertas
'''

@authentication_classes([TokenAuthentication]) #Utilizada para autenticarse
@permission_classes([IsAuthenticated]) #Si la ruta está protegida
class PuertaListAPIView(ListAPIView):
    def get_queryset(self):
        return Puerta.objects.all()

    serializer_class = PuertaListSerializer

@authentication_classes([TokenAuthentication]) #Utilizada para autenticarse
@permission_classes([IsAuthenticated]) #Si la ruta está protegida
class PuertaCreateAPIView(CreateAPIView):
    serializer_class = PuertaListSerializer

@authentication_classes([TokenAuthentication]) #Utilizada para autenticarse
@permission_classes([IsAuthenticated]) #Si la ruta está protegida
class PuertaRetrieveAPIView(RetrieveAPIView):
    serializer_class = PuertaCreateSerializer
    queryset = Puerta.objects.all()

@authentication_classes([TokenAuthentication]) #Utilizada para autenticarse
@permission_classes([IsAuthenticated]) #Si la ruta está protegida
class PuertaDestroyAPIView(DestroyAPIView):
    serializer_class = PuertaCreateSerializer
    queryset = Puerta.objects.all()

@authentication_classes([TokenAuthentication]) #Utilizada para autenticarse
@permission_classes([IsAuthenticated]) #Si la ruta está protegida
class PuertaUpdateAPIView(UpdateAPIView):
    serializer_class = PuertaUpdateSerializer
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


@api_view(['POST'])
def register(request):
    serializer = LoginSerializer(data=request.data)

    if serializer.is_valid():
        if not not UserModel.objects.filter(username=serializer.validated_data['username']).exists():
            return Response({"Error": 'El usuario ya se encuentra creado'}, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()

        user = UserModel.objects.get(username=serializer.data['username'])
        #user.set_password(serializer.data['password'])
        user.save()

        token = Token.objects.create(user=user)
        return Response(
            {'token': token.key, "user": serializer.data},
            status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(['POST'])
@authentication_classes([TokenAuthentication]) #Utilizada para autenticarse
@permission_classes([IsAuthenticated]) #Si la ruta está protegida
#Esta consulta debe enviar un HEADER de Authentication con la propiedad Token
def profile(request):
    print(request.data)

    return Response({"username": request.user.username}, status=status.HTTP_200_OK)


'''
API's de la tabla Roles
'''

@authentication_classes([TokenAuthentication]) #Utilizada para autenticarse
@permission_classes([IsAuthenticated]) #Si la ruta está protegida
class RolesListAPIView(ListAPIView):
    def get_queryset(self):
        return Roles.objects.all()

    serializer_class = RolesListSerializer

@authentication_classes([TokenAuthentication]) #Utilizada para autenticarse
@permission_classes([IsAuthenticated]) #Si la ruta está protegida
class RolesCreateAPIView(CreateAPIView):
    serializer_class = RolesListSerializer

@authentication_classes([TokenAuthentication]) #Utilizada para autenticarse
@permission_classes([IsAuthenticated]) #Si la ruta está protegida
class RolesRetrieveAPIView(RetrieveAPIView):
    serializer_class = RolesCreateSerializer
    queryset = Roles.objects.all()

@authentication_classes([TokenAuthentication]) #Utilizada para autenticarse
@permission_classes([IsAuthenticated]) #Si la ruta está protegida
class RolesDestroyAPIView(DestroyAPIView):
    serializer_class = RolesCreateSerializer
    queryset = Roles.objects.all()

@authentication_classes([TokenAuthentication]) #Utilizada para autenticarse
@permission_classes([IsAuthenticated]) #Si la ruta está protegida
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
            return Response({'error': 'Notificación no encontrada'}, status = 404)
