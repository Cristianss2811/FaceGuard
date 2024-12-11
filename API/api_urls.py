from django.urls import path

from API.views import AreaListAPIView, AreaCreateAPIView, AreaRetrieveAPIView, AreaDestroyAPIView, AreaUpdateAPIView, \
    ZonaListAPIView, ZonaCreateAPIView, ZonaRetrieveAPIView, ZonaDestroyAPIView, ZonaUpdateAPIView, PuertaListAPIView, \
    PuertaCreateAPIView, PuertaRetrieveAPIView, PuertaDestroyAPIView, PuertaUpdateAPIView, register, profile, \
    RolesListAPIView, RolesCreateAPIView, RolesRetrieveAPIView, RolesDestroyAPIView, RolesUpdateAPIView, \
    NotificacionListAPIView, NotificacionMarkAsReadAPIView
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

    path('roles/list', RolesListAPIView.as_view(), name='roles_list'),
    path('roles/create', RolesCreateAPIView.as_view(), name='roles_create'),
    path('roles/retrieve/<pk>', RolesRetrieveAPIView.as_view(), name='roles-detail'),
    path('roles/delete/<pk>', RolesDestroyAPIView.as_view(), name='roles-delete'),
    path('roles/update/<pk>', RolesUpdateAPIView.as_view(), name='roles-update'),

    path('notificaciones/list', NotificacionListAPIView.as_view(), name='notificaciones_list'),
    path('notificaciones/marcar-leida/<pk>', NotificacionMarkAsReadAPIView.as_view(), name='notificaciones_mark_as_read'),
]
