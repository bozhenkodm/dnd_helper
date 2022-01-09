from django.urls import path

from base.views import (
    EncounterChangeInitiativeView,
    EncounterDetailView,
    MainView,
    NPCDetailView,
)

urlpatterns = [
    path('npc/detail/<pk>', NPCDetailView.as_view(), name='npc'),
    path('encounter/detail/<pk>', EncounterDetailView.as_view(), name='encounter'),
    path(
        'encounter/detail/<pk>/change-initiative',
        EncounterChangeInitiativeView.as_view(),
        name='encounter-change',
    ),
    path('', MainView.as_view(), name='main_view'),
]
