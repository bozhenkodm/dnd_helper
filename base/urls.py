from django.urls import path

from base.views import EncounterDetailView, MainView, NPCDetailView

urlpatterns = [
    path('npc/detail/<pk>', NPCDetailView.as_view(), name='npc'),
    path('encounter/detail/<pk>', EncounterDetailView.as_view(), name='encounter'),
    path('', MainView.as_view(), name='main_view'),
]
