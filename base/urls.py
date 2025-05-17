from django.urls import path

from base.views import (
    EncounterDetailView,
    MainView,
    NPCDetailView,
    NPCFormView,
    NPCListView,
    NPCPowerDetailView,
    PCPartyView,
    PowerCreateFromImage,
)

urlpatterns = [
    path('npc/create/', NPCFormView.as_view(), name='npc_create'),
    path('npc/list/', NPCListView.as_view(), name='npc_list'),
    path('npc/detail/<pk>', NPCDetailView.as_view(), name='npc'),
    path(
        'npc/detail/<pk>/power/<power_pk>',
        NPCPowerDetailView.as_view(),
        name='npc_power',
    ),
    path('encounter/detail/<pk>', EncounterDetailView.as_view(), name='encounter'),
    path(
        'power/create/from-image',
        PowerCreateFromImage.as_view(),
        name='power_from_image',
    ),
    path('party/detail/<pk>', PCPartyView.as_view(), name='party'),
    path('', MainView.as_view(), name='main_view'),
]
