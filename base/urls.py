from django.urls import path

from base.views import (
    EncounterDetailView,
    MainView,
    NPCDetailView,
    NPCFormView,
    NPCListView,
    PCPartyView,
)

urlpatterns = [
    path('npc/create/', NPCFormView.as_view(), name='npc_create'),
    path('npc/list/', NPCListView.as_view(), name='npc_list'),
    path('npc/detail/<pk>', NPCDetailView.as_view(), name='npc'),
    path('encounter/detail/<pk>', EncounterDetailView.as_view(), name='encounter'),
    path('party/detail/<pk>', PCPartyView.as_view(), name='party'),
    path('', MainView.as_view(), name='main_view'),
]
