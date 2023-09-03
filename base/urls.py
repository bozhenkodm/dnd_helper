from django.urls import path

from base.views import (
    EncounterChangeInitiativeView,
    EncounterDetailView,
    MainView,
    NPCDetailView,
    NPCFormView, SubclassOptionsView,
)

api_urlpatterns = [
    path('api/v1/subclass-options', SubclassOptionsView.as_view(), name='subclass_options')
]

urlpatterns = [
    path('npc/create/', NPCFormView.as_view(), name='npc_create'),
    path('npc/detail/<pk>', NPCDetailView.as_view(), name='npc'),
    path('encounter/detail/<pk>', EncounterDetailView.as_view(), name='encounter'),
    path(
        'encounter/detail/<pk>/change-initiative',
        EncounterChangeInitiativeView.as_view(),
        name='encounter-change',
    ),
    path('', MainView.as_view(), name='main_view'),
] + api_urlpatterns
