from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveAPIView, DestroyAPIView, UpdateAPIView

from API.areas.AreaSerializer import AreaListSerializer, AreaCreateSerializer, AreaUpdateSerializer
from API.puertas.PuertaSerializer import PuertaListSerializer, PuertaCreateSerializer, PuertaUpdateSerializer
from API.zonas.ZonaSerializer import ZonaListSerializer, ZonaCreateSerializer, ZonaUpdateSerializer
from areas.models import Area, Zona, Puerta

'''
API's de la tabla Area
'''
class AreaListAPIView(ListAPIView):
    def get_queryset(self):
        return Area.objects.all()

    serializer_class = AreaListSerializer

class AreaCreateAPIView(CreateAPIView):
    serializer_class = AreaCreateSerializer

class AreaRetrieveAPIView(RetrieveAPIView):
    serializer_class = AreaCreateSerializer
    queryset = Area.objects.all()

class AreaDestroyAPIView(DestroyAPIView):
    serializer_class = AreaCreateSerializer
    queryset = Area.objects.all()

class AreaUpdateAPIView(UpdateAPIView):
    serializer_class = AreaUpdateSerializer
    queryset = Area.objects.all()

'''
API's de la tabla Zonas
'''

class ZonaListAPIView(ListAPIView):
    def get_queryset(self):
        return Zona.objects.all()

    serializer_class = AreaListSerializer

class ZonaCreateAPIView(CreateAPIView):
    serializer_class = ZonaListSerializer

class ZonaRetrieveAPIView(RetrieveAPIView):
    serializer_class = ZonaCreateSerializer
    queryset = Zona.objects.all()

class ZonaDestroyAPIView(DestroyAPIView):
    serializer_class = ZonaCreateSerializer
    queryset = Zona.objects.all()

class ZonaUpdateAPIView(UpdateAPIView):
    serializer_class = ZonaUpdateSerializer
    queryset = Zona.objects.all()

'''
API's de la tabla Puertas
'''

class PuertaListAPIView(ListAPIView):
    def get_queryset(self):
        return Puerta.objects.all()

    serializer_class = PuertaListSerializer

class PuertaCreateAPIView(CreateAPIView):
    serializer_class = PuertaListSerializer

class PuertaRetrieveAPIView(RetrieveAPIView):
    serializer_class = PuertaCreateSerializer
    queryset = Puerta.objects.all()

class PuertaDestroyAPIView(DestroyAPIView):
    serializer_class = PuertaCreateSerializer
    queryset = Puerta.objects.all()

class PuertaUpdateAPIView(UpdateAPIView):
    serializer_class = PuertaUpdateSerializer
    queryset = Puerta.objects.all()