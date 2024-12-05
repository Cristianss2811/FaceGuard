from django.urls import path

from API.views import AreaListAPIView, AreaCreateAPIView, AreaRetrieveAPIView, AreaDestroyAPIView, AreaUpdateAPIView, \
    ZonaListAPIView, ZonaCreateAPIView, ZonaRetrieveAPIView, ZonaDestroyAPIView, ZonaUpdateAPIView, PuertaListAPIView, \
    PuertaCreateAPIView, PuertaRetrieveAPIView, PuertaDestroyAPIView, PuertaUpdateAPIView, register, profile
from API.views import login

urlpatterns = [
    path('areas/list', AreaListAPIView.as_view(), name='area_list'),
    path('areas/create', AreaCreateAPIView.as_view(), name='area_create'),
    path('areas/retrieve/<pk>', AreaRetrieveAPIView.as_view(), name='area-detail'),
    path('areas/delete/<pk>', AreaDestroyAPIView.as_view(), name='area-delete'),
    path('areas/update/<pk>', AreaUpdateAPIView.as_view(), name='area-update'),

    path('zonas/list', ZonaListAPIView.as_view(), name='zonas_list'),
    path('zonas/create', ZonaCreateAPIView.as_view(), name='zonas_create'),
    path('zonas/retrieve/<pk>', ZonaRetrieveAPIView.as_view(), name='zonas-detail'),
    path('zonas/delete/<pk>', ZonaDestroyAPIView.as_view(), name='zonas-delete'),
    path('zonas/update/<pk>', ZonaUpdateAPIView.as_view(), name='zonas-update'),

    path('puertas/list', PuertaListAPIView.as_view(), name='puertas_list'),
    path('puertas/create', PuertaCreateAPIView.as_view(), name='puertas_create'),
    path('puertas/retrieve/<pk>', PuertaRetrieveAPIView.as_view(), name='puertas-detail'),
    path('puertas/delete/<pk>', PuertaDestroyAPIView.as_view(), name='puertas-delete'),
    path('puertas/update/<pk>', PuertaUpdateAPIView.as_view(), name='puertas-update'),

    path('login', login),
    path('register', register),
    path('profile', profile),
]
