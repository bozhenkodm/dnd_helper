from django.urls import path

from generator.views import (
    FantasyNameView,
    GeneratorsMainView,
    NpcGeneratorView,
    RandomNameView,
    TavernView,
)

urlpatterns = [
    path(
        'main',
        GeneratorsMainView.as_view(),
        name='generator_main',
    ),
    path(
        'tavern',
        TavernView.as_view(),
        name='generator_tavern',
    ),
    path(
        'npc/',
        NpcGeneratorView.as_view(),
        name='generator_npc',
    ),
    path(
        'npc/<race>',
        NpcGeneratorView.as_view(),
        name='generator_npc',
    ),
    path(
        'fantasy_name',
        FantasyNameView.as_view(),
        name='generator_fantasy_name',
    ),
    path(
        'random_name',
        RandomNameView.as_view(),
        name='random_fantasy_name',
    ),
]
